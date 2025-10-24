# PENGUIN Quick Reference Guide

Your questions answered with exact file locations and how to run everything!

---

## 1. Reddit API Keys - WHERE ARE THEY?

### ✅ Already Set Up!

**Location:** `.env` file (root directory)

Your credentials are already in there:
```bash
REDDIT_CLIENT_ID=AQjWXzzjFYtkMIRySAlwAA
REDDIT_CLIENT_SECRET=rBvAyEoztW1jB1FHEo3XfN_PvHQZxQ
```

### How They're Loaded

**File:** `penguin/core/config.py` (lines 18-21)

```python
class Config:
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PENGUIN Stock Tracker v0.1')
```

The config automatically reads from `.env` file, so you're all set! ✅

### How to Change Them

Just edit the `.env` file:
```bash
nano .env
# or
code .env
```

---

## 2. Excluded Words - WHERE & HOW TO ADD MORE?

### ✅ Just Updated!

**Location:** `penguin/core/constants.py` (lines 49-96)

I just added **200+ excluded words** from your `multi_subreddit_scraper.py` including:

**Categories added:**
- All single letters (A-Z)
- Trading terms (DD, YOLO, WSB, CEO, CFO, IPO, ETF, etc.)
- Exchanges (NYSE, NASDAQ, SEC, IRS, FDA, FBI, etc.)
- Countries (US, UK, EU, IT, FR, DE, JP, CN, etc.)
- Common words (OK, LOL, THE, FOR, AND, etc.)
- Reddit/WSB slang (MOON, HOLD, BUY, SELL, PUMP, DUMP, etc.)

### How Reddit Collector Uses Them

**File:** `penguin/data/collectors/social/reddit_wsb.py` (lines 1-4, 49-57)

```python
from penguin.core.constants import EXCLUDED_WORDS

def _extract_tickers(self, text: str) -> List[str]:
    potential_tickers = self.ticker_pattern.findall(text)
    tickers = [
        ticker for ticker in potential_tickers
        if ticker not in EXCLUDED_WORDS  # <-- Uses your list!
    ]
    return tickers
```

### How to Add More

Just edit `penguin/core/constants.py` and add to the `EXCLUDED_WORDS` set:

```python
EXCLUDED_WORDS = {
    'A', 'I', 'B', 'C', ...
    'YOUR_NEW_WORD_HERE',  # <-- Add here!
    'ANOTHER_WORD',
}
```

---

## 3. Rate Limits & Time Delays - WHERE ARE THEY?

### Reddit Rate Limits

**Location:** `penguin/data/collectors/social/reddit_wsb.py`

**Defined in class attributes (line 23):**
```python
class RedditWSBCollector(BaseCollector):
    name = "reddit_wsb"
    rate_limit = 60  # Reddit API: 60 requests per minute
```

**Built into PRAW library:**
PRAW (Python Reddit API Wrapper) automatically handles Reddit's rate limiting. It:
- Respects Reddit's 60 req/min limit
- Automatically sleeps when needed
- Returns 429 error if exceeded (handled gracefully)

### Yahoo Finance Rate Limits

**Location:** `penguin/data/collectors/market_data/yahoo_finance.py`

**Defined in class (line 22):**
```python
class YahooFinanceCollector(BaseCollector):
    name = "yahoo_finance"
    rate_limit = 2000  # YFinance: ~2000 requests/hour
```

**Manual delay in collect() method (line 55):**
```python
async def collect(self, symbols, **kwargs):
    for symbol in symbols:
        # Add small delay to respect rate limits
        await asyncio.sleep(0.05)  # <-- 50ms delay between symbols

        ticker = yf.Ticker(symbol)
        # ... fetch data
```

### How Rate Limiting Works

**Current Implementation:**
1. **Class attribute** `rate_limit` documents the limit
2. **Manual delays** (`asyncio.sleep()`) prevent hitting limits
3. **Error handling** catches rate limit errors

**Future Enhancement (Phase 2):**
Will add automatic rate limiter that:
- Tracks requests per collector
- Enforces limits with Redis
- Queues requests when limit reached

### Where to Change Delays

**Reddit:** No manual delay needed (PRAW handles it)

**Yahoo Finance:** Change this line in `yahoo_finance.py` (line 55):
```python
await asyncio.sleep(0.05)  # Change this number (in seconds)
```

