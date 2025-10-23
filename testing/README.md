# PENGUIN Testing - Proof of Concepts

This directory contains proof-of-concept scripts demonstrating individual data sources before full integration into the PENGUIN architecture.

## Available PoCs

### 1. Reddit WSB Scraper (`reddit_poc/`)
Scrapes r/wallstreetbets for stock mentions and sentiment analysis.

**Features:**
- Fetches top posts from r/wallstreetbets
- Extracts stock tickers
- Sentiment analysis (bullish/bearish/neutral)
- Trending stocks report
- Momentum signal detection

**Requirements:** Reddit API credentials (free)

[See reddit_poc/README.md](./reddit_poc/README.md)

### 2. Yahoo Finance Scraper (`yahoo_poc/`)
Fetches real-time stock data and performs technical analysis.

**Features:**
- Real-time stock prices
- Historical data analysis
- Momentum calculations
- Technical indicators (SMA, RSI)
- Trading signals

**Requirements:** None! (yfinance is free, no API key needed)

[See yahoo_poc/README.md](./yahoo_poc/README.md)

## Quick Start

### Reddit PoC
```bash
cd reddit_poc
pip install -r requirements.txt

# Set your Reddit API credentials
export REDDIT_CLIENT_ID='your_id'
export REDDIT_CLIENT_SECRET='your_secret'

python wsb_scraper.py
```

### Yahoo Finance PoC
```bash
cd yahoo_poc
pip install -r requirements.txt
python yahoo_scraper.py
```

## Purpose

These proof-of-concepts validate:
1. ✅ Data source APIs work as expected
2. ✅ Data extraction methods are effective
3. ✅ Basic analysis provides useful signals
4. ✅ Integration patterns for full PENGUIN system

## Next Steps

Once validated, these will be integrated into the main PENGUIN system with:
- Persistent storage (TimescaleDB)
- Historical tracking
- Multi-source correlation
- Claude AI analysis
- Real-time monitoring
- Alert system

See `/src` for the main PENGUIN implementation.
