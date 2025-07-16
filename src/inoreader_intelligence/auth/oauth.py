"""OAuth authentication for Inoreader API"""

import json
import os
import webbrowser
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs
import requests
import time
from ..config import Config

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.webdriver.common.service import Service as BaseService
    
    # WebDriver Manager for automatic driver management
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    
    SELENIUM_AVAILABLE = True
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError as e:
    SELENIUM_AVAILABLE = False
    WEBDRIVER_MANAGER_AVAILABLE = False


class InoreaderOAuth:
    """Handle OAuth authentication with Inoreader"""
    
    BASE_URL = "https://www.inoreader.com"
    AUTH_URL = f"{BASE_URL}/oauth2/auth"
    TOKEN_URL = f"{BASE_URL}/oauth2/token"
    
    def __init__(self, config: Config):
        self.config = config
        self.token_file = "inoreader_token.json"
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        
    def get_authorization_url(self, redirect_uri: str = "http://localhost:8080/callback") -> str:
        """Generate authorization URL for OAuth flow"""
        params = {
            "client_id": self.config.inoreader_app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "read",
            "state": "random_state_string"
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str, redirect_uri: str = "http://localhost:8080/callback") -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.config.inoreader_app_id,
            "client_secret": self.config.inoreader_app_key,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        
        # Save tokens to file
        self.save_tokens(token_data)
        
        return token_data
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        data = {
            "client_id": self.config.inoreader_app_id,
            "client_secret": self.config.inoreader_app_key,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(self.TOKEN_URL, data=data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
            
            # Save updated tokens
            self.save_tokens(token_data)
            
            return token_data
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                # Refresh token is invalid/expired
                print("🔄 Refresh token expired, clearing tokens...")
                self.clear_tokens()
                raise ValueError("Refresh token expired. Manual re-authentication required.")
            else:
                raise ValueError(f"Token refresh failed: {e}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error during token refresh: {e}")
    
    def clear_tokens(self) -> None:
        """Clear stored tokens"""
        self.access_token = None
        self.refresh_token = None
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
    
    def save_tokens(self, token_data: Dict[str, Any]) -> None:
        """Save tokens to file"""
        with open(self.token_file, "w") as f:
            json.dump(token_data, f)
    
    def load_tokens(self) -> bool:
        """Load tokens from file"""
        if not os.path.exists(self.token_file):
            return False
        
        try:
            with open(self.token_file, "r") as f:
                token_data = json.load(f)
            
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            
            return True
        except (json.JSONDecodeError, KeyError):
            return False
    
    def is_authenticated(self) -> bool:
        """Check if we have valid authentication"""
        return self.access_token is not None
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        if not self.access_token:
            raise ValueError("Not authenticated")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "AppId": self.config.inoreader_app_id,
            "AppKey": self.config.inoreader_app_key
        }
    
    def authenticate_interactive(self) -> None:
        """Interactive authentication flow"""
        # Try to load existing tokens
        if self.load_tokens():
            print("Loaded existing tokens")
            return
        
        # Start OAuth flow
        auth_url = self.get_authorization_url()
        print(f"Opening browser for authentication: {auth_url}")
        webbrowser.open(auth_url)
        
        print("After authorizing, you'll be redirected to a localhost URL.")
        print("Copy the 'code' parameter from the URL and paste it here:")
        
        code = input("Authorization code: ").strip()
        
        if code:
            try:
                self.exchange_code_for_token(code)
                print("Authentication successful!")
            except Exception as e:
                print(f"Authentication failed: {e}")
                raise
        else:
            raise ValueError("No authorization code provided")
    
    def authenticate_automatic(self) -> bool:
        """Automatic authentication flow for scheduled tasks"""
        try:
            # Try to load existing tokens
            if self.load_tokens():
                # Check if we can make a test request to validate the token
                if self.is_token_valid():
                    print("✅ Using existing valid tokens")
                    return True
                else:
                    print("🔄 Tokens expired, attempting refresh...")
                    # Try to refresh the token
                    self.refresh_access_token()
                    if self.is_token_valid():
                        print("✅ Token refreshed successfully")
                        return True
                    else:
                        print("❌ Token refresh failed")
                        return False
            else:
                print("❌ No existing tokens found")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def is_token_valid(self) -> bool:
        """Test if the current token is valid by making a test API call"""
        if not self.access_token:
            return False
        
        try:
            # Make a simple API call to test the token
            headers = self.get_auth_headers()
            response = requests.get(
                "https://www.inoreader.com/reader/api/0/user-info",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def authenticate_headless(self, timeout: int = 30) -> bool:
        """Headless authentication using Selenium WebDriver"""
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available. Install with:")
            print("   pip install selenium webdriver-manager")
            print("💡 Falling back to interactive authentication...")
            self.authenticate_interactive()
            return True
        
        # Try to load existing tokens first
        if self.load_tokens() and self.is_token_valid():
            print("✅ Using existing valid tokens")
            return True
        
        print("🤖 Starting headless authentication...")
        
        # Check if any browsers are installed
        self._check_browser_availability()
        
        # Try different browser drivers in order of preference
        drivers_to_try = [
            ("Chrome", self._setup_chrome_driver),
            ("Firefox", self._setup_firefox_driver),
            ("Edge", self._setup_edge_driver)
        ]
        
        for driver_name, setup_func in drivers_to_try:
            print(f"🔧 Trying {driver_name} driver...")
            driver = None
            try:
                driver = setup_func()
                if driver:
                    print(f"✅ {driver_name} driver initialized successfully")
                    return self._perform_headless_auth(driver, timeout)
            except Exception as e:
                print(f"❌ {driver_name} driver failed: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                continue
        
        print("❌ All browser drivers failed")
        self._print_troubleshooting_info()
        return False
    
    def _check_browser_availability(self):
        """Check which browsers are available on the system"""
        import shutil
        
        browsers = {
            "Chrome": ["google-chrome", "chrome", "chromium", "chromium-browser"],
            "Firefox": ["firefox", "firefox-esr"],
            "Edge": ["microsoft-edge", "msedge"]
        }
        
        available_browsers = []
        for browser_name, executables in browsers.items():
            for executable in executables:
                if shutil.which(executable):
                    available_browsers.append(browser_name)
                    break
        
        if available_browsers:
            print(f"🌐 Available browsers: {', '.join(available_browsers)}")
        else:
            print("⚠️  No browsers found in PATH")
    
    def _print_troubleshooting_info(self):
        """Print troubleshooting information for headless authentication"""
        print("\n🔧 Troubleshooting headless authentication:")
        print("1. Install a supported browser:")
        print("   - Chrome: https://www.google.com/chrome/")
        print("   - Firefox: https://www.mozilla.org/firefox/")
        print("   - Edge: https://www.microsoft.com/edge/")
        print("2. Install dependencies:")
        print("   pip install selenium webdriver-manager")
        print("3. On Linux, install browser packages:")
        print("   sudo apt-get install google-chrome-stable  # or")
        print("   sudo apt-get install firefox")
        print("4. If running in Docker/WSL, make sure X11 forwarding is not required")
        print("5. Check firewall settings for localhost:8080")
        print("💡 Use interactive authentication (option 2) as fallback")
    
    def _setup_chrome_driver(self):
        """Setup Chrome driver with headless options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                # Use WebDriver Manager to automatically download and manage ChromeDriver
                print("📦 Installing/updating ChromeDriver...")
                service = Service(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Fallback to system ChromeDriver
                print("⚠️  Using system ChromeDriver (webdriver-manager not available)")
                return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"❌ Chrome driver setup failed: {e}")
            raise
    
    def _setup_firefox_driver(self):
        """Setup Firefox driver with headless options"""
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                # Use WebDriver Manager to automatically download and manage GeckoDriver
                print("📦 Installing/updating GeckoDriver...")
                service = Service(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=firefox_options)
            else:
                # Fallback to system GeckoDriver
                print("⚠️  Using system GeckoDriver (webdriver-manager not available)")
                return webdriver.Firefox(options=firefox_options)
        except Exception as e:
            print(f"❌ Firefox driver setup failed: {e}")
            raise
    
    def _setup_edge_driver(self):
        """Setup Edge driver with headless options"""
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                # Use WebDriver Manager to automatically download and manage EdgeDriver
                print("📦 Installing/updating EdgeDriver...")
                service = Service(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=edge_options)
            else:
                # Fallback to system EdgeDriver
                print("⚠️  Using system EdgeDriver (webdriver-manager not available)")
                return webdriver.Edge(options=edge_options)
        except Exception as e:
            print(f"❌ Edge driver setup failed: {e}")
            raise
    
    def _perform_headless_auth(self, driver, timeout: int) -> bool:
        """Perform the actual headless authentication with the given driver"""
        try:
            driver.set_page_load_timeout(timeout)
            
            # Navigate to authorization URL
            auth_url = self.get_authorization_url()
            print(f"🌐 Navigating to: {auth_url}")
            driver.get(auth_url)
            
            # Wait for the page to load
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if we're already at the callback URL (already authorized)
            current_url = driver.current_url
            if "localhost:8080/callback" in current_url and "code=" in current_url:
                print("✅ Already authorized, extracting code...")
                code = self._extract_code_from_url(current_url)
                if code:
                    self.exchange_code_for_token(code)
                    print("✅ Headless authentication successful!")
                    return True
            
            # Wait for and click the authorize button
            print("🔍 Looking for authorization button...")
            try:
                # Try multiple button selectors
                button_selectors = [
                    "/html/body/div[1]/div[1]/div[2]/div/div/div[2]/form/div[2]/button",
                    "//button[contains(@class, 'btn') and contains(@class, 'btn-primary')]",
                    "//button[contains(text(), 'Authorize')]",
                    "//input[@type='submit' and @value='Authorize']"
                ]
                
                authorize_button = None
                for selector in button_selectors:
                    try:
                        authorize_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"✅ Found button with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if not authorize_button:
                    print("❌ Could not find authorization button")
                    return False
                
                print("🖱️ Clicking authorize button...")
                authorize_button.click()
                
                # Wait for redirect to callback URL
                print("⏳ Waiting for redirect to callback...")
                WebDriverWait(driver, timeout).until(
                    lambda d: "localhost:8080/callback" in d.current_url and "code=" in d.current_url
                )
                
                # Extract the authorization code from the URL
                callback_url = driver.current_url
                print(f"📍 Callback URL: {callback_url}")
                
                code = self._extract_code_from_url(callback_url)
                if code:
                    print(f"🔑 Authorization code extracted: {code[:10]}...")
                    self.exchange_code_for_token(code)
                    print("✅ Headless authentication successful!")
                    return True
                else:
                    print("❌ Failed to extract authorization code from callback URL")
                    return False
                    
            except TimeoutException:
                print("❌ Timeout waiting for authorization button or callback")
                print("💡 The application may need to be manually authorized first")
                return False
                
        except WebDriverException as e:
            print(f"❌ WebDriver error: {e}")
            raise
        except Exception as e:
            print(f"❌ Headless authentication failed: {e}")
            raise
        finally:
            if driver:
                driver.quit()
                print("🔐 Browser closed")
    
    def _extract_code_from_url(self, url: str) -> Optional[str]:
        """Extract authorization code from callback URL"""
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            if "code" in query_params:
                return query_params["code"][0]
            return None
        except Exception as e:
            print(f"❌ Error extracting code from URL: {e}")
            return None