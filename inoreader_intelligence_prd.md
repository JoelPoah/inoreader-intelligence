# Inoreader Intelligence Reports - Project Requirement Document (PRD)

## 🧠 Logical Thinking – What We Want to Build

### Purpose
To build a system that connects with Inoreader, fetches articles tagged under specific categories, and generates structured daily intelligence reports. These reports will be summarized, analyzed, and presented in a user-friendly format (e.g. PDF or email digest).

### Problem Statement
Manually filtering RSS feeds for relevant, high-impact content is time-consuming. Analysts and knowledge workers need a tool to automate this curation process and summarize key developments daily.

### Goal
Automate the collection, filtration, summarization, and report generation of important RSS feed articles, making daily briefings effortless. Send it to joelpoah@gmail.com.

---

## 📊 Analytical Thinking – Skills & Tools Required

### Core Skills

#### 🧠 General
- **Reading and Interpreting API Documentation**
  - Deep understanding of Inoreader’s [OAuth 2.0 flow](https://www.inoreader.com/developers/oauth)
  - Grasp of API endpoints for:
    - Feed and tag access
    - Stream contents
    - User subscriptions and folders
    - Article metadata, flags, and annotations
  - Ability to read and convert examples (cURL, HTTP) into Python code
  - Understanding rate limits, refresh tokens, and scopes
  - API Keys found in .env

#### 🧑‍💻 Python Development
- **RESTful API Integration**
  - Use of `requests`, `httpx`, or `aiohttp` for authenticated API calls
  - Token management and refresh
- **Async Task Scheduling**
  - For fetching data and generating reports at runtime
- **Data Handling**
  - JSON parsing, pagination, stream filtering
  - Content sanitization from HTML to plain text
- **NLP Summarization**
  - Integration with language models (e.g., GPT, Hugging Face Transformers)
  - Configurable length and tone

#### 📄 Document Creation
- PDF, HTML, or Markdown generation using:
  - `Jinja2` for templating
  - `WeasyPrint`, `PDFKit`, or `Markdown-it-py`

#### 🛠️ DevOps / Automation
- Background scheduling: `cron`, `Celery`, or `n8n`
- Lightweight deployment: Docker, Python virtual environments

#### 🖥️ Optional Frontend
- **Config GUI** (Flask, Streamlit, or Electron)
  - Tag/folder selector
  - Summary tuning settings
  - Delivery options (email, local folder, Notion, etc.)

### Tools & Libraries
| Task | Tools |
|------|-------|
| API Integration | `requests`, `aiohttp`, OAuth |
| Parsing & Extraction | `BeautifulSoup`, `lxml` |
| NLP Summarization | `transformers`, `spaCy`, `GPT API` |
| Report Generation | `WeasyPrint`, `ReportLab`, `Jinja2` |
| Scheduling | `cron`, `APScheduler`, `Celery` |
| Persistence | `SQLite`, `JSON`, or lightweight `NoSQL` |
| Deployment | Docker, systemd, GitHub Actions |

---

## 🧮 Computational Thinking – Key Features & Architecture

### Core Features
- ✅ **OAuth-based Inoreader Integration**
- ✅ **Daily Scheduled Report Generation**
- ✅ **Custom Feed Filtering**
- ✅ **Article Summarization**
- ✅ **Thematic Grouping**
- ✅ **Export Formats**
- ✅ **Report Delivery**
- ✅ **Interactive CLI/GUI Config**

### System Architecture

```
            +--------------------+
            |  Inoreader API     |
            +---------+----------+
                      |
                (OAuth + Fetch)
                      |
            +---------v----------+
            |   Article Filter    |
            +---------+----------+
                      |
            +---------v----------+
            | Summarization Engine|
            +---------+----------+
                      |
            +---------v----------+
            |  Report Generator   |
            +---------+----------+
                      |
            +---------v----------+
            |  Export + Delivery  |
            +--------------------+
```

---

## 🔁 Procedural Thinking – Detailed Workflow & Steps

### 1. **Setup**
- OAuth login and folder/tag selection

### 2. **Daily Scheduler**
- Triggered fetch, parse, and clean

### 3. **Filtering & Preprocessing**
- Duplicate removal, metadata extraction

### 4. **Summarization Process**
- AI-powered summaries, optional tagging

### 5. **Thematic Grouping**
- Based on tags, keywords, or clusters

### 6. **Report Generation**
- Format into PDF/Markdown/HTML

### 7. **Export & Distribution**
- Save locally, sync, or email

### 8. **Optional Enhancements**
- UI, GPT-based insights, feedback loop

---

## 📌 Example Daily Report Outline

```
# 📰 Daily Intelligence Report – July 11, 2025

## 📌 Theme: Geopolitical Tensions

### 1. [US and China Trade Talks Collapse](https://example.com/article1)
**Source:** Reuters  
**Summary:** Talks between the US and China collapsed over disagreements on tariffs and AI regulation. Observers warn of economic ripple effects...

---

## 🧠 Theme: Cybersecurity

### 2. [APT41 Launches New Campaign in Southeast Asia](https://example.com/article2)
**Source:** The Hacker News  
**Summary:** APT41, a Chinese-linked threat actor, has initiated a spear-phishing campaign targeting military entities across ASEAN...
```

---

## ✅ Next Steps

1. Define user personas: solo analyst vs. team
2. Develop a CLI prototype with hardcoded credentials
3. Expand to full OAuth + GUI
4. Finalize export formats
5. Test with real Inoreader feeds
6. Automate deployment