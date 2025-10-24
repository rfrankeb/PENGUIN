# Reddit + Yahoo Finance Combined Analysis PoC

This proof of concept combines Reddit sentiment analysis with Yahoo Finance fundamentals to generate stock recommendations.

## How It Works

### Phase 1: Reddit Sentiment Analysis
- Scrapes 10 investment subreddits (100 posts each)
- Extracts stock mentions and sentiment
- Calculates momentum scores based on mentions × sentiment × subreddit diversity

### Phase 2: Yahoo Finance Fundamentals
- Fetches price data, volume, volatility for top Reddit stocks
- **Rate Limiting**: 2-second delay between Yahoo requests (safe for API limits)
- Calculates 30-day price momentum and volume changes

### Phase 3: Combined Ranking
Stocks are ranked using a weighted score:
- **40%** Reddit Momentum (social buzz)
- **30%** Price Momentum (30-day change)
- **20%** Volume Momentum (buying pressure)
- **-10%** Volatility Penalty (risk adjustment)

## Usage

```bash
# Make sure you're in the venv
source ../../venv/bin/activate

# Run the combined scraper
python combined_scraper.py
```

## Rate Limiting

- **Reddit API**: 3-second delay between subreddits (~40 seconds total)
- **Yahoo Finance**: 2-second delay between stocks (~20 seconds for 10 stocks)
- **Total runtime**: ~60-90 seconds

This ensures we stay well under API limits:
- Reddit: 60 requests/minute limit
- Yahoo: No official limit, but 2s delay prevents 429 errors

## Output

The scraper provides:
1. Top 10 stocks from Reddit analysis
2. Yahoo Finance data for each stock
3. Combined ranking with multi-source analysis
4. Executive summary with best performers

## Dependencies

- `praw` - Reddit API
- `yfinance` - Yahoo Finance API
- `python-dotenv` - Environment variables
- `pandas` - Data manipulation

All dependencies are already installed in the main venv.
