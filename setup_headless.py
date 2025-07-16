#!/usr/bin/env python3
"""
Setup script for headless authentication
Installs required dependencies and checks browser availability
"""

import os
import sys
import subprocess
import shutil
import platform

def run_command(cmd, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_packages():
    """Check if required Python packages are installed"""
    packages = ['selenium', 'webdriver-manager']
    missing = []
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} is missing")
    
    return missing

def install_python_packages(packages):
    """Install missing Python packages"""
    if not packages:
        return True
    
    print(f"\n📦 Installing Python packages: {' '.join(packages)}")
    cmd = f"{sys.executable} -m pip install {' '.join(packages)}"
    success, stdout, stderr = run_command(cmd, capture_output=False)
    
    if success:
        print("✅ Python packages installed successfully")
        return True
    else:
        print(f"❌ Failed to install Python packages: {stderr}")
        return False

def check_browsers():
    """Check which browsers are available"""
    browsers = {
        "Chrome": ["google-chrome", "chrome", "chromium", "chromium-browser"],
        "Firefox": ["firefox", "firefox-esr"],
        "Edge": ["microsoft-edge", "msedge"]
    }
    
    available = []
    for browser_name, executables in browsers.items():
        for executable in executables:
            if shutil.which(executable):
                available.append(browser_name)
                print(f"✅ {browser_name} found at: {shutil.which(executable)}")
                break
        else:
            print(f"❌ {browser_name} not found")
    
    return available

def install_chrome_linux():
    """Install Chrome on Linux"""
    print("\n🔧 Installing Chrome on Linux...")
    
    # Update package list
    print("📦 Updating package list...")
    run_command("sudo apt-get update", capture_output=False)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    run_command("sudo apt-get install -y wget gnupg", capture_output=False)
    
    # Add Chrome repository
    print("📦 Adding Chrome repository...")
    run_command("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -", capture_output=False)
    run_command("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list", capture_output=False)
    
    # Update and install Chrome
    print("📦 Installing Chrome...")
    run_command("sudo apt-get update", capture_output=False)
    success, _, _ = run_command("sudo apt-get install -y google-chrome-stable", capture_output=False)
    
    if success:
        print("✅ Chrome installed successfully")
        return True
    else:
        print("❌ Failed to install Chrome")
        return False

def install_firefox_linux():
    """Install Firefox on Linux"""
    print("\n🔧 Installing Firefox on Linux...")
    success, _, _ = run_command("sudo apt-get install -y firefox", capture_output=False)
    
    if success:
        print("✅ Firefox installed successfully")
        return True
    else:
        print("❌ Failed to install Firefox")
        return False

def suggest_browser_installation():
    """Suggest how to install browsers on different platforms"""
    system = platform.system().lower()
    
    print("\n🔧 Browser installation suggestions:")
    
    if system == "linux":
        print("For Ubuntu/Debian:")
        print("  Chrome:  sudo apt-get install google-chrome-stable")
        print("  Firefox: sudo apt-get install firefox")
        print("\nFor CentOS/RHEL:")
        print("  Chrome:  sudo yum install google-chrome-stable")
        print("  Firefox: sudo yum install firefox")
        
        # Offer to install automatically
        if input("\n🤖 Would you like to try installing Chrome automatically? (y/N): ").lower() == 'y':
            install_chrome_linux()
        elif input("🤖 Would you like to try installing Firefox automatically? (y/N): ").lower() == 'y':
            install_firefox_linux()
    
    elif system == "darwin":
        print("For macOS:")
        print("  Chrome:  brew install --cask google-chrome")
        print("  Firefox: brew install --cask firefox")
        print("  Edge:    brew install --cask microsoft-edge")
        print("\nOr download from:")
        print("  https://www.google.com/chrome/")
        print("  https://www.mozilla.org/firefox/")
    
    elif system == "windows":
        print("For Windows:")
        print("  Download from:")
        print("  https://www.google.com/chrome/")
        print("  https://www.mozilla.org/firefox/")
        print("  https://www.microsoft.com/edge/")

def test_headless_setup():
    """Test if headless setup works"""
    print("\n🧪 Testing headless setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("📦 Setting up Chrome driver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("🌐 Testing navigation...")
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Headless setup test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Headless setup test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Inoreader Intelligence - Headless Authentication Setup")
    print("=" * 60)
    
    # Check Python packages
    print("\n1. Checking Python packages...")
    missing_packages = check_python_packages()
    
    if missing_packages:
        if not install_python_packages(missing_packages):
            print("❌ Setup failed: Could not install required packages")
            return False
    
    # Check browsers
    print("\n2. Checking browsers...")
    available_browsers = check_browsers()
    
    if not available_browsers:
        print("⚠️  No browsers found!")
        suggest_browser_installation()
        print("\n💡 After installing a browser, run this script again to test.")
        return False
    
    # Test headless setup
    print("\n3. Testing headless setup...")
    if test_headless_setup():
        print("\n✅ Setup complete! Headless authentication should work now.")
        print("💡 Try running './start' and choose option 4 → 1 (Headless authentication)")
        return True
    else:
        print("\n❌ Setup incomplete. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)