#!/usr/bin/env python3
"""
Test script to verify the Inoreader Intelligence system is working
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from inoreader_intelligence.config import Config
        print("✅ Config module imported")
        
        from inoreader_intelligence.api import InoreaderClient
        print("✅ API client imported")
        
        from inoreader_intelligence.summarizer import SummarizationEngine
        print("✅ Summarization engine imported")
        
        from inoreader_intelligence.reporter import ReportGenerator
        print("✅ Report generator imported")
        
        from inoreader_intelligence.delivery import EmailDelivery
        print("✅ Email delivery imported")
        
        from inoreader_intelligence.scheduler import ReportScheduler
        print("✅ Scheduler imported")
        
        from inoreader_intelligence.main import InoreaderIntelligence
        print("✅ Main application imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from inoreader_intelligence.config import Config
        
        config = Config.from_env()
        print(f"✅ Config loaded:")
        print(f"   - App ID: {config.inoreader_app_id}")
        print(f"   - Email: {config.email_recipient}")
        print(f"   - OpenAI: {'✓' if config.openai_api_key else '✗'}")
        
        config.validate()
        print("✅ Configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_summarizer():
    """Test summarization engine"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.summarizer import SummarizationEngine
        
        config = Config.from_env()
        summarizer = SummarizationEngine(config)
        print("✅ Summarization engine initialized")
        
        # Test fallback summarization
        test_text = "This is a long article about artificial intelligence and machine learning. " * 20
        summary = summarizer._truncate_text(test_text, 100)
        print(f"✅ Fallback summarization works: {len(summary)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Summarizer error: {e}")
        return False

def test_reporter():
    """Test report generator"""
    try:
        from inoreader_intelligence.config import Config
        from inoreader_intelligence.reporter import ReportGenerator
        
        config = Config.from_env()
        reporter = ReportGenerator(config)
        print("✅ Report generator initialized")
        
        # Test template rendering
        test_data = {
            "title": "Test Report",
            "themes": {"Technology": {"articles": [], "overview": "Test theme", "emoji": "⚡"}},
            "total_articles": 0,
            "total_themes": 1,
            "generation_date": "2025-01-01 00:00:00"
        }
        
        # Test data preparation
        prepared = reporter._prepare_report_data({}, {})
        print("✅ Report data preparation works")
        
        return True
    except Exception as e:
        print(f"❌ Reporter error: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    try:
        reports_dir = Path("reports")
        if not reports_dir.exists():
            reports_dir.mkdir()
            print("✅ Created reports directory")
        else:
            print("✅ Reports directory exists")
        
        return True
    except Exception as e:
        print(f"❌ Directory error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Inoreader Intelligence System")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Summarizer", test_summarizer),
        ("Reporter", test_reporter),
        ("Directories", test_directories)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n🎯 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! The system is ready to use.")
        print("\n🚀 To use the system:")
        print("1. Run: python3 run_example.py")
        print("2. Follow the OAuth authentication flow")
        print("3. Generate your first intelligence report!")
    else:
        print(f"❌ {total - passed} tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)