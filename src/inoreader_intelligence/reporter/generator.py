"""Report generation system"""

import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from jinja2 import Template
import weasyprint
import re
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from ..api.models import Article
from ..config import Config
from .templates import HTML_TEMPLATE, MARKDOWN_TEMPLATE


class ReportGenerator:
    """Generate reports in various formats"""
    
    THEME_EMOJIS = {
        "Geopolitical Tensions": "🌍",
        "Cybersecurity Warfare": "🔒",
        "Emerging Tech": "⚡",
        "National Security": "🛡️",
        "Military Modernization": "⚔️",
        "Rules-Based Order": "⚖️",
        "Strategic Foresight": "🔮"
    }
    
    def __init__(self, config: Config):
        self.config = config
        self.output_dir = Path("reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def _convert_markdown_to_html(self, text: str) -> str:
        """Convert basic markdown formatting to HTML"""
        if not text:
            return text
        
        # Convert **bold** to <strong>bold</strong>
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *italic* to <em>italic</em>
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Convert line breaks to <br> tags
        text = text.replace('\n', '<br>')
        
        return text
    
    
    def generate_report(self, categorized_articles: Dict[str, List[Article]], 
                       theme_summaries: Dict[str, str],
                       format: str = "html") -> str:
        """Generate a report in the specified format"""
        
        # Prepare report data
        report_data = self._prepare_report_data(categorized_articles, theme_summaries)
        
        if format.lower() == "html":
            return self._generate_html_report(report_data)
        elif format.lower() == "pdf":
            return self._generate_pdf_report(report_data)
        elif format.lower() == "markdown":
            return self._generate_markdown_report(report_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _prepare_report_data(self, categorized_articles: Dict[str, List[Article]], 
                           theme_summaries: Dict[str, str]) -> Dict[str, Any]:
        """Prepare data for report generation"""
        
        themes = {}
        total_articles = 0
        
        for theme_name, articles in categorized_articles.items():
            # Limit articles per theme
            limited_articles = articles[:self.config.max_articles_per_theme]
            total_articles += len(limited_articles)
            
            # Prepare article data with summaries
            article_data = []
            for article in limited_articles:
                # Convert markdown to HTML
                html_summary = self._convert_markdown_to_html(article.summary or "No summary available")
                
                article_data.append({
                    "title": article.title,
                    "summary": html_summary,
                    "url": article.url,
                    "inoreader_url": article.get_inoreader_url(),
                    "feed_title": article.feed_title,
                    "published": article.published.strftime("%Y-%m-%d %H:%M"),
                    "author": article.author or "Unknown"
                })
            
            # Handle theme overview
            theme_overview_html = self._convert_markdown_to_html(theme_summaries.get(theme_name, ""))
            
            themes[theme_name] = {
                "articles": article_data,
                "overview": theme_overview_html,
                "emoji": self.THEME_EMOJIS.get(theme_name, "📄")
            }
        
        return {
            "title": f"{self.config.report_title} – {datetime.now().strftime('%B %d, %Y')}",
            "themes": themes,
            "total_articles": total_articles,
            "total_themes": len(themes),
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML report"""
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**data)
        
        # Save to file
        filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_pdf_report(self, data: Dict[str, Any]) -> str:
        """Generate PDF report"""
        # First generate HTML
        template = Template(HTML_TEMPLATE)
        html_content = template.render(**data)
        
        # Convert to PDF
        filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = self.output_dir / filename
        
        try:
            # Configure fonts
            font_config = FontConfiguration()
            
            # Create CSS for PDF
            css = CSS(string="""
                @page {
                    size: A4;
                    margin: 2cm;
                }
                body {
                    font-family: 'DejaVu Sans', sans-serif;
                    font-size: 10pt;
                    line-height: 1.4;
                }
                h1 {
                    font-size: 18pt;
                    color: #2c3e50;
                }
                h2 {
                    font-size: 14pt;
                    color: #34495e;
                    page-break-after: avoid;
                }
                h3 {
                    font-size: 12pt;
                    color: #2c3e50;
                    page-break-after: avoid;
                }
                .article {
                    page-break-inside: avoid;
                    margin-bottom: 15px;
                }
                .container {
                    background-color: white;
                    padding: 0;
                    box-shadow: none;
                }
                body {
                    background-color: white;
                }
            """, font_config=font_config)
            
            # Generate PDF
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(str(filepath), stylesheets=[css], font_config=font_config)
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            # Fallback to HTML if PDF generation fails
            return self._generate_html_report(data)
        
        return str(filepath)
    
    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        template = Template(MARKDOWN_TEMPLATE)
        markdown_content = template.render(**data)
        
        # Save to file
        filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        return str(filepath)
    
    def get_report_summary(self, filepath: str) -> str:
        """Get a summary of the generated report"""
        file_size = os.path.getsize(filepath)
        file_size_mb = file_size / (1024 * 1024)
        
        return f"Report generated: {filepath} ({file_size_mb:.2f} MB)"