# Inoreader Intelligence - Technical Guide

## 🏗️ Architecture Overview

The Inoreader Intelligence system is built with a modular architecture that separates concerns into distinct components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │────│  Main App Core  │────│   Config Mgmt   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                       │                        │
┌───────▼────────┐    ┌─────────▼────────┐    ┌─────────▼────────┐
│  OAuth Auth    │    │   API Client     │    │  Summarization   │
│  (auth/)       │    │   (api/)         │    │  Engine (summ/)  │
└────────────────┘    └──────────────────┘    └──────────────────┘
                               │                        │
        ┌──────────────────────┼────────────────────────┘
        │                      │
┌───────▼────────┐    ┌────────▼────────┐    ┌─────────────────┐
│  Report Gen    │    │  Email Delivery │    │   Scheduler     │
│  (reporter/)   │    │  (delivery.py)  │    │  (scheduler/)   │
└────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Core Components

### 1. **Configuration System** (`config.py`)

**Purpose**: Centralized configuration management with environment variable support.

**Key Features**:
- Environment variable loading via python-dotenv
- Multiple email recipient support
- Configuration validation
- Default value handling

**Customization Example**:
```python
@dataclass
class Config:
    # Add new configuration options
    custom_api_timeout: int = 30
    custom_retry_attempts: int = 3
    
    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            # Add your custom environment variables
            custom_api_timeout=int(os.getenv("API_TIMEOUT", "30")),
            custom_retry_attempts=int(os.getenv("RETRY_ATTEMPTS", "3")),
            # ... existing config
        )
```

### 2. **Authentication Module** (`auth/oauth.py`)

**Purpose**: OAuth 2.0 flow management for Inoreader API access.

**Key Components**:
- `InoreaderOAuth` class handles token management
- Automatic token refresh
- Local token storage
- Browser-based authentication flow

**Customization Example**:
```python
class CustomInoreaderOAuth(InoreaderOAuth):
    def __init__(self, config: Config):
        super().__init__(config)
        # Custom redirect URI for headless environments
        self.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    
    def authenticate_headless(self) -> None:
        """Alternative authentication for server environments"""
        auth_url = self.get_authorization_url(self.redirect_uri)
        print(f"Visit: {auth_url}")
        code = input("Enter authorization code: ")
        self.exchange_code_for_token(code, self.redirect_uri)
```

### 3. **API Client** (`api/client.py`)

**Purpose**: Interface to Inoreader API with rate limiting and error handling.

**Key Features**:
- Automatic token refresh
- Article content cleaning
- Feed and tag management
- Pagination support

**Data Models** (`api/models.py`):
- `Article`: RSS article representation
- `Feed`: Feed subscription data
- `Tag`: Folder/tag information

**Customization Example**:
```python
class ExtendedInoreaderClient(InoreaderClient):
    def get_starred_articles(self, count: int = 50) -> List[Article]:
        """Get starred articles"""
        return self.get_stream_contents(
            "user/-/state/com.google/starred", 
            count
        )
    
    def get_articles_by_keyword(self, keyword: str, count: int = 50) -> List[Article]:
        """Search articles by keyword"""
        params = {"q": keyword, "n": count}
        response = self._make_request("search/items/ids", params)
        # Process search results...
        return articles
```

### 4. **Summarization Engine** (`summarizer/engine.py`)

**Purpose**: AI-powered article summarization and categorization.

**Key Features**:
- OpenAI GPT integration
- Fallback text truncation
- Theme-based categorization
- Configurable summary length

**Customization Example**:
```python
class CustomSummarizationEngine(SummarizationEngine):
    def __init__(self, config: Config):
        super().__init__(config)
        # Add custom categories
        self.custom_categories = {
            "Healthcare": ["health", "medical", "vaccine", "disease"],
            "Space": ["space", "nasa", "satellite", "mars", "moon"],
            "Finance": ["bitcoin", "crypto", "stock", "investment"]
        }
    
    def _get_article_category(self, article: Article) -> str:
        """Enhanced categorization with custom categories"""
        content = (article.title + " " + (article.summary or "")).lower()
        
        # Check custom categories first
        for category, keywords in self.custom_categories.items():
            if any(keyword in content for keyword in keywords):
                return category
        
        # Fall back to default categorization
        return super()._get_article_category(article)
    
    def summarize_with_sentiment(self, article: Article) -> dict:
        """Enhanced summarization with sentiment analysis"""
        summary = self.summarize_article(article)
        
        # Add sentiment analysis
        sentiment_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Analyze the sentiment of this article. Respond with: Positive, Negative, or Neutral."
            }, {
                "role": "user", 
                "content": article.content[:1000]
            }],
            max_tokens=10
        )
        
        return {
            "summary": summary,
            "sentiment": sentiment_response.choices[0].message.content.strip()
        }
```

