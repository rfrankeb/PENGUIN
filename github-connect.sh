#!/bin/bash

echo "🐧 PENGUIN - Connect to GitHub"
echo "=============================="
echo ""

# Check if remote already exists
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists:"
    git remote -v
    echo ""
    read -p "Do you want to remove and re-add it? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        git remote remove origin
        echo "✓ Removed existing remote"
    else
        echo "Keeping existing remote. Exiting."
        exit 0
    fi
fi

echo ""
echo "First, make sure you've created a GitHub repository:"
echo "1. Go to: https://github.com/new"
echo "2. Create a repository named 'penguin'"
echo "3. DO NOT initialize with README"
echo ""
read -p "Have you created the GitHub repository? (y/n): " created

if [ "$created" != "y" ]; then
    echo "Please create the repository first, then run this script again."
    exit 0
fi

echo ""
read -p "Enter your GitHub username [rfrankeb]: " username
username=${username:-rfrankeb}

read -p "Enter repository name [penguin]: " repo
repo=${repo:-penguin}

echo ""
echo "Connecting to: https://github.com/$username/$repo"

# Add remote
git remote add origin https://github.com/$username/$repo.git

echo "✓ Remote added"
echo ""

# Show current status
echo "Git status:"
git status

echo ""
read -p "Ready to commit and push? (y/n): " ready

if [ "$ready" = "y" ]; then
    echo ""
    echo "Adding files..."
    git add .

    echo "Creating initial commit..."
    git commit -m "Initial commit: PENGUIN stock tracker PoC with WSB scraper

- Reddit WSB scraper proof of concept
- Plugin-based architecture design
- Comprehensive documentation (CLAUDE.md)
- Virtual environment setup
- Helper scripts for easy setup"

    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main

    echo ""
    echo "✅ Success! Your code is now on GitHub!"
    echo "View it at: https://github.com/$username/$repo"
else
    echo ""
    echo "Skipped push. When ready, run:"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo "  git push -u origin main"
fi

echo ""
echo "=============================="
