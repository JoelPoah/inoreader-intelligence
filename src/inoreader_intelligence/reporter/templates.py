"""HTML templates for report generation"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0.1);
            height: auto;
            min-height: auto;
            overflow: visible;
            overflow-wrap: break-word;
            word-break: break-word;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            padding: 10px 0;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }
        h3 {
            color: #2c3e50;
            margin-top: 25px;
        }
        .theme-overview {
            background-color: #e8f6f3;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #27ae60;
            font-size: 1.05em;
            line-height: 1.7;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .theme-overview h2, .theme-overview h3, .theme-overview h4 {
            color: #2c3e50;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        .theme-overview h2 {
            font-size: 1.2em;
            border-bottom: 2px solid #27ae60;
            padding-bottom: 5px;
        }
        .theme-overview h3 {
            font-size: 1.1em;
            color: #34495e;
        }
        .theme-overview h4 {
            font-size: 1.05em;
            color: #34495e;
        }
        .theme-overview ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .theme-overview li {
            margin-bottom: 8px;
            list-style-type: disc;
        }
        .theme-overview::before {
            content: "📊 STRATEGIC ANALYSIS";
            display: block;
            font-weight: bold;
            color: #27ae60;
            font-size: 0.9em;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }
        .article {
            margin-bottom: 25px;
            padding: 15px;
            border-left: 3px solid #bdc3c7;
            background-color: #fafafa;
            overflow-wrap: break-word;
            word-break: break-word;
        }
        .article-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        .article-source {
            font-size: 0.9em;
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        .article-summary {
            color: #34495e;
            line-height: 1.8;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f8f9fa;
            border-left: 3px solid #3498db;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }
        .article-content {
            color: #2c3e50;
            line-height: 1.8;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #fff;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }
        .article-links {
            font-size: 0.9em;
            margin-top: 10px;
            padding: 8px 0;
            border-top: 1px solid #e9ecef;
        }
        .inoreader-link {
            color: #27ae60;
            text-decoration: none;
            font-weight: 500;
        }
        .source-link {
            color: #3498db;
            text-decoration: none;
        }
        .inoreader-link:hover, .source-link:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #bdc3c7;
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .stats {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .emoji {
            font-size: 1.2em;
            margin-right: 5px;
        }
        .theme-overview strong,
        .article-summary strong {
            color: #2c3e50;
            font-weight: 600;
        }
        .theme-overview em,
        .article-summary em {
            color: #34495e;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji">📰</span>{{ title }}</h1>
        
        <div class="stats">
            <strong>{{ total_articles }}</strong> articles across <strong>{{ total_themes }}</strong> themes
        </div>
        
        {% for theme_name, theme_data in themes.items() %}
        <h2><span class="emoji">{{ theme_data.emoji }}</span>{{ theme_name }}</h2>
        
        {% if theme_data.overview %}
        <div class="theme-overview">
            {{ theme_data.overview|safe }}
        </div>
        {% endif %}
        
        {% for article in theme_data.articles %}
        <div class="article">
            <div class="article-title">{{ loop.index }}. {{ article.title }}</div>
            <div class="article-source"><strong>Source:</strong> {{ article.feed_title }} | <strong>Published:</strong> {{ article.published }}</div>
            
            <div class="article-summary">
                <strong>📊 Analysis:</strong><br>
                {{ article.summary|safe }}
            </div>
            
            <div class="article-links">
                {% if article.inoreader_url %}
                <a href="{{ article.inoreader_url }}" target="_blank" class="inoreader-link">📖 Read in Inoreader</a>
                {% endif %}
                {% if article.url %}
                {% if article.inoreader_url %} | {% endif %}<a href="{{ article.url }}" target="_blank" class="source-link">🔗 Original Source</a>
                {% endif %}
            </div>
        </div>
        {% endfor %}
        
        {% if not theme_data.articles %}
        <p><em>No articles found for this theme.</em></p>
        {% endif %}
        
        {% endfor %}
        
        <div class="footer">
            Generated on {{ generation_date }}<br>
            <em>Inoreader Intelligence Reports</em>
        </div>
    </div>
</body>
</html>
"""

MARKDOWN_TEMPLATE = """
# {{ title }}

**{{ total_articles }}** articles across **{{ total_themes }}** themes

{% for theme_name, theme_data in themes.items() %}
## {{ theme_data.emoji }} {{ theme_name }}

{% if theme_data.overview %}
> {{ theme_data.overview }}

{% endif %}
{% for article in theme_data.articles %}
### {{ loop.index }}. {{ article.title }}

**Source:** {{ article.feed_title }}

{{ article.summary }}

{% if article.url %}
[Read full article →]({{ article.url }})
{% endif %}

---

{% endfor %}
{% if not theme_data.articles %}
*No articles found for this theme.*

{% endif %}
{% endfor %}

---

*Generated on {{ generation_date }}*  
*Inoreader Intelligence Reports*
"""