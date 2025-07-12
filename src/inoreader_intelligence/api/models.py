"""Data models for Inoreader API"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Article:
    """Represents an article from Inoreader"""
    
    id: str
    title: str
    summary: str
    content: str
    url: str
    author: Optional[str]
    published: datetime
    updated: datetime
    feed_id: str
    feed_title: str
    categories: List[str]
    tags: List[str]
    read: bool = False
    starred: bool = False
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Article":
        """Create Article from API response"""
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            summary=data.get("summary", {}).get("content", ""),
            content=data.get("content", {}).get("content", ""),
            url=data.get("alternate", [{}])[0].get("href", ""),
            author=data.get("author", ""),
            published=datetime.fromtimestamp(data.get("published", 0)),
            updated=datetime.fromtimestamp(data.get("updated", 0)),
            feed_id=data.get("origin", {}).get("streamId", ""),
            feed_title=data.get("origin", {}).get("title", ""),
            categories=data.get("categories", []),
            tags=[tag.get("label", "") for tag in data.get("tags", [])],
            read="read" in data.get("categories", []),
            starred="starred" in data.get("categories", [])
        )
    
    def get_inoreader_url(self) -> str:
        """Get Inoreader URL to view this article in Inoreader"""
        import urllib.parse
        
        # Try the original hex ID method first
        try:
            # Extract numeric part from ID like "tag:google.com,2005:reader/item/0000000012345"
            if "item/" in self.id:
                numeric_id = self.id.split("item/")[-1]
                # Check if it's all digits
                if numeric_id.isdigit():
                    # Convert to hex and format for Inoreader URL
                    hex_id = hex(int(numeric_id))[2:]  # Remove '0x' prefix
                    return f"https://www.inoreader.com/article/{hex_id}"
                else:
                    print(f"Warning: Article ID numeric part contains non-digits: {numeric_id}")
            else:
                print(f"Warning: Article ID does not contain 'item/': {self.id}")
        except ValueError as e:
            print(f"Error converting article ID {self.id} to int: {e}")
        except Exception as e:
            print(f"Unexpected error with article ID {self.id}: {e}")
        
        # Fallback: Use global search with first few words of title
        if hasattr(self, 'title') and self.title:
            # Extract first few meaningful words from title for better search
            words = self.title.split()[:4]  # Take first 4 words
            search_query = ' '.join(words)
            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)
            return f"https://www.inoreader.com/search/global/{encoded_query}"
        
        return self.url  # Final fallback to original URL
    
    def get_full_content(self) -> str:
        """Get the full content with fallback to summary"""
        if self.content and len(self.content.strip()) > len(self.summary.strip()):
            return self.content
        return self.summary


@dataclass
class Feed:
    """Represents a feed subscription"""
    
    id: str
    title: str
    url: str
    html_url: str
    description: str
    icon_url: Optional[str]
    categories: List[str]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Feed":
        """Create Feed from API response"""
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            url=data.get("url", ""),
            html_url=data.get("htmlUrl", ""),
            description=data.get("description", ""),
            icon_url=data.get("iconUrl"),
            categories=data.get("categories", [])
        )


@dataclass
class Tag:
    """Represents a tag/folder"""
    
    id: str
    label: str
    type: str
    unread_count: int = 0
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Tag":
        """Create Tag from API response"""
        # Extract label from ID if not provided
        label = data.get("label", "")
        if not label and "label/" in data["id"]:
            # Extract label from ID like "user/123/label/Focus"
            label = data["id"].split("label/")[-1]
        elif not label and "state/" in data["id"]:
            # Extract state name like "starred", "broadcast"
            label = data["id"].split("state/")[-1].split("/")[-1]
        
        return cls(
            id=data["id"],
            label=label,
            type=data.get("type", ""),
            unread_count=data.get("unreadCount", 0)
        )