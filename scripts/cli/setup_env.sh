#!/bin/bash
# Setup development environment

echo "Setting up PENGUIN development environment..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing PENGUIN in development mode..."
pip install -e .

echo "Setup complete! Virtual environment is activated."
echo "To deactivate, run: deactivate"
