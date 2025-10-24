# QuiverQuant API Setup & Usage Guide

**Created**: 2025-01-24
**Updated**: 2025-10-24
**Status**: ✅ Fully Implemented (Tier 1 - $10/month)

---

## Overview

QuiverQuant provides comprehensive financial data through their API with Tier 1 subscription ($10/month). We've implemented collectors for ALL Tier 1 endpoints:

1. **Congressional Trading** - Bulk, live (house, senate, all), and historical trades
2. **Insider Trading** - SEC Form 4 transactions
3. **Government Contracts** - Live and historical federal contract awards
4. **Lobbying** - Live and historical lobbying data
5. **Social/Reddit** - WSB, Reddit, crypto, SPAC mentions
6. **Dark Pool** - Off-exchange trading data
7. **Other Data** - CNBC trades, corporate flights, legislation, bill summaries

---

## Tier 1 Access ($10/month)

QuiverQuant offers a Tier 1 subscription with comprehensive API access for $10/month.

### How to Get Your API Key

1. **Visit**: https://www.quiverquant.com/
2. **Sign Up** for an account
3. **Subscribe to Tier 1** ($10/month)
4. **Get API Access**:
   - Navigate to API section in your account
   - Generate your API key
   - Copy the Bearer token

5. **Add to `.env` file**:
   ```env
   QUIVERQUANT_API_KEY=your_api_key_here
   ```

---

## Implemented Collectors

### 1. Congressional Trading Collector

**File**: `penguin/data/collectors/congress/quiverquant_congress.py`

**Endpoint**: `GET /beta/bulk/congresstrading`

**What You Get**:
- ✅ Full history of all Congress transactions
- ✅ House and Senate members
- ✅ Transaction details (Purchase/Sale)
- ✅ Transaction sizes (dollar ranges)
- ✅ Party, district, chamber info
- ✅ **Excess returns vs S&P 500!** 🎯

**Usage**:
```bash
# Test with single symbol
python -m penguin.cli.main collectors test quiverquant_congress --symbol NVDA

# Collect for multiple symbols
python -m penguin.cli.main collectors run quiverquant_congress --symbols NVDA,MSFT,AAPL
```

**Parameters**:
```python
collect(
    symbols=['NVDA'],           # Optional: filter by ticker
    representative='Nancy Pelosi',  # Optional: filter by name
    bioguide_id='P000197',      # Optional: BioGuide ID
    date='20250124',            # Optional: specific date (YYYYMMDD)
    nonstock=False,             # Include non-stock transactions
    normalized=False,           # Normalize names
    page=1,                     # Pagination
    page_size=100,              # Items per page
    lookback_days=30,           # How far back to look
)
```

**Data Returned**:
```python
{
    'symbol': 'NVDA',
    'value': 75000.0,  # trade_size_usd (lower bound)
    'metadata': {
        'politician_name': 'Nancy Pelosi',
        'chamber': 'House',  # or 'Senate'
        'party': 'Democrat',
        'state': 'CA',
        'district': '11',
        'transaction_type': 'Purchase',  # or 'Sale'
        'trade_size_usd': 75000.0,
        'company': 'NVIDIA Corporation',
        'transaction_date': '2025-01-23T00:00:00Z',
        'disclosure_date': '2025-01-24T10:30:00Z',
        'excess_return': '15.2%',  # 🎯 Outperformed S&P by 15.2%!
        'description': 'Common Stock',
        'comments': '',
    }
}
```

---

### 2. Insider Trading Collector

**File**: `penguin/data/collectors/insider/quiverquant_insiders.py`

**Endpoint**: `GET /beta/live/insiders`

**What You Get**:
- ✅ Recent insider transactions (Form 4)
- ✅ Director, officer, 10% owner identification
- ✅ Transaction types decoded (Purchase, Sale, Award, Exercise, etc.)
- ✅ Share counts and prices
- ✅ Direct vs indirect ownership
- ✅ Shares owned after transaction

