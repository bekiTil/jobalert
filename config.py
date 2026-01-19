"""
Configuration file for the job alert system.
Copy this to config_local.py and add your credentials.
"""

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # For Gmail
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # Use app-specific password for Gmail
    'recipient_email': 'your-email@gmail.com',
}

# Job Search Criteria
JOB_SEARCH_CONFIG = {
    'keywords': ['software engineer', 'backend developer', 'python developer'],
    'locations': ['Remote', 'United States', 'San Francisco'],
    'experience_levels': ['Entry Level', 'Mid Level', 'Senior'],
}

# Job Boards to Monitor
JOB_BOARDS = {
    'indeed': True,
    'linkedin': True,
    'greenhouse': True,
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'check_interval_minutes': 10,  # How often to check for new jobs
    'max_jobs_per_check': 50,
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
}

# Database Configuration
DATABASE_CONFIG = {
    'db_path': 'jobs.db',
}
