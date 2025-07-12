# Inoreader Intelligence Reports

A Python application that generates daily intelligence reports from your RSS feeds using Inoreader's API and AI-powered analysis. Transform your RSS feeds into structured, military-focused intelligence briefings for DIS scholarship preparation.

## 🚀 Features

- **🔐 OAuth Authentication**: Secure integration with Inoreader API
- **🧠 AI-Powered Analysis**: Uses OpenAI GPT-4 for strategic intelligence summaries and categorization
- **📊 Military-Focused Themes**: Automatically categorizes articles into 7 analytical themes relevant to defense and intelligence
- **📄 Multiple Export Formats**: Generate reports in HTML, PDF, or Markdown
- **📧 Email Delivery**: Automatically send reports with HTML content and PDF attachments
- **⏰ Singapore Time Scheduling**: Daily automated reports at 06:00 SGT
- **🎯 Focus Folder Optimization**: Efficiently processes only your curated Focus folder feeds
- **🔗 Inoreader Integration**: Direct links to view full articles in your Inoreader account

## 📊 Intelligence Themes

The system categorizes articles into these military/intelligence analytical themes:

1. **🌍 Geopolitical Tensions** - Great power competition, regional conflicts, diplomatic relations
2. **🔒 Cybersecurity Warfare** - Nation-state APTs, critical infrastructure attacks, information warfare
3. **⚡ Emerging Tech** - AI/quantum computing, autonomous weapons, space militarization, semiconductors
4. **🛡️ National Security** - Terrorism, biosecurity, homeland protection, extremist threats
5. **⚔️ Military Modernization** - Defense procurement, hybrid warfare, alliance activities
6. **⚖️ Rules-Based Order** - UN actions, international law, sovereignty issues
7. **🔮 Strategic Foresight** - Climate security, demographic shifts, future threat indicators

> **Note**: Articles not relevant to military/intelligence analysis (sports, entertainment, local news) are automatically excluded.

## 📋 Requirements

- Python 3.8+
- Inoreader account with API access
- OpenAI API key (for AI analysis and categorization)
- Email account for report delivery
- Focus folder setup in your Inoreader account

## 🎯 How the Focus Folder System Works

The system is optimized for efficiency - it **only fetches articles from your Focus folder**, not all your feeds:

### Efficient Focus Folder Flow:
1. **Find Focus Folder** → API call to get your folder list
2. **Fetch ONLY Focus Articles** → Direct API call to Focus folder contents (~100 articles)
3. **Process & Analyze** → Clean content, categorize, and generate AI summaries

### Performance Benefits:
- ✅ **40x faster**: Downloads ~100 Focus articles instead of ~4,100 from all feeds
- ✅ **Lower costs**: Reduced API usage and OpenAI token consumption  
- ✅ **Higher quality**: Curated content from your Focus folder
- ✅ **Smart pagination**: Handles >100 articles when needed

### Content Quality:
- **Full Article Content**: Uses complete "coffee cup" content from webpages when available
- **HTML Cleaning**: Strips formatting to get clean text for AI analysis
- **Fallback Support**: Uses RSS summaries if full content unavailable
- **Length Optimization**: Truncates at 4,000 characters for optimal AI processing

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
Copy `.env.example` to `.env` and fill in your credentials:
```env
INOREADER_APP_ID=your_app_id
INOREADER_APP_KEY=your_app_key

# Multiple email recipients (comma-separated)
EMAIL_RECIPIENTS=user1@gmail.com,user2@company.com

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Optional: Pagination for large Focus folders
USE_PAGINATION=true
MAX_DAILY_ARTICLES=200
```

4. **Install the package**:
```bash
pip install -e .
```

## 🚀 Quick Start

### 1. Setup Your Focus Folder in Inoreader
- Create a folder called "Focus" in your Inoreader account
- Add your most important intelligence/military news feeds to this folder
- The system will only process articles from this folder

### 2. Initial Authentication
```bash
python3 run_example.py
```
This will:
- Authenticate with Inoreader (opens browser for OAuth)
- Generate your first intelligence report
- Send it via email if configured

### 3. Daily Automated Reports at 06:00 SGT

**Start the scheduler for daily 06:00 Singapore Time reports:**
```bash
python3 -c "
from src.inoreader_intelligence import InoreaderIntelligence
app = InoreaderIntelligence()
app.setup()
app.start_scheduler(time='06:00', timezone='Asia/Singapore')
print('Daily reports scheduled for 06:00 SGT')
input('Press Enter to stop scheduler...')
"
```

**Alternative method using the CLI:**
```bash
# Create a simple scheduler script
cat > start_scheduler.py << 'EOF'
from src.inoreader_intelligence import InoreaderIntelligence

app = InoreaderIntelligence()
app.setup()
app.start_scheduler(time="06:00", timezone="Asia/Singapore")
print("📅 Daily intelligence reports scheduled for 06:00 Singapore Time")
print("📧 Reports will be emailed automatically")
print("Press Ctrl+C to stop...")

try:
    import time
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("Scheduler stopped")
EOF

python3 start_scheduler.py
```

### 4. Generate Manual Reports
```bash
# Generate HTML report with email delivery
python3 run_example.py

# Generate PDF report only
python3 -c "
from src.inoreader_intelligence import InoreaderIntelligence
app = InoreaderIntelligence()
app.setup()
report = app.generate_report(format='pdf', send_email=False)
print(f'PDF report: {report}')
"
```

## 📧 Email Configuration

### Gmail Setup (Recommended)

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