**Examples:**
```python
await asyncio.sleep(0.05)   # 50ms = fast (20 symbols/second)
await asyncio.sleep(0.1)    # 100ms = medium (10 symbols/second)
await asyncio.sleep(0.5)    # 500ms = slow (2 symbols/second)
await asyncio.sleep(1.0)    # 1 second = very safe
```

---

## 4. Yahoo Finance 98 Indicators - WHERE & HOW TO RUN?

### Where is the Code?

**Technical Analysis Module:**
`penguin/data/collectors/market_data/technical_analysis.py` (~600 lines)

**Enhanced Yahoo Collector:**
`penguin/data/collectors/market_data/yahoo_finance.py`

**Integration (lines 123-148):**
```python
# Calculate technical indicators
if include_technicals and len(hist) >= 50:
    try:
        indicators = TechnicalAnalysis.calculate_all_indicators(hist)

        tech_point = {
            'timestamp': datetime.utcnow(),
            'symbol': symbol,
            'source': self.name,
            'category': self.category.value,
            'data_type': 'technical_analysis',
            'value': hist['Close'].iloc[-1],
            'metadata': {
                **indicators,  # All 98 indicators here!
                'current_price': float(hist['Close'].iloc[-1]),
            }
        }
        data_points.append(tech_point)
```

### How to Run It

#### Method 1: CLI (Simplest)

```bash
# Test with one symbol
penguin collectors test yahoo_finance --symbol AAPL

# You'll see:
# ✅ Calculated 98 technical indicators for AAPL
# Collected 133 data points!
```

```bash
# Collect data (without saving to DB)
penguin collect yahoo_finance --symbol AAPL --symbol TSLA --no-save

# With more data for better indicators
penguin collect yahoo_finance --symbol GME --no-save
```

#### Method 2: Python Script

Create a file `test_indicators.py`:

```python
import asyncio
from penguin.data.registry import registry

async def test_indicators():
    # Discover collectors
    registry.auto_discover()

    # Get Yahoo Finance collector
    collector = registry.get_collector('yahoo_finance')

    # Collect data with technical indicators
    data = await collector.collect(
        symbols=['AAPL', 'TSLA', 'GME'],
        period='6mo',         # 6 months of data
        interval='1d',         # Daily data
        include_technicals=True,  # Calculate indicators (default: True)
        include_info=False     # Skip company info for speed
    )

    # Find technical analysis data points
    for point in data:
        if point['data_type'] == 'technical_analysis':
            symbol = point['symbol']
            indicators = point['metadata']

            print(f"\n{symbol} Technical Analysis:")
            print(f"  Current Price: ${point['value']:.2f}")
            print(f"  RSI: {indicators['rsi_14']:.2f}")
            print(f"  MACD: {indicators['macd']:.4f}")
            print(f"  Bollinger %B: {indicators['bb_percent_b']:.2f}")
            print(f"  Volume Ratio: {indicators['volume_ratio_10day']:.2f}x")
            print(f"  ATR: ${indicators['atr_14']:.2f}")
            print(f"  Total Indicators: {len(indicators)}")

# Run it
asyncio.run(test_indicators())
```

**Run:**
```bash
python test_indicators.py
```

#### Method 3: Interactive Python

```bash
python
```

```python
import asyncio
from penguin.data.registry import registry

# Setup
registry.auto_discover()
collector = registry.get_collector('yahoo_finance')

# Collect
data = asyncio.run(collector.collect(
    symbols=['AAPL'],
    period='3mo',
    include_technicals=True
))

# Get technical analysis
tech = [d for d in data if d['data_type'] == 'technical_analysis'][0]
indicators = tech['metadata']

# Explore!
print("Available indicators:")
for key in sorted(indicators.keys()):
    print(f"  {key}: {indicators[key]}")
```

### What You Get

**98 indicators organized in categories:**

1. **Trend (13):** SMA, EMA, MACD, ADX
2. **Momentum (12):** RSI, Stochastic, Williams %R, ROC, CCI
3. **Volatility (15):** Bollinger Bands, ATR, Keltner Channels
4. **Volume (14):** OBV, CMF, VWAP, volume analysis
5. **Patterns (7):** Support/Resistance, consolidation
6. **Statistics (10):** Returns, volatility, z-score
7. **Fibonacci (7):** Retracement levels
8. **Advanced (20):** Ichimoku, Pivot Points

