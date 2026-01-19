#!/bin/bash
# Quick setup script for new users

echo "🚀 Job Alert System - Setup"
echo "============================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy config template
if [ ! -f config_local.py ]; then
    echo "📝 Creating config_local.py from template..."
    cp config_template.py config_local.py
    echo "⚠️  Please edit config_local.py with your email credentials!"
else
    echo "✓ config_local.py already exists"
fi

# Create logs directory
mkdir -p logs

# Make scripts executable
chmod +x start_background.sh stop_background.sh check_status.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config_local.py with your email credentials"
echo "2. Run: python main.py test"
echo "3. If test passes, run: python main.py"
echo ""
echo "See README.md for detailed instructions!"
