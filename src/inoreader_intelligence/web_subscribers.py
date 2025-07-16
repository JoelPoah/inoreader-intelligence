"""Integration with web subscriber database"""

import os
from typing import List, Optional
from .config import Config

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    print("⚠️ PyMongo not installed. Install with: pip install pymongo")


class WebSubscriberManager:
    """Manage web subscribers directly from MongoDB"""
    
    def __init__(self, config: Config):
        self.config = config
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.client = None
        self.db = None
        self.collection = None
        
        if PYMONGO_AVAILABLE and self.mongodb_uri:
            self._connect_to_mongodb()
    
    def _connect_to_mongodb(self):
        """Connect to MongoDB database"""
        try:
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client['strategic-intelligence']
            self.collection = self.db['emails']
            print("✅ Connected to MongoDB for web subscribers")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None
    
    def get_web_subscribers(self) -> List[str]:
        """Get list of active web subscriber emails from MongoDB"""
        if not PYMONGO_AVAILABLE:
            print("⚠️ PyMongo not available. Install with: pip install pymongo")
            print("💡 Continuing with configured email recipients only")
            return []
            
        if not self.mongodb_uri:
            print("⚠️ MONGODB_URI not found in environment variables")
            print("💡 Continuing with configured email recipients only")
            return []
            
        if self.collection is None:
            print("❌ MongoDB connection not available. Cannot fetch web subscribers.")
            print("💡 Continuing with configured email recipients only")
            return []
        
        try:
            # Query for active subscribers
            cursor = self.collection.find(
                {"status": "active"}, 
                {"email": 1, "_id": 0}
            ).sort("submitted_at", -1)
            
            emails = [doc["email"] for doc in cursor]
            
            if emails:
                print(f"📧 Retrieved {len(emails)} web subscribers from MongoDB")
            else:
                print("⚠️ No web subscribers found in MongoDB")
            
            return emails
                
        except Exception as e:
            print(f"❌ Error fetching web subscribers from MongoDB: {e}")
            print("💡 Continuing with configured email recipients only")
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
        """Test connection to MongoDB"""
        if not PYMONGO_AVAILABLE:
            print("❌ PyMongo not available for testing connection")
            return False
            
        if self.client is None:
            print("❌ MongoDB client not initialized")
            return False
            
        try:
            # Ping the database
            self.client.admin.command('ping')
            
            # Try to count documents in emails collection
            if self.collection is not None:
                count = self.collection.count_documents({})
                print(f"✅ MongoDB connection successful. Total emails in database: {count}")
                return True
            else:
                print("❌ Emails collection not accessible")
                return False
                
        except Exception as e:
            print(f"❌ MongoDB connection test failed: {e}")
            return False
    
    def get_subscriber_stats(self) -> dict:
        """Get subscriber statistics from MongoDB"""
        if self.collection is None:
            return {
                "total": 0,
                "active": 0,
                "unsubscribed": 0,
                "latest_subscription": None
            }
        
        try:
            stats = {
                "total": self.collection.count_documents({}),
                "active": self.collection.count_documents({"status": "active"}),
                "unsubscribed": self.collection.count_documents({"status": "unsubscribed"}),
                "latest_subscription": None
            }
            
            # Get latest subscription
            latest = self.collection.find_one(
                {"status": "active"},
                sort=[("submitted_at", -1)]
            )
            
            if latest:
                stats["latest_subscription"] = latest.get("submitted_at")
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting subscriber stats: {e}")
            return {
                "total": 0,
                "active": 0,
                "unsubscribed": 0,
                "latest_subscription": None
            }
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client is not None:
            self.client.close()
            print("🔐 MongoDB connection closed")