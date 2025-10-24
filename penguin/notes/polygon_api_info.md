# Polygon.io API Information

**Last Updated**: 2025-01-24

## Overview

Polygon.io provides financial market data including stocks, options, forex, and crypto. However, different endpoints require different subscription tiers.

---

## Your API Keys

You have two keys/IDs:

1. **`pdZpL5jpmr5pZPEFe81BWfbKZD20oa59`** - ✅ Valid Polygon.io API key (Free Tier)
2. **`81fa7c8b-7ab5-4b5e-8c6f-c112c6d0f216`** - ❌ Not a valid Polygon key (might be for another service?)

**Use the first one** in your `.env` file.

---

## Pricing Tiers & Access

### ✅ Free Tier (Starter) - What You Have

**What's Included**:
- 5 API calls per minute
- End-of-day (EOD) stock data
- Delayed market data (15+ minutes)
- Historical stock prices
- Company information
- Market status

**What's NOT Included**:
- ❌ Options data (requires Premium tier)
- ❌ Real-time stock data
- ❌ Websocket streaming
- ❌ Technical indicators
- ❌ Crypto data

### 💰 Paid Tiers

| Tier | Price | Options Access |
|------|-------|----------------|
| **Starter** (Free) | $0/month | ❌ No |
| **Developer** | $29/month | ❌ No |
| **Advanced** | $99/month | ❌ No |
| **Premium** | $199+/month | ✅ Yes |

**For options data**, you need at least the **Premium plan ($199/month)**.

---

## Testing Results

### ✅ Stock Data Endpoint (Works)

```bash
curl "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2024-01-01/2024-01-02?apiKey=YOUR_KEY"
```

**Response**: ✅ Success (Status: OK)
```json
{
  "status": "OK",
  "results": [...]
}
```

### ❌ Options Snapshot Endpoint (Requires Upgrade)

```bash
curl "https://api.polygon.io/v3/snapshot/options/GME?apiKey=YOUR_KEY"
```

**Response**: ❌ Not Authorized
```json
{
  "status": "NOT_AUTHORIZED",
  "message": "You are not entitled to this data. Please upgrade your plan at https://polygon.io/pricing"
}
```

---

## Why the 403 Error?

When you run:
```bash
python -m penguin.cli.main collectors test polygon_options --symbol GME
```

You get:
```
Polygon API error for GME: HTTP 403
```

**Reason**: The `polygon_options` collector tries to access the **options snapshot endpoint** (`/v3/snapshot/options/{ticker}`), which requires a **paid Premium subscription**.

---

## Solutions

### Option 1: Disable Options Collector (Keep Free Tier)

The options collector won't work with the free tier. You can:

1. **Skip testing it**:
   ```bash
   # Test only free collectors
   python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL
   python -m penguin.cli.main collectors test reddit_wsb --symbol GME
   ```

2. **Keep the key in .env** (it's fine, just won't work for options)

### Option 2: Use Alternative Free Options Data

Replace Polygon options with free alternatives:

1. **Yahoo Finance Options** (Free)
   - Use `yfinance` library
   - Provides options chain data
   - No API key needed

2. **Tradier Sandbox** (Free Developer Tier)
   - Real options data
   - Sandbox environment
   - Sign up at: https://developer.tradier.com/

3. **CBOE Data** (Limited Free Access)
   - Official options exchange data
   - Some endpoints are free

### Option 3: Upgrade to Premium ($199/month)

If you need real-time options flow data:
- Visit: https://polygon.io/pricing
- Upgrade to Premium tier
- Get access to all options endpoints

---

## Recommended Approach for PENGUIN

For now, **use free data sources**:

### Stock Data
- ✅ **Yahoo Finance** (free, no limits, 98 indicators)
- ✅ **Polygon Free Tier** (EOD stock data, 5 calls/min)

### Options Data
- ✅ **Yahoo Finance Options** (free options chains via `yfinance`)
- ✅ **Tradier Sandbox** (free developer options data)

### Social Sentiment
- ✅ **Reddit** (your keys work!)
- ✅ **Twitter** (if you get API access)

### Later (When Scaling)
- Upgrade to Polygon Premium for real-time options flow
- Add Unusual Whales ($50/month for options flow)
- Add other paid sources

---

## What to Do Now

1. **Keep your Polygon key** - It works for stock data! ✅
   ```env
   POLYGON_API_KEY=pdZpL5jpmr5pZPEFe81BWfbKZD20oa59
   ```

2. **Don't worry about the 403 error** - It's expected with free tier

3. **Use Yahoo Finance for options** - It's free and works well:
   ```bash
   python -m penguin.cli.main collectors test yahoo_finance --symbol GME
   ```

4. **Focus on free collectors**:
   - `yahoo_finance` - Stock + options data (free)
   - `reddit_wsb` - Social sentiment (free)

5. **Add more free sources later**:
   - StockTwits
   - News APIs
   - Congressional trading (free)

---

## File Locations

- **API Key**: `.env` file (root directory)
- **Config Loader**: `penguin/core/config.py` (now loads .env correctly!)
- **Polygon Collector**: `penguin/data/collectors/options/polygon_options.py`
- **Yahoo Collector**: `penguin/data/collectors/market_data/yahoo_finance.py` (free alternative)

---

## Summary

✅ **Your Polygon key IS valid** - it just doesn't include options access
❌ **Options endpoint requires Premium ($199/month)**
✅ **Use Yahoo Finance for free options data instead**
✅ **Fixed the .env loading issue** - keys now load correctly!

The 403 error is not a bug - it's Polygon telling you to upgrade. For now, stick with free data sources!

---

## Next Steps

1. Test Yahoo Finance (includes options):
   ```bash
   python -m penguin.cli.main collectors test yahoo_finance --symbol GME
   ```

2. Test Reddit:
   ```bash
   python -m penguin.cli.main collectors test reddit_wsb --symbol GME
   ```

3. Consider adding Tradier Sandbox (free) for options data later

---

**Bottom line**: Your setup is correct, Polygon just needs a paid plan for options. Use Yahoo Finance instead (it's free and has options data)! 🚀
