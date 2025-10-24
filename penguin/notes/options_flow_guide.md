# Options Flow Data Collection Guide

## Overview

Options flow data is one of the most powerful signals for predicting stock movements. When large institutional traders ("smart money") place big options bets, it often precedes significant price moves.

This guide explains how PENGUIN collects and analyzes options flow data.

---

## Why Options Flow Matters

### What is Options Flow?

Options flow refers to the real-time activity in the options market:
- **Call options**: Bets that a stock will go UP
- **Put options**: Bets that a stock will go DOWN
- **Volume**: Number of contracts traded
- **Premium**: Dollar amount spent on contracts
- **Open Interest**: Total outstanding contracts

### Key Signals

1. **Unusual Volume**
   - When options volume is significantly higher than normal
   - Example: Stock averages 1,000 contracts/day, suddenly trades 10,000
   - Indicates big players are positioning

2. **Large Premium Spent**
   - When someone spends $100K+ on a single options contract
   - Big money = institutional traders with research
   - They don't bet big unless they know something

3. **Sweep Orders**
   - Aggressive buying across multiple exchanges simultaneously
   - Buyer wants position immediately, not patient
   - Often signals urgency (earnings, news coming)

4. **Put/Call Ratio**
   - Ratio of put volume to call volume
   - High ratio (>1.0) = bearish sentiment
   - Low ratio (<1.0) = bullish sentiment

5. **Near-Term Expiration with High Volume**
   - Options expiring soon with massive volume
   - Can cause "gamma squeeze" (forces market makers to buy stock)
   - Example: GameStop (GME) in January 2021

---

## Our Implementation

### Polygon.io Collector

**File:** `penguin/data/collectors/options/polygon_options.py`

**What it does:**
1. Fetches options contracts for watchlist symbols
2. Analyzes volume vs open interest
3. Calculates premium spent
4. Identifies unusual activity
5. Computes put/call ratio
6. Determines sentiment (bullish/bearish/neutral)

### Data Sources

#### Free Tier: Polygon.io
- **Cost**: Free (with registration)
- **Rate Limit**: 5 API calls per minute
- **Data**: End-of-day options data
- **Coverage**: All US options
- **Sign up**: https://polygon.io/dashboard/signup

**Limitations:**
- EOD data only (not real-time)
- 5 calls/min (slow for many symbols)
- No sweep/block detection (need premium)

#### Premium Options (Future)
- **Unusual Whales**: $50-200/month, real-time flow
- **FlowAlgo**: $149/month, sweep alerts
- **Tradier**: Requires brokerage account
- **CBOE Data Shop**: Enterprise pricing

For MVP, we start with Polygon.io free tier.

---

## Setup Instructions

### 1. Get Polygon.io API Key

1. Go to https://polygon.io/dashboard/signup
2. Sign up for free account
3. Verify email
4. Go to Dashboard → API Keys
5. Copy your API key

### 2. Add to .env File

```bash
# Add this line to your .env file
POLYGON_API_KEY=your_api_key_here
```

### 3. Test the Collector

```bash
# Test with default symbols (AAPL, TSLA, GME, AMC, SPY)
python -m penguin.cli.main collectors test polygon_options

# Test with specific symbol
python -m penguin.cli.main collectors test polygon_options --symbol GME

# Collect data (no database save)
python -m penguin.cli.main collect polygon_options --symbol AAPL --no-save
```

---

## How the Collector Works

### Data Collection Flow

```
1. Fetch options contracts for symbol
   ↓
2. For each contract, extract:
   - Strike price
   - Expiration date
   - Volume
   - Open interest
   - Last price
   - Greeks (delta, gamma, etc.)
   ↓
3. Calculate metrics:
   - Premium = price × volume × 100
   - Volume/OI ratio
   - Put/Call ratio
   ↓
4. Detect unusual activity:
   - Volume > threshold (default: 100)
   - Premium > threshold (default: $10,000)
   ↓
5. Classify sentiment:
   - More big calls = bullish
   - More big puts = bearish
   ↓
6. Return normalized data points
```

### What Gets Collected

For each symbol, we create 2 data points:

