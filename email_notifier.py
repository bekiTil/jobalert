"""
Email notification module for sending job alerts.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime


class EmailNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, 
                 sender_email: str, sender_password: str, recipient_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
    
    def send_job_alert(self, jobs: List[Dict]) -> bool:
        """
        Send an email alert with new job listings.
        Returns True if successful, False otherwise.
        """
        if not jobs:
            return False
        
        subject = f"🚨 Job Alert: {len(jobs)} New Job{'s' if len(jobs) > 1 else ''} Found!"
        html_content = self._create_html_email(jobs)
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Create plain text version
            text_content = self._create_text_email(jobs)
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✓ Email sent successfully: {len(jobs)} job(s)")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
    
    def _create_text_email(self, jobs: List[Dict]) -> str:
        """Create plain text version of the email."""
        lines = [
            f"New Job Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 60,
            ""
        ]
        
        for i, job in enumerate(jobs, 1):
            lines.append(f"{i}. {job['title']}")
            lines.append(f"   Company: {job['company']}")
            lines.append(f"   Location: {job.get('location', 'N/A')}")
            lines.append(f"   Source: {job['source']}")
            lines.append(f"   URL: {job['url']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _create_html_email(self, jobs: List[Dict]) -> str:
        """Create HTML version of the email with better formatting."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .job-card {{
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }}
                .job-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                }}
                .job-title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .job-company {{
                    font-size: 16px;
                    color: #667eea;
                    margin-bottom: 8px;
                }}
                .job-details {{
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 5px;
                }}
                .apply-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 15px;
                    font-weight: bold;
                }}
                .apply-button:hover {{
                    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #e0e0e0;
                    color: #666;
                    font-size: 14px;
                }}
                .badge {{
                    display: inline-block;
                    background: #f0f0f0;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    margin-right: 8px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 New Job Alert!</h1>
                <p>Found {len(jobs)} new job{'s' if len(jobs) > 1 else ''} matching your criteria</p>
                <p style="font-size: 14px; opacity: 0.9;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        """
        
        for job in jobs:
            html += f"""
            <div class="job-card">
                <div class="job-title">{job['title']}</div>
                <div class="job-company">🏢 {job['company']}</div>
                <div class="job-details">
                    <span class="badge">📍 {job.get('location', 'N/A')}</span>
                    <span class="badge">🔗 {job['source'].title()}</span>
                </div>
                {f'<div class="job-details" style="margin-top: 10px;">{job.get("description", "")[:200]}...</div>' if job.get('description') else ''}
                <a href="{job['url']}" class="apply-button">Apply Now →</a>
            </div>
            """
        
        html += """
            <div class="footer">
                <p>This is an automated job alert from your Job Alert System.</p>
                <p>Apply early to increase your chances! 🚀</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_test_email(self) -> bool:
        """Send a test email to verify configuration."""
        test_job = [{
            'title': 'Test Job Posting',
            'company': 'Test Company',
            'location': 'Remote',
            'url': 'https://example.com',
            'source': 'test',
            'description': 'This is a test email to verify your job alert system is working correctly.'
        }]
        
        return self.send_job_alert(test_job)
