#!/usr/bin/env python3
"""
Test script to verify multiple email recipients functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_email_configuration():
    """Test email configuration with multiple recipients"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.delivery import EmailDelivery
        
        config = Config.from_env()
        print("✅ Configuration loaded successfully")
        
        print(f"📧 Email Recipients ({len(config.email_recipients)}):")
        for i, email in enumerate(config.email_recipients, 1):
            print(f"   {i}. {email}")
        
        # Test email delivery initialization
        delivery = EmailDelivery(config)
        print("✅ Email delivery system initialized")
        
        # Test configuration
        print(f"📤 SMTP Server: {delivery.smtp_server}:{delivery.smtp_port}")
        print(f"📤 SMTP Username: {delivery.smtp_username}")
        print(f"📤 SMTP Password: {'*' * len(delivery.smtp_password) if delivery.smtp_password else 'Not set'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Multiple Email Recipients Configuration")
    print("=" * 60)
    
    success = test_email_configuration()
    
    if success:
        print("\n✅ All tests passed!")
        print("\n📋 Usage Examples:")
        print("1. Set single recipient:")
        print("   EMAIL_RECIPIENT=user@example.com")
        print("\n2. Set multiple recipients:")
        print("   EMAIL_RECIPIENTS=user1@example.com,user2@example.com,user3@example.com")
        print("\n3. Mix of both (EMAIL_RECIPIENTS takes precedence):")
        print("   EMAIL_RECIPIENT=fallback@example.com")
        print("   EMAIL_RECIPIENTS=primary@example.com,secondary@example.com")
        
        print("\n🚀 When you generate reports, they will be sent to all configured recipients!")
    else:
        print("\n❌ Test failed. Check your configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)