### Multiple Recipients
```env
# Send to multiple people (comma-separated)
EMAIL_RECIPIENTS=analyst1@ministry.gov.sg,analyst2@ministry.gov.sg,team@defense.gov.sg
```

### What You'll Receive
- **HTML email** with immediate report viewing
- **PDF attachment** with full content for offline reading
- **Inoreader links** to view articles in your account
- **Original source links** for non-subscribers

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INOREADER_APP_ID` | required | Your Inoreader application ID |
| `INOREADER_APP_KEY` | required | Your Inoreader application key |
| `EMAIL_RECIPIENTS` | required | Comma-separated email list |
| `OPENAI_API_KEY` | required | OpenAI API key for AI analysis |
| `OPENAI_MODEL` | `gpt-4` | OpenAI model (gpt-4, gpt-4-turbo, etc.) |
| `SMTP_SERVER` | `smtp.gmail.com` | Email server |
| `SMTP_PORT` | `587` | Email server port |
| `USE_PAGINATION` | `false` | Handle >100 articles in Focus folder |
| `MAX_DAILY_ARTICLES` | `100` | Maximum articles to process |

### Pagination for Large Focus Folders

If your Focus folder has >100 articles daily:
```env
USE_PAGINATION=true
MAX_DAILY_ARTICLES=300
```

## 📊 Report Structure

Each intelligence report includes:

1. **📈 Executive Summary**: Article count and theme breakdown
2. **📊 Strategic Analysis**: AI-generated thematic overviews with trends and implications
3. **📄 Full Article Content**: Complete article text with AI analysis
4. **🔗 Access Links**: 
   - 📖 Inoreader links for subscribers
   - 🔗 Original source links
5. **📱 Professional Formatting**: Clean layout optimized for both screen and print

## 🕐 Singapore Time Scheduling

The system is configured for Singapore operations:

### Default Schedule
- **Time**: 06:00 Singapore Time (Asia/Singapore timezone)
- **Frequency**: Daily
- **Delivery**: Automatic email with HTML + PDF attachment

### Custom Scheduling
```python
# Different times (still Singapore timezone)
app.start_scheduler(time="08:00", timezone="Asia/Singapore")  # 8 AM SGT
app.start_scheduler(time="18:00", timezone="Asia/Singapore")  # 6 PM SGT
```

## 🗂️ Project Structure

```
inoreader-intelligence/
├── src/inoreader_intelligence/
│   ├── auth/              # OAuth authentication
│   ├── api/               # Inoreader API client  
│   ├── summarizer/        # AI analysis engine
│   ├── reporter/          # Report generation
│   ├── scheduler/         # Daily scheduling
│   └── main.py           # Main application
├── requirements.txt       # Dependencies
├── .env.example          # Configuration template
├── run_example.py        # Quick start script
└── README.md            # This file
```

## 🔒 Security Features

- **OAuth 2.0 Authentication**: Secure token-based access to Inoreader
- **Environment Variables**: API keys stored securely in .env files
- **Automatic Token Refresh**: Handles expired tokens transparently
- **Content Filtering**: Only processes curated Focus folder content
- **No Sensitive Logging**: Credentials never appear in logs

## 🚧 Troubleshooting

### Common Issues

1. **"No articles found"**
   - Ensure your Focus folder contains feeds
   - Check if Focus folder has recent articles
   - Verify folder name is exactly "Focus"

2. **Email delivery fails**
   - Verify SMTP credentials and app passwords
   - Check recipient email addresses
   - Test with single recipient first

3. **Authentication errors**
   - Verify Inoreader API credentials
   - Check if OAuth tokens need refresh
   - Ensure correct app permissions

4. **Empty reports**
   - Verify OpenAI API key is valid
   - Check if articles match intelligence themes
   - Review content filtering settings

### Test Commands
```bash
# Test email configuration
python3 -c "
from src.inoreader_intelligence.delivery import EmailDelivery
from src.inoreader_intelligence.config import Config
delivery = EmailDelivery(Config.from_env())
print('Email test - check configuration')
"

# Test Inoreader connection
python3 -c "
from src.inoreader_intelligence import InoreaderIntelligence
app = InoreaderIntelligence()
app.setup()
print('Inoreader connection successful')
"
```

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
1. Check this documentation
2. Review the troubleshooting section
3. Create an issue with detailed information

---

**⚡ Quick Command Reference**

```bash
# Setup and first run
python3 run_example.py

# Start daily 06:00 SGT scheduler
python3 start_scheduler.py

# Manual report generation
python3 -c "from src.inoreader_intelligence import InoreaderIntelligence; app = InoreaderIntelligence(); app.setup(); print(app.generate_report(send_email=True))"
```

**🎯 Optimized for DIS Scholarship Preparation**
- Focuses on military and intelligence themes
- Filters out irrelevant content automatically  
- Provides strategic analysis and trend insights
- Scheduled for Singapore timezone operations


Backend Deployment (Railway):
  cd /home/joel/Inoreader/backend
  railway login
  railway link
  railway up

  Frontend Deployment (Vercel):
  cd /home/joel/Inoreader/frontend/strategic-intelligence
  vercel --prod

  Environment Variables:
  After deployment, set these in Railway dashboard:
  - MONGODB_URI
  - STRIPE_SECRET_KEY
  - NODE_ENV=production

  And in Vercel dashboard:
  - REACT_APP_API_URL (Railway backend URL)
  - REACT_APP_STRIPE_PUBLISHABLE_KEY