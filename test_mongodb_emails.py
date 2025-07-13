#!/usr/bin/env python3
"""
Test script to verify MongoDB email pulling functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mongodb_connection():
    """Test MongoDB connection and email functionality"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.web_subscribers import WebSubscriberManager
        
        # Load configuration
        config = Config.from_env()
        print("✅ Configuration loaded successfully")
        
        # Initialize web subscriber manager
        web_manager = WebSubscriberManager(config)
        print("✅ WebSubscriberManager initialized")
        
        # Test MongoDB connection
        print("\n🔌 Testing MongoDB Connection...")
        connection_success = web_manager.test_connection()
        
        if not connection_success:
            print("❌ MongoDB connection failed")
            return False
        
        # Get subscriber statistics
        print("\n📊 Getting subscriber statistics...")
        stats = web_manager.get_subscriber_stats()
        print(f"📈 Total subscribers: {stats['total']}")
        print(f"✅ Active subscribers: {stats['active']}")
        print(f"❌ Unsubscribed: {stats['unsubscribed']}")
        print(f"📅 Latest subscription: {stats['latest_subscription']}")
        
        # Test getting web subscribers
        print("\n📧 Testing email retrieval...")
        web_emails = web_manager.get_web_subscribers()
        print(f"📬 Retrieved {len(web_emails)} web subscriber emails")
        
        if web_emails:
            print("📋 Web subscriber emails:")
            for i, email in enumerate(web_emails, 1):
                print(f"   {i}. {email}")
        else:
            print("⚠️ No web subscribers found")
        
        # Test combined recipients (config + web)
        print("\n🔄 Testing combined recipients...")
        all_recipients = web_manager.get_combined_recipients()
        print(f"📬 Total combined recipients: {len(all_recipients)}")
        
        if all_recipients:
            print("📋 All recipients:")
            for i, email in enumerate(all_recipients, 1):
                print(f"   {i}. {email}")
        
        # Close connection
        web_manager.close_connection()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure PyMongo is installed: pip install pymongo")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_email_integration():
    """Test email system integration with MongoDB"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.web_subscribers import WebSubscriberManager
        from inoreader_intelligence.delivery import EmailDelivery
        
        # Load configuration
        config = Config.from_env()
        web_manager = WebSubscriberManager(config)
        
        # Get all recipients
        all_recipients = web_manager.get_combined_recipients()
        
        # Test with email delivery system
        delivery = EmailDelivery(config)
        
        # Override config recipients with combined list for testing
        config.email_recipients = all_recipients
        
        print(f"\n📤 Email delivery configured for {len(all_recipients)} recipients")
        print("📧 Email settings:")
        print(f"   Server: {delivery.smtp_server}:{delivery.smtp_port}")
        print(f"   Username: {delivery.smtp_username}")
        print(f"   Password: {'✅ Set' if delivery.smtp_password else '❌ Not set'}")
        
        web_manager.close_connection()
        
        return True
        
    except Exception as e:
        print(f"❌ Email integration test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing MongoDB Email Functionality")
    print("=" * 60)
    
    # Test MongoDB connection and email retrieval
    print("\n1️⃣ Testing MongoDB Connection & Email Retrieval")
    print("-" * 40)
    mongo_success = test_mongodb_connection()
    
    # Test email system integration
    print("\n2️⃣ Testing Email System Integration")
    print("-" * 40)
    email_success = test_email_integration()
    
    # Summary
    print("\n📋 Test Summary")
    print("-" * 40)
    print(f"MongoDB functionality: {'✅ PASS' if mongo_success else '❌ FAIL'}")
    print(f"Email integration: {'✅ PASS' if email_success else '❌ FAIL'}")
    
    overall_success = mongo_success and email_success
    
    if overall_success:
        print("\n🎉 All tests passed!")
        print("\n💡 Tips:")
        print("• Make sure MONGODB_URI is set in your environment")
        print("• Ensure the database has an 'emails' collection")
        print("• Email documents should have 'email' and 'status' fields")
        print("• Active subscribers should have status='active'")
    else:
        print("\n❌ Some tests failed. Check your configuration.")
        print("\n🔧 Troubleshooting:")
        print("• Check MONGODB_URI environment variable")
        print("• Verify MongoDB connection and database access")
        print("• Install PyMongo: pip install pymongo")
        print("• Check email collection structure in database")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)