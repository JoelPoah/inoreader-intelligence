#!/usr/bin/env python3
"""
Script to find the Focus folder tag ID
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def find_focus_folder():
    """Find the Focus folder tag ID"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.api import InoreaderClient
        
        config = Config.from_env()
        client = InoreaderClient(config)
        
        print("🔍 Looking for Focus folder...")
        
        # Get all tags/folders
        tags = client.get_tag_list()
        
        print(f"\n📁 Found {len(tags)} folders/tags:")
        focus_tag = None
        
        for tag in tags:
            print(f"  - {tag.label} (ID: {tag.id}) - {tag.unread_count} unread")
            if "focus" in tag.label.lower():
                focus_tag = tag
                print(f"    ⭐ FOUND FOCUS FOLDER!")
        
        if focus_tag:
            print(f"\n✅ Focus folder details:")
            print(f"   Label: {focus_tag.label}")
            print(f"   ID: {focus_tag.id}")
            print(f"   Unread: {focus_tag.unread_count}")
            
            # Test getting articles from Focus folder
            print(f"\n📰 Testing article fetch from Focus folder...")
            focus_articles = client.get_articles_by_tag(focus_tag.id, count=5)
            print(f"   Found {len(focus_articles)} articles in Focus folder")
            
            for i, article in enumerate(focus_articles[:3], 1):
                print(f"   {i}. {article.title[:60]}...")
            
            return focus_tag.id
        else:
            print("\n❌ Focus folder not found. Available folders:")
            for tag in tags:
                if tag.type == "folder":
                    print(f"   - {tag.label}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    focus_id = find_focus_folder()
    if focus_id:
        print(f"\n💡 To use Focus folder only, set this in your .env:")
        print(f"   FOCUS_FOLDER_ID={focus_id}")
    else:
        print(f"\n💡 Create a Focus folder in Inoreader and add feeds to it.")