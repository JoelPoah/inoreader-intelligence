#!/usr/bin/env python3
"""
Test script to find and use Focus folder
"""

import sys
import os
from pathlib import Path

# Add src to path and set environment
sys.path.insert(0, str(Path(__file__).parent / "src"))
os.environ['PATH'] = f"/home/joel/.local/bin:{os.environ.get('PATH', '')}"
os.environ['PYTHONPATH'] = f"{Path(__file__).parent}/src"

def test_focus_folder():
    """Test Focus folder functionality"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.api import InoreaderClient
        
        config = Config.from_env()
        client = InoreaderClient(config)
        
        # Load tokens
        if not client.oauth.load_tokens():
            print("❌ No authentication tokens found")
            return False
        
        print("🔍 Testing Focus folder functionality...")
        
        # List all folders
        print("\n📁 Available folders:")
        tags = client.get_tag_list()
        focus_found = False
        
        print(f"Debug: Found {len(tags)} total tags")
        for i, tag in enumerate(tags):
            print(f"Debug tag {i}: label='{tag.label}', type='{tag.type}', id='{tag.id}'")
            if tag.label:  # Show all labeled items (folders and labels)
                icon = "⭐" if tag.label and "focus" in tag.label.lower() else "📁"
                print(f"   {icon} {tag.label} ({tag.unread_count} unread)")
                if tag.label and "focus" in tag.label.lower():
                    focus_found = True
                    print(f"   >>> FOUND FOCUS: {tag.label}")
        
        if not focus_found:
            print("\n❌ No Focus folder found!")
            print("💡 Please create a 'Focus' folder in Inoreader and add your important feeds to it.")
            print("   1. Go to Inoreader.com")
            print("   2. Create a new folder called 'Focus'")
            print("   3. Move your most important feeds into the Focus folder")
            print("   4. Run this test again")
            return False
        
        # Test Focus folder article fetching
        print(f"\n📰 Testing Focus folder article fetching...")
        focus_articles = client.get_focus_folder_articles(count=10)
        
        if focus_articles:
            print(f"✅ Found {len(focus_articles)} articles in Focus folder:")
            for i, article in enumerate(focus_articles[:5], 1):
                print(f"   {i}. {article.title[:60]}...")
                print(f"      From: {article.feed_title}")
            
            if len(focus_articles) > 5:
                print(f"   ... and {len(focus_articles) - 5} more articles")
        else:
            print("⚠️  No articles found in Focus folder")
            print("💡 Make sure your Focus folder has feeds with recent articles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_report_generation():
    """Test report generation with Focus folder"""
    try:
        from inoreader_intelligence.main import InoreaderIntelligence
        
        print(f"\n🔄 Testing report generation with Focus folder...")
        
        app = InoreaderIntelligence()
        
        # Setup authentication
        app.setup()
        
        # Generate report from Focus folder only
        report_path = app.generate_report(
            format="html",
            use_focus_folder=True,
            send_email=False
        )
        
        print(f"✅ Report generated successfully: {report_path}")
        
        # Check file size
        import os
        file_size = os.path.getsize(report_path)
        print(f"📄 Report size: {file_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Focus Folder Integration")
    print("=" * 50)
    
    # Test 1: Focus folder detection
    focus_test = test_focus_folder()
    
    if focus_test:
        # Test 2: Report generation
        report_test = test_report_generation()
        
        if report_test:
            print(f"\n🎉 All tests passed!")
            print(f"\n📋 Usage:")
            print(f"   # Generate report from Focus folder only")
            print(f"   python3 run_cli.py generate --focus --email")
            print(f"   ")
            print(f"   # Generate report from all feeds")
            print(f"   python3 run_cli.py generate --all --email")
        else:
            print(f"\n⚠️  Focus folder found but report generation failed")
    else:
        print(f"\n❌ Focus folder test failed")
    
    return focus_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)