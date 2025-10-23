# 🐧 PENGUIN
**Portfolio Evaluation Network with Global Updates, Insights, and Navigation**

AI-powered stock analysis platform that aggregates data from thousands of sources to identify investment opportunities before they become mainstream.

[![GitHub](https://img.shields.io/badge/GitHub-rfrankeb%2FPENGUIN-blue)](https://github.com/rfrankeb/PENGUIN)

## 🎯 Project Vision

PENGUIN detects emerging stock trends (short squeezes, momentum shifts, insider movements) by synthesizing diverse data signals through Claude AI. The core premise: catch opportunities like the BYND short squeeze *before* they go mainstream by monitoring social sentiment, options flow, congressional trading, and more.

## 📁 Project Structure

```
PENGUIN/
├── testing/              # Proof-of-concept scripts
│   ├── reddit_poc/       # Reddit WSB scraper ✅
│   └── yahoo_poc/        # Yahoo Finance scraper ✅
├── src/                  # Main application (under development)
├── CLAUDE.md             # Complete architecture & roadmap (1863 lines)
├── requirements.txt      # Root dependencies
└── README.md             # This file
```

## 🚀 Quick Start - Test the PoCs

### Reddit WSB Scraper
```bash
cd testing/reddit_poc
pip install -r requirements.txt

# Get Reddit API credentials from https://www.reddit.com/prefs/apps
export REDDIT_CLIENT_ID='your_client_id'
export REDDIT_CLIENT_SECRET='your_secret'

python wsb_scraper.py
```

**Output:** Trending stocks from r/wallstreetbets with sentiment analysis and momentum signals.

### Yahoo Finance Scraper (No API Key!)
```bash
cd testing/yahoo_poc
pip install -r requirements.txt
python yahoo_scraper.py
```

**Output:** Real-time stock data with technical indicators (SMA, RSI) and trading signals.

## 🏗️ Architecture Overview

PENGUIN uses a **plugin-based architecture** supporting unlimited data sources:

### Data Sources (Planned: 1000+)
- **Social Sentiment**: Reddit (50+ subs), Twitter, StockTwits, Discord
- **News & Media**: Bloomberg, Reuters, WSJ, Benzinga (200+ sources)
- **Insider Trading**: Congressional trades, SEC Form 4, 13F filings
- **Options Flow**: Unusual Whales, FlowAlgo, dark pool data
- **Technical**: 200+ indicators (RSI, MACD, Bollinger Bands, etc.)
- **Fundamental**: Earnings, financials, analyst ratings
- **Alternative**: Web traffic, satellite imagery, credit card data
- **Macro**: Economic indicators, Fed data, sector rotation

### AI Analysis Layer
Claude AI synthesizes multi-source signals to generate:
- Investment theses with supporting evidence
- Confidence scoring (0-100)
- Risk assessment
- Entry/exit strategies
- Time horizon recommendations

See **[CLAUDE.md](./CLAUDE.md)** for the complete 1800+ line architecture document.

## 📊 Proof-of-Concept Results

### ✅ Reddit WSB Scraper
- Extracts stock tickers from posts
- Sentiment analysis (bullish/bearish/neutral)
- Mention counting and trending detection
- **Use case**: Detected BYND early via WSB momentum

### ✅ Yahoo Finance Scraper
- Real-time price data
- Technical indicators (SMA, RSI)
- Momentum calculations
- Volume spike detection

## 🗺️ Roadmap

### Phase 1: Foundation (Weeks 1-2) - *In Progress*
- [x] Reddit PoC validation
- [x] Yahoo Finance PoC validation
- [ ] Set up PostgreSQL + TimescaleDB
- [ ] Implement BaseCollector interface
- [ ] Create plugin registry

### Phase 2: Signal Detection (Weeks 3-4)
- [ ] MomentumSpikeDetector
- [ ] Technical indicators integration
- [ ] Signal aggregation
- [ ] CLI: `penguin scan`

### Phase 3: AI Integration (Weeks 5-6)
- [ ] Claude API client
- [ ] Multi-signal synthesis
- [ ] Recommendation generation
- [ ] Database storage

### Phase 4-6: See CLAUDE.md for full roadmap

## 🛠️ Technology Stack

**Backend:** Python, FastAPI, Celery
**Databases:** PostgreSQL, TimescaleDB, Redis
**AI:** Anthropic Claude API
**Data Sources:** PRAW, yfinance, Alpha Vantage, QuiverQuant
**Analysis:** TA-Lib, pandas, scikit-learn

## 📖 Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Complete architecture & implementation guide
- **[testing/README.md](./testing/README.md)** - Proof-of-concept documentation
- **[GITHUB_SETUP.md](./GITHUB_SETUP.md)** - Git workflow & collaboration
- **[QUICKSTART.md](./QUICKSTART.md)** - Quick reference guide

## 🔐 Security

- API keys stored in `.env` (never committed to git)
- `.gitignore` configured to protect secrets
- Reddit API credentials required (free)
- Yahoo Finance requires no API key

## 🤝 Contributing

This is currently a solo project, but contributions welcome once MVP is complete!

## 📝 License

MIT License - See LICENSE file for details

## 🎓 Learning Resources

This project demonstrates:
- Plugin-based architecture design
- Multi-source data aggregation
- AI-powered analysis (Claude)
- Financial data APIs (Reddit, Yahoo Finance)
- Time-series database usage (TimescaleDB)
- Sentiment analysis & NLP
- Technical indicator calculations

## ⚠️ Disclaimer

**NOT FINANCIAL ADVICE.** This is an educational project for learning about data aggregation, AI analysis, and software architecture. Always do your own research before making investment decisions.

---

**Built with Claude Code** | [Documentation](./CLAUDE.md) | [GitHub](https://github.com/rfrankeb/PENGUIN)