### 5. **Report Generator** (`reporter/generator.py`)

**Purpose**: Generate reports in multiple formats (HTML, PDF, Markdown).

**Key Components**:
- Jinja2 templating system
- WeasyPrint for PDF generation
- Theme-based organization
- Responsive HTML design

**Templates** (`reporter/templates.py`):
- `HTML_TEMPLATE`: Styled HTML report
- `MARKDOWN_TEMPLATE`: Plain text format

**Customization Example**:
```python
# Custom template
CUSTOM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        /* Your custom CSS */
        .custom-header { background: #your-color; }
        .article-card { border: 1px solid #ccc; margin: 10px; }
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>{{ title }}</h1>
        <p>Generated: {{ generation_date }}</p>
    </div>
    
    {% for theme_name, theme_data in themes.items() %}
    <section class="theme-section">
        <h2>{{ theme_name }}</h2>
        {% for article in theme_data.articles %}
        <div class="article-card">
            <h3>{{ article.title }}</h3>
            <p class="source">{{ article.feed_title }}</p>
            <p>{{ article.summary }}</p>
            <div class="metadata">
                <span>Published: {{ article.published }}</span>
                {% if article.sentiment %}
                <span class="sentiment">Sentiment: {{ article.sentiment }}</span>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </section>
    {% endfor %}
</body>
</html>
"""

class CustomReportGenerator(ReportGenerator):
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate report with custom template"""
        template = Template(CUSTOM_TEMPLATE)
        html_content = template.render(**data)
        
        filename = f"custom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return str(filepath)
```

### 6. **Email Delivery** (`delivery.py`)

**Purpose**: Multi-recipient email delivery with HTML and attachment support.

**Key Features**:
- Multiple SMTP server support
- HTML and plain text email formats
- Attachment handling
- Individual recipient processing

**Customization Example**:
```python
class CustomEmailDelivery(EmailDelivery):
    def __init__(self, config: Config):
        super().__init__(config)
        # Add support for different email providers
        self.providers = {
            "gmail": {"server": "smtp.gmail.com", "port": 587},
            "outlook": {"server": "smtp-mail.outlook.com", "port": 587},
            "yahoo": {"server": "smtp.mail.yahoo.com", "port": 587},
            "custom": {"server": config.smtp_server, "port": config.smtp_port}
        }
    
    def send_with_custom_template(self, report_path: str, template_name: str = "default"):
        """Send email with custom template"""
        templates = {
            "executive": "📊 Executive Intelligence Brief",
            "technical": "🔧 Technical Intelligence Report", 
            "security": "🔒 Security Intelligence Alert"
        }
        
        subject = templates.get(template_name, "Daily Intelligence Report")
        return self.send_html_report(report_path, subject)
    
    def send_to_slack(self, report_path: str, webhook_url: str):
        """Alternative delivery via Slack webhook"""
        import requests
        
        with open(report_path, 'r') as f:
            content = f.read()
        
        payload = {
            "text": "Daily Intelligence Report Ready",
            "attachments": [{
                "title": "Intelligence Report",
                "text": content[:1000] + "...",
                "color": "good"
            }]
        }
        
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
```

### 7. **Scheduler** (`scheduler/scheduler.py`)

**Purpose**: Automated daily report generation with APScheduler.

**Key Features**:
- Cron-based scheduling
- Timezone support
- Error handling and logging
- Multiple job management

