"""
Main job alert system.
This script monitors job boards and sends email notifications for new postings.
"""
import sys
import time
import schedule
from datetime import datetime
from typing import List, Dict

try:
    from config_local import EMAIL_CONFIG, JOB_SEARCH_CONFIG, JOB_BOARDS, SCRAPING_CONFIG, DATABASE_CONFIG
except ImportError:
    print("⚠️  Warning: config_local.py not found. Using default config.py")
    print("⚠️  Please copy config.py to config_local.py and add your email credentials.")
    from config import EMAIL_CONFIG, JOB_SEARCH_CONFIG, JOB_BOARDS, SCRAPING_CONFIG, DATABASE_CONFIG

from database import JobDatabase
from email_notifier import EmailNotifier
from scrapers import get_all_scrapers


class JobAlertSystem:
    def __init__(self):
        self.db = JobDatabase(DATABASE_CONFIG['db_path'])
        self.notifier = EmailNotifier(
            smtp_server=EMAIL_CONFIG['smtp_server'],
            smtp_port=EMAIL_CONFIG['smtp_port'],
            sender_email=EMAIL_CONFIG['sender_email'],
            sender_password=EMAIL_CONFIG['sender_password'],
            recipient_email=EMAIL_CONFIG['recipient_email']
        )
        
        scraper_config = {
            'user_agent': SCRAPING_CONFIG['user_agent'],
            'job_boards': JOB_BOARDS
        }
        self.scrapers = get_all_scrapers(scraper_config)
        
        self.keywords = JOB_SEARCH_CONFIG['keywords']
        self.locations = JOB_SEARCH_CONFIG['locations']
        self.max_jobs = SCRAPING_CONFIG['max_jobs_per_check']
        
        print("✓ Job Alert System initialized")
        print(f"✓ Monitoring {len(self.scrapers)} job board(s)")
        print(f"✓ Keywords: {', '.join(self.keywords)}")
        print(f"✓ Locations: {', '.join(self.locations)}")
    
    def check_for_jobs(self):
        """Main function to check for new jobs and send notifications."""
        print(f"\n{'='*60}")
        print(f"🔍 Checking for new jobs at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        all_new_jobs = []
        
        # Scrape jobs from all enabled job boards
        for scraper in self.scrapers:
            scraper_name = scraper.__class__.__name__.replace('Scraper', '')
            print(f"\n📊 Scraping {scraper_name}...")
            
            try:
                jobs = scraper.scrape_jobs(
                    keywords=self.keywords,
                    locations=self.locations,
                    max_jobs=self.max_jobs
                )
                
                print(f"✓ Found {len(jobs)} job(s) from {scraper_name}")
                
                # Add new jobs to database
                new_jobs_count = 0
                for job in jobs:
                    if self.db.add_job(job):
                        all_new_jobs.append(job)
                        new_jobs_count += 1
                
                if new_jobs_count > 0:
                    print(f"✓ {new_jobs_count} new job(s) added to database")
                else:
                    print("  No new jobs found")
                
            except Exception as e:
                print(f"✗ Error scraping {scraper_name}: {str(e)}")
                continue
        
        # Send email notification if there are new jobs
        if all_new_jobs:
            print(f"\n📧 Sending email notification for {len(all_new_jobs)} new job(s)...")
            success = self.notifier.send_job_alert(all_new_jobs)
            
            if success:
                # Mark jobs as notified
                for job in all_new_jobs:
                    self.db.mark_as_notified(job['job_id'])
                print("✓ Email sent and jobs marked as notified")
            else:
                print("✗ Failed to send email notification")
        else:
            print("\n  No new jobs to notify")
        
        # Print statistics
        stats = self.db.get_stats()
        print(f"\n📈 Statistics:")
        print(f"   Total jobs tracked: {stats['total_jobs']}")
        print(f"   Jobs notified: {stats['notified_jobs']}")
        print(f"   Pending notifications: {stats['pending_notifications']}")
        
        print(f"\n{'='*60}\n")
    
    def run_once(self):
        """Run the job check once and exit."""
        self.check_for_jobs()
    
    def run_scheduled(self, interval_minutes: int = None):
        """Run the job check on a schedule."""
        if interval_minutes is None:
            interval_minutes = SCRAPING_CONFIG['check_interval_minutes']
        
        print(f"\n🚀 Starting Job Alert System")
        print(f"⏰ Checking for jobs every {interval_minutes} minute(s)")
        print(f"📧 Email notifications will be sent to: {EMAIL_CONFIG['recipient_email']}")
        print(f"\nPress Ctrl+C to stop\n")
        
        # Run immediately on start
        self.check_for_jobs()
        
        # Schedule periodic checks
        schedule.every(interval_minutes).minutes.do(self.check_for_jobs)
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Job Alert System stopped by user")
            sys.exit(0)
    
    def test_email(self):
        """Test email configuration."""
        print("📧 Testing email configuration...")
        success = self.notifier.send_test_email()
        if success:
            print("✓ Test email sent successfully!")
        else:
            print("✗ Failed to send test email. Please check your configuration.")
        return success


def main():
    """Main entry point."""
    system = JobAlertSystem()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            # Test email configuration
            system.test_email()
        
        elif command == 'once':
            # Run once and exit
            system.run_once()
        
        elif command == 'stats':
            # Show statistics
            stats = system.db.get_stats()
            print("\n📈 Job Alert System Statistics")
            print("=" * 40)
            print(f"Total jobs tracked: {stats['total_jobs']}")
            print(f"Jobs notified: {stats['notified_jobs']}")
            print(f"Pending notifications: {stats['pending_notifications']}")
            print(f"Number of sources: {stats['sources']}")
            print()
        
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python main.py          - Run continuously with scheduled checks")
            print("  python main.py test     - Send a test email")
            print("  python main.py once     - Run once and exit")
            print("  python main.py stats    - Show database statistics")
    
    else:
        # Run scheduled checks
        system.run_scheduled()


if __name__ == "__main__":
    main()