#### 1. Options Flow (Unusual Activity)
```python
{
    'timestamp': '2025-10-24T14:30:00Z',
    'symbol': 'AAPL',
    'source': 'polygon_options',
    'category': 'options_derivatives',
    'data_type': 'options_flow',
    'value': 2500000,  # Total premium spent
    'metadata': {
        'total_call_volume': 15000,
        'total_put_volume': 8000,
        'put_call_ratio': 0.53,
        'unusual_calls': [
            {
                'strike': 270,
                'expiration': '2025-11-15',
                'volume': 5000,
                'open_interest': 10000,
                'last_price': 8.50,
                'premium': 4250000,  # $4.25M!
                'volume_oi_ratio': 0.5,
                'delta': 0.65,
                'gamma': 0.03
            },
            # ... top 5 unusual calls
        ],
        'unusual_puts': [...],  # Top 5 unusual puts
        'unusual_calls_count': 12,
        'unusual_puts_count': 5,
        'total_premium': 2500000,
        'sentiment': 'bullish'  # More big calls than puts
    }
}
```

#### 2. Put/Call Ratio
```python
{
    'timestamp': '2025-10-24T14:30:00Z',
    'symbol': 'AAPL',
    'source': 'polygon_options',
    'category': 'options_derivatives',
    'data_type': 'put_call_ratio',
    'value': 0.53,  # 0.53:1 ratio (bullish)
    'metadata': {
        'total_call_volume': 15000,
        'total_put_volume': 8000,
        'sentiment': 'bullish'  # Ratio < 1 = bullish
    }
}
```

---

## Interpreting the Signals

### Bullish Signals
- ✅ High call volume with low put volume
- ✅ Large premium on call contracts ($100K+)
- ✅ Put/Call ratio < 0.7
- ✅ Near-term calls with high volume (gamma squeeze potential)
- ✅ High delta calls (0.6-0.9) showing confidence

### Bearish Signals
- 🔴 High put volume with low call volume
- 🔴 Large premium on put contracts
- 🔴 Put/Call ratio > 1.5
- 🔴 Near-term puts with high volume
- 🔴 Protective puts (institutions hedging)

### Neutral/Mixed Signals
- ⚠️ Put/Call ratio near 1.0
- ⚠️ Similar premium on both sides
- ⚠️ Low overall volume (no conviction)

---

## Configuration

### Adjustable Parameters

In `polygon_options.py`, you can modify:

```python
# Minimum volume to flag as unusual (default: 100 contracts)
min_volume = kwargs.get('min_volume', 100)

# Minimum premium to flag as unusual (default: $10,000)
min_premium = kwargs.get('min_premium', 10000)

# Rate limiting (12 seconds = 5 req/min for free tier)
await asyncio.sleep(12)
```

### Custom Collection

```python
import asyncio
from penguin.data.registry import registry

# Setup
registry.auto_discover()
collector = registry.get_collector('polygon_options')

# Collect with custom thresholds
data = asyncio.run(collector.collect(
    symbols=['GME', 'AMC'],
    min_volume=500,      # Higher threshold
    min_premium=50000,   # $50K minimum
    date='2025-10-23'    # Specific date
))

# Analyze results
for point in data:
    if point['data_type'] == 'options_flow':
        meta = point['metadata']
        print(f"{point['symbol']}: {meta['sentiment']}")
        print(f"  Unusual calls: {meta['unusual_calls_count']}")
        print(f"  Unusual puts: {meta['unusual_puts_count']}")
        print(f"  Total premium: ${meta['total_premium']:,.0f}")
```

---

## Rate Limits & Costs

### Free Tier (Polygon.io)
- **Rate**: 5 API calls per minute
- **Cost**: $0
- **Data**: End-of-day (EOD)
- **Best for**: Daily scans, backtesting

**Calculation:**
- 5 calls/min = 300 calls/hour = 7,200 calls/day
- Can scan ~7,000 symbols per day
- More than enough for MVP

### Upgrade Path

When you need real-time data:

1. **Polygon.io Starter** ($29/month)
   - 1,000 calls/min
   - Real-time data (15-minute delay)
   - WebSocket access

2. **Polygon.io Developer** ($99/month)
   - Unlimited calls
   - Real-time (no delay)
   - Historical data

3. **Premium Flow Services** ($50-200/month)
   - Unusual Whales
   - FlowAlgo
   - Pre-filtered unusual activity

---

## Code Locations

