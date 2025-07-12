#!/usr/bin/env python3
"""
Debug script to find folders and authenticate
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
os.environ['PATH'] = f"/home/joel/.local/bin:{os.environ.get('PATH', '')}"

def debug_folders():
    """Debug folder detection"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.api import InoreaderClient
        
        config = Config.from_env()
        client = InoreaderClient(config)
        
        print("🔧 Checking authentication...")
        
        # Load existing tokens and authenticate if needed
        if not client.oauth.load_tokens():
            print("❌ No saved tokens found. Running authentication...")
            client.authenticate()
        
        # Try to get user info first
        try:
            user_info = client.get_user_info()
            print(f"✅ Authenticated as: {user_info.get('userName', 'Unknown')}")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("🔄 Trying to refresh tokens...")
            try:
                client.oauth.refresh_access_token()
                user_info = client.get_user_info()
                print(f"✅ Re-authenticated as: {user_info.get('userName', 'Unknown')}")
            except Exception as refresh_error:
                print(f"❌ Token refresh failed: {refresh_error}")
                print("🔄 Need to re-authenticate manually")
                return False
        
        print("📁 Listing all tags and folders...")
        
        # Get all tags/folders
        tags = client.get_tag_list()
        
        print(f"\n📋 Found {len(tags)} items:")
        focus_candidates = []
        
        for i, tag in enumerate(tags, 1):
            icon = "📁" if tag.type == "folder" else "🏷️"
            print(f"  {i:2d}. {icon} {tag.label}")
            print(f"      Type: {tag.type}, Unread: {tag.unread_count}")
            print(f"      ID: {tag.id}")
            
            # Check for Focus folder candidates
            if "focus" in tag.label.lower():
                focus_candidates.append(tag)
                print(f"      ⭐ POTENTIAL FOCUS FOLDER!")
            
            print()
        
        if focus_candidates:
            print(f"🎯 Found {len(focus_candidates)} Focus folder candidates:")
            for candidate in focus_candidates:
                print(f"   - {candidate.label} (ID: {candidate.id})")
                
                # Test fetching articles from this folder
                print(f"     Testing article fetch...")
                try:
                    articles = client.get_articles_by_tag(candidate.id, count=5)
                    print(f"     ✅ Found {len(articles)} articles")
                    for j, article in enumerate(articles[:3], 1):
                        print(f"        {j}. {article.title[:50]}...")
                except Exception as e:
                    print(f"     ❌ Error fetching articles: {e}")
        else:
            print("❌ No Focus folder found!")
            print("💡 Folders available for Focus setup:")
            for tag in tags:
                if tag.type == "folder":
                    print(f"   - {tag.label}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_folders()