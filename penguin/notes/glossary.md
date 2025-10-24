# PENGUIN Glossary

A comprehensive guide to terms, concepts, and technical indicators used in PENGUIN.

---

## Architecture Terms

### BaseCollector
An abstract base class that defines the interface for all data collectors. Every data source (Reddit, Yahoo Finance, etc.) inherits from this.

**Why it exists:** Ensures all collectors have the same methods and can be used interchangeably.

### Plugin Registry
A system that automatically discovers and manages data collectors. Scans directories for classes that inherit from BaseCollector.

**How it works:** Import reflection - looks at Python files, finds classes, checks inheritance.

### Data Normalization
Converting different API response formats into a single, consistent structure.

**Example:** Reddit returns JSON with 'created_utc', Yahoo returns DataFrame with 'Date' - both become 'timestamp' in our format.

### ORM (Object-Relational Mapping)
SQLAlchemy feature that lets you work with database tables as Python classes.

**Example:** Instead of `SELECT * FROM stocks WHERE symbol='AAPL'`, you write `session.query(Stock).filter_by(symbol='AAPL')`.

---

## Stock Market Terms

### Ticker Symbol
A short code identifying a stock (e.g., AAPL = Apple, TSLA = Tesla, GME = GameStop).

### OHLCV
Standard stock price data format:
- **O**pen: Price at market open
- **H**igh: Highest price during period
- **L**ow: Lowest price during period
- **C**lose: Price at market close
- **V**olume: Number of shares traded

### Market Cap (Market Capitalization)
Total value of all company shares = Share Price × Number of Shares Outstanding

**Size categories:**
- Large cap: > $10 billion
- Mid cap: $2-10 billion
- Small cap: $300M - $2 billion
- Micro cap: < $300M

### Volume
Number of shares traded during a time period. High volume = high interest/liquidity.

### Volatility
How much a stock's price fluctuates. High volatility = bigger price swings.

### Bull vs Bear
- **Bullish**: Expecting price to go up
- **Bearish**: Expecting price to go down

---

## Technical Analysis Terms

### Moving Average (MA)
Average price over N periods. Smooths out price data to identify trends.

**Types:**
- **SMA** (Simple): Straight average
- **EMA** (Exponential): Recent prices weighted more
- **WMA** (Weighted): Custom weights

**Common periods:** 20-day, 50-day, 200-day

**What it tells you:**
- Price above MA = potential uptrend
- Price below MA = potential downtrend
- MA crossovers = trend changes

### RSI (Relative Strength Index)
Momentum indicator measuring speed and magnitude of price changes. Scale: 0-100.

**Interpretation:**
- RSI > 70: **Overbought** (might drop soon)
- RSI < 30: **Oversold** (might rise soon)
- RSI 40-60: Neutral

**Formula:** RSI = 100 - (100 / (1 + RS))
Where RS = Average Gain / Average Loss over N periods (typically 14)

### MACD (Moving Average Convergence Divergence)
Trend-following momentum indicator showing relationship between two EMAs.

**Components:**
- **MACD Line**: 12-day EMA - 26-day EMA
- **Signal Line**: 9-day EMA of MACD line
- **Histogram**: MACD Line - Signal Line

**Signals:**
- MACD crosses above signal = Bullish
- MACD crosses below signal = Bearish
- Histogram expanding = Strong trend
- Histogram contracting = Weakening trend

### Bollinger Bands
Volatility indicator with three lines:
- **Middle**: 20-day SMA
- **Upper**: Middle + (2 × standard deviation)
- **Lower**: Middle - (2 × standard deviation)

**What it tells you:**
- Price near upper band = Potentially overbought
- Price near lower band = Potentially oversold
- Bands squeeze = Low volatility (breakout coming)
- Bands widen = High volatility

### Stochastic Oscillator
Momentum indicator comparing closing price to price range over time. Scale: 0-100.

**Components:**
- %K line: (Current Close - Lowest Low) / (Highest High - Lowest Low) × 100
- %D line: 3-period SMA of %K