### Parameters Explained

**period:** How much historical data to fetch
- `'1d'` = 1 day (not enough for indicators)
- `'5d'` = 5 days
- `'1mo'` = 1 month
- `'3mo'` = 3 months ✅ **Recommended minimum**
- `'6mo'` = 6 months ✅ **Best for all indicators**
- `'1y'` = 1 year
- `'2y'` = 2 years

**interval:** Data granularity
- `'1m'` = 1 minute bars (only for last 7 days)
- `'5m'` = 5 minute bars
- `'1h'` = 1 hour bars
- `'1d'` = Daily bars ✅ **Recommended**

**include_technicals:** Calculate indicators?
- `True` (default) = Yes, calculate all 98
- `False` = Skip, just get prices

**include_info:** Get company info?
- `True` = Yes, include sector, market cap, etc.
- `False` (default) = Skip for speed

---

## File Structure Summary

```
PENGUIN/
├── .env                          # ✅ Your Reddit API keys
│
├── penguin/
│   ├── core/
│   │   ├── config.py            # Loads .env credentials
│   │   └── constants.py         # ✅ EXCLUDED_WORDS (200+)
│   │
│   ├── data/
│   │   ├── collectors/
│   │   │   ├── social/
│   │   │   │   └── reddit_wsb.py        # Reddit collector (rate_limit: 60/min)
│   │   │   └── market_data/
│   │   │       ├── yahoo_finance.py     # ✅ Yahoo collector (rate_limit: 2000/hr)
│   │   │       └── technical_analysis.py # ✅ 98 indicators
│   │   │
│   │   ├── base.py              # BaseCollector (defines rate_limit attribute)
│   │   └── registry.py          # Auto-discovers collectors
│   │
│   └── notes/                    # ✅ All documentation
│       ├── phase1_foundation.md  # Complete Phase 1 guide
│       ├── phase2_prep.md        # Technical indicators guide
│       └── glossary.md           # All terms explained
│
└── QUICK_REFERENCE.md           # This file!
```

---

## Common Commands

### Direct Python Commands

```bash
# Check system status
python -m penguin.cli.main status

# List all collectors
python -m penguin.cli.main collectors list

# Test Reddit collector
python -m penguin.cli.main collectors test reddit_wsb --symbol GME

# Test Yahoo Finance with indicators
python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL

# Test Polygon Options collector
python -m penguin.cli.main collectors test polygon_options --symbol GME

# Collect Reddit data (no DB save)
python -m penguin.cli.main collect reddit_wsb --limit 100 --no-save

# Collect Yahoo data with indicators (no DB save)
python -m penguin.cli.main collect yahoo_finance --symbol AAPL --symbol TSLA --no-save

# Help on any command
python -m penguin.cli.main --help
python -m penguin.cli.main collect --help
python -m penguin.cli.main collectors test --help
```

### Shell Script Shortcuts (Easier to Remember!)

```bash
# Setup environment
./scripts/cli/setup_env.sh

# List all collectors
./scripts/cli/list_collectors.sh

# Test all collectors at once
./scripts/cli/test_collectors.sh

# Collect data from all sources (default symbols: GME,AMC,AAPL,TSLA)
./scripts/cli/collect_data.sh

# Collect data with custom symbols
./scripts/cli/collect_data.sh "NVDA,MSFT,GOOGL,AMZN"

# View technical indicators for a stock
./scripts/cli/view_indicators.sh AAPL
```

---

## Quick Modifications

### Change Reddit rate limit delay
**File:** Reddit uses PRAW which handles rate limiting automatically. No changes needed!

### Change Yahoo rate limit delay
**File:** `penguin/data/collectors/market_data/yahoo_finance.py` line 55
```python
await asyncio.sleep(0.05)  # Change this number (seconds)
```

### Add excluded words
**File:** `penguin/core/constants.py` lines 49-96
```python
EXCLUDED_WORDS = {
    'A', 'I', 'DD', ...
    'YOUR_WORD_HERE',  # Add here
}
```

### Change Reddit credentials
**File:** `.env` (root directory)
```bash
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```