### Main Files
- **Collector**: `penguin/data/collectors/options/polygon_options.py` (~320 lines)
- **Config**: `penguin/core/config.py` (lines 23-26)
- **Constants**: `penguin/core/constants.py` (DataCategory.OPTIONS_DERIVATIVES)

### Key Functions
- `collect()` - Main collection method (line 29)
- `_get_options_contracts()` - Fetch from API (line 99)
- `_analyze_options_activity()` - Detect unusual activity (line 141)

---

## Integration with Signal Detection

Once collected, options flow data feeds into Phase 2 signal detectors:

### Future Detectors (Phase 2)
1. **OptionsFlowDetector**
   - Triggers on unusual premium ($100K+)
   - Correlates with stock price movement
   - Confidence based on size and timing

2. **GammaSqueezeDetector**
   - Identifies high call volume near expiration
   - Calculates gamma exposure
   - Predicts forced buying by market makers

3. **DarkHorseDetector**
   - Finds stocks with options activity but low social buzz
   - "Smart money" plays before retail awareness
   - High conviction signal

---

## Real-World Examples

### GameStop (GME) - January 2021
**Options Signal:**
- Massive call buying in $20-$60 strikes
- Volume 50x normal
- Premium: $500M+ in one week
- Put/Call ratio: 0.1 (extremely bullish)

**Result:** Stock went from $20 → $483 in 2 weeks

**What PENGUIN would detect:**
- Unusual call volume (✓)
- Huge premium spent (✓)
- Low put/call ratio (✓)
- Gamma squeeze setup (✓)

### Tesla (TSLA) - Pre-Earnings
**Options Signal:**
- Large call sweep: $2M at $300 strike
- Expiration: 1 week (after earnings)
- Delta: 0.7 (high confidence)

**Interpretation:**
- Someone betting big on earnings beat
- Willing to pay high premium
- Short timeframe = insider confidence?

**Result:** Earnings beat, stock +15%

---

## Troubleshooting

### No data returned
**Possible causes:**
1. API key not configured → Check `.env`
2. Rate limit exceeded → Wait 60 seconds
3. Symbol has no options → Try SPY, AAPL, TSLA
4. Weekend/after hours → Options data is EOD

### "Unusual activity" not detected
**Solutions:**
1. Lower thresholds: `min_volume=50`, `min_premium=5000`
2. Check volatile stocks: GME, AMC, TSLA
3. Use market days (Mon-Fri) when volume is higher

### Slow collection
**Optimization:**
- Free tier: 5 calls/min (12 seconds per symbol)
- Upgrade to paid tier for faster collection
- Use smaller watchlist (top 50 stocks)
- Run during off-hours

---

## Next Steps

### Phase 2: Signal Detection
After collecting options data, we'll build detectors:

1. **OptionsFlowDetector** - Unusual activity alerts
2. **GammaSqueezeDetector** - Predict forced buying
3. **SmartMoneyDetector** - Follow institutional flows

### Phase 3: AI Analysis
Feed options signals to Claude AI:
```
Signal: $2M call sweep on AAPL $270 strike
Expiration: 2 weeks
Context: Apple earnings in 10 days

Claude Analysis:
"Large institutional bet on AAPL beating earnings.
$270 strike implies 5% upside expectation.
Short timeframe suggests high confidence.
Thesis: Earnings beat likely, target $275-280."
```

---

## Resources

### Learn More
- **Tastytrade**: Free options education
- **CBOE Options Institute**: Comprehensive guides
- **r/options**: Reddit community
- **OptionAlpha**: Free courses

### Data Providers
- **Polygon.io**: https://polygon.io
- **Unusual Whales**: https://unusualwhales.com
- **FlowAlgo**: https://flowalgo.com
- **Market Chameleon**: https://www.marketchameleon.com

---

## Summary

**Options flow collector provides:**
- ✅ Unusual call/put activity detection
- ✅ Put/Call ratio sentiment
- ✅ Premium analysis (smart money tracking)
- ✅ Volume vs Open Interest comparison
- ✅ Free tier available (Polygon.io)

**Perfect for:**
- Early detection of institutional positioning
- Pre-earnings plays
- Gamma squeeze setups
- Sentiment confirmation

**Next:** Add more symbols to watchlist and integrate with signal detection!
