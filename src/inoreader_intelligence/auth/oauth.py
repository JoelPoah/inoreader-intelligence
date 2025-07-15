"""OAuth authentication for Inoreader API"""

import json
import os
import webbrowser
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs
import requests
from ..config import Config


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