# Where Is The Code? - Project Structure Guide

**Last Updated**: 2025-01-24

Quick reference for finding code in the PENGUIN project.

---

## 🔐 SECURITY FIRST: API Keys & Secrets

### ✅ The Right Way (What You Should Do)

**`.env`** file (root directory) - **ALL SECRETS GO HERE**
```env
# All API keys go in this file:
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
POLYGON_API_KEY=your_key_here
```

**Protected by `.gitignore`** ✅ - Never goes to GitHub!

### How It Works

**`penguin/core/config.py`** - Loads secrets from `.env`
```python
class Config:
    # Reads from .env, defaults to empty string
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', '')
```

### ❌ NEVER Do This!

```python
# DON'T hardcode secrets in config.py:
REDDIT_CLIENT_ID = 'AQjWXzzjFYtkMIRySAlwAA'  # ❌ EXPOSED ON GITHUB!

# DO use os.getenv with empty default:
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')  # ✅ SAFE!
```

**Why?** When you push to GitHub (even if you need it public for Reddit API), your `.gitignore` protects `.env` but NOT hardcoded values in `.py` files!

---

## 📊 Technical Indicators (98 Indicators)

### Main Implementation
**File:** `penguin/data/collectors/market_data/technical_analysis.py`
- **Lines:** ~600 lines of code
- **What it does:** Calculates all 98 technical indicators
- **Functions:**
  - `calculate_all_indicators()` - Main function (line 15)
  - `_calculate_moving_averages()` - SMA, EMA (line 57)
  - `_calculate_macd()` - MACD indicator (line 78)
  - `_calculate_rsi()` - RSI indicator (line 99)
  - `_calculate_bollinger_bands()` - Bollinger Bands (line 206)
  - ... 15+ more functions

### Integration into Yahoo Finance
**File:** `penguin/data/collectors/market_data/yahoo_finance.py`
- **Import:** Line 13 - `from penguin.data.collectors.market_data.technical_analysis import TechnicalAnalysis`
- **Usage:** Lines 123-148 - Calculates indicators and creates data point

**Key section (lines 123-148):**
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
                **indicators,  # <-- All 98 indicators here!
                'current_price': float(hist['Close'].iloc[-1]),
            }
        }
        data_points.append(tech_point)
```

---

## 🔧 Configuration Files

### Reddit API Keys
**File:** `.env` (root directory)
```bash
REDDIT_CLIENT_ID=AQjWXzzjFYtkMIRySAlwAA
REDDIT_CLIENT_SECRET=rBvAyEoztW1jB1FHEo3XfN_PvHQZxQ
```

**Loaded by:** `penguin/core/config.py` (lines 18-21)
```python
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
```

### Excluded Words (200+ words)
**File:** `penguin/core/constants.py` (lines 49-96)
```python
EXCLUDED_WORDS = {
    'A', 'I', 'B', 'C', ...
    # 200+ words
}
```

**Used by:** `penguin/data/collectors/social/reddit_wsb.py` (line 3 import, line 55 usage)
```python
from penguin.core.constants import EXCLUDED_WORDS

tickers = [
    ticker for ticker in potential_tickers
    if ticker not in EXCLUDED_WORDS
]
```

---

## ⏱️ Rate Limits & Delays

### Reddit Rate Limit
**File:** `penguin/data/collectors/social/reddit_wsb.py`
- **Defined:** Line 23
  ```python
  rate_limit = 60  # Reddit API: 60 requests per minute
  ```
- **Handled by:** PRAW library (automatic, no manual code needed)

### Yahoo Finance Rate Limit
**File:** `penguin/data/collectors/market_data/yahoo_finance.py`
- **Defined:** Line 22
  ```python
  rate_limit = 2000  # YFinance: ~2000 requests/hour
  ```
- **Manual delay:** Line 55
  ```python
  await asyncio.sleep(0.05)  # 50ms delay between symbols
  ```

---

## 🎯 How to Run & View Data

### Method 1: Simple Test (CLI)
```bash
penguin collectors test yahoo_finance --symbol AAPL
```
**Output:** "Collected 133 data points" (but doesn't show details)

### Method 2: View All Indicators (Python Script)
**File:** `view_indicators.py` (I just created this for you!)

**Run it:**
```bash
python view_indicators.py
```

**Output:** Shows all 98 indicators with values organized by category

### Method 3: Python Interactive
```bash
python
```
```python
import asyncio
from penguin.data.registry import registry

registry.auto_discover()
collector = registry.get_collector('yahoo_finance')
data = asyncio.run(collector.collect(symbols=['AAPL']))