---

## Testing Checklist

✅ Reddit API keys working?
```bash
python -m penguin.cli.main collectors test reddit_wsb --symbol GME
```

✅ Yahoo Finance working?
```bash
python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL
```

✅ Polygon Options API key configured?
```bash
# First, add your API key to .env:
# POLYGON_API_KEY=your_actual_key_here

# Then test:
python -m penguin.cli.main collectors test polygon_options --symbol GME
```

✅ Technical indicators calculating?
```bash
# Look for: "✅ Calculated 98 technical indicators"
python -m penguin.cli.main collectors test yahoo_finance --symbol TSLA
```

✅ Excluded words filtering?
```bash
# Reddit collector automatically uses EXCLUDED_WORDS
python -m penguin.cli.main collect reddit_wsb --limit 10 --no-save
```

---

## Need More Help?

**Documentation locations:**
- `penguin/notes/phase1_foundation.md` - Everything about Phase 1
- `penguin/notes/phase2_prep.md` - Technical indicators explained
- `penguin/notes/glossary.md` - All terms defined
- `USAGE.md` - Usage guide
- `CLAUDE.md` - Full architecture spec

**Quick reference:**
- Reddit keys: `.env`
- Excluded words: `penguin/core/constants.py`
- Rate limits: Each collector's `rate_limit` attribute
- Delays: `await asyncio.sleep()` in collect methods
- Technical indicators: `penguin/data/collectors/market_data/technical_analysis.py`

---

## Troubleshooting Common Errors

### ❌ Polygon API Error: HTTP 403

**Error Message:**
```
Polygon API error for GME: HTTP 403
Collected 0 data points!
```

**Cause:** Your Polygon API key is not configured or is invalid.

**Solution:**

1. **Get a free API key:**
   - Go to: https://polygon.io/dashboard/signup
   - Sign up for a free account
   - Copy your API key from the dashboard

2. **Add it to your .env file:**
   ```bash
   # Open .env
   nano .env
   # OR
   code .env
   ```

3. **Add this line (replace with your actual key):**
   ```
   POLYGON_API_KEY=your_actual_api_key_here
   ```

4. **Test again:**
   ```bash
   python -m penguin.cli.main collectors test polygon_options --symbol GME
   ```

**Note:** Polygon free tier provides:
- End-of-day (EOD) data only
- 5 API calls per minute
- Previous day's options data (not real-time)

### ❌ Module Not Found Error

**Error Message:**
```
ModuleNotFoundError: No module named 'penguin'
```

**Solution:**
```bash
# Make sure you're in the PENGUIN directory
cd ~/Desktop/Niche/PENGUIN

# Activate virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .
```

### ❌ Reddit Authentication Error

**Error Message:**
```
Reddit API authentication failed
```

**Solution:**
```bash
# Check your .env file
cat .env | grep REDDIT

# Make sure both are set:
# REDDIT_CLIENT_ID=AQjWXzzjFYtkMIRySAlwAA
# REDDIT_CLIENT_SECRET=rBvAyEoztW1jB1FHEo3XfN_PvHQZxQ
```

---

## 5. QuiverQuant Data - CONGRESSIONAL, INSIDER, CONTRACTS & MORE

### ✅ Fully Implemented (Tier 1 - $10/month)

**Location:** Multiple collectors across different categories

**API Key:** Already configured in `.env`:
```bash
QUIVERQUANT_API_KEY=91ac18b99a52b23a4645451e6401261e6a5dc769
```

### Collectors Implemented (18 Endpoints Total)

#### 1. Congressional Trading (Bulk)
**File:** `penguin/data/collectors/congress/quiverquant_congress.py`

**What It Does:** Historical congressional stock trades with excess returns

**Usage:**
```bash
# Test with single symbol
python -m penguin.cli.main collectors test quiverquant_congress --symbol NVDA

# Collect for multiple symbols
python -m penguin.cli.main collectors run quiverquant_congress --symbols NVDA,MSFT,AAPL
```

**Endpoint:** `GET /beta/bulk/congresstrading`

#### 2. Congressional Trading (Live - 4 endpoints)
**File:** `penguin/data/collectors/congress/quiverquant_congress_live.py`

**What It Does:** Real-time congressional trades, can filter by House/Senate