**Interpretation:**
- > 80: Overbought
- < 20: Oversold
- %K crosses above %D = Buy signal
- %K crosses below %D = Sell signal

### ADX (Average Directional Index)
Measures trend strength (not direction). Scale: 0-100.

**Interpretation:**
- ADX > 25: Strong trend
- ADX < 20: Weak/no trend
- ADX > 50: Very strong trend

**Components:**
- +DI: Positive directional indicator
- -DI: Negative directional indicator
- +DI > -DI = Uptrend
- -DI > +DI = Downtrend

### ATR (Average True Range)
Volatility indicator measuring average range between high and low prices.

**What it tells you:**
- High ATR = High volatility
- Low ATR = Low volatility
- Used for setting stop-loss levels

**Formula:** Average of True Range over N periods (typically 14)
Where True Range = Max of:
- Current High - Current Low
- |Current High - Previous Close|
- |Current Low - Previous Close|

### OBV (On-Balance Volume)
Cumulative volume indicator predicting price changes based on volume flow.

**How it works:**
- If close > previous close: Add volume to OBV
- If close < previous close: Subtract volume from OBV
- If close = previous close: No change

**What it tells you:**
- OBV rising + price rising = Strong uptrend
- OBV falling + price falling = Strong downtrend
- OBV diverging from price = Potential reversal

### VWAP (Volume Weighted Average Price)
Average price weighted by volume. Traders use it as trading benchmark.

**Formula:** VWAP = Σ(Price × Volume) / Σ(Volume)

**What it tells you:**
- Price above VWAP = Bullish
- Price below VWAP = Bearish
- Often used for intraday trading

---

## Valuation Ratios

### P/E Ratio (Price-to-Earnings)
Stock price / Earnings per share

**Interpretation:**
- High P/E: Expensive or high growth expectations
- Low P/E: Cheap or low growth expectations
- Compare to industry average

### PEG Ratio (Price/Earnings to Growth)
P/E Ratio / Earnings Growth Rate

**Interpretation:**
- PEG < 1: Potentially undervalued
- PEG > 1: Potentially overvalued
- PEG = 1: Fairly valued

### P/B Ratio (Price-to-Book)
Stock price / Book value per share

**What it tells you:**
- P/B < 1: Trading below book value (value play)
- P/B > 1: Trading above book value
- Good for asset-heavy companies

### Dividend Yield
Annual dividend / Stock price × 100%

**Example:** Stock at $100 pays $3/year dividend = 3% yield

---

## Pattern Recognition

### Head and Shoulders
Reversal pattern with three peaks (middle highest).

**Structure:**
1. Left shoulder
2. Head (highest peak)
3. Right shoulder
4. Neckline (support/resistance)

**Signal:** Break below neckline = Bearish reversal

### Cup and Handle
Bullish continuation pattern.

**Structure:**
- Cup: U-shaped decline and recovery
- Handle: Small downward drift
- Breakout: Price breaks above handle

### Double Top/Bottom
Reversal patterns.

**Double Top:** Two peaks at similar level = Bearish reversal
**Double Bottom:** Two troughs at similar level = Bullish reversal

### Triangle Patterns
Consolidation patterns indicating potential breakout.

**Types:**
- **Ascending**: Higher lows + flat highs = Bullish
- **Descending**: Flat lows + lower highs = Bearish
- **Symmetrical**: Lower highs + higher lows = Breakout either way

---

## Sentiment Analysis

### Bullish Keywords
Words indicating positive sentiment:
- moon, rocket, buy, calls, pump
- rally, squeeze, gains, long
- breakout, opportunity, bullish

### Bearish Keywords
Words indicating negative sentiment:
- crash, dump, puts, short
- fall, drop, tank, bearish
- overvalued, rug pull, dead cat

### Sentiment Score
Numerical representation of sentiment (-1 to +1):
- +1: Very bullish
- 0: Neutral
- -1: Very bearish

