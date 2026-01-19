#!/bin/bash
# Check status of Job Alert System

echo "📊 Job Alert System Status"
echo "=========================="
echo ""

# Check if process is running
if pgrep -f "python main.py" > /dev/null; then
    echo "✅ Status: RUNNING"
    echo ""
    echo "Process details:"
    ps aux | grep "python main.py" | grep -v grep
    echo ""
else
    echo "❌ Status: NOT RUNNING"
    echo ""
fi

# Check logs
if [ -f ~/jobalert/logs/output.log ]; then
    echo "📝 Last 10 lines of log:"
    echo "------------------------"
    tail -n 10 ~/jobalert/logs/output.log
else
    echo "⚠️  No log file found"
fi

echo ""
echo "Commands:"
echo "  View full logs: tail -f ~/jobalert/logs/output.log"
echo "  Start system:   cd ~/jobalert && ./start_background.sh"
echo "  Stop system:    cd ~/jobalert && ./stop_background.sh"