**Customization Example**:
```python
class CustomReportScheduler(ReportScheduler):
    def setup_custom_schedules(self):
        """Set up multiple custom schedules"""
        schedules = [
            {"time": "06:00", "tags": ["urgent"], "format": "html", "recipients": ["ceo@company.com"]},
            {"time": "08:00", "tags": ["general"], "format": "pdf", "recipients": ["team@company.com"]},
            {"time": "18:00", "tags": ["daily"], "format": "markdown", "recipients": ["archive@company.com"]}
        ]
        
        for i, schedule in enumerate(schedules):
            hour, minute = map(int, schedule["time"].split(":"))
            self.scheduler.add_job(
                func=self.generate_custom_report,
                args=[schedule],
                trigger=CronTrigger(hour=hour, minute=minute),
                id=f"custom_report_{i}",
                replace_existing=True
            )
    
    def generate_custom_report(self, schedule_config: dict):
        """Generate report with custom configuration"""
        # Override config for this specific schedule
        temp_config = self.config
        temp_config.email_recipients = schedule_config["recipients"]
        
        # Generate report with specific tags and format
        articles = self.client.get_articles_by_tags(schedule_config["tags"])
        # ... rest of custom generation logic
```

## 🔄 Data Flow

The system follows this data flow:

```
1. Authentication
   ├── OAuth token retrieval/refresh
   └── API client initialization

2. Data Fetching
   ├── Get user feeds/tags
   ├── Fetch articles (today's/filtered)
   └── Clean HTML content

3. Processing
   ├── Categorize articles by theme
   ├── Generate individual summaries
   └── Create theme overviews

4. Report Generation
   ├── Prepare report data structure
   ├── Render with Jinja2 templates
   └── Export to HTML/PDF/Markdown

5. Delivery
   ├── Send to multiple recipients
   ├── Handle delivery errors
   └── Log success/failure
```

## 📧 SMTP Configuration Guide

### Gmail Setup

1. **Enable 2-Factor Authentication** in your Google account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

3. **Configuration**:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password_here
```

### Outlook/Hotmail Setup

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your.email@outlook.com
SMTP_PASSWORD=your_password_here
```

### Yahoo Mail Setup

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your.email@yahoo.com
SMTP_PASSWORD=your_app_password_here
```

### Custom SMTP Server

```env
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587  # or 25, 465, 2525
SMTP_USERNAME=your.username
SMTP_PASSWORD=your_password
```

### Corporate Exchange Server

```env
SMTP_SERVER=smtp.company.com
SMTP_PORT=587
SMTP_USERNAME=domain\username  # or username@domain.com
SMTP_PASSWORD=your_password
```

## 🛠️ Common Customizations

### Adding New Report Formats

1. **Create new template**:
```python
# In reporter/templates.py
XML_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<intelligence_report date="{{ generation_date }}">
    <summary articles="{{ total_articles }}" themes="{{ total_themes }}"/>
    {% for theme_name, theme_data in themes.items() %}
    <theme name="{{ theme_name }}">
        <overview>{{ theme_data.overview }}</overview>
        {% for article in theme_data.articles %}
        <article>
            <title>{{ article.title }}</title>
            <source>{{ article.feed_title }}</source>
            <summary>{{ article.summary }}</summary>
            <url>{{ article.url }}</url>
        </article>
        {% endfor %}
    </theme>
    {% endfor %}