**Calculation:** (Bullish words - Bearish words) / Total sentiment words

---

## Reddit/WSB Specific

### WSB (r/wallstreetbets)
Popular subreddit for retail investors, known for meme stocks and high-risk plays.

### DD (Due Diligence)
Research/analysis post explaining investment thesis.

### YOLO
"You Only Live Once" - risky all-in trade.

### Tendies
Slang for profits/gains (from chicken tenders).

### Diamond Hands 💎🙌
Holding position despite volatility.

### Paper Hands 📄🙌
Selling too early (weak hands).

### Apes Together Strong 🦍
Community solidarity mantra.

### Short Squeeze
When heavily shorted stock rises, forcing shorts to cover, pushing price higher.

### Gamma Squeeze
When market makers buy stock to hedge options, pushing price up, triggering more buying.

---

## Database Terms

### Time-Series Data
Data points indexed by time (e.g., stock prices over days/hours).

### Hypertable (TimescaleDB)
PostgreSQL table optimized for time-series queries with automatic partitioning.

### Index
Database structure that speeds up queries at cost of slower writes.

**Types we use:**
- Single column: `(symbol)`, `(timestamp)`
- Composite: `(symbol, timestamp)` for queries like "AAPL prices last 24h"

### JSONB (PostgreSQL)
Binary JSON storage format - faster than regular JSON.

**Where we use it:** `extra_data` field in DataPoint (flexible metadata).

---

## Statistical Terms

### Standard Deviation (σ)
Measure of data spread/volatility. Higher = more volatile.

**Used in:** Bollinger Bands, Z-score calculations

### Correlation
Statistical relationship between two variables (-1 to +1).
- +1: Perfect positive correlation
- 0: No correlation
- -1: Perfect negative correlation

**Example:** BTC price and COIN stock are often correlated.

### Mean Reversion
Theory that prices tend to return to their average over time.

**Trading strategy:** Buy when below average, sell when above average.

### Percentile
Position relative to all values. 95th percentile = higher than 95% of values.

**Example:** Volume in 95th percentile = unusually high volume day.

---

## Signal Detection Terms

### Signal
An event or condition that suggests a trading opportunity.

**Examples:**
- Momentum spike: 300% increase in Reddit mentions
- Volume anomaly: 5x average volume
- RSI oversold: RSI < 30

### Signal Strength
Numerical measure (0-1) indicating confidence in signal.
- 0-0.3: Weak
- 0.3-0.7: Medium
- 0.7-1.0: Strong

### Signal Aggregation
Combining multiple signals to make better decisions.

**Example:**
- Reddit mentions spiking (0.8)
- Volume 3x average (0.6)
- RSI oversold (0.7)
- → Aggregated confidence: 0.7 (strong buy signal)

---

## API Terms

### Rate Limit
Maximum number of API requests allowed per time period.

**Examples:**
- Reddit: 60 requests/minute
- Yahoo Finance: ~2000 requests/hour

### Authentication
Proving your identity to an API (API keys, OAuth tokens).

### Webhook
Automatic HTTP callback when event occurs (push instead of pull).

---

## Python Terms

### Async/Await
Python's asynchronous programming model.

**Why use it:** Can wait for API responses without blocking (collect from multiple sources simultaneously).

### Context Manager
Python's `with` statement for resource management.

**Example:**
```python
with db.get_session() as session:
    # session automatically closed
```

### Decorator
Function that wraps another function to add behavior.

**Example:** `@abstractmethod` marks methods that must be implemented by subclasses.

---

## Phase 2 Terms (Coming Soon)

### Momentum
Rate of price change acceleration.

### Breakout
Price moving above resistance or below support level.

### Support/Resistance
Price levels where stock tends to stop falling/rising.

### Backtesting
Testing trading strategy on historical data.

### Sharpe Ratio
Risk-adjusted return metric. Higher = better risk/reward.

---

**This glossary will be updated as new concepts are introduced in each phase.**
