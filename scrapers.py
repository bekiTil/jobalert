"""
Job board scraper modules.
Each scraper should return a list of job dictionaries with standardized fields.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import hashlib
import time
from urllib.parse import urlencode, quote_plus


class JobScraper:
    """Base class for job scrapers."""
    
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
    
    def generate_job_id(self, title: str, company: str, url: str) -> str:
        """Generate a unique job ID based on title, company, and URL."""
        unique_string = f"{title}{company}{url}"
        return hashlib.md5(unique_string.encode()).hexdigest()


class IndeedScraper(JobScraper):
    """Scraper for Indeed.com"""
    
    def __init__(self, user_agent: str):
        super().__init__(user_agent)
        self.base_url = "https://www.indeed.com"
    
    def scrape_jobs(self, keywords: List[str], locations: List[str], max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from Indeed."""
        jobs = []
        
        for keyword in keywords:
            for location in locations:
                try:
                    search_url = f"{self.base_url}/jobs"
                    params = {
                        'q': keyword,
                        'l': location,
                        'sort': 'date'  # Sort by date to get newest first
                    }
                    
                    full_url = f"{search_url}?{urlencode(params)}"
                    
                    response = self.session.get(full_url, timeout=10)
                    if response.status_code != 200:
                        print(f"✗ Indeed: Failed to fetch results (status {response.status_code})")
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Indeed's structure may change, this is a basic example
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards[:max_jobs]:
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', {'data-testid': 'company-name'})
                            location_elem = card.find('div', {'data-testid': 'text-location'})
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Filter for internships only
                            if 'intern' not in title.lower():
                                continue
                            
                            company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                            job_location = location_elem.get_text(strip=True) if location_elem else location
                            
                            # Get job URL
                            link = title_elem.find('a')
                            if link and link.get('href'):
                                job_url = f"{self.base_url}{link['href']}"
                            else:
                                continue
                            
                            job_data = {
                                'job_id': self.generate_job_id(title, company, job_url),
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'url': job_url,
                                'source': 'indeed',
                                'description': ''
                            }
                            
                            jobs.append(job_data)
                            
                        except Exception as e:
                            print(f"✗ Error parsing Indeed job card: {str(e)}")
                            continue
                    
                    time.sleep(2)  # Be respectful with rate limiting
                    
                except Exception as e:
                    print(f"✗ Indeed scraping error: {str(e)}")
                    continue
        
        return jobs


class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn Jobs (requires authentication for best results)"""
    
    def __init__(self, user_agent: str):
        super().__init__(user_agent)
        self.base_url = "https://www.linkedin.com"
    
    def scrape_jobs(self, keywords: List[str], locations: List[str], max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from LinkedIn - optimized to do fewer searches."""
        jobs = []
        jobs_found = set()  # Track unique jobs to avoid duplicates
        
        # OPTIMIZATION: Strategic keyword+location combos to cover all internship types
        # Covers: Software Engineering, Data Science, ML/AI, Backend, Frontend, Full Stack
        search_combos = [
            # Software Engineering internships
            ('software engineering intern', 'United States'),
            ('software engineer intern', 'Remote'),
            ('swe intern', 'United States'),
            
            # Data Science & ML internships
            ('data science intern', 'United States'),
            ('machine learning intern', 'United States'),
            ('ai intern', 'Remote'),
            
            # Specific tech roles
            ('backend intern', 'United States'),
            ('frontend intern', 'United States'),
            ('full stack intern', 'Remote'),
            
            # Python & General CS
            ('python intern', 'United States'),
            ('computer science intern', 'United States'),
            
            # Just "intern" to catch everything
            ('software intern', 'United States'),
            ('engineering intern', 'Remote'),
        ]
        
        print(f"  Searching {len(search_combos)} keyword+location combinations...")
        
        for i, (keyword, location) in enumerate(search_combos, 1):
            try:
                print(f"  [{i}/{len(search_combos)}] '{keyword}' in {location}...", end=' ')
                
                # LinkedIn's public job search endpoint
                search_url = f"{self.base_url}/jobs-guest/jobs/api/seeMoreJobPostings/search"
                params = {
                    'keywords': keyword,
                    'location': location,
                    'sortBy': 'DD',  # Sort by date (most recent first)
                    'start': 0,
                    'f_TPR': 'r86400'  # Posted in last 24 hours
                }
                
                response = self.session.get(search_url, params=params, timeout=5)
                
                if response.status_code != 200:
                    print(f"✗ Failed ({response.status_code})")
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('li')
                
                internships_found = 0
                
                for card in job_cards[:max_jobs]:
                    try:
                        base_card = card.find('div', class_='base-card')
                        if not base_card:
                            continue
                        
                        title_elem = base_card.find('h3', class_='base-search-card__title')
                        company_elem = base_card.find('h4', class_='base-search-card__subtitle')
                        location_elem = base_card.find('span', class_='job-search-card__location')
                        link_elem = base_card.find('a', class_='base-card__full-link')
                        
                        if not title_elem or not link_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        job_url = link_elem.get('href', '')
                        
                        # Skip if we've already found this job
                        if job_url in jobs_found:
                            continue
                        
                        # Filter for internships only
                        if 'intern' not in title.lower():
                            continue
                        
                        company = company_elem.get_text(strip=True) if company_elem else 'N/A'
                        job_location = location_elem.get_text(strip=True) if location_elem else location
                        
                        if not job_url:
                            continue
                        
                        job_data = {
                            'job_id': self.generate_job_id(title, company, job_url),
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'linkedin',
                            'description': ''
                        }
                        
                        jobs.append(job_data)
                        jobs_found.add(job_url)
                        internships_found += 1
                        
                    except Exception as e:
                        continue
                
                if internships_found > 0:
                    print(f"✓ Found {internships_found} internship(s)")
                else:
                    print("⊘ No internships")
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"✗ Error")
                continue
        
        return jobs


