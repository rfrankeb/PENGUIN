# PENGUIN - WSB Proof of Concept

This is a proof-of-concept script that demonstrates the core functionality of the PENGUIN system by scraping r/wallstreetbets.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **name**: PENGUIN (or anything)
   - **App type**: Select "script"
   - **description**: Stock tracking app
   - **redirect uri**: http://localhost:8080
4. Click "Create app"
5. Copy your credentials:
   - **client_id**: The string under "personal use script"
   - **client_secret**: The "secret" field

### 3. Set Environment Variables

**Option A: Environment Variables (Recommended)**
```bash
export REDDIT_CLIENT_ID='your_client_id'
export REDDIT_CLIENT_SECRET='your_client_secret'
```

**Option B: Edit the Script Directly**
Open `testing.py` and replace the placeholder values on lines 16-17.

### 4. Run the Script

```bash
python testing.py
```

## What It Does

The script will:

1. **Connect to Reddit** using PRAW (Python Reddit API Wrapper)
2. **Fetch the top 100 hot posts** from r/wallstreetbets
3. **Extract stock tickers** mentioned in titles and post bodies
4. **Analyze sentiment** (bullish/bearish/neutral) using keyword matching
5. **Count mentions** and calculate engagement metrics
6. **Generate a report** showing:
   - Top trending stocks by mention count
   - Sentiment breakdown for each stock
   - Momentum signals for high-activity stocks
   - Top posts for each ticker

## Sample Output

```
r/WALLSTREETBETS ANALYSIS REPORT
======================================================================
Analysis Time: 2025-01-15 14:30:00
Total Posts Analyzed: 95
Unique Tickers Found: 127

----------------------------------------------------------------------
TOP TRENDING STOCKS (Min 3 mentions)
----------------------------------------------------------------------

1. $TSLA
   Mentions: 12
   Avg Score: 245.3 upvotes
   Sentiment: 🚀 BULLISH (75% bull / 17% bear)
   Total Comments: 3,421
   Top Post: "TSLA calls printing after Cybertruck delivery beat..." (892 upvotes)

2. $GME
   Mentions: 8
   Avg Score: 312.5 upvotes
   Sentiment: 🚀 BULLISH (88% bull / 0% bear)
   Total Comments: 2,156
   ...
```

## What This Proves

This proof-of-concept validates:

✅ **Reddit API Integration**: Successfully connects and fetches data
✅ **Ticker Extraction**: Identifies stock symbols from unstructured text
✅ **Sentiment Analysis**: Basic bullish/bearish detection
✅ **Mention Tracking**: Counts and ranks stocks by activity
✅ **Momentum Detection**: Identifies spikes in mentions

## Next Steps

This is exactly what we'll build into Phase 1 of PENGUIN, but with:

- **Persistent storage** (TimescaleDB for time-series data)
- **Historical tracking** (detect mention velocity changes)
- **Claude AI integration** (sophisticated analysis)
- **Multiple data sources** (Twitter, StockTwits, etc.)
- **Real-time monitoring** (WebSocket streams)
- **Alert system** (notify on momentum spikes)

## Troubleshooting

**"Import praw could not be resolved"**
```bash
pip install praw
```

**"Invalid credentials"**
- Double-check your client_id and client_secret
- Make sure there are no extra spaces
- Verify the app type is "script" in Reddit settings

**"Forbidden" or "403 error"**
- Check your user agent string
- Make sure you're not making too many requests (rate limit: 60/min)

## Notes

- Reddit API has a rate limit of ~60 requests per minute
- Some tickers may be false positives (common words that are also tickers)
- Sentiment analysis is basic; Claude AI will make this much more sophisticated
- This script doesn't store data; it's just a snapshot of current activity