**Usage**:
```bash
# Test with single symbol
python -m penguin.cli.main collectors test quiverquant_insiders --symbol AAPL

# Collect for multiple symbols
python -m penguin.cli.main collectors run quiverquant_insiders --symbols AAPL,TSLA,MSFT
```

**Parameters**:
```python
collect(
    symbols=['AAPL'],           # Optional: filter by ticker
    date='20250124',            # Optional: filing date (YYYYMMDD)
    uploaded='20250124',        # Optional: upload date (YYYYMMDD)
    limit_codes=False,          # Limit transaction codes
    page=1,                     # Pagination
    page_size=100,              # Items per page
    lookback_days=7,            # How far back to look
    min_shares=1000,            # Minimum shares filter
    min_value=50000,            # Minimum transaction value
    transaction_types=['P', 'S'],  # Filter by code (P=purchase, S=sale)
)
```

**Data Returned**:
```python
{
    'symbol': 'AAPL',
    'value': 9275000.0,  # total_value (shares * price)
    'metadata': {
        'insider_name': 'Timothy D. Cook',
        'insider_title': 'Chief Executive Officer',
        'insider_role': 'Director, Officer',
        'is_director': True,
        'is_officer': True,
        'is_ten_percent_owner': False,
        'transaction_date': '2025-01-23T00:00:00Z',
        'filing_date': '2025-01-24T16:30:00Z',
        'transaction_type': 'Open Market Sale (Disposed)',
        'transaction_code': 'S',  # SEC transaction code
        'acquired_disposed_code': 'D',  # D = disposed
        'shares': 50000,
        'price_per_share': 185.50,
        'total_value': 9275000.0,
        'shares_owned_after': 3200000,
        'ownership_type': 'D',  # D = direct, I = indirect
        'is_direct': True,
    }
}
```

---

### 3. Congressional Trading Live Collector

**File**: `penguin/data/collectors/congress/quiverquant_congress_live.py`

**Endpoints**:
- `GET /beta/live/congresstrading` - All Congress trades
- `GET /beta/live/housetrading` - House trades only
- `GET /beta/live/senatetrading` - Senate trades only
- `GET /beta/historical/congresstrading/{ticker}` - Historical trades for symbol

**What You Get**:
- ✅ Real-time congressional trades (updated frequently)
- ✅ Filter by chamber (House vs Senate)
- ✅ Historical trades for specific stocks
- ✅ Same rich metadata as bulk collector

**Usage**:
```bash
# Test all Congress trades
python -m penguin.cli.main collectors test quiverquant_congress_live --symbol NVDA

# Test with specific endpoint
python -m penguin.cli.main collectors run quiverquant_congress_live --symbols NVDA --endpoint house

# Test historical endpoint
python -m penguin.cli.main collectors run quiverquant_congress_live --symbols AAPL --endpoint historical
```

**Parameters**:
```python
collect(
    symbols=['NVDA'],           # Optional: filter by ticker
    endpoint='all',             # 'all', 'house', 'senate', or 'historical'
    page=1,                     # Pagination
    page_size=100,              # Items per page
    lookback_days=7,            # How far back to look (live endpoints)
)
```

---

### 4. Government Contracts Collector

**File**: `penguin/data/collectors/alternative/quiverquant_contracts.py`

**Endpoints**:
- `GET /beta/live/govcontracts` - Recent government contracts
- `GET /beta/historical/govcontracts/{ticker}` - Historical contracts by company
- `GET /beta/historical/govcontractsall/{ticker}` - All historical contracts

**What You Get**:
- ✅ Federal government contract awards
- ✅ Contract amounts and agencies
- ✅ Award types and descriptions
- ✅ Historical contract data by company

