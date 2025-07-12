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