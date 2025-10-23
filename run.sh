#!/bin/bash
# Quick run script that activates venv and runs the scraper

echo "🐧 PENGUIN WSB Scraper"
echo "====================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the script
python testing.py

# Deactivate when done
deactivate
