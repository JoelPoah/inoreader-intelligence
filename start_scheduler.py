#!/usr/bin/env python3
"""Start daily intelligence report scheduler at 06:00 Singapore Time"""

from src.inoreader_intelligence import InoreaderIntelligence
import time

def main():
    try:
        app = InoreaderIntelligence()
        app.setup()
        
        # Start scheduler for 06:00 Singapore Time
        app.start_scheduler(time="06:00", timezone="Asia/Singapore")
        
        print("📅 Daily intelligence reports scheduled for 06:00 Singapore Time")
        print("📧 Reports will be emailed automatically")
        print("📊 Reports include AI analysis and full article content")
        print("🔗 Reports include Inoreader links for full access")
        print("\nPress Ctrl+C to stop the scheduler...")
        
        # Keep the scheduler running
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
    except Exception as e:
        print(f"❌ Error starting scheduler: {e}")
        print("💡 Make sure your .env file is configured properly")

if __name__ == "__main__":
    main()