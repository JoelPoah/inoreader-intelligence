#!/usr/bin/env python3
"""
Test script to debug long analysis with sample data
Simulates scenarios with long content to identify issues with report generation
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def create_long_sample_data():
    """Create sample data with varying content lengths"""
    try:
        from inoreader_intelligence.api.models import Article
        
        # Create articles with different content lengths
        articles = []
        
        # Short content article
        short_article = Article(
            id="short_001",
            title="Short Analysis: Brief Market Update",
            summary="This is a short summary for testing purposes.",
            content="Brief content about market conditions.",
            url="https://example.com/short",
            feed_title="Test Feed",
            published=datetime.now() - timedelta(hours=1),
            author="Test Author"
        )
        articles.append(short_article)
        
        # Medium content article
        medium_summary = "This is a medium-length summary that provides more detailed analysis. " * 10
        medium_article = Article(
            id="medium_001",
            title="Medium Analysis: Detailed Market Trends",
            summary=medium_summary,
            content="Medium-length content with more details. " * 20,
            url="https://example.com/medium",
            feed_title="Test Feed",
            published=datetime.now() - timedelta(hours=2),
            author="Test Author"
        )
        articles.append(medium_article)
        
        # Long content article (as suggested in the prompt)
        long_summary = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 500
        long_article = Article(
            id="long_001",
            title="Long Analysis: Comprehensive Strategic Assessment",
            summary=long_summary,
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 1000,
            url="https://example.com/long",
            feed_title="Test Feed",
            published=datetime.now() - timedelta(hours=3),
            author="Test Author"
        )
        articles.append(long_article)
        
        # Extremely long content article to test cutoff limits
        extremely_long_summary = ("**Critical Strategic Intelligence Analysis:** This comprehensive assessment covers multiple dimensions of global security architecture, including detailed geopolitical analysis, cybersecurity threat landscapes, emerging technological disruptions, military modernization programs, economic warfare implications, supply chain vulnerabilities, critical infrastructure dependencies, diplomatic relationship matrices, intelligence coordination frameworks, defense procurement strategies, technological sovereignty considerations, information warfare capabilities, hybrid threat methodologies, counter-intelligence operations, strategic communication approaches, alliance interoperability requirements, crisis management protocols, escalation prevention mechanisms, deterrence theory applications, and long-term strategic planning methodologies. " * 200)
        
        extremely_long_content = ("**EXECUTIVE SUMMARY:**\n\nThis exhaustive intelligence report provides a comprehensive analysis of current global strategic dynamics, emerging threats, and potential future scenarios that could significantly impact national security interests.\n\n**DETAILED ANALYSIS:**\n\n" + 
                                "**Section 1: Geopolitical Landscape Assessment**\n" + 
                                "The current geopolitical environment is characterized by unprecedented complexity and multi-polar dynamics. " * 300 +
                                "\n\n**Section 2: Cybersecurity Threat Analysis**\n" + 
                                "Advanced persistent threats continue to evolve with increasing sophistication. " * 300 +
                                "\n\n**Section 3: Technological Disruption Impact**\n" + 
                                "Emerging technologies are fundamentally altering the strategic balance. " * 300 +
                                "\n\n**Section 4: Economic Security Implications**\n" + 
                                "Economic interdependencies create both vulnerabilities and opportunities. " * 300 +
                                "\n\n**Section 5: Military Modernization Trends**\n" + 
                                "Defense capabilities are rapidly advancing across multiple domains. " * 300 +
                                "\n\n**RECOMMENDATIONS:**\n" + 
                                "Based on this comprehensive analysis, the following strategic recommendations are proposed. " * 200)
        
        extremely_long_article = Article(
            id="extremely_long_001",
            title="EXTREMELY LONG ANALYSIS: Comprehensive Strategic Intelligence Assessment - Testing Content Truncation Limits",
            summary=extremely_long_summary,
            content=extremely_long_content,
            url="https://example.com/extremely-long",
            feed_title="Strategic Intelligence Feed",
            published=datetime.now() - timedelta(hours=4),
            author="Senior Intelligence Analyst"
        )
        articles.append(extremely_long_article)
        
        # Massive content article to definitely test limits
        massive_summary = ("**MASSIVE INTELLIGENCE BRIEFING:** " + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. " * 1000)
        
        massive_content = ("**CLASSIFICATION: TOP SECRET//SI//NOFORN**\n\n" + 
                          "**INTELLIGENCE ASSESSMENT REPORT**\n\n" +
                          "This is an extremely long intelligence report designed to test the absolute limits of report generation systems. " * 2000 +
                          "\n\n**APPENDIX A: Detailed Technical Analysis**\n" +
                          "Technical specifications and detailed methodological approaches. " * 1000 +
                          "\n\n**APPENDIX B: Historical Context and Precedent Analysis**\n" +
                          "Comprehensive historical review of similar situations and outcomes. " * 1000 +
                          "\n\n**APPENDIX C: Predictive Modeling and Scenario Planning**\n" +
                          "Advanced analytical models and potential future scenarios. " * 1000)
        
        massive_article = Article(
            id="massive_001",
            title="MASSIVE ANALYSIS: Ultimate Stress Test for Report Generation Systems - Maximum Content Length Testing",
            summary=massive_summary,
            content=massive_content,
            url="https://example.com/massive",
            feed_title="Maximum Load Test Feed",
            published=datetime.now() - timedelta(hours=5),
            author="Lead Systems Analyst"
        )
        articles.append(massive_article)
        
        print(f"✅ Created {len(articles)} test articles with varying content lengths")
        
        # Print content length statistics
        for article in articles:
            summary_len = len(article.summary) if article.summary else 0
            content_len = len(article.content) if article.content else 0
            print(f"📄 {article.id}: Summary={summary_len} chars, Content={content_len} chars")
        
        return articles
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return []

def test_report_generation_with_long_content():
    """Test report generation with long content data"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter.generator import ReportGenerator
        
        # Load configuration
        config = Config.from_env()
        
        # Create sample articles
        articles = create_long_sample_data()
        if not articles:
            return False
        
        # Categorize articles by theme with maximum content for testing
        categorized_articles = {
            "Geopolitical Tensions": [articles[0], articles[2]],  # short + extremely long
            "Cybersecurity Warfare": [articles[1], articles[3]],  # medium + massive
            "Strategic Foresight": [articles[4]] if len(articles) > 4 else [articles[3]]  # massive content
        }
        
        # Create theme summaries with extremely long content to test limits
        theme_summaries = {
            "Geopolitical Tensions": "**COMPREHENSIVE GEOPOLITICAL ASSESSMENT:** The current global geopolitical landscape is characterized by unprecedented complexity, multi-polar dynamics, and rapidly evolving strategic relationships that require continuous monitoring and analysis to maintain situational awareness and strategic advantage. " * 50,
            "Cybersecurity Warfare": "**ADVANCED CYBERSECURITY THREAT ANALYSIS:** The cybersecurity domain continues to evolve with increasing sophistication as state and non-state actors develop advanced capabilities that challenge traditional defense mechanisms and require innovative countermeasures and adaptive strategies. " * 75,
            "Strategic Foresight": "**COMPREHENSIVE STRATEGIC FORESIGHT ANALYSIS:** This extensive strategic foresight analysis covers multiple dimensions of future scenarios, potential implications for global security architecture, emerging technological disruptions, geopolitical realignments, economic transformations, and their cascading effects on national security interests and strategic planning requirements. " * 100
        }
        
        print("\n📊 Testing Report Generation with Long Content")
        print("-" * 50)
        
        # Initialize report generator
        generator = ReportGenerator(config)
        print("✅ ReportGenerator initialized")
        
        # Test HTML report generation
        print("\n🌐 Testing HTML Report Generation...")
        try:
            html_path = generator.generate_report(categorized_articles, theme_summaries, format="html")
            print(f"✅ HTML report generated: {html_path}")
            
            # Check file size
            html_size = Path(html_path).stat().st_size
            print(f"📄 HTML file size: {html_size:,} bytes ({html_size/1024:.1f} KB)")
            
            # Check for content truncation by reading the HTML file
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Test for specific content that should be present
            test_strings = [
                "MASSIVE INTELLIGENCE BRIEFING",
                "CLASSIFICATION: TOP SECRET",
                "APPENDIX C: Predictive Modeling",
                "Lead Systems Analyst"
            ]
            
            missing_content = []
            for test_string in test_strings:
                if test_string not in html_content:
                    missing_content.append(test_string)
            
            if missing_content:
                print(f"⚠️ POTENTIAL CONTENT TRUNCATION DETECTED in HTML!")
                print(f"❌ Missing content: {missing_content}")
            else:
                print("✅ All test content found in HTML - no truncation detected")
            
            if html_size > 1024 * 1024:  # > 1MB
                print("⚠️ HTML file is quite large (>1MB)")
            
        except Exception as e:
            print(f"❌ HTML generation failed: {e}")
            return False
        
        # Test PDF report generation
        print("\n📋 Testing PDF Report Generation...")
        try:
            pdf_path = generator.generate_report(categorized_articles, theme_summaries, format="pdf")
            print(f"✅ PDF report generated: {pdf_path}")
            
            # Check file size
            pdf_size = Path(pdf_path).stat().st_size
            print(f"📄 PDF file size: {pdf_size:,} bytes ({pdf_size/1024:.1f} KB)")
            
            # For PDF, we can't easily check content directly, but we can compare file sizes
            # and check if it completed without errors
            if pdf_size < 100 * 1024:  # Less than 100KB might indicate truncation
                print("⚠️ PDF file seems unusually small - possible content truncation")
            elif pdf_size > 10 * 1024 * 1024:  # > 10MB
                print("⚠️ PDF file is extremely large (>10MB)")
            else:
                print("✅ PDF file size appears reasonable")
            
            # Check if PDF was actually generated vs HTML fallback
            if pdf_path.endswith('.html'):
                print("⚠️ PDF generation fell back to HTML - likely due to content issues")
            else:
                print("✅ True PDF file generated successfully")
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            print("💡 This might be due to extremely long content causing PDF rendering issues")
            print("💡 Common causes: Memory limits, WeasyPrint limitations, font issues")
            return False
        
        # Test Markdown report generation
        print("\n📝 Testing Markdown Report Generation...")
        try:
            md_path = generator.generate_report(categorized_articles, theme_summaries, format="markdown")
            print(f"✅ Markdown report generated: {md_path}")
            
            # Check file size
            md_size = Path(md_path).stat().st_size
            print(f"📄 Markdown file size: {md_size:,} bytes ({md_size/1024:.1f} KB)")
            
        except Exception as e:
            print(f"❌ Markdown generation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Report generation test error: {e}")
        return False

