"""
Database module for storing and retrieving job listings.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class JobDatabase:
    def __init__(self, db_path: str = 'jobs.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT NOT NULL,
                description TEXT,
                posted_date TEXT,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                notified INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_job_id ON jobs(job_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_notified ON jobs(notified)
        ''')
        
        conn.commit()
        conn.close()
    
    def job_exists(self, job_id: str) -> bool:
        """Check if a job already exists in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM jobs WHERE job_id = ?', (job_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def add_job(self, job_data: Dict) -> bool:
        """
        Add a new job to the database.
        Returns True if the job was added, False if it already exists.
        """
        if self.job_exists(job_data['job_id']):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO jobs (job_id, title, company, location, url, 
                                description, posted_date, source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data['job_id'],
                job_data['title'],
                job_data['company'],
                job_data.get('location', ''),
                job_data['url'],
                job_data.get('description', ''),
                job_data.get('posted_date', ''),
                job_data['source'],
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    def mark_as_notified(self, job_id: str):
        """Mark a job as notified."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE jobs SET notified = 1 WHERE job_id = ?', (job_id,))
        
        conn.commit()
        conn.close()
    
    def get_unnotified_jobs(self) -> List[Dict]:
        """Get all jobs that haven't been notified yet."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs WHERE notified = 0 ORDER BY created_at DESC
        ''')
        
        jobs = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jobs
    
    def get_recent_jobs(self, limit: int = 50) -> List[Dict]:
        """Get the most recent jobs."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        
        jobs = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return jobs
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM jobs')
        total_jobs = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE notified = 1')
        notified_jobs = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT source) FROM jobs')
        sources = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_jobs': total_jobs,
            'notified_jobs': notified_jobs,
            'pending_notifications': total_jobs - notified_jobs,
            'sources': sources
        }
