"""Main entry point for Inoreader Intelligence"""

import sys
from pathlib import Path
from typing import Optional, List

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .config import Config
from .api import InoreaderClient
from .summarizer import SummarizationEngine
from .reporter import ReportGenerator
from .delivery import EmailDelivery
from .scheduler import ReportScheduler
from .web_subscribers import WebSubscriberManager


class InoreaderIntelligence:
    """Main application class"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.client = InoreaderClient(self.config)
        self.summarizer = SummarizationEngine(self.config)
        self.reporter = ReportGenerator(self.config)
        self.delivery = EmailDelivery(self.config)
        self.scheduler = ReportScheduler(self.config)
        self.web_subscribers = WebSubscriberManager(self.config)
    
    def setup(self, interactive: bool = True) -> None:
        """Set up the application"""
        self.config.validate()
        self.client.authenticate(interactive=interactive)
    
    def generate_report(self, 
                       tag_ids: Optional[List[str]] = None,
                       format: str = "html",
                       send_email: bool = False,
                       use_focus_folder: bool = True,
                       interactive: bool = True) -> str:
        """Generate a single report"""
        
        # Ensure authentication is valid
        if not self.client.oauth.is_authenticated():
            self.client.authenticate(interactive=interactive)
        
        # Fetch articles
        if use_focus_folder and not tag_ids:
            articles = self.client.get_focus_folder_articles(
                count=self.config.max_daily_articles,
                use_pagination=self.config.use_pagination,
                max_total_articles=self.config.max_daily_articles
            )
            # Fallback to all unread articles if Focus folder is empty or not found
            if not articles:
                print("📰 Focus folder empty or not found, falling back to unread articles...")
                articles = self.client.get_todays_articles(tag_ids)
        else:
            articles = self.client.get_todays_articles(tag_ids)
        
        if not articles:
            raise ValueError("No articles found")
        
        # Clean content
        cleaned_articles = []
        for article in articles:
            cleaned = self.client.clean_article_content(article)
            cleaned_articles.append(cleaned)
        
        # Categorize
        categorized = self.summarizer.categorize_articles(cleaned_articles)
        
        # Generate summaries
        theme_summaries = {}
        for theme, theme_articles in categorized.items():
            if theme_articles:
                theme_summaries[theme] = self.summarizer.generate_theme_summary(theme, theme_articles)
        
        # Generate article summaries
        for theme_articles in categorized.values():
            for article in theme_articles:
                if not article.summary:
                    article.summary = self.summarizer.summarize_article(article)
        
        # Generate report
        report_path = self.reporter.generate_report(categorized, theme_summaries, format)
        
        # Send email if requested
        if send_email:
            # Get combined recipients (config + web subscribers)
            all_recipients = self.web_subscribers.get_combined_recipients()
            
            if format == "html":
                # Generate single consolidated PDF for attachment
                pdf_path = self.reporter.generate_report(categorized, theme_summaries, "pdf")
                self.delivery.send_html_with_pdf_attachment(report_path, pdf_path, recipients=all_recipients)
            else:
                # For non-HTML formats, send the file directly
                self.delivery.send_report(report_path)
        
        return report_path
    
    def start_scheduler(self, time: str = "06:00", timezone: str = "Asia/Singapore") -> None:
        """Start the daily scheduler"""
        self.scheduler.setup_daily_schedule(time, timezone)
        self.scheduler.start_scheduler()
    
    def run_once(self, tag_ids: Optional[List[str]] = None) -> str:
        """Run report generation once"""
        return self.scheduler.run_once(tag_ids)


def main():
    """Main function for direct execution"""
    try:
        app = InoreaderIntelligence()
        app.setup()
        
        print("Inoreader Intelligence is ready!")
        print("Use the CLI commands or call methods directly.")
        
        # Example usage
        report_path = app.generate_report(send_email=True)
        print(f"Report generated: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()