# Get technical analysis data point
tech_data = [d for d in data if d['data_type'] == 'technical_analysis'][0]
print(tech_data['metadata'])  # All 98 indicators
```

---

## 📁 Complete File Structure

```
PENGUIN/
│
├── .env                                    # 🔐 ALL SECRETS GO HERE (not committed)
├── .env.example                            # Template (safe to commit)
├── .gitignore                              # Protects .env from GitHub
├── requirements.txt                        # Python dependencies
├── setup.py                                # Package installation
│
├── QUICK_REFERENCE.md                      # 🚀 Quick commands reference
├── WHERE_IS_THE_CODE.md                   # 📍 This file!
├── CLAUDE.md                               # Full project docs
│
├── view_indicators.py                      # Script to view all indicators
│
├── penguin/                                # 🐧 Main Python package
│   │
│   ├── core/
│   │   ├── config.py                      # 🔑 Loads .env secrets into Python
│   │   ├── constants.py                   # EXCLUDED_WORDS (200+)
│   │   ├── logging.py                     # Logging setup
│   │   └── exceptions.py                  # Custom exceptions
│   │
│   ├── data/
│   │   ├── base.py                        # BaseCollector interface
│   │   ├── registry.py                    # Plugin registry
│   │   │
│   │   └── collectors/                    # 🔌 Data source plugins
│   │       ├── social/
│   │       │   └── reddit_wsb.py         # Reddit collector
│   │       │       • Line 3: Import EXCLUDED_WORDS
│   │       │       • Line 23: rate_limit = 60
│   │       │       • Line 55: Uses EXCLUDED_WORDS
│   │       │
│   │       ├── market_data/
│   │       │   ├── yahoo_finance.py       # Yahoo Finance collector
│   │       │   │   • Line 13: Import TechnicalAnalysis
│   │       │   │   • Line 22: rate_limit = 2000
│   │       │   │   • Line 55: asyncio.sleep(0.05)
│   │       │   │   • Lines 123-148: Calculate indicators
│   │       │   │
│   │       │   └── technical_analysis.py  # 98 INDICATORS HERE!
│   │       │       • ~600 lines of code
│   │       │       • calculate_all_indicators()
│   │       │
│   │       └── options/
│   │           └── polygon_options.py     # Polygon.io options
│   │
│   ├── cli/                                # 💻 Python CLI code
│   │   ├── main.py                        # Main CLI entry point
│   │   └── commands/                      # Command implementations
│   │
│   └── indicators/                         # Technical indicators
│
├── scripts/                                # 🛠️ Utility scripts
│   └── cli/                                # 📜 Shell script shortcuts
│       ├── README.md                      # Shell scripts guide
│       ├── setup_env.sh                   # Setup environment
│       ├── list_collectors.sh             # List collectors
│       ├── test_collectors.sh             # Test all collectors
│       ├── collect_data.sh                # Collect data
│       └── view_indicators.sh             # View indicators
│
└── tests/                                  # 🧪 Test files
```

---

## 🤔 CLI Organization: Why Two Directories?

### `penguin/cli/` - Python Package (The Real Code)
- **Contains**: Actual CLI implementation in Python
- **Purpose**: Importable Python code with logic
- **Used by**: `python -m penguin.cli.main collectors test reddit_wsb`
- **Example**: `penguin/cli/main.py` has argparse, command routing, etc.

### `scripts/cli/` - Shell Scripts (Convenience Shortcuts)
- **Contains**: Shell scripts (.sh files)
- **Purpose**: Quick shortcuts for common commands
- **Used by**: `./scripts/cli/test_collectors.sh`
- **Example**: Runs multiple Python commands at once

### Both Are Valid! Use Whichever You Prefer

**Full Python command** (more control):
```bash
python -m penguin.cli.main collectors test polygon_options --symbol GME
```

**Shell script shortcut** (easier):
```bash
./scripts/cli/test_collectors.sh  # Tests all collectors at once
```

**No duplication** - Shell scripts just call the Python CLI!

---

## 🔍 What Each File Does

### `technical_analysis.py` (The Heart of the Indicators)
**Location:** `penguin/data/collectors/market_data/technical_analysis.py`

**Structure:**
```python
class TechnicalAnalysis:
    @staticmethod
    def calculate_all_indicators(df):
        """Main entry point - calculates all 98 indicators"""
        indicators = {}

        # Call each category
        indicators.update(_calculate_moving_averages(df))
        indicators.update(_calculate_macd(df))
        indicators.update(_calculate_rsi(df))
        # ... 15+ more functions

        return indicators  # Returns dict with 98 indicators

    @staticmethod
    def _calculate_moving_averages(df):
        """Calculate SMA, EMA, etc."""
        return {
            'sma_5': ...,
            'sma_10': ...,
            'ema_9': ...,
            # etc.
        }

    # ... 15+ more functions for each category
