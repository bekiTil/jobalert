# Job Alert System 🚨

An automated job alert system that monitors multiple job boards and sends **instant email notifications** when new internships are posted. Built to help you apply early and beat the competition!

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Why This Project?

> "Once roles enter shared GitHub repos or are reposted by influencers, they're immediately flooded with applicants. The key is to **apply early** so your application lands at the front of the queue."

This system helps you:
- ✅ Get notified **within minutes** when new internships are posted
- ✅ Apply **before the flood** of applicants
- ✅ Track **multiple job boards** automatically (LinkedIn, Greenhouse, Lever)
- ✅ Filter by keywords and locations you care about
- ✅ Never miss an opportunity with continuous 24/7 monitoring

## ✨ Features

- **Multi-Board Monitoring**: Scrapes LinkedIn, Greenhouse (Stripe, Airbnb, etc.), and Lever (Netflix, Shopify, etc.)
- **Email Notifications**: Beautiful HTML emails with job details sent instantly
- **Smart Deduplication**: Tracks jobs in SQLite database to avoid duplicate notifications
- **Customizable Filters**: Search by keywords, locations, and experience level
- **Fast & Efficient**: Optimized searches complete in ~15-30 seconds
- **Background Running**: Deploy on server or run locally 24/7

## 📋 Prerequisites

- Python 3.7 or higher
- Gmail account (or any SMTP email service)
- For Gmail: [App Password](https://support.google.com/accounts/answer/185833) (required)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/bekiTil/jobalert.git
cd jobalert
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Settings

```bash
# Copy the template
cp config_template.py config_local.py

# Edit with your credentials
nano config_local.py
```

**Required changes in `config_local.py`:**
- `sender_email`: Your Gmail address
- `sender_password`: Your Gmail App Password
- `recipient_email`: Where to receive alerts

**Optional customizations:**
- `keywords`: Job titles you're interested in
- `locations`: Where you want to work
- `check_interval_minutes`: How often to check (default: 10 minutes)

### 4. Test Email Configuration

```bash
python main.py test
```

You should receive a test email!

### 5. Run the System

```bash
# Run continuously (checks every 10 minutes)
python main.py

# Or run once for testing
python main.py once

# Check database statistics
python main.py stats
```

## 📧 Setting Up Gmail App Password

1. Go to [Google Account](https://myaccount.google.com/)
2. Select **Security**
3. Enable **2-Step Verification** (if not already on)
4. Under "How you sign in to Google", select **App passwords**
5. Generate a new app password for "Mail"
6. Copy the 16-character password (no spaces)
7. Paste it in `config_local.py` as `sender_password`

## 🎨 Customization

### Modify Search Criteria

Edit `config_local.py`:

```python
JOB_SEARCH_CONFIG = {
    'keywords': [
        'software engineering intern',
        'data science intern',
        # Add more keywords
    ],
    'locations': [
        'Remote',
        'San Francisco',
        # Add more locations
    ],
}
```

### Enable/Disable Job Boards

```python
JOB_BOARDS = {
    'indeed': False,     # Often blocks scrapers
    'linkedin': True,    # Recommended
    'greenhouse': True,  # Big tech companies
    'lever': True,       # Startups
}
```

### Add More Companies

Edit `scrapers.py` to add companies to Greenhouse or Lever lists:

```python
# Around line 500
company_boards = [
    'airbnb', 'stripe', 'uber',
    'your-company-here',  # Add here
]
```

## 🖥️ Deploy to Server (24/7 Monitoring)

### Using nohup (Simplest)

```bash
# On your server
cd ~/jobalert
source venv/bin/activate
./start_background.sh

# Check status
./check_status.sh

# View logs
tail -f logs/output.log

# Stop
./stop_background.sh
```

### Using systemd (Auto-restart on reboot)

See [DEPLOY.md](DEPLOY.md) for complete instructions.

## 📊 Project Structure

```
jobalert/
├── main.py                 # Main application
├── scrapers.py            # Job board scrapers
├── email_notifier.py      # Email notification system
├── database.py            # SQLite database management
├── config_template.py     # Configuration template
├── config_local.py        # Your personal config (gitignored)
├── requirements.txt       # Python dependencies
├── DEPLOY.md             # Deployment guide
├── start_background.sh   # Start in background
├── stop_background.sh    # Stop the system
└── check_status.sh       # Check system status
```

## 🔧 Management Commands

```bash
python main.py          # Run continuously
python main.py test     # Send test email
python main.py once     # Run one check and exit
python main.py stats    # View statistics
```

## 📈 How It Works

1. **Every 10 minutes** (configurable), the system checks job boards
2. **Scrapes internships** from LinkedIn, Greenhouse, Lever
3. **Compares with database** to find new postings
4. **Sends email immediately** when new internships are found
5. **Tracks all jobs** to prevent duplicate notifications

## ⚠️ Important Notes

- **Rate Limiting**: Built-in delays to respect job board servers
- **Job Board Changes**: HTML structures change; scrapers may need updates
- **Email Limits**: Gmail has daily sending limits
- **Privacy**: Never commit `config_local.py` to version control

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new job board scrapers
- Improve email templates
- Add new features
- Fix bugs

## 📝 License

MIT License - Feel free to use and modify as needed.

## 💡 Tips for Success

1. **Check email frequently** - Set up mobile notifications
2. **Have resume ready** - Keep an updated resume handy
3. **Apply within hours** - The sooner you apply, the better
4. **Track applications** - Keep notes on what you've applied to
5. **Customize per role** - Quality > quantity, even when applying early

## 🆘 Troubleshooting

**Email not sending?**
- Verify Gmail App Password is correct (16 characters, no spaces)
- Check that 2-Step Verification is enabled
- Try the `python main.py test` command

**No jobs being found?**
- Broaden your keywords and locations
- Check if job boards are accessible
- LinkedIn may temporarily block requests - wait and try again

**Database errors?**
- Delete `jobs.db` and restart
- Check file permissions

## 🙏 Acknowledgments

Inspired by the need to apply early to competitive internship postings before they get flooded with applications.

## 📞 Questions?

Open an issue on GitHub!

---

**Good luck with your internship search! Apply early and land that dream role! 🚀**
