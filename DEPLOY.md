# 🚀 Deploy Job Alert System to Ubuntu Server

## Step 1: Copy Files to Server

From your local machine, run:

```bash
# Copy the entire project to your server
scp -i ~/.ssh/test -r /Users/berekettilahunshimekit/jobalert berekettilahunshimekit@136.115.193.75:~/
```

## Step 2: SSH into Your Server

```bash
ssh -i ~/.ssh/test berekettilahunshimekit@136.115.193.75
```

## Step 3: Install Dependencies on Server

```bash
# Update system
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Navigate to project
cd ~/jobalert

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 4: Test That It Works

```bash
# Still in the virtual environment
python main.py test
```

You should get "✓ Test email sent successfully!"

## Step 5: Set Up systemd Service (Run Forever)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/jobalert.service
```

Paste this content (replace USERNAME with your actual username):

```ini
[Unit]
Description=Job Alert System - Internship Monitor
After=network.target

[Service]
Type=simple
User=berekettilahunshimekit
WorkingDirectory=/home/berekettilahunshimekit/jobalert
ExecStart=/home/berekettilahunshimekit/jobalert/venv/bin/python /home/berekettilahunshimekit/jobalert/main.py
Restart=always
RestartSec=10

# Logging
StandardOutput=append:/home/berekettilahunshimekit/jobalert/logs/output.log
StandardError=append:/home/berekettilahunshimekit/jobalert/logs/error.log

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, then Y, then Enter)

## Step 6: Create Logs Directory

```bash
mkdir -p ~/jobalert/logs
```

## Step 7: Enable and Start the Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable jobalert

# Start the service
sudo systemctl start jobalert

# Check status
sudo systemctl status jobalert
```

## 🎯 Service Management Commands

```bash
# Check if it's running
sudo systemctl status jobalert

# Stop the service
sudo systemctl stop jobalert

# Start the service
sudo systemctl start jobalert

# Restart the service
sudo systemctl restart jobalert

# View logs (live)
tail -f ~/jobalert/logs/output.log

# View errors
tail -f ~/jobalert/logs/error.log

# View last 100 lines
tail -n 100 ~/jobalert/logs/output.log
```

## 📊 Check Stats

```bash
cd ~/jobalert
source venv/bin/activate
python main.py stats
```

## ✅ What You Get

- ✅ Runs 24/7 automatically
- ✅ Starts on server reboot
- ✅ Restarts automatically if it crashes
- ✅ Logs all activity to files
- ✅ Checks for internships every 10 minutes
- ✅ Sends instant email notifications

## 🔧 Troubleshooting

If it's not working:

```bash
# Check logs
sudo journalctl -u jobalert -n 50

# Check service status
sudo systemctl status jobalert

# Test manually
cd ~/jobalert
source venv/bin/activate
python main.py once
```

## 🛑 Alternative: Use Screen (Simpler)

If you prefer a simpler approach:

```bash
# SSH into server
ssh -i ~/.ssh/test berekettilahunshimekit@136.115.193.75

# Navigate to project
cd ~/jobalert
source venv/bin/activate

# Start in screen session
screen -S jobalert
python main.py

# Detach: Press Ctrl+A then D
# Reattach later: screen -r jobalert
```

The screen method is simpler but won't auto-restart on reboot.
