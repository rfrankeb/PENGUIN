# Reddit WSB Proof of Concept

This proof-of-concept demonstrates scraping r/wallstreetbets for stock mentions and sentiment analysis.

## Setup

```bash
cd reddit_poc
pip install -r requirements.txt
```

## Configuration

1. Get Reddit API credentials from https://www.reddit.com/prefs/apps
2. Copy `.env.example` to `.env`
3. Add your credentials to `.env`

## Run

```bash
python wsb_scraper.py
```

## What It Does

- Fetches top 100 hot posts from r/wallstreetbets
- Extracts stock tickers ($TSLA, $GME, etc.)
- Analyzes sentiment (bullish/bearish/neutral)
- Generates trending stocks report
- Detects momentum signals