**Usage**:
```bash
# Test live contracts
python -m penguin.cli.main collectors test quiverquant_contracts --symbol AAPL

# Test historical contracts
python -m penguin.cli.main collectors run quiverquant_contracts --symbols BA,LMT --endpoint historical
```

**Parameters**:
```python
collect(
    symbols=['AAPL'],           # For historical endpoints
    endpoint='live',            # 'live', 'historical', or 'all_historical'
    page=1,                     # Pagination
    page_size=100,              # Items per page
    lookback_days=30,           # For live endpoint
    min_amount=0,               # Minimum contract amount filter
)
```

**Data Returned**:
```python
{
    'symbol': 'AAPL',
    'value': 1379815.03,  # contract amount
    'metadata': {
        'company': 'Apple Inc.',
        'contract_date': '2025-10-15T00:00:00Z',
        'amount': 1379815.03,
        'agency': 'Department of Defense',
        'description': 'IT Equipment and Services',
        'award_type': 'Delivery Order',
        'source_endpoint': 'live',
    }
}
```

---

### 5. QuiverQuant All (Comprehensive Collector)

**File**: `penguin/data/collectors/alternative/quiverquant_all.py`

**Endpoints (11 total)**:

**Lobbying**:
- `GET /beta/live/lobbying` - Recent lobbying activity
- `GET /beta/historical/lobbying/{ticker}` - Historical lobbying by company

**Social/Reddit**:
- `GET /beta/live/wsbcomments` - WallStreetBets mentions
- `GET /beta/live/redditcomments` - General Reddit mentions
- `GET /beta/live/cryptocomments` - Crypto-related mentions
- `GET /beta/live/spaccomments` - SPAC-related mentions

**Dark Pool**:
- `GET /beta/live/offexchange` - Off-exchange trading data

**Other**:
- `GET /beta/live/cnbc` - CNBC analyst trades
- `GET /beta/live/flights` - Corporate flight tracking
- `GET /beta/live/legislation` - Legislative activity
- `GET /beta/live/bill_summaries` - Bill summaries

**What You Get**:
- ✅ Unified access to all alternative data endpoints
- ✅ Flexible endpoint selection
- ✅ Comprehensive lobbying, social, and dark pool data
- ✅ Legislative and bill tracking

**Usage**:
```bash
# Test all endpoints (default)
python -m penguin.cli.main collectors test quiverquant_all --symbol GME

# Test specific endpoints only
python -m penguin.cli.main collectors run quiverquant_all --symbols GME,AMC --endpoints wsb,darkpool,lobbying_live
```

**Parameters**:
```python
collect(
    symbols=['GME'],            # Optional: filter by ticker
    endpoints=['wsb', 'darkpool', 'cnbc'],  # List of endpoint keys (default: all)
    page=1,                     # Pagination
    page_size=100,              # Items per page
    lookback_days=7,            # How far back to look
)
```

**Available Endpoint Keys**:
- `lobbying_live`, `lobbying_historical`
- `wsb`, `reddit`, `crypto`, `spac`
- `darkpool`
- `cnbc`, `flights`, `legislation`, `bills`

**Data Returned** (varies by endpoint):
```python
{
    'symbol': 'GME',  # or 'N/A' for non-stock-specific data
    'value': 450.0,   # context-dependent (mentions, volume, amount, etc.)
    'data_type': 'social_sentiment',  # or 'lobbying', 'dark_pool_trading', etc.
    'metadata': {
        'endpoint': 'wsb',
        'raw_data': {...},  # Full response from API
    }
}
```

**Note**: Some social endpoints (wsb, reddit, crypto, spac, cnbc) may return HTTP 403 errors. These might require Tier 2 access or have specific availability restrictions. The collector handles these gracefully and continues with available endpoints.

---

## Transaction Codes Reference

### Insider Trading Codes (SEC Form 4)

