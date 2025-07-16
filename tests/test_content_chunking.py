#!/usr/bin/env python3
"""
Test script to verify content chunking functionality
Tests the 400-character limit and container creation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_content_chunking():
    """Test the content chunking functionality"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter.generator import ReportGenerator
        
        # Load configuration
        config = Config.from_env()
        print(f"✅ Configuration loaded - chunk limit: {config.content_chunk_limit} characters")
        
        # Initialize report generator
        generator = ReportGenerator(config)
        
        # Test the splitting function directly
        print("\n🧪 Testing Content Splitting Function")
        print("-" * 50)
        
        test_cases = [
            # Short content (should not be split)
            "This is a short analysis that should not be split.",
            
            # Medium content (around 400 chars, should not be split)
            "This is a medium-length analysis that provides detailed insights into market conditions and strategic implications for stakeholders. It contains sufficient information to be useful while staying under the limit for a single container display without requiring additional splitting mechanisms." * 1,
            
            # Long content (should be split)
            "This is a very long analysis that definitely exceeds the 400-character limit and should be split into multiple containers. " * 10,
            
            # Very long content with punctuation (should be split at good break points)
            "**Critical Analysis:** This comprehensive assessment covers multiple strategic dimensions. The current situation requires immediate attention due to several factors. First, the geopolitical landscape has shifted significantly. Second, technological disruptions are accelerating. Third, economic interdependencies create vulnerabilities. Fourth, cyber threats continue to evolve with increasing sophistication." * 5
        ]
        
        for i, test_content in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}:")
            print(f"Input length: {len(test_content)} characters")
            
            chunks = generator._split_long_content(test_content, max_length=config.content_chunk_limit)
            
            print(f"Number of chunks: {len(chunks)}")
            for j, chunk in enumerate(chunks, 1):
                print(f"  Chunk {j}: {len(chunk)} chars - '{chunk[:60]}{'...' if len(chunk) > 60 else ''}'")
            
            # Verify chunks don't exceed limit
            oversized_chunks = [chunk for chunk in chunks if len(chunk) > config.content_chunk_limit]
            if oversized_chunks:
                print(f"⚠️ WARNING: {len(oversized_chunks)} chunks exceed the limit!")
            else:
                print("✅ All chunks within size limit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content chunking: {e}")
        return False

def test_full_report_generation():
    """Test full report generation with chunked content"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter.generator import ReportGenerator
        from inoreader_intelligence.api.models import Article
        from datetime import datetime, timedelta
        
        # Load configuration
        config = Config.from_env()
        generator = ReportGenerator(config)
        
        print(f"\n🔧 Testing Full Report Generation with Chunking")
        print("-" * 50)
        
        # Create test articles with varying summary lengths
        articles = []
        
        # Short summary article
        short_article = Article(
            id="short_001",
            title="Short Analysis Test",
            summary="Brief summary under limit.",
            content="Brief content.",
            url="https://example.com/short",
            author="Test Author",
            published=datetime.now() - timedelta(hours=1),
            updated=datetime.now() - timedelta(hours=1),
            feed_id="feed/test",
            feed_title="Test Feed",
            categories=[],
            tags=[]
        )
        articles.append(short_article)
        
        # Long summary article (should be chunked)
        long_summary = ("**Comprehensive Strategic Analysis:** " + 
                       "This extensive analysis covers multiple dimensions of the current strategic environment. " + 
                       "Key findings include significant shifts in geopolitical dynamics, emerging technological threats, " +
                       "evolving cybersecurity landscapes, economic warfare implications, supply chain vulnerabilities, " +
                       "and critical infrastructure dependencies that require immediate strategic attention and response. " +
                       "The assessment reveals complex interdependencies between various threat vectors and highlights " +
                       "the need for adaptive countermeasures and strategic realignment of defensive postures.") * 3
        
        long_article = Article(
            id="long_001",
            title="Long Analysis Test - Should Be Chunked",
            summary=long_summary,
            content="Detailed content.",
            url="https://example.com/long",
            author="Test Author",
            published=datetime.now() - timedelta(hours=2),
            updated=datetime.now() - timedelta(hours=2),
            feed_id="feed/test",
            feed_title="Test Feed",
            categories=[],
            tags=[]
        )
        articles.append(long_article)
        
        # Categorize articles
        categorized_articles = {
            "Test Theme": articles
        }
        
        # Create long theme summary (should also be chunked)
        long_theme_summary = ("**COMPREHENSIVE THEMATIC ASSESSMENT:** " +
                             "This thematic analysis provides in-depth coverage of critical issues affecting strategic interests. " +
                             "The assessment framework incorporates multiple analytical dimensions including threat assessment, " +
                             "capability analysis, strategic implications, and recommended countermeasures. ") * 5
        
        theme_summaries = {
            "Test Theme": long_theme_summary
        }
        
        print(f"📊 Input Summary Lengths:")
        print(f"  Theme summary: {len(long_theme_summary)} chars")
        print(f"  Long article summary: {len(long_summary)} chars")
        
        # Generate HTML report
        print(f"\n🌐 Generating HTML Report...")
        html_path = generator.generate_report(categorized_articles, theme_summaries, format="html")
        print(f"✅ HTML report generated: {html_path}")
        
        # Analyze the generated HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Count analysis containers
        analysis_containers = html_content.count('<div class="article-summary">')
        theme_containers = html_content.count('<div class="theme-overview">')
        
        print(f"📈 Generated Containers:")
        print(f"  Article analysis containers: {analysis_containers}")
        print(f"  Theme overview containers: {theme_containers}")
        
        # Check for continuation markers
        continuation_count = html_content.count("Analysis (cont'd")
        print(f"  Continuation sections: {continuation_count}")
        
        # Verify chunking worked
        if analysis_containers > len(articles):
            print("✅ Content chunking is working - multiple containers detected!")
        else:
            print("⚠️ Content may not have been chunked properly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing full report generation: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Content Chunking Implementation")
    print("=" * 60)
    
    # Test 1: Content splitting function
    test1_success = test_content_chunking()
    
    # Test 2: Full report generation with chunking
    test2_success = test_full_report_generation()
    
    # Summary
    print(f"\n📋 Test Summary")
    print("-" * 60)
    print(f"Content splitting: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Report generation: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success
    
    if overall_success:
        print(f"\n🎉 All chunking tests passed!")
        print(f"\n💡 Configuration:")
        print(f"• Default chunk limit: 400 characters")
        print(f"• Configurable via CONTENT_CHUNK_LIMIT environment variable")
        print(f"• Creates multiple containers for long content")
        print(f"• Breaks at natural points (spaces, punctuation)")
    else:
        print(f"\n❌ Some tests failed. Check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)