**Usage:**
```bash
# All Congress trades
python -m penguin.cli.main collectors test quiverquant_congress_live --symbol NVDA

# House only
python -m penguin.cli.main collectors run quiverquant_congress_live --symbols AAPL --endpoint house

# Senate only
python -m penguin.cli.main collectors run quiverquant_congress_live --symbols TSLA --endpoint senate

# Historical for specific stock
python -m penguin.cli.main collectors run quiverquant_congress_live --symbols GME --endpoint historical
```

**Endpoints:**
- `/beta/live/congresstrading` - All Congress
- `/beta/live/housetrading` - House only
- `/beta/live/senatetrading` - Senate only
- `/beta/historical/congresstrading/{ticker}` - Historical for symbol

#### 3. Insider Trading
**File:** `penguin/data/collectors/insider/quiverquant_insiders.py`

**What It Does:** SEC Form 4 insider transactions with transaction type decoding

**Usage:**
```bash
# Recent insider trades
python -m penguin.cli.main collectors test quiverquant_insiders --symbol AAPL

# Filter by transaction type (purchases only)
python -m penguin.cli.main collectors run quiverquant_insiders --symbols TSLA,NVDA --transaction_types P

# Filter significant transactions
python -m penguin.cli.main collectors run quiverquant_insiders --symbols MSFT --min_value 1000000
```

**Endpoint:** `/beta/live/insiders`

**Transaction Codes:**
- `P` = Open Market Purchase
- `S` = Open Market Sale
- `M` = Exercise of Options
- `A` = Award/Grant

#### 4. Government Contracts (3 endpoints)
**File:** `penguin/data/collectors/alternative/quiverquant_contracts.py`

**What It Does:** Federal government contract awards

**Usage:**
```bash
# Recent contracts
python -m penguin.cli.main collectors test quiverquant_contracts --symbol AAPL

# Historical contracts for defense contractors
python -m penguin.cli.main collectors run quiverquant_contracts --symbols BA,LMT,RTX --endpoint historical

# All historical contracts
python -m penguin.cli.main collectors run quiverquant_contracts --symbols MSFT --endpoint all_historical

# Filter by minimum contract amount ($1M+)
python -m penguin.cli.main collectors run quiverquant_contracts --symbols all --min_amount 1000000
```

**Endpoints:**
- `/beta/live/govcontracts` - Recent contracts
- `/beta/historical/govcontracts/{ticker}` - Historical by company
- `/beta/historical/govcontractsall/{ticker}` - All historical

#### 5. QuiverQuant All (11 endpoints)
**File:** `penguin/data/collectors/alternative/quiverquant_all.py`

**What It Does:** Unified collector for lobbying, social, dark pool, and other data

**Usage:**
```bash
# Test all available endpoints
python -m penguin.cli.main collectors test quiverquant_all --symbol GME

# Test specific endpoints only
python -m penguin.cli.main collectors run quiverquant_all --symbols AMC,GME --endpoints lobbying_live,darkpool,bills

# Dark pool trading only
python -m penguin.cli.main collectors run quiverquant_all --symbols AAPL,TSLA --endpoints darkpool

# Lobbying data
python -m penguin.cli.main collectors run quiverquant_all --symbols MSFT,GOOGL --endpoints lobbying_live,lobbying_historical

# Legislative tracking
python -m penguin.cli.main collectors run quiverquant_all --endpoints legislation,bills
```

**Endpoints:**
- **Lobbying (2):**
  - `/beta/live/lobbying` - Recent lobbying
  - `/beta/historical/lobbying/{ticker}` - Historical lobbying

- **Social/Reddit (4):**
  - `/beta/live/wsbcomments` - WallStreetBets mentions
  - `/beta/live/redditcomments` - General Reddit
  - `/beta/live/cryptocomments` - Crypto mentions
  - `/beta/live/spaccomments` - SPAC mentions

- **Dark Pool (1):**
  - `/beta/live/offexchange` - Off-exchange trading

- **Other (4):**
  - `/beta/live/cnbc` - CNBC analyst trades
  - `/beta/live/flights` - Corporate flight tracking
  - `/beta/live/legislation` - Legislative activity
  - `/beta/live/bill_summaries` - Bill summaries