</intelligence_report>
"""
```

2. **Add generation method**:
```python
# In reporter/generator.py
def _generate_xml_report(self, data: Dict[str, Any]) -> str:
    """Generate XML report"""
    template = Template(XML_TEMPLATE)
    xml_content = template.render(**data)
    
    filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    filepath = self.output_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    return str(filepath)
```

### Adding Custom Article Filters

```python
class CustomInoreaderClient(InoreaderClient):
    def get_articles_by_importance(self, importance_level: str) -> List[Article]:
        """Filter articles by importance keywords"""
        importance_keywords = {
            "critical": ["breaking", "urgent", "alert", "emergency"],
            "high": ["important", "significant", "major"],
            "medium": ["update", "news", "report"],
            "low": ["opinion", "analysis", "commentary"]
        }
        
        all_articles = self.get_todays_articles()
        keywords = importance_keywords.get(importance_level, [])
        
        filtered_articles = []
        for article in all_articles:
            content = (article.title + " " + article.summary).lower()
            if any(keyword in content for keyword in keywords):
                filtered_articles.append(article)
        
        return filtered_articles
```

### Custom Notification Systems

```python
class MultiChannelDelivery(EmailDelivery):
    def __init__(self, config: Config):
        super().__init__(config)
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.teams_webhook = os.getenv("TEAMS_WEBHOOK_URL")
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    
    def send_to_all_channels(self, report_path: str):
        """Send to all configured channels"""
        results = {}
        
        # Email
        results["email"] = self.send_html_report(report_path)
        
        # Slack
        if self.slack_webhook:
            results["slack"] = self.send_slack_notification(report_path)
        
        # Microsoft Teams
        if self.teams_webhook:
            results["teams"] = self.send_teams_notification(report_path)
        
        # Discord
        if self.discord_webhook:
            results["discord"] = self.send_discord_notification(report_path)
        
        return results
    
    def send_slack_notification(self, report_path: str) -> bool:
        """Send notification to Slack"""
        # Implementation for Slack webhook
        pass
```

## 🔧 Configuration Options

### Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `INOREADER_APP_ID` | string | required | Inoreader application ID |
| `INOREADER_APP_KEY` | string | required | Inoreader application key |
| `EMAIL_RECIPIENTS` | string | required | Comma-separated email list |
| `EMAIL_RECIPIENT` | string | fallback | Single email (backward compatibility) |
| `OPENAI_API_KEY` | string | optional | OpenAI API key for AI features |
| `SMTP_SERVER` | string | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | integer | `587` | SMTP server port |
| `SMTP_USERNAME` | string | required | SMTP authentication username |
| `SMTP_PASSWORD` | string | required | SMTP authentication password |
| `REPORT_TIME` | string | `08:00` | Daily report generation time |
| `TIMEZONE` | string | `UTC` | Timezone for scheduling |
| `MAX_ARTICLES_PER_THEME` | integer | `10` | Maximum articles per category |
| `SUMMARY_MAX_LENGTH` | integer | `200` | Maximum summary length in words |

### Advanced Configuration

```python
# Custom config class
@dataclass
class ExtendedConfig(Config):
    # Report customization
    report_logo_url: str = ""
    report_footer_text: str = "Generated by Inoreader Intelligence"
    
    # API settings
    api_timeout: int = 30
    api_retry_attempts: int = 3
    
    # Content filtering
    exclude_keywords: List[str] = None
    include_only_keywords: List[str] = None
    
    # Advanced email settings
    email_priority: str = "normal"  # low, normal, high
    email_reply_to: str = ""
    
    def __post_init__(self):
        if self.exclude_keywords is None:
            self.exclude_keywords = []
        if self.include_only_keywords is None:
            self.include_only_keywords = []
```

## 🐛 Troubleshooting

### Common Issues

**1. Authentication Failures**
```python
# Debug OAuth issues
import logging
logging.basicConfig(level=logging.DEBUG)

# Check token file
if os.path.exists("inoreader_token.json"):
    with open("inoreader_token.json") as f:
        print(json.load(f))
```

**2. Email Delivery Issues**
```python
# Test SMTP connection
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('username', 'password')
    print("SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"SMTP error: {e}")
```

**3. Memory Issues with Large Reports**
```python
# Process articles in batches
def process_articles_in_batches(articles: List[Article], batch_size: int = 50):
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        yield batch

# Usage
for batch in process_articles_in_batches(all_articles):
    process_batch(batch)
```

**4. API Rate Limiting**
```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(60 / calls_per_minute)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Apply to API methods
@rate_limit(30)  # 30 calls per minute
def _make_request(self, endpoint: str, params: dict = None):
    # API request implementation
    pass
```

## 📚 API Reference

### Core Classes

**InoreaderIntelligence**
```python
class InoreaderIntelligence:
    def setup() -> None: ...
    def generate_report(tag_ids: List[str], format: str, send_email: bool) -> str: ...
    def start_scheduler(time: str, timezone: str) -> None: ...
```

**Config**
```python
@dataclass
class Config:
    @classmethod
    def from_env() -> Config: ...
    def validate() -> None: ...
```

**InoreaderClient**
```python
class InoreaderClient:
    def authenticate() -> None: ...
    def get_todays_articles(tag_ids: List[str]) -> List[Article]: ...
    def get_subscription_list() -> List[Feed]: ...
    def get_tag_list() -> List[Tag]: ...
```

**SummarizationEngine**
```python
class SummarizationEngine:
    def summarize_article(article: Article) -> str: ...
    def categorize_articles(articles: List[Article]) -> Dict[str, List[Article]]: ...
    def generate_theme_summary(theme: str, articles: List[Article]) -> str: ...
```

This technical guide provides the foundation for understanding and customizing the Inoreader Intelligence system. Use these patterns and examples to extend the system for your specific needs.