| Code | Type | Description |
|------|------|-------------|
| **P** | Purchase | Open market purchase |
| **S** | Sale | Open market sale |
| **M** | Exercise | Exercise of options (in the money) |
| **A** | Award | Grant, award, or other acquisition |
| **D** | Disposition | Disposition to the issuer |
| **F** | Payment | Payment of exercise price or tax liability |
| **I** | Discretionary | Discretionary transaction |
| **C** | Conversion | Conversion of derivative security |
| **G** | Gift | Bona fide gift |

**Full reference**: https://www.sec.gov/files/forms-3-4-5.pdf

---

## Advantages of QuiverQuant

### vs Capitol Trades (our previous implementation)
- ✅ **Real data** (not sample/scraped)
- ✅ **API access** (stable, documented)
- ✅ **Excess returns** included!
- ✅ **Historical data** available
- ✅ **FREE tier** available

### vs SEC-API.io
- ✅ **Simpler API** (cleaner response format)
- ✅ **More features** (excess returns, better filtering)
- ✅ **FREE tier** (SEC-API.io is also free, but this is better)
- ✅ **All in one place** (congress + insiders + more)

---

## Rate Limits & Best Practices

### Tier 1 Limits
- **Rate limit**: Not explicitly stated, but be conservative
- **Recommended**: 1 request per second (60/minute)
- **Current implementation**: 1 second delay between requests ✅
- **Cost**: $10/month for Tier 1 access

### Pagination
- **Default page_size**: 100 items
- **Use pagination** for large datasets:
  ```python
  # Get first 100
  page=1, page_size=100

  # Get next 100
  page=2, page_size=100
  ```

### Filtering Tips

**Congressional Trading:**
- Filter by `representative` for specific politicians
- Filter by `ticker` for specific stocks
- Use `lookback_days` to limit results
- Set `page_size=100` for max efficiency

**Insider Trading:**
- Use `transaction_types` to focus on purchases/sales only
- Set `min_value` to filter significant transactions
- Use `limit_codes=True` to reduce noise
- Set `lookback_days=7` for recent activity

---

## Configuration

### .env File
```env
# QuiverQuant API (Tier 1 - $10/month)
# Sign up at: https://www.quiverquant.com/
QUIVERQUANT_API_KEY=your_api_key_here
```

### config.py
Already configured! ✅
```python
QUIVERQUANT_API_KEY = os.getenv('QUIVERQUANT_API_KEY', '')
```

---

## Testing

### Test Congressional Collector
```bash
python -m penguin.cli.main collectors test quiverquant_congress --symbol NVDA
```

**Expected Output**:
```
Testing collector: quiverquant_congress
Validating credentials...
Credentials valid!
Collecting data...
Collected X data points!

Sample data point:
- Politician: Nancy Pelosi
- Chamber: House
- Transaction: Purchase
- Amount: $50,001 - $100,000
- Excess Return: +15.2% vs S&P 500
```

### Test Insider Collector
```bash
python -m penguin.cli.main collectors test quiverquant_insiders --symbol AAPL
```

**Expected Output**:
```
Testing collector: quiverquant_insiders
Validating credentials...
Credentials valid!
Collecting data...
Collected X data points!

Sample data point:
- Insider: Timothy D. Cook (CEO)
- Transaction: Open Market Sale
- Shares: 50,000 @ $185.50
- Total Value: $9,275,000
- Owned After: 3,200,000 shares
```

---

## Troubleshooting

### 401 Unauthorized
**Problem**: `QuiverQuant authentication failed`

**Solution**:
1. Check your API key in `.env`
2. Verify key is correct (no extra spaces)
3. Make sure `.env` is loading (check `config.py` has `load_dotenv()`)

### 429 Rate Limit
**Problem**: `QuiverQuant rate limit exceeded`

**Solution**:
1. Wait 1 minute
2. Reduce `page_size`
3. Add longer delays between requests
4. Consider upgrading to paid tier for higher limits

### No Data Returned
**Problem**: `Collected 0 data points`

