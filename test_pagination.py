#!/usr/bin/env python3
"""
Test script for pagination functionality
"""

import sys
import os
from pathlib import Path

# Add src to path and set environment
sys.path.insert(0, str(Path(__file__).parent / "src"))
os.environ['PATH'] = f"/home/joel/.local/bin:{os.environ.get('PATH', '')}"
os.environ['PYTHONPATH'] = f"{Path(__file__).parent}/src"

def test_pagination():
    """Test pagination functionality"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.api import InoreaderClient
        
        config = Config.from_env()
        client = InoreaderClient(config)
        
        # Load tokens
        if not client.oauth.load_tokens():
            print("❌ No authentication tokens found")
            return False
        
        print("🧪 Testing Pagination Functionality")
        print("=" * 50)
        
        # Test 1: Regular fetch (100 articles max)
        print("\n📋 Test 1: Regular fetch (limit 100)")
        regular_articles = client.get_focus_folder_articles(
            count=100,
            use_pagination=False
        )
        print(f"✅ Regular fetch: {len(regular_articles)} articles")
        
        # Test 2: Paginated fetch (up to 200 articles)
        print(f"\n📋 Test 2: Paginated fetch (limit 200)")
        paginated_articles = client.get_focus_folder_articles(
            count=200,
            use_pagination=True,
            max_total_articles=200
        )
        print(f"✅ Paginated fetch: {len(paginated_articles)} articles")
        
        # Test 3: Small pagination test (limit 50)
        print(f"\n📋 Test 3: Small pagination test (limit 50)")
        small_paginated = client.get_focus_folder_articles(
            count=50,
            use_pagination=True,
            max_total_articles=50
        )
        print(f"✅ Small pagination: {len(small_paginated)} articles")
        
        # Compare results
        print(f"\n📊 Results Comparison:")
        print(f"   Regular (100 max):    {len(regular_articles)} articles")
        print(f"   Paginated (200 max):  {len(paginated_articles)} articles")
        print(f"   Small paginated (50): {len(small_paginated)} articles")
        
        # Show first few article titles from each
        print(f"\n📰 Sample Articles:")
        print(f"   Regular fetch first 3:")
        for i, article in enumerate(regular_articles[:3], 1):
            print(f"     {i}. {article.title[:50]}...")
        
        if len(paginated_articles) > len(regular_articles):
            print(f"   \n   Additional articles from pagination:")
            extra_articles = paginated_articles[len(regular_articles):]
            for i, article in enumerate(extra_articles[:3], 1):
                print(f"     {i}. {article.title[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_pagination():
    """Test CLI pagination options"""
    print(f"\n🖥️  CLI Pagination Examples:")
    print(f"=" * 30)
    print(f"# Regular fetch (100 articles)")
    print(f"python3 run_cli.py generate --focus")
    print(f"")
    print(f"# Paginated fetch (200 articles)")
    print(f"python3 run_cli.py generate --focus --paginate --max-articles 200")
    print(f"")
    print(f"# Large paginated fetch (500 articles)")
    print(f"python3 run_cli.py generate --focus --paginate --max-articles 500 --email")
    print(f"")
    print(f"# Configuration via environment:")
    print(f"export USE_PAGINATION=true")
    print(f"export MAX_DAILY_ARTICLES=300")
    print(f"python3 run_cli.py generate --focus --email")

def main():
    """Main test function"""
    success = test_pagination()
    
    if success:
        test_cli_pagination()
        print(f"\n🎉 Pagination tests completed successfully!")
        print(f"\n💡 Benefits of pagination:")
        print(f"   ✅ Fetch more than 100 articles")
        print(f"   ✅ Configurable limits to control costs")
        print(f"   ✅ Automatic page handling")
        print(f"   ✅ Progress tracking")
        print(f"   ✅ Robust error handling")
    else:
        print(f"\n❌ Pagination tests failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)