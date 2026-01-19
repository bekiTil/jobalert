"""
Comprehensive list of tech companies and their job board platforms.
Add more companies as you discover them!
"""

# Big Tech Companies (mostly use Greenhouse or custom platforms)
BIG_TECH = [
    'google', 'microsoft', 'apple', 'amazon', 'meta', 'netflix', 
    'tesla', 'nvidia', 'intel', 'amd', 'salesforce', 'oracle',
    'adobe', 'ibm', 'cisco', 'qualcomm', 'broadcom'
]

# Unicorn Startups & High-Growth Companies
GREENHOUSE_COMPANIES = [
    'airbnb', 'stripe', 'uber', 'lyft', 'doordash', 'instacart',
    'robinhood', 'coinbase', 'snowflake', 'databricks', 'palantir',
    'affirm', 'chime', 'plaid', 'square', 'cash-app', 'brex',
    'ramp', 'mercury', 'gusto', 'rippling', 'deel', 'remote',
    'notion', 'airtable', 'miro', 'figma', 'canva', 'dropbox',
    'box', 'zoom', 'slack', 'asana', 'monday', 'atlassian',
    'gitlab', 'github', 'vercel', 'netlify', 'cloudflare',
    'datadog', 'splunk', 'new-relic', 'pagerduty', 'sentry',
    'twilio', 'sendgrid', 'segment', 'amplitude', 'mixpanel',
    'waymo', 'cruise', 'zoox', 'argo-ai', 'aurora', 'motional',
    'scale-ai', 'c3-ai', 'datarobot', 'h2o-ai', 'weights-biases',
    'openai', 'anthropic', 'cohere', 'hugging-face', 'stability-ai',
    'reddit', 'discord', 'pinterest', 'snap', 'twitter', 'tiktok',
    'shopify', 'etsy', 'wayfair', 'wish', 'poshmark', 'mercari',
    'peloton', 'calm', 'headspace', 'noom', 'whoop', 'oura',
    'oscar-health', 'ro', 'hims-hers', 'tempus', '23andme',
]

# Companies using Lever ATS
LEVER_COMPANIES = [
    'netflix', 'shopify', 'canva', 'figma', 'plaid', 'faire',
    'reddit', 'squarespace', 'gitlab', 'grammarly', 'carta',
    'brex', 'gusto', 'samsara', 'verkada', 'anduril', 'lattice',
    'superhuman', 'airtable', 'webflow', 'retool', 'postman',
]

# Companies using Ashby ATS (newer, modern startups)
ASHBY_COMPANIES = [
    'ramp.com', 'anthropic.com', 'scale.com', 'retool.com',
    'notion.so', 'varda.com', 'anduril.com', 'astranis.com',
    'watershed.com', 'ramp', 'merge.dev', 'census.dev',
]

# Top AI/ML Companies
AI_ML_COMPANIES = [
    'openai', 'anthropic', 'deepmind', 'meta-ai', 'google-ai',
    'microsoft-research', 'nvidia-research', 'scale-ai',
    'cohere', 'hugging-face', 'stability-ai', 'midjourney',
    'character-ai', 'adept', 'inflection-ai', 'runway',
]

# Top Fintech Companies
FINTECH_COMPANIES = [
    'stripe', 'plaid', 'square', 'robinhood', 'coinbase',
    'chime', 'affirm', 'brex', 'ramp', 'mercury', 'bill',
    'marqeta', 'checkout', 'adyen', 'wise', 'revolut',
]

# Cloud & Infrastructure Companies
CLOUD_COMPANIES = [
    'aws', 'azure', 'gcp', 'cloudflare', 'vercel', 'netlify',
    'heroku', 'digital-ocean', 'linode', 'vultr', 'fly-io',
    'railway', 'render', 'planetscale', 'neon', 'supabase',
]

# Data & Analytics Companies
DATA_COMPANIES = [
    'snowflake', 'databricks', 'datadog', 'splunk', 'elastic',
    'amplitude', 'mixpanel', 'segment', 'looker', 'tableau',
    'dbt', 'fivetran', 'airbyte', 'census', 'hightouch',
]

# Cybersecurity Companies
SECURITY_COMPANIES = [
    'crowdstrike', 'palo-alto-networks', 'okta', 'auth0',
    'snyk', 'lacework', 'wiz', 'orca-security', 'sysdig',
    '1password', 'bitwarden', 'lastpass', 'duo-security',
]

# Developer Tools & Platforms
DEVTOOLS_COMPANIES = [
    'github', 'gitlab', 'jetbrains', 'postman', 'docker',
    'hashicorp', 'vercel', 'netlify', 'railway', 'render',
    'linear', 'notion', 'coda', 'airtable', 'retool',
]

# Social Media & Communication
SOCIAL_COMPANIES = [
    'meta', 'twitter', 'tiktok', 'snapchat', 'pinterest',
    'discord', 'reddit', 'telegram', 'whatsapp', 'signal',
]

# E-commerce & Marketplace
ECOMMERCE_COMPANIES = [
    'amazon', 'shopify', 'etsy', 'ebay', 'mercari', 'poshmark',
    'depop', 'faire', 'whatnot', 'grailed', 'stockx', 'goat',
]

# Gaming Companies
GAMING_COMPANIES = [
    'riot-games', 'epic-games', 'unity', 'roblox', 'discord',
    'twitch', 'blizzard', 'activision', 'ea', 'ubisoft',
]

# Autonomous Vehicles & Robotics
AV_ROBOTICS_COMPANIES = [
    'waymo', 'cruise', 'zoox', 'argo-ai', 'aurora', 'motional',
    'nuro', 'embark', 'plus-ai', 'tesla-autopilot', 'comma-ai',
    'boston-dynamics', 'anduril', 'skydio', 'zipline',
]

# Space Tech
SPACE_COMPANIES = [
    'spacex', 'blue-origin', 'rocket-lab', 'relativity-space',
    'astra', 'firefly', 'varda', 'astranis', 'planet-labs',
]


def get_all_companies():
    """Get all unique company names."""
    all_companies = set()
    all_companies.update(BIG_TECH)
    all_companies.update(GREENHOUSE_COMPANIES)
    all_companies.update(LEVER_COMPANIES)
    all_companies.update(AI_ML_COMPANIES)
    all_companies.update(FINTECH_COMPANIES)
    all_companies.update(CLOUD_COMPANIES)
    all_companies.update(DATA_COMPANIES)
    all_companies.update(SECURITY_COMPANIES)
    all_companies.update(DEVTOOLS_COMPANIES)
    all_companies.update(SOCIAL_COMPANIES)
    all_companies.update(ECOMMERCE_COMPANIES)
    all_companies.update(GAMING_COMPANIES)
    all_companies.update(AV_ROBOTICS_COMPANIES)
    all_companies.update(SPACE_COMPANIES)
    return list(all_companies)
