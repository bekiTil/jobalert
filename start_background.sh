#!/bin/bash
# Start Job Alert System in background using nohup
# Run this on your Ubuntu server

cd ~/jobalert
source venv/bin/activate

# Create logs directory if it doesn't exist
mkdir -p logs

# Stop any existing process
pkill -f "python main.py"

# Start in background
nohup python main.py > logs/output.log 2>&1 &

# Get the process ID
PID=$!

echo "✅ Job Alert System started!"
echo "   Process ID: $PID"
echo ""
echo "To check status:"
echo "   ps aux | grep 'python main.py'"
echo ""
echo "To view logs:"
echo "   tail -f ~/jobalert/logs/output.log"
echo ""
echo "To stop:"
echo "   pkill -f 'python main.py'"