class GreenhouseScraper(JobScraper):
    """
    Scraper for companies using Greenhouse ATS.
    You can add specific company boards here.
    """
    
    def __init__(self, user_agent: str, company_boards: List[str] = None):
        super().__init__(user_agent)
        # Example company boards: ['company1.greenhouse.io', 'company2.greenhouse.io']
        self.company_boards = company_boards or []
    
    def scrape_jobs(self, keywords: List[str], locations: List[str], max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from Greenhouse company boards."""
        jobs = []
        
        for i, board in enumerate(self.company_boards, 1):
            try:
                print(f"  [{i}/{len(self.company_boards)}] Checking {board}...", end=' ')
                api_url = f"https://boards-api.greenhouse.io/v1/boards/{board.split('.')[0]}/jobs"
                
                response = self.session.get(api_url, timeout=5)
                if response.status_code != 200:
                    print(f"✗ Failed")
                    continue
                
                data = response.json()
                internship_count = 0
                
                for job in data.get('jobs', [])[:max_jobs]:
                    try:
                        title = job.get('title', '')
                        
                        # Filter for internships only
                        if 'intern' not in title.lower():
                            continue
                        
                        location_obj = job.get('location', {})
                        job_location = location_obj.get('name', 'N/A') if isinstance(location_obj, dict) else str(location_obj)
                        job_url = job.get('absolute_url', '')
                        company = board.split('.')[0].replace('-', ' ').title()
                        
                        # Filter by keywords if specified
                        if keywords:
                            if not any(kw.lower() in title.lower() for kw in keywords):
                                continue
                        
                        # Filter for US locations
                        if locations and location_obj:
                            if not any(loc.lower() in job_location.lower() for loc in locations):
                                continue
                        
                        job_data = {
                            'job_id': self.generate_job_id(title, company, job_url),
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': f'greenhouse-{board}',
                            'description': job.get('content', '')[:500]
                        }
                        
                        jobs.append(job_data)
                        internship_count += 1
                        
                    except Exception as e:
                        continue
                
                if internship_count > 0:
                    print(f"✓ Found {internship_count} internship(s)")
                else:
                    print("⊘ No internships")
                
                time.sleep(0.5)  # Reduced delay
                
            except Exception as e:
                print(f"✗ Greenhouse scraping error for {board}: {str(e)}")
                continue
        
        return jobs


class AshbyScraper(JobScraper):
    """
    Scraper for companies using Ashby ATS.
    Ashby is used by many startups and tech companies.
    """
    
    def __init__(self, user_agent: str, company_boards: List[str] = None):
        super().__init__(user_agent)
        # List of known Ashby job boards
        self.company_boards = company_boards or [
            # Big tech and well-known companies
            'ramp.com',
            'varda.com',
            'anduril.com',
            'astranis.com',
            'rippling.com',
            'watershed.com',
            'anthropic.com',
            'scale.com',
            'retool.com',
            'notion.so',
            # Add more companies as you discover them
        ]
    
    def scrape_jobs(self, keywords: List[str], locations: List[str], max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from Ashby company boards."""
        jobs = []
        
        for board in self.company_boards:
            try:
                # Ashby typically uses jobs.ashbyhq.com or jobs.<company>.com
                api_url = f"https://jobs.ashbyhq.com/{board.split('.')[0]}"
                
                response = self.session.get(api_url, timeout=10)
                if response.status_code != 200:
                    # Try alternative format
                    api_url = f"https://jobs.{board}"
                    response = self.session.get(api_url, timeout=10)
                    if response.status_code != 200:
                        print(f"✗ Ashby ({board}): Failed to fetch results")
                        continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for job listings - Ashby structure varies
                job_cards = soup.find_all(['div', 'a'], class_=lambda x: x and ('job' in x.lower() or 'posting' in x.lower()))
                
                for card in job_cards[:max_jobs]:
                    try:
                        # Try to extract job information
                        title_elem = card.find(['h3', 'h2', 'span'], class_=lambda x: x and 'title' in x.lower())
                        if not title_elem:
                            title_elem = card.find('a')
                        
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        # Filter for internships only
                        if not any(kw.lower() in title.lower() for kw in ['intern']):
                            continue
                        
                        # Filter by keywords
                        if keywords:
                            if not any(kw.lower() in title.lower() for kw in keywords):
                                continue
                        
                        # Get job URL
                        link = card.find('a') or card
                        job_url = link.get('href', '') if link.name == 'a' else ''
                        if job_url and not job_url.startswith('http'):
                            job_url = f"https://jobs.ashbyhq.com{job_url}"
                        
                        if not job_url:
                            continue
                        
                        # Try to get location
                        location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
                        job_location = location_elem.get_text(strip=True) if location_elem else 'United States'
                        
                        company = board.split('.')[0].replace('-', ' ').title()
                        
                        job_data = {
                            'job_id': self.generate_job_id(title, company, job_url),
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': f'ashby-{board}',
                            'description': ''
                        }
                        
                        jobs.append(job_data)
                        
                    except Exception as e:
                        print(f"✗ Error parsing Ashby job: {str(e)}")
                        continue
                
                time.sleep(1)
                
            except Exception as e:
                print(f"✗ Ashby scraping error for {board}: {str(e)}")
                continue
        
        return jobs


class LeverScraper(JobScraper):
    """
    Scraper for companies using Lever ATS.
    Lever is used by many startups and tech companies.
    """
    
    def __init__(self, user_agent: str, company_boards: List[str] = None):
        super().__init__(user_agent)
        # List of known Lever job boards
        self.company_boards = company_boards or [
            # Popular companies using Lever
            'netflix',
            'shopify',
            'canva',
            'figma',
            'plaid',
            'faire',
            'reddit',
            'squarespace',
            'gitlab',
            'grammarly',
            # Add more companies
        ]
    
    def scrape_jobs(self, keywords: List[str], locations: List[str], max_jobs: int = 50) -> List[Dict]:
        """Scrape jobs from Lever company boards."""
        jobs = []
        
        for i, board in enumerate(self.company_boards, 1):
            try:
                print(f"  [{i}/{len(self.company_boards)}] Checking {board}...", end=' ')
                # Lever API endpoint
                api_url = f"https://api.lever.co/v0/postings/{board}"
                
                response = self.session.get(api_url, timeout=5)
                if response.status_code != 200:
                    print(f"✗ Failed")
                    continue
                
                data = response.json()
                internship_count = 0
                
                for job in data[:max_jobs]:
                    try:
                        title = job.get('text', '')
                        
                        # Filter for internships only
                        if 'intern' not in title.lower():
                            continue
                        
                        # Filter by keywords
                        if keywords:
                            if not any(kw.lower() in title.lower() for kw in keywords):
                                continue
                        
                        categories = job.get('categories', {})
                        job_location = categories.get('location', 'United States')
                        
                        # Filter by US locations
                        if locations and 'United States' in locations:
                            if 'United States' not in job_location and 'US' not in job_location and 'Remote' not in job_location:
                                # Check if it's a US city
                                us_cities = ['New York', 'San Francisco', 'Seattle', 'Boston', 'Austin', 'Chicago', 'Los Angeles']
                                if not any(city in job_location for city in us_cities):
                                    continue
                        
                        job_url = job.get('hostedUrl', '')
                        company = board.replace('-', ' ').title()
                        
                        job_data = {
                            'job_id': self.generate_job_id(title, company, job_url),
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': f'lever-{board}',
                            'description': job.get('description', '')[:500]
                        }
                        
                        jobs.append(job_data)
                        internship_count += 1
                        
                    except Exception as e:
                        continue
                
                if internship_count > 0:
                    print(f"✓ Found {internship_count} internship(s)")
                else:
                    print("⊘ No internships")
                
                time.sleep(0.5)  # Reduced delay
                
            except Exception as e:
                print(f"✗ Error")
                continue
        
        return jobs


def get_all_scrapers(config: dict) -> List[JobScraper]:
    """Initialize and return all enabled scrapers."""
    scrapers = []
    user_agent = config.get('user_agent', 'Mozilla/5.0')
    
    job_boards = config.get('job_boards', {})
    
    if job_boards.get('indeed', False):
        scrapers.append(IndeedScraper(user_agent))
    
    if job_boards.get('linkedin', False):
        scrapers.append(LinkedInScraper(user_agent))
    
    if job_boards.get('greenhouse', False):
        # Top tech companies using Greenhouse - most likely to have internships
        company_boards = [
            'airbnb', 'stripe', 'uber', 'robinhood', 'snowflake',
            'databricks', 'coinbase', 'reddit', 'doordash', 'instacart',
        ]
        scrapers.append(GreenhouseScraper(user_agent, company_boards))
    
    if job_boards.get('ashby', False):
        # Top companies using Ashby
        company_boards = [
            'ramp.com', 'anthropic.com', 'scale.com',
        ]
        scrapers.append(AshbyScraper(user_agent, company_boards))
    
    if job_boards.get('lever', False):
        # Top companies using Lever
        company_boards = [
            'netflix', 'shopify', 'canva', 'figma', 'plaid',
        ]
        scrapers.append(LeverScraper(user_agent, company_boards))
    
    return scrapers
