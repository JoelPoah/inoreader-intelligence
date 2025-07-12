#!/usr/bin/env python3
"""
Example script to demonstrate Inoreader Intelligence usage
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from inoreader_intelligence.main import InoreaderIntelligence


def main():
    """Example usage of Inoreader Intelligence"""
    
    print("🚀 Inoreader Intelligence Example")
    print("=" * 50)
    
    try:
        # Initialize the application
        app = InoreaderIntelligence()
        
        # Setup and authenticate
        print("Setting up...")
        app.setup()
        print("✅ Setup complete!")
        
        # Generate a report
        print("\nGenerating report...")
        report_path = app.generate_report(
            format="html",
            send_email=True  # Set to False if you don't want to send email
        )
        
        print(f"✅ Report generated: {report_path}")
        
        # Option to start scheduler
        start_scheduler = input("\nStart daily scheduler? (y/n): ").lower().strip()
        
        if start_scheduler == 'y':
            print("Starting daily scheduler (Ctrl+C to stop)...")
            app.start_scheduler()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()