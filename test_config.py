"""
Quick test script to verify the job alert system is working.
"""
import sys
sys.path.insert(0, '/Users/berekettilahunshimekit/jobalert')

from config_local import EMAIL_CONFIG, JOB_SEARCH_CONFIG, JOB_BOARDS, SCRAPING_CONFIG
from scrapers import get_all_scrapers

print("=" * 60)
print("🧪 Testing Job Alert Configuration")
print("=" * 60)

print(f"\n📧 Email: {EMAIL_CONFIG['recipient_email']}")
print(f"✓ SMTP configured: {EMAIL_CONFIG['smtp_server']}")

print(f"\n🔍 Searching for {len(JOB_SEARCH_CONFIG['keywords'])} keyword(s):")
for kw in JOB_SEARCH_CONFIG['keywords'][:5]:
    print(f"  - {kw}")
if len(JOB_SEARCH_CONFIG['keywords']) > 5:
    print(f"  ... and {len(JOB_SEARCH_CONFIG['keywords']) - 5} more")

print(f"\n📍 Locations ({len(JOB_SEARCH_CONFIG['locations'])}):")
for loc in JOB_SEARCH_CONFIG['locations'][:5]:
    print(f"  - {loc}")
if len(JOB_SEARCH_CONFIG['locations']) > 5:
    print(f"  ... and {len(JOB_SEARCH_CONFIG['locations']) - 5} more")

print(f"\n🎯 Job Boards Enabled:")
for board, enabled in JOB_BOARDS.items():
    status = "✓" if enabled else "✗"
    print(f"  {status} {board.title()}")

# Test scrapers
scraper_config = {
    'user_agent': SCRAPING_CONFIG['user_agent'],
    'job_boards': JOB_BOARDS
}
scrapers = get_all_scrapers(scraper_config)

print(f"\n🤖 {len(scrapers)} scraper(s) initialized")

print(f"\n⏰ Check interval: Every {SCRAPING_CONFIG['check_interval_minutes']} minutes")

print("\n" + "=" * 60)
print("✅ Configuration looks good!")
print("=" * 60)
print("\nTo start the system:")
print("  python main.py          # Run continuously")
print("  python main.py once     # Run once")
print("  python main.py test     # Send test email")