```

### `yahoo_finance.py` (The Collector)
**Location:** `penguin/data/collectors/market_data/yahoo_finance.py`

**What it does:**
1. **Fetches data** from Yahoo Finance (OHLCV)
2. **Calls** `TechnicalAnalysis.calculate_all_indicators()`
3. **Creates data point** with all indicators in metadata
4. **Returns** list of data points

**Key flow:**
```python
async def collect(self, symbols, **kwargs):
    for symbol in symbols:
        # Fetch OHLCV data
        hist = ticker.history(period='3mo', interval='1d')

        # Calculate indicators
        if include_technicals:
            indicators = TechnicalAnalysis.calculate_all_indicators(hist)

            # Create data point
            tech_point = {
                'data_type': 'technical_analysis',
                'value': current_price,
                'metadata': indicators  # <-- All 98 here!
            }

        return data_points
```

---

## 🎓 How to Modify

### Add More Excluded Words
1. Open: `penguin/core/constants.py`
2. Find: `EXCLUDED_WORDS = {`
3. Add: Your words to the set
4. Save
5. Done! Reddit collector automatically uses it

### Change Yahoo Delay
1. Open: `penguin/data/collectors/market_data/yahoo_finance.py`
2. Find: Line 55 - `await asyncio.sleep(0.05)`
3. Change: `0.05` to your desired seconds
4. Save
5. Done!

### Add New Technical Indicator
1. Open: `penguin/data/collectors/market_data/technical_analysis.py`
2. Add new function:
   ```python
   @staticmethod
   def _calculate_my_indicator(df):
       # Your calculation here
       return {'my_indicator': value}
   ```
3. Call it in `calculate_all_indicators()`:
   ```python
   indicators.update(_calculate_my_indicator(df))
   ```
4. Save
5. Done! Now you have 99 indicators!

---

## 📊 The Data Flow

```
User runs: penguin collectors test yahoo_finance --symbol AAPL
    ↓
CLI (penguin/cli/main.py)
    ↓
Registry discovers collectors (penguin/data/registry.py)
    ↓
Gets YahooFinanceCollector (penguin/data/collectors/market_data/yahoo_finance.py)
    ↓
Calls collector.collect(['AAPL'])
    ↓
Fetches OHLCV from Yahoo Finance API
    ↓
Calls TechnicalAnalysis.calculate_all_indicators(hist)
    ↓
TechnicalAnalysis module (technical_analysis.py) calculates 98 indicators
    ↓
Returns dict with all indicators
    ↓
YahooFinanceCollector creates data point with indicators in metadata
    ↓
Returns 133 data points total:
    • 66 price points (OHLCV for each time period)
    • 66 volume points
    • 1 technical analysis point (with all 98 indicators)
    ↓
CLI prints: "Collected 133 data points!"
```

To **see** the indicators, use: `python view_indicators.py`

---

## 🚀 Quick Commands Reference

```bash
# View all 98 indicators with values
python view_indicators.py

# Test collector (shows count only)
penguin collectors test yahoo_finance --symbol AAPL

# Test with multiple symbols
penguin collectors test yahoo_finance --symbol AAPL --symbol TSLA

# Collect without saving to database
penguin collect yahoo_finance --symbol AAPL --no-save

# Check system status
penguin status

# List all collectors
penguin collectors list
```

---

## 📖 Documentation Files

1. **QUICK_REFERENCE.md** - Answers to your questions with exact locations
2. **WHERE_IS_THE_CODE.md** - This file - detailed file locations
3. **penguin/notes/phase1_foundation.md** - Complete Phase 1 guide
4. **penguin/notes/phase2_prep.md** - Technical indicators explained
5. **penguin/notes/glossary.md** - All terms and concepts

---

## 🎯 Summary

**The code you're looking for is in 2 main files:**

1. **`penguin/data/collectors/market_data/technical_analysis.py`**
   - 600 lines
   - All 98 indicator calculations
   - Main function: `calculate_all_indicators()`

2. **`penguin/data/collectors/market_data/yahoo_finance.py`**
   - Fetches data from Yahoo Finance
   - Calls technical_analysis module
   - Returns data points with indicators

**To view the data:**
```bash
python view_indicators.py
```

**That's it!** All 98 indicators calculated and displayed.
