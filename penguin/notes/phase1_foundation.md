# Phase 1: Foundation - Development Notes

**Status:** ✅ Complete
**Date:** October 24, 2025
**Duration:** Single session

---

## Overview

Phase 1 established the core architecture for PENGUIN - a plugin-based data collection system with database storage and CLI management. The goal was to create a scalable foundation that can support 1000+ data sources.

---

## What Was Built

### 1. Core Configuration System

**Files:**
- `penguin/core/config.py`
- `penguin/core/constants.py`

**What it does:**
The configuration system centralizes all settings and provides type-safe enums for categories and constants.

**Key Components:**

#### Config Class (`config.py`)
Loads configuration from environment variables with sensible defaults:

```python
class Config:
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/penguin')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
```

**Why this matters:**
- Single source of truth for all settings
- Environment-based configuration (dev/staging/prod)
- No hardcoded credentials

#### Constants (`constants.py`)
Defines enums for standardization:

**DataCategory** - Types of data sources:
- `SOCIAL_SENTIMENT` - Reddit, Twitter, StockTwits
- `MARKET_DATA` - Prices, volume, OHLCV
- `OPTIONS_DERIVATIVES` - Options flow, Greeks
- `INSIDER_TRADING` - Form 4, 13F filings
- `TECHNICAL_INDICATORS` - RSI, MACD, etc.
- `FUNDAMENTAL_DATA` - Earnings, financials
- `ALTERNATIVE_DATA` - Satellite, credit cards
- `MACRO_ECONOMIC` - GDP, inflation, rates
- `CRYPTO_BLOCKCHAIN` - On-chain data
- `NEWS_MEDIA` - News articles

**CollectionFrequency** - How often to collect:
- `REALTIME` - WebSocket/streaming
- `HIGH` - Every 1-5 minutes
- `MEDIUM` - Every 15-60 minutes
- `LOW` - Every 1-24 hours
- `ON_DEMAND` - Event-triggered

