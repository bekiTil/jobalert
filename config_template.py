"""
Configuration template for the job alert system.
COPY THIS FILE TO config_local.py AND ADD YOUR CREDENTIALS!
"""

# Email Configuration
# For Gmail: Use an App Password (https://support.google.com/accounts/answer/185833)
# For other providers: Use your regular SMTP settings
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # For Gmail (or smtp.office365.com for Outlook)
    'smtp_port': 587,
    'sender_email': 'YOUR_EMAIL@gmail.com',  # ← CHANGE THIS
    'sender_password': 'YOUR_APP_PASSWORD',   # ← CHANGE THIS (use app-specific password)
    'recipient_email': 'YOUR_EMAIL@gmail.com',  # ← CHANGE THIS
}

# Job Search Criteria - Customize based on your needs
JOB_SEARCH_CONFIG = {
    'keywords': [
        'software engineering intern',
        'software engineer intern',
        'swe intern',
        'data science intern',
        'machine learning intern',
        'ml intern',
        'ai intern',
        'backend intern',
        'frontend intern',
        'full stack intern',
        'python intern',
        'computer science intern',
        'software development intern',
        'engineering intern',
        'tech intern',
    ],
    'locations': [
        'Remote',
        'United States',
        'New York',
        'San Francisco',
        'Seattle',
        'Austin',
        'Boston',
        'Los Angeles',
        'Chicago',
        'Denver',
        'San Diego',
        'Portland',
        'Atlanta',
        'Palo Alto',
        'Mountain View',
        'Menlo Park',
        'Redmond',
    ],
    'experience_levels': ['Internship', 'Entry Level'],
}

# Job Boards to Monitor - Enable/disable as needed
JOB_BOARDS = {
    'indeed': False,     # Often blocks automated scraping
    'linkedin': True,    # Reliable for finding internships
    'greenhouse': True,  # Big tech companies (Stripe, Airbnb, etc.)
    'ashby': False,      # Modern startups
    'lever': True,       # Tech startups (Netflix, Shopify, etc.)
}

# Scraping Configuration
SCRAPING_CONFIG = {
    'check_interval_minutes': 10,  # How often to check for new jobs
    'max_jobs_per_check': 50,      # Maximum jobs to fetch per check
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Database Configuration
DATABASE_CONFIG = {
    'db_path': 'jobs.db',
}
