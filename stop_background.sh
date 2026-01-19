#!/bin/bash
# Stop the Job Alert System

echo "🛑 Stopping Job Alert System..."

pkill -f "python main.py"

if [ $? -eq 0 ]; then
    echo "✅ Job Alert System stopped"
else
    echo "⚠️  No running process found"
fi

echo ""
echo "To check if it's still running:"
echo "   ps aux | grep 'python main.py'"
