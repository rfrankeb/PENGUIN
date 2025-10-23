#!/bin/bash

echo "🐧 PENGUIN - GitHub Setup Script"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Check if user.name is set
if ! git config user.name &> /dev/null; then
    echo ""
    read -p "Enter your name for git commits: " name
    git config user.name "$name"
    echo "✓ Git user.name set to: $name"
else
    echo "✓ Git user.name: $(git config user.name)"
fi

# Check if user.email is set
if ! git config user.email &> /dev/null; then
    echo ""
    read -p "Enter your email for git commits: " email
    git config user.email "$email"
    echo "✓ Git user.email set to: $email"
else
    echo "✓ Git user.email: $(git config user.email)"
fi

echo ""
echo "================================"
echo "Git configuration complete!"
echo ""
echo "Next steps:"
echo "1. Create a GitHub repository at: https://github.com/new"
echo "   - Name: penguin"
echo "   - Visibility: Private (recommended)"
echo "   - DO NOT initialize with README"
echo ""
echo "2. After creating, run these commands:"
echo "   git remote add origin https://github.com/rfrankeb/penguin.git"
echo "   git add ."
echo "   git commit -m 'Initial commit: PENGUIN stock tracker PoC'"
echo "   git push -u origin main"
echo ""
echo "Or run: ./github-connect.sh"
echo "================================"