**Available Endpoint Keys:**
```python
# Lobbying
'lobbying_live', 'lobbying_historical'

# Social
'wsb', 'reddit', 'crypto', 'spac'

# Dark Pool
'darkpool'

# Other
'cnbc', 'flights', 'legislation', 'bills'
```

### What You Get (Data Fields)

**Congressional Trading:**
- Politician name, chamber (House/Senate), party, state, district
- Transaction type (Purchase/Sale), amount range
- Transaction date, disclosure date
- **Excess return vs S&P 500** (unique to QuiverQuant!)
- Company name, ticker

**Insider Trading:**
- Insider name, title, role (Director/Officer/10% Owner)
- Transaction type (decoded from SEC codes)
- Shares, price per share, total value
- Shares owned after transaction
- Direct vs indirect ownership
- Filing date, transaction date

**Government Contracts:**
- Contract amount, agency, award type
- Contract date, company name
- Description of work/goods

**Lobbying:**
- Lobbying amount spent
- Company, date, description

**Dark Pool:**
- Off-exchange trading volume

**Social/Reddit:**
- Mention counts, comment counts
- Source subreddit

**Legislative:**
- Bill summaries, current status, chamber
- Last action date

### Rate Limits & Best Practices

**Tier 1 Limits:**
- **Recommended:** 1 request per second (60/minute)
- **Current implementation:** 1 second delay between requests ✅
- **Cost:** $10/month

**Pagination:**
```python
# Default page size: 100 items
page=1, page_size=100  # First 100
page=2, page_size=100  # Next 100
```

**Filtering Tips:**
- Use `lookback_days` to limit recent data (7, 30, etc.)
- Use `min_amount` for contracts to filter significant deals
- Use `transaction_types` for insiders to focus on purchases ('P') or sales ('S')
- Use `endpoints` parameter in quiverquant_all to only fetch what you need

### Common Use Cases

**Track Nancy Pelosi's Trades:**
```bash
python -m penguin.cli.main collectors run quiverquant_congress --representative "Nancy Pelosi"
```

**Find Recent Insider Purchases:**
```bash
python -m penguin.cli.main collectors run quiverquant_insiders --symbols AAPL,MSFT,GOOGL --transaction_types P --lookback_days 7
```

**Monitor Government Contracts for Defense Stocks:**
```bash
python -m penguin.cli.main collectors run quiverquant_contracts --symbols LMT,BA,RTX,NOC --min_amount 10000000
```

**Track WallStreetBets Mentions:**
```bash
python -m penguin.cli.main collectors run quiverquant_all --symbols GME,AMC,BBBY --endpoints wsb
```

**Find Dark Pool Activity:**
```bash
python -m penguin.cli.main collectors run quiverquant_all --symbols NVDA,AMD,TSM --endpoints darkpool
```

### Documentation

**Full guide:** `penguin/notes/quiverquant_setup.md`

**Includes:**
- Complete endpoint documentation
- All parameters explained
- Data schemas
- Transaction code reference
- Troubleshooting guide
- Quick start examples

---

## Available Shell Scripts

All scripts are in `scripts/cli/` and are executable:

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup_env.sh` | Setup dev environment | `./scripts/cli/setup_env.sh` |
| `list_collectors.sh` | List all collectors | `./scripts/cli/list_collectors.sh` |
| `test_collectors.sh` | Test all collectors | `./scripts/cli/test_collectors.sh` |
| `collect_data.sh` | Collect data | `./scripts/cli/collect_data.sh "GME,AMC"` |
| `view_indicators.sh` | View indicators | `./scripts/cli/view_indicators.sh AAPL` |

---

**All set! Try these commands:**
```bash
# List all available collectors
python -m penguin.cli.main collectors list

# Test Yahoo Finance (no API key needed)
python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL

# Test Reddit (uses your existing API keys)
python -m penguin.cli.main collectors test reddit_wsb --symbol GME

# Test QuiverQuant collectors (Tier 1 - $10/month)
python -m penguin.cli.main collectors test quiverquant_congress_live --symbol NVDA
python -m penguin.cli.main collectors test quiverquant_insiders --symbol AAPL
python -m penguin.cli.main collectors test quiverquant_contracts --symbol LMT
python -m penguin.cli.main collectors test quiverquant_all --symbol GME
```
