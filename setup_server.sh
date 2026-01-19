#!/bin/bash
# Quick deploy script for Ubuntu server

echo "🚀 Setting up Job Alert System on Ubuntu Server"
echo "================================================"

# Update and install dependencies
echo "📦 Installing Python and dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "🐍 Creating virtual environment..."
cd ~/jobalert
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p ~/jobalert/logs

# Test email configuration
echo "📧 Testing email configuration..."
python main.py test

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. If email test worked, proceed to setup systemd service"
echo "2. Run: sudo nano /etc/systemd/system/jobalert.service"
echo "3. Copy the service configuration from DEPLOY.md"
echo "4. Run: sudo systemctl enable jobalert && sudo systemctl start jobalert"
echo ""
echo "Or use screen method:"
echo "  screen -S jobalert"
echo "  python main.py"
echo "  Press Ctrl+A then D to detach"
