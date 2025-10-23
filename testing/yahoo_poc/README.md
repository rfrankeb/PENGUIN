# Yahoo Finance Proof of Concept

This proof-of-concept demonstrates fetching real-time stock data from Yahoo Finance and performing technical analysis.

## Features

- Real-time stock price data
- Historical data analysis
- Momentum calculations (30-day returns, volume changes, volatility)
- Technical indicators (SMA, RSI)
- Trading signal detection

## Setup

```bash
cd yahoo_poc
pip install -r requirements.txt
```

## Run

```bash
python yahoo_scraper.py
```

## What It Does

1. **Fetches Stock Information**
   - Current price, market cap, P/E ratio
   - Sector and industry
   - 52-week high/low

2. **Momentum Analysis**
   - 30-day returns
   - Volume changes
   - Volatility calculations

3. **Technical Signals**
   - Moving Average crossovers (SMA 20/50)
   - RSI (Relative Strength Index)
   - Volume spike detection
   - Oversold/overbought indicators

## Example Output

```
MOMENTUM ANALYSIS (30-day returns)
ticker  current_price  30d_return  volume_change_pct  volatility
NVDA    145.32        +12.3%      +45.2%            2.8%
TSLA    242.18        +8.7%       +23.1%            3.5%
AAPL    178.45        +5.2%       -12.3%            1.9%

TECHNICAL SIGNALS
$NVDA - $145.32
  RSI: 68.4
  Signals:
    - Bullish: 20-day MA above 50-day MA
    - Volume Spike: 1.8x average
```

## No API Key Required!

Unlike many financial data sources, Yahoo Finance (via yfinance) is **completely free** and requires no API key. Perfect for proof-of-concept testing!

## Next Steps

This will integrate with PENGUIN's multi-source architecture to combine:
- Social sentiment (Reddit, Twitter)
- Technical indicators (Yahoo Finance)
- Options flow
- News sentiment
- Congressional trading

All analyzed together by Claude AI for comprehensive stock recommendations.
