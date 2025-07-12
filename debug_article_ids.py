#!/usr/bin/env python3
"""Debug script to examine article IDs from Inoreader API"""

import sys
import os
sys.path.append('src')

try:
    from inoreader_intelligence.api import InoreaderClient
    from inoreader_intelligence.config import Config
    
    # Load config from environment
    config = Config.from_env()
    
    if not config.inoreader_app_id or not config.inoreader_app_key:
        print("Error: Inoreader credentials not found in environment")
        print("Please set INOREADER_APP_ID and INOREADER_APP_KEY")
        sys.exit(1)
    
    # Initialize client
    client = InoreaderClient(config)
    
    print("Fetching a few articles to examine ID structure...")
    
    # Get focus folder articles (just a few for debugging)
    try:
        articles = client.get_focus_folder_articles(count=3)
        
        print(f"\nFound {len(articles)} articles:")
        for i, article in enumerate(articles, 1):
            print(f"\nArticle {i}:")
            print(f"  ID: {article.id}")
            print(f"  Title: {article.title[:50]}...")
            print(f"  URL: {article.url}")
            print(f"  Inoreader URL: {article.get_inoreader_url()}")
            
            # Check if the conversion worked
            if article.get_inoreader_url() == article.url:
                print(f"  ⚠️  WARNING: get_inoreader_url() fell back to original URL")
                
                # Debug the conversion process
                if "item/" in article.id:
                    numeric_part = article.id.split("item/")[-1]
                    print(f"  Debug - Numeric part: {numeric_part}")
                    try:
                        hex_id = hex(int(numeric_part))[2:]
                        print(f"  Debug - Hex conversion: {hex_id}")
                        expected_url = f"https://www.inoreader.com/article/{hex_id}"
                        print(f"  Debug - Expected Inoreader URL: {expected_url}")
                    except Exception as e:
                        print(f"  Debug - Conversion error: {e}")
                else:
                    print(f"  Debug - No 'item/' found in ID")
            else:
                print(f"  ✅ Inoreader URL conversion successful")
                
    except Exception as e:
        print(f"Error fetching articles: {e}")
        
        # Try to get any articles just to see ID structure
        try:
            print("\nTrying to get today's articles instead...")
            articles = client.get_todays_articles()[:3]
            
            for i, article in enumerate(articles, 1):
                print(f"\nArticle {i}:")
                print(f"  ID: {article.id}")
                print(f"  Inoreader URL: {article.get_inoreader_url()}")
                
        except Exception as e2:
            print(f"Error fetching today's articles: {e2}")

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
except Exception as e:
    print(f"Unexpected error: {e}")