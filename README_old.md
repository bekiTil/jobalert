# 🚨 Job Alert System - Get Notified Early!

An automated job alert system that monitors multiple job boards and sends **instant email notifications** when new jobs are posted. Apply early and beat the competition!

## 🎯 Why This Matters

As highlighted in the original post:
> "Once roles enter shared GitHub repos or are reposted by influencers, they're immediately flooded with applicants. The key is to **apply early** so your application lands at the front of the queue."

This system helps you:
- ✅ **Get notified immediately** when new jobs are posted
- ✅ **Apply before the flood** of applicants
- ✅ **Track multiple job boards** automatically
- ✅ **Filter by keywords and locations** you care about
- ✅ **Never miss an opportunity** with continuous monitoring

## 🚀 Features

- **Multi-Board Monitoring**: Scrapes Indeed, LinkedIn, and company Greenhouse boards
- **Email Notifications**: Beautiful HTML emails sent instantly for new jobs
- **Smart Deduplication**: Tracks jobs in a database to avoid duplicate notifications
- **Customizable Search**: Filter by keywords, locations, and more
- **Background Running**: Run continuously or on a schedule
- **Beautiful Email Templates**: Professional HTML emails with job details

## 📋 Prerequisites

- Python 3.7 or higher
- Gmail account (or any SMTP email service)
- For Gmail: You'll need an [App Password](https://support.google.com/accounts/answer/185833)

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure your settings**:
   - Open `config_local.py`
   - Add your email credentials:
     ```python
     EMAIL_CONFIG = {
         'smtp_server': 'smtp.gmail.com',
         'smtp_port': 587,
         'sender_email': 'your-email@gmail.com',
         'sender_password': 'your-app-password',  # Gmail App Password
         'recipient_email': 'your-email@gmail.com',
     }
     ```
   - Customize your job search criteria:
     ```python
     JOB_SEARCH_CONFIG = {
         'keywords': ['software engineer', 'python developer'],
         'locations': ['Remote', 'San Francisco'],
     }
     ```

## 🎮 Usage

### Test Email Configuration
```bash
python main.py test
```
Sends a test email to verify your configuration is working.

### Run Once
```bash
python main.py once
```
Check for jobs once and exit (useful for testing).

### Run Continuously (Recommended)
```bash
python main.py
```
Runs continuously, checking for new jobs every 10 minutes (configurable).

### Check Statistics
```bash
python main.py stats
```
View statistics about tracked jobs.

## 📧 Setting Up Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/)
2. Select **Security**
3. Enable **2-Step Verification** (if not already enabled)
4. Under "Signing in to Google", select **App passwords**
5. Generate a new app password for "Mail"
6. Copy the password and paste it in `config_local.py`

## 🎨 Customization

### Add More Job Boards

Edit `scrapers.py` to add more scrapers. The system supports:
- Indeed
- LinkedIn
- Greenhouse (for specific companies)

### Modify Email Template

Edit the `_create_html_email()` method in `email_notifier.py` to customize the email design.

### Change Check Interval

Edit `SCRAPING_CONFIG` in `config_local.py`:
```python
SCRAPING_CONFIG = {
    'check_interval_minutes': 5,  # Check every 5 minutes
}
```

## 🔧 Running as a Background Service

### macOS/Linux (using screen)
```bash
# Start a screen session
screen -S jobalert

# Run the system
python main.py

# Detach: Press Ctrl+A then D
# Reattach later: screen -r jobalert
```

### Using systemd (Linux)
Create a systemd service file `/etc/systemd/system/jobalert.service`:
```ini
[Unit]
Description=Job Alert System
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/jobalert
ExecStart=/usr/bin/python3 /path/to/jobalert/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable jobalert
sudo systemctl start jobalert
```

### macOS (using launchd)
Create a plist file at `~/Library/LaunchAgents/com.jobalert.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jobalert</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/jobalert/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/jobalert</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then:
```bash
launchctl load ~/Library/LaunchAgents/com.jobalert.plist
```

## 📊 Database

Jobs are stored in a SQLite database (`jobs.db`). The database tracks:
- Job title, company, location, URL
- When the job was discovered
- Whether you've been notified
- Source job board

## ⚠️ Important Notes

1. **Rate Limiting**: The scrapers include delays to be respectful to job board servers. Don't remove these delays.

2. **Job Board Changes**: Job board HTML structures change frequently. If a scraper stops working, it may need updates.

3. **Email Limits**: Gmail has sending limits. If you're getting too many notifications, consider increasing the check interval.

4. **Privacy**: Keep your `config_local.py` file secure and never commit it to version control.

## 🤝 Contributing

Feel free to:
- Add new job board scrapers
- Improve email templates
- Add new features
- Fix bugs

## 📝 License

MIT License - Feel free to use and modify as needed.

## 💡 Tips for Job Searching

1. **Check your email frequently** - Set up mobile notifications for your email
2. **Have your resume ready** - Keep an updated resume on hand
3. **Apply within hours** - The sooner you apply, the better your chances
4. **Customize applications** - Even though you're applying early, quality still matters
5. **Track your applications** - Keep notes on what you've applied to

## 🆘 Troubleshooting

**Email not sending?**
- Verify your Gmail App Password is correct
- Check that 2-Step Verification is enabled
- Try the `python main.py test` command

**No jobs being found?**
- Broaden your keywords and locations
- Check if the job boards are accessible
- Some job boards may block scrapers - consider using APIs if available

**Database errors?**
- Delete `jobs.db` and restart the system
- Check file permissions

## 📞 Support

If you have questions or issues, please open an issue on GitHub.

---

**Good luck with your job search! Apply early and land that dream job! 🚀**