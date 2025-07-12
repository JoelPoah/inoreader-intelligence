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
        
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data["access_token"]
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]
        
        # Save updated tokens
        self.save_tokens(token_data)
        
        return token_data
    
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