def test_markdown_to_html_conversion():
    """Test markdown to HTML conversion with long content"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter.generator import ReportGenerator
        
        config = Config.from_env()
        generator = ReportGenerator(config)
        
        print("\n🔄 Testing Markdown to HTML Conversion")
        print("-" * 50)
        
        # Test cases with different markdown patterns
        test_cases = [
            "Short **bold** text with *italic* formatting.",
            "Medium text with **multiple bold sections** and *italic text* spread across\nmultiple lines with\nline breaks.",
            ("Long text with **extensive bold formatting** and *comprehensive italic sections* " * 50) + "\nWith\nmultiple\nline\nbreaks\nthroughout\nthe\ncontent.",
            "Very long Lorem ipsum **dolor sit amet**, *consectetur adipiscing elit*. " * 100 + "\n" + "Line break pattern\n" * 20
        ]
        
        for i, test_text in enumerate(test_cases, 1):
            print(f"\n🧪 Test case {i} (length: {len(test_text)} chars)")
            
            try:
                converted = generator._convert_markdown_to_html(test_text)
                print(f"✅ Conversion successful (output: {len(converted)} chars)")
                
                # Check for expected HTML elements
                if "**" in test_text and "<strong>" not in converted:
                    print("⚠️ Bold conversion may have failed")
                if "*" in test_text and "<em>" not in converted:
                    print("⚠️ Italic conversion may have failed")
                if "\n" in test_text and "<br>" not in converted:
                    print("⚠️ Line break conversion may have failed")
                    
            except Exception as e:
                print(f"❌ Conversion failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Markdown conversion test error: {e}")
        return False

def test_performance_with_large_datasets():
    """Test performance with larger datasets"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter.generator import ReportGenerator
        import time
        
        config = Config.from_env()
        generator = ReportGenerator(config)
        
        print("\n⚡ Testing Performance with Large Datasets")
        print("-" * 50)
        
        # Create a large dataset
        articles = create_long_sample_data()
        
        # Multiply articles to create larger dataset
        large_dataset = articles * 10  # 40 articles total
        
        categorized_articles = {
            "Geopolitical Tensions": large_dataset[:15],
            "Cybersecurity Warfare": large_dataset[15:25],
            "Strategic Foresight": large_dataset[25:35],
            "National Security": large_dataset[35:]
        }
        
        theme_summaries = {theme: f"Analysis for {theme}. " * 20 for theme in categorized_articles.keys()}
        
        print(f"📊 Testing with {sum(len(articles) for articles in categorized_articles.values())} articles")
        
        # Time HTML generation
        start_time = time.time()
        html_path = generator.generate_report(categorized_articles, theme_summaries, format="html")
        html_time = time.time() - start_time
        
        print(f"🌐 HTML generation: {html_time:.2f} seconds")
        
        # Check file size
        html_size = Path(html_path).stat().st_size
        print(f"📄 HTML file size: {html_size:,} bytes ({html_size/1024/1024:.2f} MB)")
        
        if html_time > 30:  # More than 30 seconds
            print("⚠️ HTML generation is slow (>30s)")
        
        if html_size > 10 * 1024 * 1024:  # More than 10MB
            print("⚠️ HTML file is very large (>10MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Long Analysis Debug Scenarios")
    print("=" * 60)
    
    # Test 1: Report generation with long content
    print("\n1️⃣ Report Generation with Long Content")
    test1_success = test_report_generation_with_long_content()
    
    # Test 2: Markdown to HTML conversion
    print("\n2️⃣ Markdown to HTML Conversion")
    test2_success = test_markdown_to_html_conversion()
    
    # Test 3: Performance with large datasets
    print("\n3️⃣ Performance with Large Datasets")
    test3_success = test_performance_with_large_datasets()
    
    # Summary
    print("\n📋 Test Summary")
    print("-" * 60)
    print(f"Report generation: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Markdown conversion: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Performance test: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success and test3_success
    
    if overall_success:
        print("\n🎉 All long analysis tests passed!")
        print("\n💡 Debug Tips:")
        print("• Monitor file sizes for very large reports")
        print("• Check PDF generation with long content")
        print("• Verify markdown formatting is preserved")
        print("• Watch for performance issues with large datasets")
    else:
        print("\n❌ Some tests failed.")
        print("\n🔧 Common Issues:")
        print("• PDF generation may fail with very long content")
        print("• HTML files can become very large")
        print("• Performance degrades with many articles")
        print("• Markdown formatting edge cases")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)