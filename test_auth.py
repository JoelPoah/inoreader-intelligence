#!/usr/bin/env python3
"""
Test script to verify automatic authentication and token refresh
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from inoreader_intelligence.auth.oauth import InoreaderOAuth
from inoreader_intelligence.config import Config

def test_automatic_auth():
    """Test automatic authentication flow"""
    try:
        # Initialize config from environment
        config = Config.from_env()
        oauth = InoreaderOAuth(config)
        
        print("🧪 Testing automatic authentication...")
        
        # Test automatic authentication
        success = oauth.authenticate_automatic()
        
        if success:
            print("✅ Automatic authentication successful!")
            print(f"✅ Access token present: {oauth.access_token is not None}")
            print(f"✅ Refresh token present: {oauth.refresh_token is not None}")
            
            # Test token validity
            if oauth.is_token_valid():
                print("✅ Token is valid!")
            else:
                print("❌ Token is invalid")
                
        else:
            print("❌ Automatic authentication failed")
            print("💡 This is expected if no token file exists")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_automatic_auth()