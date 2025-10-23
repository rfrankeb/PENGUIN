#!/bin/bash

echo "================================"
echo "PENGUIN WSB PoC Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get Reddit API credentials from https://www.reddit.com/prefs/apps"
echo "2. Set environment variables:"
echo "   export REDDIT_CLIENT_ID='your_client_id'"
echo "   export REDDIT_CLIENT_SECRET='your_secret'"
echo "3. Run: python testing.py"
echo ""
echo "Or activate the virtual environment and run:"
echo "   source venv/bin/activate"
echo "   python testing.py"
echo ""