**Solutions**:
1. **Increase `lookback_days`** (try 30 instead of 7)
2. **Remove filters** (min_value, transaction_types)
3. **Try different symbols** (some stocks have more activity)
4. **Check API status** (QuiverQuant might be down)

---

## Next Steps

### Immediate
1. ✅ Get QuiverQuant API key: https://www.quiverquant.com/
2. ✅ Subscribe to Tier 1 ($10/month)
3. ✅ Add to `.env`: `QUIVERQUANT_API_KEY=your_key`
4. ✅ Test all collectors

### Implemented (All Tier 1 Endpoints)

**✅ Congressional Trading:**
- Bulk historical data
- Live feeds (all, house, senate)
- Historical by symbol

**✅ Insider Trading:**
- Form 4 filings with transaction decoding

**✅ Government Contracts:**
- Live contracts
- Historical by company
- All historical contracts

**✅ Lobbying:**
- Live lobbying activity
- Historical by company

**✅ Social/Reddit:**
- WallStreetBets mentions
- General Reddit mentions
- Crypto mentions
- SPAC mentions

**✅ Dark Pool:**
- Off-exchange trading data

**✅ Other Data:**
- CNBC analyst trades
- Corporate flight tracking
- Legislative activity
- Bill summaries

### Future Enhancements (Tier 2 - Not Implemented)

**Requires Tier 2 upgrade:**
- 13F Hedge Fund Filings
- Historical/recent patents
- Political beta calculations
- App ratings
- ETF holdings

---

## Summary

### What We Have Now

| Data Source | Cost | API | Quality | Status |
|-------------|------|-----|---------|--------|
| **QuiverQuant Congress (All)** | $10/mo | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Implemented (4 endpoints) |
| **QuiverQuant Insiders** | $10/mo | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Implemented |
| **QuiverQuant Contracts** | $10/mo | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Implemented (3 endpoints) |
| **QuiverQuant All** | $10/mo | ✅ Yes | ⭐⭐⭐⭐⭐ | ✅ Implemented (11 endpoints) |
| **Yahoo Options** | ✅ Free | ✅ Yes | ⭐⭐⭐⭐ | ✅ Implemented |
| Capitol Trades | ✅ Free | ❌ Scraping | ⭐⭐ | ⚠️ Sample data |
| SEC-API.io | ✅ Free | ✅ Yes | ⭐⭐⭐ | ✅ Implemented |

### Recommendation

**Use QuiverQuant for all alternative data** - comprehensive Tier 1 access for $10/month:
- ✅ Clean, well-documented API
- ✅ 18 total endpoints implemented
- ✅ Excess returns included (congress trades)
- ✅ Better filtering than free sources
- ✅ More reliable than scraping
- ✅ Lobbying, contracts, social, dark pool data

**Keep Yahoo Options** - it's perfect for options chains and completely free!

**Total Monthly Cost**: $10 for QuiverQuant Tier 1 (all implemented collectors)

---

## API Documentation

- **QuiverQuant API Docs**: https://api.quiverquant.com/
- **QuiverQuant Website**: https://www.quiverquant.com/
- **QuiverQuant Python Package**: https://pypi.org/project/quiverquant/

---

---

## Quick Start

```bash
# 1. Add your API key to .env
echo "QUIVERQUANT_API_KEY=91ac18b99a52b23a4645451e6401261e6a5dc769" >> .env

# 2. Test congressional trading
python -m penguin.cli.main collectors test quiverquant_congress_live --symbol NVDA

# 3. Test government contracts
python -m penguin.cli.main collectors test quiverquant_contracts --symbol AAPL

# 4. Test all endpoints
python -m penguin.cli.main collectors test quiverquant_all --symbol GME

# 5. Test insider trading
python -m penguin.cli.main collectors test quiverquant_insiders --symbol TSLA
```

---

**Ready to go! You now have access to 18 QuiverQuant endpoints across 5 collectors!** 🚀
