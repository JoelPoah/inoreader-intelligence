# Inoreader Intelligence Reports

A Python application that generates daily intelligence reports from your RSS feeds using Inoreader's API. Transform your RSS feeds into structured, AI-powered intelligence briefings.

## 🚀 Features

- **🔐 OAuth Authentication**: Secure integration with Inoreader API
- **🧠 AI-Powered Summarization**: Uses OpenAI GPT to generate concise article summaries
- **📊 Thematic Categorization**: Automatically groups articles by themes (Geopolitics, Cybersecurity, Technology, etc.)
- **📄 Multiple Export Formats**: Generate reports in HTML, PDF, or Markdown
- **📧 Email Delivery**: Automatically send reports to your email
- **⏰ Daily Scheduling**: Set up automated daily report generation
- **🖥️ CLI Interface**: Easy-to-use command-line interface

## 📋 Requirements

- Python 3.8+
- Inoreader account with API access
- OpenAI API key (optional, for AI summarization)
- Email account for report delivery (optional)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/joelpoah/inoreader-intelligence.git
cd inoreader-intelligence
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
Edit `.env` file with your credentials:
```env
INOREADER_APP_ID=your_app_id
INOREADER_APP_KEY=your_app_key

# Multiple email recipients (comma-separated)
EMAIL_RECIPIENTS=user1@gmail.com,user2@company.com,user3@example.com

# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_api_key

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

4. **Install the package**:
```bash
pip install -e .
```

## 🚀 Quick Start

### 1. Initial Setup
```bash
inoreader-intelligence setup
```

### 2. Generate Your First Report
```bash
inoreader-intelligence generate --format html --email
```

### 3. Schedule Daily Reports
```bash
inoreader-intelligence schedule --time "08:00" --timezone "UTC" --start
```

## 📖 Usage

### Command Line Interface

**Setup and authenticate**:
```bash
inoreader-intelligence setup
```

**List your feeds**:
```bash
inoreader-intelligence feeds
```

**List your tags/folders**:
```bash
inoreader-intelligence tags
```

**Generate a report**:
```bash
inoreader-intelligence generate --format pdf --email
```

**Test the system**:
```bash
inoreader-intelligence test
```

### Python API

```python
from inoreader_intelligence.main import InoreaderIntelligence

# Initialize
app = InoreaderIntelligence()
app.setup()

# Generate report
report_path = app.generate_report(
    format="html",
    send_email=True
)

# Start scheduler
app.start_scheduler(time="08:00", timezone="UTC")
```

### Example Script

Run the included example:
```bash
python run_example.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `INOREADER_APP_ID` | Yes | Your Inoreader app ID |
| `INOREADER_APP_KEY` | Yes | Your Inoreader app key |
| `EMAIL_RECIPIENTS` | Yes | Email addresses for reports (comma-separated) |
| `EMAIL_RECIPIENT` | Yes | Single email address (fallback for EMAIL_RECIPIENTS) |
| `OPENAI_API_KEY` | Optional | For AI summarization |
| `SMTP_SERVER` | Optional | Email server for sending reports |
| `SMTP_USERNAME` | Optional | Email username |
| `SMTP_PASSWORD` | Optional | Email password |
| `USE_PAGINATION` | Optional | Enable pagination for >100 articles (true/false) |
| `MAX_DAILY_ARTICLES` | Optional | Maximum articles to process daily (default: 100) |

### Report Formats

- **HTML**: Rich, styled reports perfect for email
- **PDF**: Professional documents for archiving
- **Markdown**: Plain text format for integration

## 📧 SMTP Email Setup

### Gmail Configuration

1. **Enable 2-Factor Authentication** in your Google account
2. **Generate App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update .env file**:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

### Outlook/Hotmail Configuration

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your.email@outlook.com
SMTP_PASSWORD=your_account_password
```

### Yahoo Mail Configuration

1. **Enable App Passwords** in Yahoo Account Security
2. **Generate App Password** for mail applications
3. **Configuration**:
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your.email@yahoo.com
SMTP_PASSWORD=your_app_password
```

### Corporate/Custom SMTP

```env
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587  # Common ports: 25, 465, 587, 2525
SMTP_USERNAME=your.username
SMTP_PASSWORD=your_password
```

### Multiple Email Recipients

Configure multiple recipients using comma-separated values:

```env
# Single recipient
EMAIL_RECIPIENTS=user@example.com

# Multiple recipients
EMAIL_RECIPIENTS=user1@gmail.com,user2@company.com,user3@yahoo.com

# Mix personal and work emails
EMAIL_RECIPIENTS=personal@gmail.com,work@company.com,team@organization.org
```

### Troubleshooting Email Issues

**Common Problems**:

1. **"Authentication failed"** - Check username/password and app passwords
2. **"Connection refused"** - Verify SMTP server and port
3. **"SSL/TLS errors"** - Try different ports (587 for STARTTLS, 465 for SSL)
4. **"Blocked by provider"** - Enable "less secure apps" or use app passwords

**Test Email Configuration**:
```bash
# Test your email setup
python3 run_cli.py test
```

## 📄 Pagination Support

### Handle Large Article Volumes

The system supports pagination to process more than 100 articles when your Focus folder has high volume.

### Configuration Options

**Environment Variables**:
```env
# Enable pagination
USE_PAGINATION=true
MAX_DAILY_ARTICLES=300
```

**CLI Options**:
```bash
# Generate report with pagination (up to 200 articles)
python3 run_cli.py generate --focus --paginate --max-articles 200

# Large reports (up to 500 articles)
python3 run_cli.py generate --focus --paginate --max-articles 500 --email
```

### Pagination Benefits

- ✅ **Process unlimited articles** from Focus folder
- ✅ **Configurable limits** to control processing costs
- ✅ **Automatic page handling** with continuation tokens
- ✅ **Progress tracking** during multi-page fetches
- ✅ **Cost control** with maximum article limits

### Usage Examples

```bash
# Standard: 100 articles (no pagination)
python3 run_cli.py generate --focus

# Medium: 200 articles with pagination  
python3 run_cli.py generate --focus --paginate --max-articles 200

# Large: 500 articles with pagination
python3 run_cli.py generate --focus --paginate --max-articles 500

# Test pagination functionality
python3 test_pagination.py
```

## 🤖 AI Features

When configured with an OpenAI API key, the system provides:

- **Smart Summarization**: Concise summaries of lengthy articles
- **Thematic Analysis**: AI-powered categorization of articles
- **Theme Summaries**: Overview of key trends per category

Without an API key, the system uses:
- Simple text truncation for summaries
- Keyword-based categorization
- Basic statistics

## 📊 Report Structure

Each report includes:

1. **Summary Statistics**: Article count and theme breakdown
2. **Thematic Sections**: Articles grouped by category
3. **Article Summaries**: Key insights from each article
4. **Source Links**: Direct links to original articles

## 🗂️ Project Structure

```
inoreader-intelligence/
├── src/inoreader_intelligence/
│   ├── auth/              # OAuth authentication
│   ├── api/               # Inoreader API client
│   ├── summarizer/        # AI summarization engine
│   ├── reporter/          # Report generation
│   ├── scheduler/         # Daily scheduling
│   ├── cli.py            # Command-line interface
│   └── main.py           # Main application
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
├── .env                  # Environment variables
└── run_example.py        # Example usage
```

## 🔒 Security

- API keys are stored securely in environment variables
- OAuth tokens are saved locally and refreshed automatically
- No sensitive data is logged or transmitted unnecessarily

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## 🚧 Development

To set up for development:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy src/
```