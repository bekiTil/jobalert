#!/bin/bash
# One-command deployment script
# Usage: ./deploy_to_server.sh

echo "🚀 Deploying Job Alert System to Server"
echo "========================================"

SERVER="136.115.193.75"
USER="berekettilahunshimekit"
KEY="~/.ssh/test"

echo "📦 Packaging project..."
cd /Users/berekettilahunshimekit
tar -czf jobalert.tar.gz jobalert/

echo "📤 Uploading to server..."
scp -i ~/.ssh/test jobalert.tar.gz $USER@$SERVER:~/

echo "🔧 Setting up on server..."
ssh -i ~/.ssh/test $USER@$SERVER << 'ENDSSH'
    # Extract
    tar -xzf jobalert.tar.gz
    cd jobalert
    
    # Install Python and deps
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
    
    # Setup virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Create logs directory
    mkdir -p logs
    
    # Make scripts executable
    chmod +x start_background.sh stop_background.sh check_status.sh
    
    # Test email
    python main.py test
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "To start the system in background:"
    echo "  cd ~/jobalert"
    echo "  ./start_background.sh"
    echo ""
    echo "To check status:"
    echo "  ./check_status.sh"
    echo ""
    echo "To stop:"
    echo "  ./stop_background.sh"
ENDSSH

echo ""
echo "✅ Deployment complete!"
echo ""
echo "To start the job alert system:"
echo "  ssh -i ~/.ssh/test $USER@$SERVER"
echo "  cd jobalert && source venv/bin/activate"
echo "  screen -S jobalert && python main.py"
