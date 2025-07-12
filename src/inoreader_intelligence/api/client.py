"""Inoreader API client"""

import requests
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time

from ..auth import InoreaderOAuth
from ..config import Config
from .models import Article, Feed, Tag


class InoreaderClient:
    """Client for interacting with Inoreader API"""
    
    BASE_URL = "https://www.inoreader.com/reader/api/0"
    
    def __init__(self, config: Config):
        self.config = config
        self.oauth = InoreaderOAuth(config)
        self.session = requests.Session()
        
    def authenticate(self) -> None:
        """Authenticate with Inoreader"""
        self.oauth.authenticate_interactive()
        
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make authenticated request to Inoreader API"""
        if not self.oauth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.BASE_URL}/{endpoint}"
        headers = self.oauth.get_auth_headers()
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                # Try to refresh token
                self.oauth.refresh_access_token()
                headers = self.oauth.get_auth_headers()
                response = self.session.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            raise
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information"""
        return self._make_request("user-info")
    
    def get_subscription_list(self) -> List[Feed]:
        """Get list of subscribed feeds"""
        response = self._make_request("subscription/list")
        feeds = []
        
        for sub in response.get("subscriptions", []):
            feeds.append(Feed.from_api_response(sub))
        
        return feeds
    
    def get_tag_list(self) -> List[Tag]:
        """Get list of tags/folders"""
        response = self._make_request("tag/list")
        tags = []
        
        for tag in response.get("tags", []):
            tags.append(Tag.from_api_response(tag))
        
        return tags
    
    def get_stream_contents(self, stream_id: str, count: int = 20, 
                          start_time: Optional[datetime] = None, 
                          continuation: Optional[str] = None) -> tuple[List[Article], Optional[str]]:
        """Get articles from a stream (feed, tag, or folder)"""
        params = {
            "n": count,
            "output": "json"
        }
        
        if start_time:
            params["ot"] = int(start_time.timestamp())
        
        if continuation:
            params["c"] = continuation
        
        response = self._make_request(f"stream/contents/{stream_id}", params)
        articles = []
        
        for item in response.get("items", []):
            articles.append(Article.from_api_response(item))
        
        next_continuation = response.get("continuation")
        return articles, next_continuation
    
    def get_unread_articles(self, count: int = 50, 
                           start_time: Optional[datetime] = None) -> List[Article]:
        """Get unread articles"""
        articles, _ = self.get_stream_contents("user/-/state/com.google/reading-list", count, start_time)
        return articles
    
    def get_articles_by_tag(self, tag_id: str, count: int = 50,
                           start_time: Optional[datetime] = None) -> List[Article]:
        """Get articles from a specific tag/folder"""
        articles, _ = self.get_stream_contents(tag_id, count, start_time)
        return articles
    
    def get_todays_articles(self, tag_ids: Optional[List[str]] = None) -> List[Article]:
        """Get articles from today"""
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        articles = []
        
        if tag_ids:
            for tag_id in tag_ids:
                tag_articles = self.get_articles_by_tag(tag_id, count=100, start_time=start_time)
                articles.extend(tag_articles)
        else:
            articles = self.get_unread_articles(count=100, start_time=start_time)
        
        # Remove duplicates
        seen_ids = set()
        unique_articles = []
        for article in articles:
            if article.id not in seen_ids:
                seen_ids.add(article.id)
                unique_articles.append(article)
        
        return unique_articles
    
    def get_focus_folder_articles(self, count: int = 100, 
                                 start_time: Optional[datetime] = None,
                                 use_pagination: bool = False,
                                 max_total_articles: int = 500) -> List[Article]:
        """Get articles from Focus folder only"""
        # Find Focus folder
        focus_tag_id = self.find_focus_folder_id()
        if not focus_tag_id:
            print("❌ Focus folder not found. Please create a 'Focus' folder in Inoreader.")
            return []
        
        if start_time is None:
            start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if use_pagination:
            print(f"📁 Fetching articles from Focus folder with pagination (max: {max_total_articles})...")
            return self.get_all_focus_articles_paginated(focus_tag_id, start_time, max_total_articles)
        else:
            print(f"📁 Fetching articles from Focus folder...")
            articles = self.get_articles_by_tag(focus_tag_id, count, start_time)
            print(f"📰 Found {len(articles)} articles in Focus folder")
            return articles
    
    def get_all_focus_articles_paginated(self, focus_tag_id: str, 
                                       start_time: Optional[datetime] = None,
                                       max_total_articles: int = 500) -> List[Article]:
        """Get all articles from Focus folder using pagination"""
        all_articles = []
        continuation = None
        page_count = 0
        articles_per_page = 100
        
        while len(all_articles) < max_total_articles:
            page_count += 1
            remaining_articles = max_total_articles - len(all_articles)
            fetch_count = min(articles_per_page, remaining_articles)
            
            print(f"📄 Fetching page {page_count} ({fetch_count} articles)...")
            
            try:
                articles, continuation = self.get_stream_contents(
                    focus_tag_id, 
                    count=fetch_count, 
                    start_time=start_time,
                    continuation=continuation
                )
                
                if not articles:
                    print("📭 No more articles available")
                    break
                
                all_articles.extend(articles)
                print(f"📰 Page {page_count}: Found {len(articles)} articles (total: {len(all_articles)})")
                
                # If no continuation token or we got fewer articles than requested, we're done
                if not continuation or len(articles) < fetch_count:
                    print("📋 Reached end of available articles")
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching page {page_count}: {e}")
                break
        
        print(f"✅ Pagination complete: {len(all_articles)} total articles from {page_count} pages")
        return all_articles
    
    def find_focus_folder_id(self) -> Optional[str]:
        """Find the Focus folder/label ID"""
        try:
            tags = self.get_tag_list()
            for tag in tags:
                # Check if label contains "focus" (case insensitive)
                if tag.label and "focus" in tag.label.lower():
                    print(f"✅ Found Focus folder: {tag.label} (ID: {tag.id})")
                    return tag.id
            
            print("❌ Focus folder/label not found in tags:")
            for tag in tags:
                if tag.label:  # Only show labeled items
                    print(f"   - {tag.label}")
            return None
        except Exception as e:
            print(f"Error finding Focus folder: {e}")
            return None
    
    def clean_article_content(self, article: Article) -> Article:
        """Clean article content from HTML"""
        if article.content:
            soup = BeautifulSoup(article.content, "html.parser")
            article.content = soup.get_text().strip()
        
        if article.summary:
            soup = BeautifulSoup(article.summary, "html.parser")  
            article.summary = soup.get_text().strip()
        
        return article
    
    def mark_as_read(self, article_ids: List[str]) -> None:
        """Mark articles as read"""
        # This would require a POST request to mark articles as read
        # Implementation depends on specific API endpoints
        pass