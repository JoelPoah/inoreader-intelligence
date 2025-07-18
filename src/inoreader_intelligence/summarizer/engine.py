"""AI-powered summarization engine"""

from typing import List, Dict, Any, Optional
from collections import defaultdict
import re
import openai
from openai import OpenAI

from ..api.models import Article
from ..config import Config


class SummarizationEngine:
    """Handle article summarization and thematic grouping"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        if config.openai_api_key:
            self.client = OpenAI(api_key=config.openai_api_key)
    
    def _format_markdown_to_html(self, text: str) -> str:
        """Convert basic markdown formatting to HTML"""
        # Convert headers
        text = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        
        # Convert bullet points
        text = re.sub(r'^- (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        
        # Wrap consecutive <li> items in <ul>
        text = re.sub(r'(<li>.*?</li>)\n?(?=<li>)', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'(<li>.*?</li>(?:\n<li>.*?</li>)*)', r'<ul>\1</ul>', text, flags=re.DOTALL)
        
        # Convert **bold** to <strong>
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *italic* to <em>
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Convert line breaks to <br>
        text = text.replace('\n', '<br>')
        
        return text
    
    def summarize_article(self, article: Article) -> str:
        """Generate a summary for a single article"""
        if not self.client:
            # Fallback to simple text truncation if no OpenAI key
            return self._truncate_text(article.content or article.summary, self.config.summary_max_length)
        
        # Check if article already has a summary
        if article.summary:
            return article.summary
        
        content = article.content
        if not content:
            return "No content"
        
        # Truncate content if too long
        if len(content) > 4000:
            content = content[:4000] + "..."
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an intelligence analyst for DIS scholarship preparation. Summarize this article in {self.config.summary_max_length} words or less with strategic focus: 1) Key events and actors involved 2) Strategic implications and goals 3) Relevance to regional security or global order 4) Potential escalations or indicators to monitor. Be analytical, not just descriptive."
                    },
                    {
                        "role": "user",
                        "content": f"Title: {article.title}\n\nContent: {content}"
                    }
                ],
                max_tokens=1000,
                temperature=0
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error summarizing article {article.id}: {e}")
            return self._truncate_text(content, self.config.summary_max_length)
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Simple text truncation fallback"""
        if len(text) <= max_length:
            return text
        
        # Try to truncate at sentence boundary
        sentences = text.split('. ')
        result = ""
        for sentence in sentences:
            if len(result + sentence + '. ') <= max_length:
                result += sentence + '. '
            else:
                break
        
        return result.strip() or text[:max_length] + "..."
    
    def categorize_articles(self, articles: List[Article]) -> Dict[str, List[Article]]:
        """Group articles by themes/categories, excluding irrelevant content"""
        if not self.client:
            return self._simple_categorization(articles)
        
        # Use AI to categorize articles
        categories = defaultdict(list)
        
        for article in articles:
            try:
                category = self._get_article_category(article)
                # Only include articles that fit into our analytical themes
                if category and category != "Uncategorized":
                    categories[category].append(article)
                # Skip articles that don't fit our military/intelligence themes
            except Exception as e:
                print(f"Error categorizing article {article.id}: {e}")
                # Don't add to any category if categorization fails
        
        return dict(categories)
    
    def _get_article_category(self, article: Article) -> str:
        """Get category for a single article using AI"""
        content = (article.title + " " + (article.summary or article.content or ""))[:1000]
        
        response = self.client.chat.completions.create(
            model=self.config.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligence analyst for DIS scholarship preparation. Categorize the following article into one of these analytical themes: Geopolitical Tensions, Cybersecurity Warfare, Emerging Tech, National Security, Military Modernization, Rules-Based Order, or Strategic Foresight. If the article is not relevant to military/intelligence analysis (e.g., sports, entertainment, local news, celebrity gossip), respond with 'IRRELEVANT'. Otherwise, respond with only the category name."
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=10,
            temperature=0.1
        )
        
        category = response.choices[0].message.content.strip()
        
        # Map common variations to analytical themes
        category_map = {
            "geopolitics": "Geopolitical Tensions",
            "geopolitical": "Geopolitical Tensions",
            "tensions": "Geopolitical Tensions",
            "statecraft": "Geopolitical Tensions",
            "diplomacy": "Geopolitical Tensions",
            "cyber": "Cybersecurity Warfare",
            "cybersecurity": "Cybersecurity Warfare",
            "security": "Cybersecurity Warfare",
            "warfare": "Cybersecurity Warfare",
            "espionage": "Cybersecurity Warfare",
            "tech": "Emerging Tech",
            "technology": "Emerging Tech",
            "emerging": "Emerging Tech",
            "innovation": "Emerging Tech",
            "ai": "Emerging Tech",
            "quantum": "Emerging Tech",
            "national": "National Security",
            "homeland": "National Security",
            "terrorism": "National Security",
            "extremism": "National Security",
            "biosecurity": "National Security",
            "military": "Military Modernization",
            "defense": "Military Modernization",
            "modernization": "Military Modernization",
            "doctrine": "Military Modernization",
            "alliance": "Military Modernization",
            "rules": "Rules-Based Order",
            "law": "Rules-Based Order",
            "legal": "Rules-Based Order",
            "international": "Rules-Based Order",
            "un": "Rules-Based Order",
            "treaty": "Rules-Based Order",
            "foresight": "Strategic Foresight",
            "trends": "Strategic Foresight",
            "climate": "Strategic Foresight",
            "demographic": "Strategic Foresight",
            "future": "Strategic Foresight",
            "asean": "Geopolitical Tensions"
        }
        
        # Filter out irrelevant content
        if category.lower() in ["irrelevant", "other", "uncategorized", "none"]:
            return None
        
        return category_map.get(category.lower(), category)
    
    def _simple_categorization(self, articles: List[Article]) -> Dict[str, List[Article]]:
        """Simple keyword-based categorization fallback"""
        categories = defaultdict(list)
        
        keyword_map = {
            "Geopolitical Tensions": ["china", "russia", "taiwan", "ukraine", "iran", "diplomacy", "sanctions", "trade war", "nuclear", "middle east", "africa", "asean", "indo-pacific"],
            "Cybersecurity Warfare": ["cyber", "hack", "breach", "malware", "ransomware", "apt", "espionage", "disinformation", "deepfake", "infrastructure attack", "zero-day"],
            "Emerging Tech": ["ai", "artificial intelligence", "quantum", "autonomous", "drone", "space", "satellite", "semiconductor", "chip", "biotech", "crispr", "5g"],
            "National Security": ["terrorism", "extremism", "pandemic", "biosecurity", "food security", "energy security", "homeland", "radicalization", "social cohesion"],
            "Military Modernization": ["military", "defense", "weapons", "hypersonic", "fighter", "naval", "alliance", "nato", "exercise", "doctrine", "hybrid warfare"],
            "Rules-Based Order": ["un", "united nations", "sanctions", "peacekeeping", "unclos", "maritime law", "sovereignty", "international law", "humanitarian"],
            "Strategic Foresight": ["climate", "demographic", "aging", "urbanization", "migration", "arctic", "resource", "megacities", "non-state", "wagner", "pmc"]
        }
        
        for article in articles:
            content = (article.title + " " + (article.summary or "")).lower()
            categorized = False
            
            for category, keywords in keyword_map.items():
                if any(keyword in content for keyword in keywords):
                    categories[category].append(article)
                    categorized = True
                    break
            
            # Skip articles that don't match any military/intelligence themes
            # Don't add to "Uncategorized" - just exclude them completely
        
        return dict(categories)
    
    def generate_theme_summary(self, theme: str, articles: List[Article]) -> str:
        """Generate a summary for a theme based on its articles"""
        if not self.client:
            return f"Theme: {theme} - {len(articles)} articles"
        
        if not articles:
            return f"No articles found for theme: {theme}"
        
        # Collect article summaries
        article_summaries = []
        for article in articles[:self.config.max_articles_per_theme]:
            summary = self.summarize_article(article)
            article_summaries.append(f"• {article.title}: {summary}")
        
        summaries_text = "\n".join(article_summaries)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an intelligence analyst for DIS scholarship preparation. Analyze the {theme} theme based on these articles. Provide a strategic brief covering: 1) Top 2-3 key developments and why they matter 2) Strategic trends and connections between events 3) First and second-order effects 4) Relevance to Singapore/regional stability if applicable 5) Key indicators to monitor next. Be analytical and trend-aware, not just summarizing."
                    },
                    {
                        "role": "user",
                        "content": summaries_text
                    }
                ],
                max_tokens=1500,
                temperature=0
            )
            
            formatted_content = self._format_markdown_to_html(response.choices[0].message.content.strip())
            return formatted_content
        except Exception as e:
            print(f"Error generating theme summary for {theme}: {e}")
            return f"Theme: {theme} - {len(articles)} articles covering recent developments."