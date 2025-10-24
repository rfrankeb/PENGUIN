# 🐧 PENGUIN - Quick Start Guide

## Current Status

✅ Virtual environment created and activated
✅ Dependencies installed (PRAW for Reddit API)
✅ Git repository initialized
✅ .gitignore configured (protecting your .env file)
✅ Helper scripts created

⏳ Waiting for Reddit API credentials
⏳ Ready to connect to GitHub

---

## 📋 To-Do Checklist

### 1. Get Reddit API Credentials
- [ ] Check email for Reddit developer account confirmation
- [ ] Go to https://www.reddit.com/prefs/apps
- [ ] Create new app (type: "script")
- [ ] Copy client_id and client_secret
- [ ] Add to `.env` file (replace the placeholders)

### 2. Test the WSB Scraper
```bash
# Run the proof of concept
./run.sh

# Or manually:
source venv/bin/activate
python testing.py
```

### 3. Set Up GitHub
```bash
# Step 1: Configure git (interactive)
./git-setup.sh

# Step 2: Create repo at https://github.com/new
# - Name: penguin
# - Private (recommended)
# - Don't initialize with README

# Step 3: Connect and push (interactive)
./github-connect.sh
```

---

## 📁 Project Files

### Main Files
- **`testing.py`** - WSB scraper proof of concept
- **`CLAUDE.md`** - Complete PENGUIN architecture (1863 lines!)
- **`README.md`** - Detailed documentation

### Helper Scripts
- **`run.sh`** - Quick run scraper
- **`git-setup.sh`** - Configure git
- **`github-connect.sh`** - Connect to GitHub
- **`activate.sh`** - Activate virtual environment

### Configuration
- **`.env`** - Your API keys (NOT tracked by git)
- **`.env.example`** - Template
- **`.gitignore`** - Protects secrets
- **`requirements.txt`** - Python dependencies

### Documentation
- **`GITHUB_SETUP.md`** - Detailed GitHub instructions
- **`QUICKSTART.md`** - This file

---

## 🚀 Quick Commands

### Run the Scraper
```bash
./run.sh
```

### Git Workflow
```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push
```

### Virtual Environment
```bash
# Activate
source venv/bin/activate

# Deactivate
deactivate
```

---

## 📊 What the Scraper Does

1. **Connects to r/wallstreetbets**
2. **Fetches top 100 hot posts**
3. **Extracts stock tickers** ($TSLA, $GME, etc.)
4. **Analyzes sentiment** (bullish/bearish/neutral)
5. **Counts mentions** and engagement
6. **Generates report** with:
   - Top trending stocks
   - Sentiment breakdown
   - Momentum signals
   - Top posts per ticker

**Example Output:**
```
TOP TRENDING STOCKS
1. $NVDA
   Mentions: 15
   Sentiment: 🚀 BULLISH (80% bull / 13% bear)
   Avg Score: 342.1 upvotes

MOMENTUM SIGNALS
$NVDA: 15 mentions, 80% bullish, Momentum Score: 27.0
```

---

## 🔐 Security Notes

✅ **Protected by .gitignore:**
- `.env` (API keys)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)

⚠️ **NEVER commit:**
- API keys
- Passwords
- Tokens
- Database credentials

The `.gitignore` is already configured to protect these!

---

## 🎯 Next Steps After PoC

Once the proof of concept works:

### Phase 1: MVP Foundation (Weeks 1-2)
- [ ] Set up PostgreSQL + TimescaleDB
- [ ] Implement BaseCollector interface
- [ ] Create plugin registry
- [ ] Move Reddit scraper to plugin architecture
- [ ] Add historical tracking (detect mention spikes)

### Phase 2: Signal Detection (Weeks 3-4)
- [ ] Implement MomentumSpikeDetector
- [ ] Add technical indicators (RSI, volume)
- [ ] Build signal aggregation
- [ ] CLI: `penguin scan`

### Phase 3: AI Integration (Weeks 5-6)
- [ ] Integrate Claude API
- [ ] Multi-signal synthesis
- [ ] Generate investment recommendations
- [ ] Store in database

See `CLAUDE.md` for full roadmap!

---

## 🆘 Troubleshooting

**"Import praw could not be resolved"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Invalid credentials"**
- Check `.env` file has correct credentials
- No extra spaces
- App type must be "script" in Reddit

**Git push requires password**
- Use GitHub Personal Access Token
- Or set up SSH keys (see GITHUB_SETUP.md)

**Can't find venv**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📞 Support

- **Documentation**: All `.md` files in this directory
- **Architecture**: See `CLAUDE.md`
- **GitHub Setup**: See `GITHUB_SETUP.md`
- **Reddit API**: https://www.reddit.com/dev/api

---

## 🎉 You're All Set!

Your project is ready. Just waiting on:
1. Reddit API credentials → Test the scraper
2. GitHub repo created → Push your code

**Let's build PENGUIN!** 🚀
