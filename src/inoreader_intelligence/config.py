"""Configuration management for Inoreader Intelligence"""

import os
from dataclasses import dataclass
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration"""
    
    # Inoreader API Configuration
    inoreader_app_id: str
    inoreader_app_key: str
    
    # Email Configuration
    email_recipients: List[str]
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Report Configuration
    report_title: str = "Daily Intelligence Report"
    max_articles_per_theme: int = 10
    summary_max_length: int = 200
    max_daily_articles: int = 100
    use_pagination: bool = False
    content_chunk_limit: int = 400  # Character limit for content chunks
    
    # Scheduling Configuration
    report_time: str = "06:00"  # 6 AM SGT daily
    timezone: str = "Asia/Singapore"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables"""
        # Parse email recipients (comma-separated)
        email_recipients_str = os.getenv("EMAIL_RECIPIENTS", os.getenv("EMAIL_RECIPIENT", ""))
        email_recipients = []
        if email_recipients_str:
            email_recipients = [email.strip() for email in email_recipients_str.split(",")]
        
        return cls(
            inoreader_app_id=os.getenv("INOREADER_APP_ID", ""),
            inoreader_app_key=os.getenv("INOREADER_APP_KEY", ""),
            email_recipients=email_recipients,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
            max_daily_articles=int(os.getenv("MAX_DAILY_ARTICLES", "100")),
            use_pagination=os.getenv("USE_PAGINATION", "false").lower() == "true",
            content_chunk_limit=int(os.getenv("CONTENT_CHUNK_LIMIT", "400")),
        )
    
    def validate(self) -> None:
        """Validate required configuration"""
        if not self.inoreader_app_id:
            raise ValueError("INOREADER_APP_ID is required")
        if not self.inoreader_app_key:
            raise ValueError("INOREADER_APP_KEY is required")
        if not self.email_recipients:
            raise ValueError("EMAIL_RECIPIENTS or EMAIL_RECIPIENT is required")