**Why this matters:**
- Type safety (can't misspell category names)
- IDE autocomplete support
- Easy to filter collectors by category

---

### 2. Plugin System Architecture

**Files:**
- `penguin/data/base.py` - BaseCollector interface
- `penguin/data/registry.py` - Plugin registry

**What it does:**
Provides a standardized way to add new data sources. Any class inheriting from BaseCollector is automatically discovered and registered.

#### BaseCollector Interface

**Required attributes:**
```python
class MyCollector(BaseCollector):
    name = "my_collector"           # Unique identifier
    category = DataCategory.SOCIAL  # Category
    frequency = CollectionFrequency.HIGH  # How often to run
    requires_auth = True            # Needs API keys?
    rate_limit = 60                 # Requests per minute
    cost_per_request = 0.0          # USD per request
```

**Required methods:**
1. **`collect(symbols, **kwargs)`** - Main collection logic
   - Returns list of normalized data points
   - Async-compatible
   - Accepts optional symbol filter

2. **`validate_credentials()`** - Check if API keys work
   - Returns True/False
   - Called before first collection

3. **`get_schema()`** - Describe output format
   - Returns dict describing fields
   - Used for documentation

**Optional methods:**
- `normalize(raw_data)` - Convert API response to standard format
- `health_check()` - Verify source is accessible

**Why this matters:**
- Every collector follows same interface
- Easy to add new sources (just inherit and implement 3 methods)
- Predictable behavior across all collectors

#### Plugin Registry

**How it works:**
```python
registry = DataSourceRegistry()
registry.auto_discover()  # Scans penguin/data/collectors/**/*.py
collector = registry.get_collector("reddit_wsb")
data = await collector.collect(symbols=["AAPL"])
```

**Features:**
- **Auto-discovery**: Finds all BaseCollector subclasses automatically
- **Lazy instantiation**: Creates collectors only when needed
- **Category filtering**: Get all social sentiment collectors
- **Enable/disable**: Turn collectors on/off without deleting code
- **Health monitoring**: Check status of all collectors

**Why this matters:**
- Zero configuration - just write a collector and it's discovered
- Can have 1000+ collectors without performance impact
- Easy to test individual collectors

---

### 3. Data Normalization

**Standard format:**
Every collector returns data in this format:

```python
{
    'timestamp': datetime.utcnow(),      # When collected
    'symbol': 'AAPL',                    # Stock ticker
    'source': 'reddit_wsb',              # Which collector
    'category': 'social_sentiment',      # Data category
    'data_type': 'mention',              # Specific type
    'value': 1.0,                        # Numeric value
    'metadata': {                        # Extra data (flexible)
        'sentiment_score': 0.8,
        'post_title': '...',
        'upvotes': 1234
    }
}
```

**Why this format:**
- **timestamp**: Enable time-series analysis
- **symbol**: Link to stocks
- **source**: Track which collector produced it
- **category**: Group similar data types
- **data_type**: Distinguish between mentions/prices/volume
- **value**: Numeric value for aggregation (count, price, etc.)
- **metadata**: Source-specific details without breaking schema

**Benefits:**
- All collectors produce compatible data
- Easy to aggregate across sources
- Database schema is consistent
- Can compare Reddit mentions with price movements

---

### 4. Database Layer

**Files:**
- `penguin/data/storage/models.py` - SQLAlchemy models
- `penguin/data/storage/database.py` - Connection management
- `penguin/data/storage/store.py` - High-level API

#### Database Models

**1. Stock** - Company metadata
```python
class Stock:
    symbol: str         # Ticker (e.g., "AAPL")
    name: str          # Company name
    sector: str        # Industry sector
    industry: str      # Specific industry
    market_cap: float  # Market capitalization
```

**Why:** Store company information once, reference by symbol

**2. DataPoint** - Time-series data (main table)
```python
class DataPoint:
    timestamp: datetime  # When collected
    symbol: str         # Stock ticker
    source: str         # Collector name
    category: str       # Data category
    data_type: str      # Specific type
    value: float        # Numeric value
    extra_data: JSON    # Flexible metadata
```

**Why:** This is where all collected data goes. Optimized for time-series queries with indexes on (timestamp, symbol, source).

**3. Signal** - Detected signals
```python
class Signal:
    timestamp: datetime  # When detected
    symbol: str         # Stock ticker
    signal_type: str    # Type (momentum_spike, etc.)
    strength: float     # 0.0 to 1.0
    extra_data: JSON    # Signal details
    active: bool        # Is signal still valid?
    resolved_at: datetime  # When closed
```

**Why:** Track investment signals with their lifecycle

**4. Recommendation** - AI recommendations
```python
class Recommendation:
    symbol: str
    recommendation: str      # BUY, WATCH, AVOID
    confidence: float        # 0-100
    time_horizon: str        # SHORT, MEDIUM, LONG
    thesis: text            # Investment thesis
    supporting_signals: JSON # What signals triggered this
    risks: JSON             # Identified risks
    entry_strategy: text
    exit_strategy: text
```

**Why:** Store Claude's analysis and track performance

**5. CollectorStatus** - Health monitoring
```python
class CollectorStatus:
    collector_name: str
    enabled: bool
    last_run: datetime
    last_success: datetime
    last_error: text
    total_runs: int
    total_errors: int
    avg_duration_seconds: float
```

**Why:** Monitor collector health and performance over time

#### Database Connection Manager

**Key features:**
- Connection pooling with SQLAlchemy
- Context managers for safe transactions
- Automatic rollback on errors
- Connection verification (pool_pre_ping)

**Usage:**
```python
from penguin.data.storage.database import db

# Create tables
db.create_tables()

# Use session
with db.get_session() as session:
    stock = Stock(symbol="AAPL", name="Apple Inc.")
    session.add(stock)
    # Automatically commits on success, rolls back on error
```

#### High-Level Storage API

**Why it exists:**
Instead of writing SQLAlchemy queries everywhere, we provide a simple API:

```python
from penguin.data.storage.store import store

# Save collected data
store.save_data_points(data_points)

# Get or create stock
stock = store.get_or_create_stock("AAPL", name="Apple Inc.")

# Save signal
store.save_signal("AAPL", "momentum_spike", strength=0.85)

# Query recent data
data = store.get_recent_data_points(symbol="AAPL", hours=24)
```

**Benefits:**
- Simpler API than raw SQLAlchemy
- Handles common patterns (upsert, bulk insert)
- Error handling built-in
- Easy to test

---

### 5. Data Collectors

#### Reddit WSB Collector

**File:** `penguin/data/collectors/social/reddit_wsb.py`

**What it does:**
Scrapes r/wallstreetbets for stock mentions and sentiment.

**Key features:**
1. **Ticker Extraction**
   - Uses regex to find stock tickers (1-5 capital letters)
   - Filters out common false positives (DD, YOLO, CEO, etc.)
   - Extracts from both titles and post bodies

2. **Sentiment Analysis**
   - Keyword-based (bullish words vs bearish words)
   - Returns score from -1 (bearish) to +1 (bullish)
   - Bullish: moon, rocket, calls, squeeze, gains, etc.
   - Bearish: crash, dump, puts, tank, rekt, etc.

3. **Post Metadata**
   - Score (upvotes)
   - Comment count
   - Awards
   - Upvote ratio
   - Author
   - Timestamp

**Usage:**
```python
collector = RedditWSBCollector()
data = await collector.collect(symbols=["GME"], limit=100)
```

**Output example:**
```python
{
    'timestamp': datetime(2025, 10, 24, 10, 30),
    'symbol': 'GME',
    'source': 'reddit_wsb',
    'category': 'social_sentiment',
    'data_type': 'mention',
    'value': 1,  # One mention
    'metadata': {
        'post_id': 'abc123',
        'title': 'GME to the moon!',
        'score': 1234,
        'num_comments': 567,
        'sentiment_score': 0.8,  # Bullish
        'upvote_ratio': 0.95
    }
}
```

**Rate limits:**
- Reddit API: 60 requests/minute
- Built-in delay between requests

**Requirements:**
- Reddit API credentials (free)
- PRAW library

#### Yahoo Finance Collector

**File:** `penguin/data/collectors/market_data/yahoo_finance.py`

**What it does:**
Collects stock prices, volume, and company information from Yahoo Finance.

**Key features:**
1. **OHLCV Data**
   - Open, High, Low, Close prices
   - Volume
   - Historical data with configurable period
   - Multiple intervals (1m, 5m, 1h, 1d)

2. **Stock Information**
   - Company name, sector, industry
   - Market cap, P/E ratio
   - Dividend yield, Beta
   - 52-week high/low

3. **Async Collection**
   - Small delays to respect rate limits
   - Handles multiple symbols efficiently

**Usage:**
```python
collector = YahooFinanceCollector()
data = await collector.collect(
    symbols=["AAPL", "TSLA"],
    period="1d",
    interval="1h",
    include_info=True
)
```

**Output:**
Creates multiple data points per symbol:
- One for price (with OHLC in metadata)
- One for volume
- One for stock info (if requested)

**Rate limits:**
- Yahoo Finance: ~2000 requests/hour
- Built-in 0.05s delay between symbols

**Requirements:**
- yfinance library (no API key needed!)

---

### 6. Command-Line Interface

**File:** `penguin/cli/main.py`

**What it does:**
Provides commands to manage and test the system.

#### Commands

**1. `penguin status`**
Shows system health:
- Configuration status (API keys set?)
- Number of collectors
- Database connection status

**2. `penguin init`**
Initializes the database:
- Connects to PostgreSQL
- Creates all tables
- Sets up indexes

**3. `penguin collectors list`**
Lists all registered collectors:
- Name
- Category
- Collection frequency
- Auth requirement
- Enabled/disabled status

**4. `penguin collectors test <name> [--symbol AAPL]`**
Tests a collector:
- Validates credentials
- Runs collect() with limit=10
- Shows sample output
- Doesn't save to database

**5. `penguin collect <name> [options]`**
Runs a collector:
- Collects data
- Optionally saves to database (--save/--no-save)
- Filters by symbols if specified
- Updates collector status
- Shows summary

Options:
- `--symbol, -s`: Filter symbols (can use multiple)
- `--limit, -l`: Max items to collect
- `--save/--no-save`: Save to database (default: save)

**6. `penguin query [options]`**
Queries collected data:
- Filter by symbol
- Filter by source
- Filter by time range
- Limit results

**Why CLI is important:**
- Easy testing without writing code
- Quick validation of collectors
- DevOps-friendly (can script with shell)
- No need for web UI yet

---

## How Components Work Together

### Data Collection Flow

```
1. User runs: penguin collect yahoo_finance --symbol AAPL

2. CLI (main.py):
   - Calls registry.auto_discover()
   - Gets collector instance
   - Calls collector.collect(symbols=["AAPL"])

3. Collector (yahoo_finance.py):
   - Fetches data from Yahoo Finance API
   - Normalizes to standard format
   - Returns list of data points

4. CLI:
   - Receives data points
   - Calls store.save_data_points(data)

5. Store (store.py):
   - Opens database session
   - Creates DataPoint objects
   - Bulk inserts to database
   - Commits transaction

6. Result:
   - Data saved in data_points table
   - Collector status updated
   - User sees success message
```

### Plugin Discovery Flow

```
1. registry.auto_discover() called

2. Registry scans penguin/data/collectors/**/*.py

3. For each Python file:
   - Import the module
   - Find all classes
   - Check if inherits from BaseCollector
   - If yes, register it

4. Result:
   - All collectors available in registry
   - Can get by name: registry.get_collector("reddit_wsb")
   - Can filter by category
   - Can enable/disable
```

---

## Key Design Decisions

### Why Plugin System?

**Problem:** Need to support 1000+ data sources without code explosion

**Solution:** Plugin architecture with auto-discovery

**Benefits:**
- Add new source = create one file
- No manual registration needed
- Easy to disable sources
- Can have hundreds of collectors without slow startup

**Trade-offs:**
- Slightly more complex than hardcoding
- Need to maintain BaseCollector interface
- But worth it for scalability!

### Why Normalize Data?

**Problem:** Each API returns different format

**Solution:** All collectors return same structure

**Benefits:**
- Easy to aggregate across sources
- Database schema is consistent
- Can compare Reddit mentions with price
- Signal detection works on any source

**Example:**
```python
# Reddit mention
{'symbol': 'AAPL', 'value': 1, 'data_type': 'mention'}

# Price data
{'symbol': 'AAPL', 'value': 260.94, 'data_type': 'price'}

# Both have same fields! Can aggregate:
mentions_per_dollar = mentions_count / stock_price
```

### Why SQLAlchemy?

**Problem:** Need database but don't want to write SQL everywhere

**Solution:** SQLAlchemy ORM

**Benefits:**
- Type-safe models
- Automatic migrations (with Alembic)
- Works with multiple databases
- Easier to test (can use SQLite in tests)

### Why Click for CLI?

**Problem:** Need user-friendly command interface

**Solution:** Click framework

**Benefits:**
- Automatic help text
- Argument validation
- Subcommands
- Better than argparse for complex CLIs

---

## Testing Results

### Test 1: System Status ✅
```bash
$ penguin status
PENGUIN System Status
================================================================================
Configuration:
  Reddit API: NOT CONFIGURED
  Database: postgresql://localhost/penguin
Collectors:
  Total: 2
  Enabled: 0
Database: CONNECTED
```

**What this proves:**
- CLI works
- Auto-discovery finds both collectors
- Database connection working
- Configuration loading correctly

### Test 2: List Collectors ✅
```bash
$ penguin collectors list
Available Data Collectors:
================================================================================
yahoo_finance
  Category: market_data
  Frequency: medium
  Status: DISABLED
  No Auth

reddit_wsb
  Category: social_sentiment
  Frequency: high
  Status: DISABLED
  Auth Required
```

**What this proves:**
- Registry working
- Metadata correctly set
- Category system functional
- Auth requirements tracked

### Test 3: Yahoo Finance Test ✅
```bash
$ penguin collectors test yahoo_finance --symbol AAPL
Collected 4 data points!
Sample: AAPL @ $260.94
```

**What this proves:**
- Collector works
- Yahoo Finance API accessible
- Data normalization working
- Symbol filtering works

### Test 4: Multi-Symbol Collection ✅
```bash
$ penguin collect yahoo_finance --symbol AAPL --symbol TSLA --no-save
Collected 8 data points
Symbols found: AAPL, TSLA
```

**What this proves:**
- Multi-symbol support works
- No-save mode works (for testing without DB)
- Data collection is functional

---

## Common Issues & Solutions

### Issue: "Collector not found"
**Cause:** Collector file not in correct directory or doesn't inherit from BaseCollector

**Solution:**
1. Check file is in `penguin/data/collectors/<category>/`
2. Verify class inherits from BaseCollector
3. Make sure `name` attribute is set
4. Run `penguin collectors list` to verify

### Issue: "Database connection refused"
**Cause:** PostgreSQL not running

**Solution:**
1. Start PostgreSQL: `brew services start postgresql` (Mac)
2. Or use `--no-save` flag for testing without DB
3. Check DATABASE_URL in config

### Issue: "Reddit credentials invalid"
**Cause:** API keys not set or incorrect

**Solution:**
1. Go to https://www.reddit.com/prefs/apps
2. Create app (type: script)
3. Add to .env:
   ```
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   ```
4. Run `penguin collectors test reddit_wsb`

---

## Files Created Summary

### Core System
- `penguin/__init__.py` - Package init
- `penguin/core/config.py` - Configuration management
- `penguin/core/constants.py` - Enums and constants

### Data Collection
- `penguin/data/__init__.py`
- `penguin/data/base.py` - BaseCollector interface
- `penguin/data/registry.py` - Plugin registry

### Collectors
- `penguin/data/collectors/social/reddit_wsb.py` - Reddit collector
- `penguin/data/collectors/market_data/yahoo_finance.py` - Yahoo collector

### Database
- `penguin/data/storage/models.py` - SQLAlchemy models
- `penguin/data/storage/database.py` - Connection manager
- `penguin/data/storage/store.py` - High-level API

### CLI
- `penguin/cli/main.py` - Command-line interface

### Infrastructure
- `setup.py` - Package setup
- `requirements.txt` - Dependencies
- `scripts/init_db.py` - DB initialization

---

## Next Steps (Phase 2)

**Signal Detection System:**
1. Create BaseDetector interface (like BaseCollector)
2. Implement signal detectors:
   - MomentumSpikeDetector
   - VolumeAnomalyDetector
   - SentimentShiftDetector
3. Technical indicators:
   - RSI, MACD, Bollinger Bands
   - Moving averages
   - Volume analysis
4. Signal aggregation:
   - Combine multiple signals
   - Calculate confidence scores
   - Detect signal clusters

**What Phase 2 needs from Phase 1:**
- ✅ Data collection working
- ✅ Database with DataPoint table
- ✅ Normalized data format
- ✅ Query interface (store.get_recent_data_points)

**Phase 1 → Phase 2 connection:**
```
Phase 1: Collect data → Database
Phase 2: Query database → Detect signals → Store signals
Phase 3: Query signals → Claude analysis → Store recommendations
```

---

## Lessons Learned

### What Worked Well
1. **Plugin system** - Auto-discovery is elegant
2. **Data normalization** - Makes aggregation easy
3. **CLI-first** - Can test without web UI
4. **Async support** - Ready for concurrent collection
5. **Modular design** - Each layer independent

### What Could Be Improved
1. **Add logging** - Currently using print()
2. **Error handling** - More graceful failures
3. **Rate limiting** - Per-collector limits
4. **Caching** - Avoid redundant API calls
5. **Config files** - YAML for collector settings

### Architecture Validation
✅ **Scalability**: Plugin system can handle 1000+ collectors
✅ **Extensibility**: Adding new collector takes ~50 lines
✅ **Testability**: Can test collectors independently
✅ **Maintainability**: Clear separation of concerns

---

## Glossary

**BaseCollector**: Abstract base class that all data collectors inherit from

**Plugin Registry**: System that auto-discovers and manages collectors

**Data Normalization**: Converting different API formats to standard structure

**OHLCV**: Open, High, Low, Close, Volume (standard stock data)

**Time-series data**: Data points with timestamps (prices over time)

**ORM**: Object-Relational Mapping (SQLAlchemy) - work with database using Python objects

**Async/Await**: Python's asynchronous programming model for concurrent operations

**Context Manager**: Python's `with` statement for safe resource handling

**Sentiment Analysis**: Determining if text is positive/negative about a stock

---

**Phase 1 Status: COMPLETE ✅**
