"""Command-line interface for Inoreader Intelligence"""

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, TaskID
from typing import Optional, List
import sys

from .config import Config
from .api import InoreaderClient
from .summarizer import SummarizationEngine
from .reporter import ReportGenerator
from .delivery import EmailDelivery
from .scheduler import ReportScheduler

app = typer.Typer(help="Inoreader Intelligence Reports CLI")
console = Console()


@app.command()
def setup():
    """Initial setup and authentication"""
    console.print("🔧 Setting up Inoreader Intelligence...", style="bold blue")
    
    try:
        config = Config.from_env()
        config.validate()
        
        client = InoreaderClient(config)
        client.authenticate()
        
        # Test connection
        user_info = client.get_user_info()
        console.print(f"✅ Successfully authenticated as: {user_info.get('userName', 'Unknown')}")
        
        # Show available feeds and tags
        feeds = client.get_subscription_list()
        tags = client.get_tag_list()
        
        console.print(f"📰 Found {len(feeds)} feeds and {len(tags)} tags")
        console.print(f"📧 Email recipients: {', '.join(config.email_recipients)}")
        
        console.print("✅ Setup complete!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Setup failed: {e}", style="bold red")
        sys.exit(1)


@app.command()
def feeds():
    """List all subscribed feeds"""
    try:
        config = Config.from_env()
        client = InoreaderClient(config)
        
        feeds = client.get_subscription_list()
        
        if not feeds:
            console.print("No feeds found", style="yellow")
            return
        
        table = Table(title="Subscribed Feeds")
        table.add_column("Title", style="cyan")
        table.add_column("URL", style="magenta")
        table.add_column("Categories", style="green")
        
        for feed in feeds:
            categories = ", ".join(feed.categories) if feed.categories else "None"
            table.add_row(feed.title, feed.url, categories)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")


@app.command()
def tags():
    """List all tags/folders"""
    try:
        config = Config.from_env()
        client = InoreaderClient(config)
        
        tags = client.get_tag_list()
        
        if not tags:
            console.print("No tags found", style="yellow")
            return
        
        table = Table(title="Tags and Folders")
        table.add_column("Label", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Unread", style="green")
        table.add_column("ID", style="dim")
        
        for tag in tags:
            table.add_row(tag.label, tag.type, str(tag.unread_count), tag.id)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")


@app.command()
def generate(
    format: str = typer.Option("html", help="Output format: html, pdf, markdown"),
    tag_ids: Optional[List[str]] = typer.Option(None, "--tag", help="Filter by tag IDs"),
    send_email: bool = typer.Option(False, "--email", help="Send report via email"),
    focus_only: bool = typer.Option(True, "--focus/--all", help="Use Focus folder only or all articles"),
    max_articles: int = typer.Option(100, "--max-articles", help="Maximum number of articles to process"),
    paginate: bool = typer.Option(False, "--paginate", help="Use pagination to fetch all available articles")
):
    """Generate a report now"""
    
    console.print("🔄 Generating intelligence report...", style="bold blue")
    
    if paginate:
        console.print(f"📄 Pagination enabled - fetching up to {max_articles} articles", style="blue")
    
    try:
        config = Config.from_env()
        client = InoreaderClient(config)
        summarizer = SummarizationEngine(config)
        reporter = ReportGenerator(config)
        delivery = EmailDelivery(config)
        
        with Progress() as progress:
            task = progress.add_task("Fetching articles...", total=100)
            
            # Fetch articles
            if focus_only and not tag_ids:
                articles = client.get_focus_folder_articles(
                    count=max_articles,
                    use_pagination=paginate,
                    max_total_articles=max_articles
                )
            else:
                articles = client.get_todays_articles(tag_ids)
            progress.update(task, advance=20)
            
            if not articles:
                console.print("❌ No articles found", style="yellow")
                return
            
            progress.update(task, description="Cleaning content...", advance=10)
            
            # Clean content
            cleaned_articles = []
            for article in articles:
                cleaned = client.clean_article_content(article)
                cleaned_articles.append(cleaned)
            
            progress.update(task, description="Categorizing articles...", advance=20)
            
            # Categorize
            categorized = summarizer.categorize_articles(cleaned_articles)
            
            progress.update(task, description="Generating summaries...", advance=30)
            
            # Generate summaries
            theme_summaries = {}
            for theme, theme_articles in categorized.items():
                if theme_articles:
                    theme_summaries[theme] = summarizer.generate_theme_summary(theme, theme_articles)
            
            # Generate article summaries
            for theme_articles in categorized.values():
                for article in theme_articles:
                    if not article.summary:
                        article.summary = summarizer.summarize_article(article)
            
            progress.update(task, description="Generating report...", advance=15)
            
            # Generate report
            report_path = reporter.generate_report(categorized, theme_summaries, format)
            
            progress.update(task, description="Complete!", advance=5)
        
        console.print(f"✅ Report generated: {report_path}", style="bold green")
        
        # Send email if requested
        if send_email:
            console.print("📧 Sending email...", style="blue")
            if format == "html":
                success = delivery.send_html_report(report_path)
            else:
                success = delivery.send_report(report_path)
            
            if success:
                console.print("✅ Email sent!", style="green")
            else:
                console.print("❌ Failed to send email", style="red")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def schedule(
    time: str = typer.Option("08:00", help="Time for daily reports (HH:MM)"),
    timezone: str = typer.Option("UTC", help="Timezone for scheduling"),
    start: bool = typer.Option(False, "--start", help="Start the scheduler immediately")
):
    """Set up daily report scheduling"""
    
    console.print("⏰ Setting up daily report schedule...", style="bold blue")
    
    try:
        config = Config.from_env()
        scheduler = ReportScheduler(config)
        
        scheduler.setup_daily_schedule(time, timezone)
        
        console.print(f"✅ Daily reports scheduled for {time} {timezone}", style="green")
        
        if start:
            console.print("🚀 Starting scheduler...", style="blue")
            scheduler.start_scheduler()
        else:
            console.print("Use 'inoreader-intelligence schedule --start' to start the scheduler", style="dim")
    
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")


@app.command()
def test():
    """Test the system with current configuration"""
    
    console.print("🧪 Testing Inoreader Intelligence...", style="bold blue")
    
    try:
        config = Config.from_env()
        config.validate()
        
        # Test authentication
        console.print("Testing authentication...", style="blue")
        client = InoreaderClient(config)
        user_info = client.get_user_info()
        console.print(f"✅ Authentication: {user_info.get('userName', 'Unknown')}", style="green")
        
        # Test article fetching
        console.print("Testing article fetching...", style="blue")
        articles = client.get_todays_articles()
        console.print(f"✅ Found {len(articles)} articles", style="green")
        
        # Test summarization
        if config.openai_api_key:
            console.print("Testing AI summarization...", style="blue")
            summarizer = SummarizationEngine(config)
            if articles:
                summary = summarizer.summarize_article(articles[0])
                console.print(f"✅ Summarization: {len(summary)} characters", style="green")
        else:
            console.print("⚠️  No OpenAI API key - using fallback summarization", style="yellow")
        
        # Test report generation
        console.print("Testing report generation...", style="blue")
        reporter = ReportGenerator(config)
        console.print("✅ Report generator ready", style="green")
        
        console.print("✅ All tests passed!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="bold red")


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()