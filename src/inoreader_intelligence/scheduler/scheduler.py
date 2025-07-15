"""Daily scheduling system for report generation"""

import time
from datetime import datetime, timedelta
from typing import List, Optional, Callable
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from ..config import Config
from ..api import InoreaderClient
from ..summarizer import SummarizationEngine
from ..reporter import ReportGenerator
from ..delivery import EmailDelivery


class ReportScheduler:
    """Handle scheduled report generation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.scheduler = BlockingScheduler()
        self.client = InoreaderClient(config)
        self.summarizer = SummarizationEngine(config)
        self.reporter = ReportGenerator(config)
        self.delivery = EmailDelivery(config)
        
    def setup_daily_schedule(self, time_str: str = "22:00", timezone: str = "UTC") -> None:
        """Set up daily report generation schedule"""
        
        # Parse time
        hour, minute = map(int, time_str.split(":"))
        tz = pytz.timezone(timezone)
        
        # Add job to scheduler
        self.scheduler.add_job(
            func=self.generate_daily_report,
            trigger=CronTrigger(
                hour=hour,
                minute=minute,
                timezone=tz
            ),
            id="daily_report",
            name="Daily Intelligence Report Generation",
            replace_existing=True
        )
        
        print(f"Scheduled daily report generation at {time_str} {timezone}")
    
    def generate_daily_report(self, tag_ids: Optional[List[str]] = None, use_focus_folder: bool = True) -> str:
        """Generate a daily intelligence report"""
        
        print(f"Starting daily report generation at {datetime.now()}")
        
        try:
            # Ensure authentication is valid
            print("🔐 Checking authentication...")
            self.client.authenticate(interactive=False)
            
            # Fetch articles
            if use_focus_folder and not tag_ids:
                print("Fetching articles from Focus folder...")
                articles = self.client.get_focus_folder_articles(
                    count=self.config.max_daily_articles,
                    use_pagination=self.config.use_pagination,
                    max_total_articles=self.config.max_daily_articles
                )
            else:
                print("Fetching articles...")
                articles = self.client.get_todays_articles(tag_ids)
            
            if not articles:
                print("No articles found for today")
                return ""
            
            print(f"Found {len(articles)} articles")
            
            # Clean article content
            print("Cleaning article content...")
            cleaned_articles = []
            for article in articles:
                cleaned = self.client.clean_article_content(article)
                cleaned_articles.append(cleaned)
            
            # Categorize articles
            print("Categorizing articles...")
            categorized = self.summarizer.categorize_articles(cleaned_articles)
            
            # Generate summaries
            print("Generating summaries...")
            theme_summaries = {}
            for theme, theme_articles in categorized.items():
                if theme_articles:
                    theme_summaries[theme] = self.summarizer.generate_theme_summary(theme, theme_articles)
            
            # Generate individual article summaries
            print("Generating article summaries...")
            for theme_articles in categorized.values():
                for article in theme_articles:
                    if not article.summary:
                        article.summary = self.summarizer.summarize_article(article)
            
            # Generate report
            print("Generating report...")
            report_path = self.reporter.generate_report(
                categorized, 
                theme_summaries, 
                format="html"
            )
            
            print(f"Report generated: {report_path}")
            
            # Send email
            print("Sending email...")
            success = self.delivery.send_html_report(report_path)
            
            if success:
                print("Report sent successfully!")
            else:
                print("Failed to send report via email")
            
            return report_path
            
        except Exception as e:
            print(f"Error generating daily report: {e}")
            # If authentication failed, provide helpful message
            if "authentication" in str(e).lower():
                print("💡 Authentication failed. Please run './start' and choose option 4 to re-authenticate.")
            raise
    
    def run_once(self, tag_ids: Optional[List[str]] = None) -> str:
        """Run report generation once (for testing)"""
        return self.generate_daily_report(tag_ids)
    
    def start_scheduler(self) -> None:
        """Start the scheduler"""
        print("Starting report scheduler...")
        print("Press Ctrl+C to stop")
        
        try:
            self.scheduler.start()
        except KeyboardInterrupt:
            print("Scheduler stopped")
            self.scheduler.shutdown()
    
    def stop_scheduler(self) -> None:
        """Stop the scheduler"""
        self.scheduler.shutdown()
    
    def list_jobs(self) -> None:
        """List all scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        if not jobs:
            print("No scheduled jobs")
        else:
            print("Scheduled jobs:")
            for job in jobs:
                print(f"  - {job.name}: {job.next_run_time}")
    
    def remove_job(self, job_id: str) -> None:
        """Remove a scheduled job"""
        self.scheduler.remove_job(job_id)
        print(f"Removed job: {job_id}")
    
    def setup_test_schedule(self, interval_minutes: int = 30) -> None:
        """Set up a test schedule for debugging"""
        
        self.scheduler.add_job(
            func=self.generate_daily_report,
            trigger="interval",
            minutes=interval_minutes,
            id="test_report",
            name=f"Test Report Generation (every {interval_minutes} minutes)",
            replace_existing=True
        )
        
        print(f"Scheduled test report generation every {interval_minutes} minutes")