"""Integration with web subscriber database"""

import requests
import os
from typing import List, Optional
from .config import Config


class WebSubscriberManager:
    """Manage web subscribers from MongoDB API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.api_base_url = os.getenv("WEB_API_URL", "http://localhost:3001/api")
    
    def get_web_subscribers(self) -> List[str]:
        """Get list of active web subscriber emails"""
        try:
            response = requests.get(f"{self.api_base_url}/active", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("emails"):
                    print(f"📧 Retrieved {len(data['emails'])} web subscribers")
                    return data["emails"]
                else:
                    print("⚠️ No web subscribers found")
                    return []
            else:
                print(f"❌ Failed to fetch web subscribers: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            print(f"❌ Error fetching web subscribers: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error fetching web subscribers: {e}")
            return []
    
    def get_combined_recipients(self) -> List[str]:
        """Get combined list of config recipients + web subscribers"""
        # Start with configured recipients
        recipients = list(self.config.email_recipients) if self.config.email_recipients else []
        
        # Add web subscribers
        web_subscribers = self.get_web_subscribers()
        
        # Combine and deduplicate
        all_recipients = list(set(recipients + web_subscribers))
        
        print(f"📬 Total recipients: {len(all_recipients)} "
              f"(Config: {len(recipients)}, Web: {len(web_subscribers)})")
        
        return all_recipients
    
    def test_connection(self) -> bool:
        """Test connection to web API"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Web API connection successful: {data.get('message', 'OK')}")
                return True
            else:
                print(f"❌ Web API connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Web API connection error: {e}")
            return False