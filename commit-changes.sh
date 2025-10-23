#!/bin/bash
cd /Users/reedfrankeberger/Desktop/Niche/PENGUIN

echo "🐧 PENGUIN - Committing Reorganization"
echo "======================================"
echo ""

# Show what's changed
echo "Changes to be committed:"
git status --short

echo ""
read -p "Proceed with commit? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Commit cancelled."
    exit 0
fi

# Add all changes
git add .

# Commit
git commit -m "Reorganize project structure

- Create testing/ directory for proof-of-concepts
  - Reddit WSB scraper in testing/reddit_poc/
  - Yahoo Finance scraper in testing/yahoo_poc/ (new!)
- Create src/ directory for main application (under development)
- Update README.md with new structure and comprehensive docs
- Add documentation for all PoCs
- Preserve git history

Changes:
- ✅ Reddit PoC validated
- ✅ Yahoo Finance PoC added (no API key needed!)
- 🚧 Main application structure prepared in src/

Next: Begin MVP Phase 1 implementation"

# Push to GitHub
echo ""
read -p "Push to GitHub? (y/n): " push_confirm

if [ "$push_confirm" = "y" ]; then
    git push
    echo ""
    echo "✅ Changes pushed to GitHub!"
    echo "View at: https://github.com/rfrankeb/PENGUIN"
else
    echo ""
    echo "Changes committed locally. Push later with: git push"
fi

echo ""
echo "======================================"
