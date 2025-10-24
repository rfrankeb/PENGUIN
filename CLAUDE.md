# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PENGUIN: Portfolio Evaluation Network with Global Updates, Insights, and Navigation**

PENGUIN is an AI-powered stock analysis and recommendation platform that aggregates data from thousands of sources to identify investment opportunities before they become mainstream. The core premise is to detect emerging trends (like short squeezes, momentum shifts, insider movements) by synthesizing diverse data signals through Claude AI.

### Key Objectives
- Aggregate data from thousands of sources (social media, news, congressional trading, technical metrics, options flow, etc.)
- Detect early momentum signals before they reach mainstream awareness
- Use Claude AI to synthesize multi-source data and generate actionable investment recommendations
- Build a scalable, plugin-based architecture that makes adding new data sources trivial
- Provide real-time alerts and comprehensive analysis

### Long-term Vision
Build toward a robust trading platform (similar to Robinhood), but focus initially on analysis and recommendations. Eventually support paper trading, backtesting, and live trading execution.

---

## Scalable Architecture Design

### Core Principle: Plugin-Based Extensibility

The architecture is designed to support **unlimited data sources** through a standardized plugin system. Each data source implements a common interface, allowing the system to discover, load, and orchestrate sources dynamically.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  (Web Dashboard, Mobile App, CLI, API, Alerts/Notifications) │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  AI Analysis & Recommendation Layer          │
│     (Claude Integration, Signal Synthesis, Confidence        │
│      Scoring, Investment Thesis Generation)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Signal Detection Layer                    │
│   (Momentum Detectors, Anomaly Detection, Pattern           │
│    Recognition, Correlation Analysis)                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Data Processing & Normalization              │
│   (Sentiment Analysis, Time-Series Aggregation,              │
│    Feature Engineering, Data Quality Checks)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Data Ingestion & Orchestration Layer            │
│   (Plugin Manager, Rate Limiter, Scheduler, Cache)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Source Plugins                       │
│  (1000+ individual collectors implementing BaseCollector)    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Storage Layer                           │
│  (TimescaleDB, PostgreSQL, Redis, S3/Object Storage)         │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Source Plugin System

### BaseCollector Interface

Every data source implements this interface:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DataCategory(Enum):
    SOCIAL_SENTIMENT = "social_sentiment"
    NEWS_MEDIA = "news_media"
    MARKET_DATA = "market_data"
    OPTIONS_DERIVATIVES = "options_derivatives"
    INSIDER_TRADING = "insider_trading"
    TECHNICAL_INDICATORS = "technical_indicators"
    FUNDAMENTAL_DATA = "fundamental_data"
    ALTERNATIVE_DATA = "alternative_data"
    MACRO_ECONOMIC = "macro_economic"
    CRYPTO_BLOCKCHAIN = "crypto_blockchain"

class CollectionFrequency(Enum):
    REALTIME = "realtime"        # WebSocket/streaming
    HIGH = "high"                 # Every 1-5 minutes
    MEDIUM = "medium"             # Every 15-60 minutes
    LOW = "low"                   # Every 1-24 hours
    ON_DEMAND = "on_demand"       # Triggered by events

class BaseCollector(ABC):
    """Base class for all data source collectors"""

    # Metadata
    name: str                          # e.g., "Reddit WSB"
    category: DataCategory
    frequency: CollectionFrequency
    requires_auth: bool
    rate_limit: Optional[int]          # requests per minute
    cost_per_request: float            # in USD (0 for free sources)

    @abstractmethod
    async def collect(self, symbols: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        Collect data for given stock symbols
        Returns: List of normalized data points
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Check if API credentials are valid"""
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema of data this collector produces"""
        pass

    def normalize(self, raw_data: Any) -> Dict[str, Any]:
        """Convert raw API response to normalized format"""
        pass

    def health_check(self) -> bool:
        """Check if the data source is accessible"""
        pass
```

### Plugin Registration & Discovery

```python
# penguin/data/registry.py
class DataSourceRegistry:
    """Central registry for all data source plugins"""

    def __init__(self):
        self._collectors = {}
        self._load_plugins()

    def _load_plugins(self):
        """Auto-discover and register all collector plugins"""
        # Scan penguin/data/collectors/ directory
        # Import all classes inheriting from BaseCollector
        # Register them by name
        pass

    def register(self, collector_class: Type[BaseCollector]):
        """Manually register a collector"""
        pass

    def get_collector(self, name: str) -> BaseCollector:
        """Get collector instance by name"""
        pass

    def get_by_category(self, category: DataCategory) -> List[BaseCollector]:
        """Get all collectors in a category"""
        pass

    def enable_collector(self, name: str, config: Dict):
        """Enable a collector with given config"""
        pass

    def disable_collector(self, name: str):
        """Disable a collector"""
        pass
```

---

## Comprehensive Data Source Catalog

### 1. Social Sentiment Sources (100+ sources)

#### Reddit (50+ subreddits)
- r/wallstreetbets (highest priority)
- r/pennystocks
- r/stocks
- r/investing
- r/options
- r/Daytrading
- r/ValueInvesting
- r/StockMarket
- r/RobinHood
- r/Crypto_General
- r/Superstonk
- r/Shortsqueeze
- r/SPAC
- r/thetagang
- r/SecurityAnalysis
- r/Vitards (materials/steel)
- r/EV_Stocks
- r/Biotech_Stocks
- r/weedstocks
- r/ASX_Bets (Australian)
- r/CanadianInvestor
- r/UKInvesting
- Stock-specific subreddits (r/TSLA, r/GME, etc.)

**Data Collected**: Post frequency, comment count, upvote ratio, sentiment, top keywords, mention velocity, award counts, unique author count

#### Twitter/X (Financial Influencers & Keywords)
- Follow prominent traders/analysts (e.g., @DeItaone, @GurgavinCapital, @unusual_whales)
- Track hashtags (#stocks, #trading, #earnings, etc.)
- Monitor verified accounts
- Track retweet velocity
- Sentiment analysis on tweets
- Link extraction (news sources)

#### StockTwits
- Stock-specific streams
- Bull/bear sentiment ratio
- Message volume
- Trending stocks
- Influencer activity

#### Discord Servers
- WallStreetBets Discord
- Options-focused servers
- Day trading communities
- Stock-specific servers

#### TikTok
- Financial content creators
- Trending stock-related videos
- Hashtag tracking (#stocktok, #investing)

#### YouTube
- Financial channel uploads (Graham Stephan, Meet Kevin, etc.)
- Comment sentiment
- View velocity on stock-related videos

#### Seeking Alpha Comments
- Article comment sentiment
- User rating changes

#### LinkedIn
- Company announcements
- Employee sentiment (Glassdoor crossref)
- Executive movements

#### 4chan /biz/
- High-risk/high-volatility mentions
- Pump & dump detection

#### Telegram Groups
- Stock signal channels
- Crypto-to-stock correlation groups

---

### 2. News & Media Sources (200+ sources)

#### Financial News Outlets
- Bloomberg (via API/scraping)
- Reuters
- Wall Street Journal
- Financial Times
- MarketWatch
- Barron's
- Investor's Business Daily
- TheStreet
- Benzinga
- Yahoo Finance News
- CNBC
- Fox Business
- Business Insider
- Forbes Markets
- The Motley Fool
- Zacks
- Kiplinger

#### News Aggregators
- Google News (stock-specific queries)
- NewsAPI
- Bing News
- Feedly

#### Press Release Wires
- PR Newswire
- Business Wire
- GlobeNewswire
- Accesswire

#### Earnings Call Transcripts
- Seeking Alpha Transcripts
- Motley Fool Transcripts
- AlphaStreet

#### Analyst Reports
- TipRanks (analyst ratings)
- Benzinga Analyst Ratings
- MarketBeat Ratings
- Zacks Rank changes

#### International News (for ADRs)
- Nikkei (Japan)
- China Daily
- Handelsblatt (Germany)
- Les Echos (France)

**Data Collected**: Headline sentiment, publish timestamp, source credibility score, mention count, sentiment trend, breaking news velocity

---

### 3. Insider & Congressional Trading (50+ sources)

#### Congressional Trading
- House Stock Watcher API
- Senate periodic transaction reports
- QuiverQuant Congressional Trading
- Unusual Whales Congress
- Capitol Trades
- Track by politician (Nancy Pelosi, etc.)
- Track by committee assignment

#### Insider Trading (SEC Form 4)
- SEC EDGAR filings
- OpenInsider
- GuruFocus Insider Trades
- Insider Monkey
- DataRoma
- Track C-suite activity
- Track 10%+ owners
- Calculate cluster buying/selling

#### Institutional Holdings (13F Filings)
- WhaleWisdom
- 13F filings (quarterly)
- Track Buffett, Ackman, Burry, etc.
- Hedge fund hotel stocks

#### Short Interest
- Fintel Short Interest
- MarketBeat Short Interest
- S3 Partners (expensive but comprehensive)
- Ortex Short Interest
- High Frequency Lending data

#### Form 3, 4, 5 Tracking
- Beneficial ownership changes
- Insider cluster activity

**Data Collected**: Transaction amount, buy/sell ratio, timing relative to events, politician committee, insider role, percentage of holdings

---

### 4. Options & Derivatives Data (100+ sources)

#### Options Flow
- Unusual Whales Options Flow
- FlowAlgo
- Cheddar Flow
- BlackBoxStocks
- Market Chameleon
- Barchart Unusual Options Activity
- Tradytics

#### Options Metrics
- Put/Call Ratio
- Implied Volatility (IV) vs Historical Volatility (HV)
- IV Rank and Percentile
- Options Volume vs Open Interest
- Max Pain calculations
- Gamma Exposure (GEX)
- Delta Exposure (DEX)
- Vanna and Charm exposure

#### Specific Signal Types
- Sweep orders (aggressive buying)
- Block trades (large single orders)
- Unusual volume (vs 30-day avg)
- Premium spent (dollar volume)
- Bullish vs bearish flow
- Smart money indicators
- Retail vs institutional flow

#### Dark Pool Data
- Dark pool prints
- Large block trades off-exchange
- Dark pool vs lit exchange ratio

#### Futures Data
- E-mini S&P 500 futures
- VIX futures
- Individual stock futures (where available)

**Data Collected**: Strike price, expiration, premium, volume, open interest, Greeks, order type, exchange

---

### 5. Technical Indicators & Market Data (200+ indicators)

#### Price & Volume
- OHLCV data (1min, 5min, 15min, 1hr, 1day)
- Volume analysis (above/below average)
- VWAP (Volume Weighted Average Price)
- Money flow (buying vs selling pressure)
- Tick data (uptick/downtick ratio)

#### Momentum Indicators
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Stochastic Oscillator
- ADX (Average Directional Index)
- CCI (Commodity Channel Index)
- Williams %R
- Rate of Change (ROC)

#### Trend Indicators
- Moving Averages (SMA, EMA, WMA)
- Bollinger Bands
- Keltner Channels
- Donchian Channels
- Ichimoku Cloud
- Parabolic SAR

#### Volatility Indicators
- ATR (Average True Range)
- Bollinger Band Width
- Historical Volatility
- Implied Volatility
- VIX correlation
- Beta vs SPY

#### Volume Indicators
- OBV (On-Balance Volume)
- Accumulation/Distribution
- Chaikin Money Flow
- Volume Profile
- VPVR (Volume Profile Visible Range)

#### Mean Reversion Indicators
- Bollinger Band %B
- Z-Score from moving average
- Distance from VWAP
- Regression channel deviation

#### Chart Patterns (Automated Detection)
- Head & Shoulders
- Double/Triple Top/Bottom
- Cup & Handle
- Bull/Bear Flags
- Triangles (ascending, descending, symmetrical)
- Wedges
- Channels

#### Fibonacci Analysis
- Retracement levels
- Extension levels
- Time zones
- Arcs

#### Market Breadth
- Advance/Decline ratio
- New Highs/New Lows
- Trin (Arms Index)
- McClellan Oscillator
- Sector rotation metrics

**Data Collected**: Indicator values, threshold crossings, pattern completions, signal strength

---

### 6. Fundamental Data (150+ metrics)

#### Financial Statements
- Income Statement (quarterly, annual)
- Balance Sheet
- Cash Flow Statement
- Revenue growth rate
- EPS growth rate
- Profit margins (gross, operating, net)

#### Valuation Ratios
- P/E Ratio (trailing, forward)
- PEG Ratio
- P/S Ratio
- P/B Ratio
- EV/EBITDA
- EV/Revenue
- Price/Cash Flow
- Dividend Yield

#### Profitability Metrics
- ROE (Return on Equity)
- ROA (Return on Assets)
- ROIC (Return on Invested Capital)
- Operating Margin
- Net Margin
- Gross Margin

#### Liquidity & Solvency
- Current Ratio
- Quick Ratio
- Debt-to-Equity
- Interest Coverage Ratio
- Cash Ratio

#### Growth Metrics
- Revenue Growth (YoY, QoQ)
- Earnings Growth
- Book Value Growth
- FCF Growth

#### Earnings Data
- Earnings announcements (date/time)
- EPS estimates vs actuals
- Revenue estimates vs actuals
- Earnings surprise percentage
- Guidance updates
- Analyst estimate revisions

#### Dividend Data
- Dividend history
- Payout ratio
- Dividend growth rate
- Ex-dividend dates

**Data Collected**: Raw values, percentile rankings vs industry, historical trends, estimate beats/misses

---

### 7. Alternative Data (300+ sources)

#### Web Traffic & App Analytics
- SimilarWeb (website traffic)
- Apptopia (mobile app downloads/revenue)
- Sensor Tower (app rankings)
- Google Trends (search volume)
- Alexa rankings (deprecated, use alternatives)

#### Satellite Imagery
- Planet Labs (parking lot monitoring for retailers)
- Orbital Insight (oil storage, construction activity)
- RS Metrics (retail/commercial foot traffic)

#### Credit Card Data
- Facteus
- Second Measure
- M Science
- Yodlee

#### Employment Data
- LinkedIn employee count changes
- Glassdoor reviews/ratings trends
- Indeed job postings
- H1B visa applications (tech hiring)

#### Supply Chain Data
- Import/export data (Panjiva, ImportGenius)
- Shipping data (freight rates, container counts)
- Flight data (airline stocks)
- Truck GPS data (logistics, retail)

#### Weather Data
- NOAA (agriculture, utilities)
- Weather API (retail foot traffic, energy)

#### Geolocation Data
- Foursquare foot traffic
- SafeGraph (POI visits)
- Placer.ai (retail analytics)

#### Social Metrics
- Instagram follower growth (consumer brands)
- TikTok engagement (viral products)
- YouTube subscriber counts

#### Patent Filings
- USPTO database
- Patent trends by company

#### Product Reviews
- Amazon review velocity/sentiment
- Trustpilot ratings
- G2 Crowd (B2B software)

#### Commodity Prices
- Oil (WTI, Brent)
- Gold, Silver
- Lumber, Copper
- Agricultural commodities

#### Crypto Correlation
- Bitcoin/Ethereum correlation with stocks
- Crypto whale movements
- DeFi protocol usage (for fintech stocks)

**Data Collected**: Varies by source; normalized to time-series format with metadata

---

### 8. Macro-Economic Data (100+ indicators)

#### Economic Indicators
- GDP Growth
- Unemployment Rate
- CPI (Consumer Price Index)
- PPI (Producer Price Index)
- PMI (Purchasing Managers Index)
- Retail Sales
- Housing Starts
- Durable Goods Orders
- Consumer Confidence Index
- Leading Economic Index

#### Federal Reserve Data
- FOMC minutes/statements
- Federal Funds Rate
- Fed balance sheet size
- Treasury yields (2yr, 10yr, 30yr)
- Yield curve (inversions)
- Fed Governor speeches (sentiment)

#### Global Markets
- Major indices (S&P 500, Nasdaq, Dow, Russell 2000)
- International indices (FTSE, DAX, Nikkei, Shanghai)
- Currency exchange rates (DXY, EUR/USD, etc.)
- VIX (volatility index)

#### Sector Performance
- Sector ETF performance (XLF, XLK, XLE, etc.)
- Relative sector strength
- Sector rotation signals

**Data Collected**: Values, changes vs prior period, consensus estimates, surprise percentage

---

### 9. Regulatory & Legal Sources (50+ sources)

#### SEC Filings
- 10-K (annual reports)
- 10-Q (quarterly reports)
- 8-K (material events)
- S-1 (IPO registration)
- 13D/13G (beneficial ownership)
- Form 4 (insider trading)
- 424B (prospectus)

#### Legal Databases
- Class action lawsuits (securities fraud)
- Patent litigation
- Merger/acquisition filings (HSR)

#### Regulatory Actions
- FDA approvals/rejections (biotech/pharma)
- FAA certifications (aerospace)
- FCC filings (telecom)
- EPA compliance/violations

**Data Collected**: Filing type, sentiment extraction, material events, timing

---

### 10. Crypto & Blockchain (for correlation analysis)

#### On-Chain Data
- Whale wallet movements
- Exchange inflows/outflows
- Network activity (transactions/day)

#### Crypto Sentiment
- Crypto Twitter sentiment
- r/CryptoCurrency mentions
- Fear & Greed Index

#### Correlation Tracking
- BTC correlation with tech stocks
- Crypto-related stock movements (COIN, MSTR, RIOT)

**Data Collected**: Prices, volumes, on-chain metrics, correlations

---

## Signal Detection Framework

### Signal Types

```python
class SignalType(Enum):
    MOMENTUM_SPIKE = "momentum_spike"              # Rapid increase in activity
    SENTIMENT_SHIFT = "sentiment_shift"            # Bullish/bearish flip
    VOLUME_ANOMALY = "volume_anomaly"              # Unusual trading volume
    OPTIONS_FLOW = "options_flow"                  # Large options bets
    INSIDER_CLUSTER = "insider_cluster"            # Multiple insiders buying
    CONGRESSIONAL_BUY = "congressional_buy"        # Congress member purchase
    MEAN_REVERSION = "mean_reversion"              # Oversold/overbought
    PATTERN_BREAKOUT = "pattern_breakout"          # Chart pattern completion
    EARNINGS_SURPRISE = "earnings_surprise"        # Beat/miss estimates
    SHORT_SQUEEZE = "short_squeeze"                # High SI + price surge
    DARK_POOL_PRINT = "dark_pool_print"           # Large dark pool trade
    CORRELATION_DIVERGENCE = "correlation_divergence"  # Breaks correlation
    GAMMA_SQUEEZE = "gamma_squeeze"                # Options-driven rally
    SECTOR_ROTATION = "sector_rotation"            # Money flow into sector
    FUNDAMENTAL_IMPROVEMENT = "fundamental_improvement"  # Metrics improving
    ALTERNATIVE_DATA_SPIKE = "alternative_data_spike"  # Web traffic, etc.
```

### Signal Detection Modules

Each signal type has its own detector module:

```python
# penguin/signals/detectors/momentum_spike.py
class MomentumSpikeDetector(BaseDetector):
    """Detect rapid increases in social mentions or trading volume"""

    def detect(self, symbol: str, lookback_hours: int = 24) -> Optional[Signal]:
        # Get mention counts for last N hours
        recent_mentions = self.get_mentions(symbol, hours=1)
        baseline_mentions = self.get_mentions(symbol, hours=lookback_hours)

        # Calculate spike percentage
        if baseline_mentions == 0:
            return None

        spike_pct = (recent_mentions - baseline_mentions) / baseline_mentions

        # Threshold: 300% increase
        if spike_pct > 3.0:
            return Signal(
                type=SignalType.MOMENTUM_SPIKE,
                symbol=symbol,
                strength=min(spike_pct / 10, 1.0),  # Normalize to 0-1
                metadata={
                    "recent_mentions": recent_mentions,
                    "baseline_mentions": baseline_mentions,
                    "spike_percentage": spike_pct * 100,
                    "sources": self.get_top_sources(symbol)
                }
            )
        return None
```

### Signal Aggregation & Correlation

```python
class SignalAggregator:
    """Combine multiple signals for a holistic view"""

    def aggregate(self, symbol: str) -> AggregatedSignal:
        # Run all detectors
        signals = []
        for detector in self.detectors:
            signal = detector.detect(symbol)
            if signal:
                signals.append(signal)

        # Calculate correlations
        correlations = self.find_correlations(signals)

        # Weight signals by strength and correlation
        weighted_score = self.calculate_weighted_score(signals, correlations)

        return AggregatedSignal(
            symbol=symbol,
            signals=signals,
            correlations=correlations,
            overall_score=weighted_score,
            recommendation=self.generate_recommendation(weighted_score)
        )
```

---

## Claude AI Integration Architecture

### Multi-Layered Analysis Approach

#### Layer 1: Individual Signal Analysis
Claude analyzes each signal type independently for context and significance.

```python
# Example prompt for single signal
"""
You are analyzing a momentum spike signal for {symbol}.

Signal Data:
- Type: Social Media Momentum Spike
- Recent mentions: {recent_mentions}
- Baseline mentions: {baseline_mentions}
- Spike: {spike_pct}%
- Top sources: {sources}
- Sentiment: {sentiment}/100

Additional Context:
- Current price: ${price}
- Today's change: {change}%
- Market cap: ${market_cap}

Analyze this signal:
1. Is this signal significant? (Yes/No)
2. What might be driving this spike?
3. What are the risks?
4. Confidence level (0-100)
"""
```

#### Layer 2: Multi-Signal Synthesis
Claude receives all signals for a stock and synthesizes them.

```python
"""
You are analyzing {symbol} with multiple signals:

Signals Detected:
1. Reddit Momentum Spike (+450% mentions in 1hr)
2. Unusual Options Flow ($2M bullish call sweep)
3. Congressional Purchase (Rep. X bought $50K)
4. Technical: RSI oversold bounce
5. Dark Pool Print: 500K shares at ${price}

Current Market Data:
- Price: ${price} ({change}% today)
- Volume: {volume} ({vol_vs_avg}x average)
- Short Interest: {short_interest}%
- Volatility: IV={iv}%, HV={hv}%

Recent News:
{news_headlines}

Task:
1. Synthesize these signals into a cohesive investment thesis
2. Identify the primary catalyst
3. Determine if signals are mutually reinforcing or contradictory
4. Assess risk/reward
5. Provide recommendation: BUY / WATCH / AVOID
6. Confidence: 0-100
7. Time horizon: SHORT (1-7 days) / MEDIUM (1-4 weeks) / LONG (1-6 months)
"""
```

#### Layer 3: Portfolio-Level Analysis
Claude analyzes all recommendations together for correlation and risk.

```python
"""
You have generated {num_recommendations} buy recommendations today:

1. {symbol1}: Thesis: {thesis1}, Confidence: {conf1}
2. {symbol2}: Thesis: {thesis2}, Confidence: {conf2}
...

Analyze:
1. Are any of these correlated? (same sector, similar thesis)
2. What is the portfolio-level risk?
3. Rank them by risk-adjusted expected return
4. Suggest position sizing
5. Identify any diversification opportunities
"""
```

### Structured Output Format

Use JSON mode for consistent parsing:

```json
{
  "symbol": "BYND",
  "recommendation": "BUY",
  "confidence": 78,
  "time_horizon": "SHORT",
  "thesis": "Strong Reddit momentum combined with unusual bullish options flow suggests retail-driven squeeze potential. Congressional purchase adds credibility.",
  "supporting_signals": [
    {"type": "momentum_spike", "weight": 0.4, "description": "450% increase in WSB mentions"},
    {"type": "options_flow", "weight": 0.3, "description": "$2M call sweep at $15 strike"},
    {"type": "congressional_buy", "weight": 0.3, "description": "Rep purchased $50K"}
  ],
  "risks": [
    "High volatility stock (IV=120%)",
    "Retail-driven moves can reverse quickly",
    "Fundamentals remain weak"
  ],
  "entry_strategy": "Buy on pullback to $12.50-13.00 support",
  "exit_strategy": "Take profits at $18-20 resistance, stop loss at $11",
  "position_size_suggestion": "Small (1-2% of portfolio) due to high risk"
}
```

---

## Data Pipeline & Processing

### Real-Time vs Batch Processing

#### Real-Time Pipeline (Streaming)
```python
# penguin/data/streaming.py
class StreamingPipeline:
    """Handle real-time data sources (WebSockets, webhooks)"""

    async def start(self):
        # Connect to streaming sources
        await self.reddit_stream.connect()
        await self.twitter_stream.connect()
        await self.options_flow_stream.connect()

        # Process messages as they arrive
        async for message in self.multiplexed_stream():
            await self.process_message(message)

    async def process_message(self, message: StreamMessage):
        # Normalize
        normalized = self.normalize(message)

        # Store in Redis (fast cache)
        await self.redis.store(normalized)

        # Check if triggers signal detection
        if self.should_trigger_detection(normalized):
            await self.signal_queue.enqueue(normalized.symbol)
```

#### Batch Pipeline (Scheduled)
```python
# penguin/data/batch.py
class BatchPipeline:
    """Handle scheduled data collection"""

    async def run_hourly(self):
        # Collect from hourly sources
        collectors = self.registry.get_by_frequency(CollectionFrequency.MEDIUM)

        for collector in collectors:
            symbols = self.get_active_symbols()
            data = await collector.collect(symbols)
            await self.store(data)

    async def run_daily(self):
        # Fundamental data, SEC filings, etc.
        collectors = self.registry.get_by_frequency(CollectionFrequency.LOW)

        for collector in collectors:
            data = await collector.collect(self.get_all_symbols())
            await self.store(data)
```

### Data Normalization

All data is normalized to a common schema:

```python
{
    "timestamp": "2025-01-15T14:30:00Z",
    "symbol": "AAPL",
    "source": "reddit_wsb",
    "category": "social_sentiment",
    "data_type": "mention",
    "value": 145,  # mention count
    "metadata": {
        "sentiment": 0.65,  # -1 to 1
        "subreddit": "wallstreetbets",
        "top_post_title": "AAPL to the moon",
        "upvote_ratio": 0.92
    }
}
```

---

## Technology Stack (Detailed)

### Backend Services

#### Core Application
- **Python 3.11+**: Primary language
- **FastAPI**: REST API (async support)
- **Pydantic V2**: Data validation and serialization
- **asyncio/aiohttp**: Async HTTP requests
- **websockets**: Real-time data streams

#### Task Orchestration
- **Celery**: Distributed task queue
- **Celery Beat**: Task scheduling
- **Redis**: Celery broker + cache
- **Flower**: Celery monitoring UI

#### Data Processing
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Polars**: Fast DataFrame library (alternative to Pandas)
- **Dask**: Parallel computing for large datasets

#### Machine Learning / AI
- **Anthropic Claude API**: Primary AI engine
- **scikit-learn**: ML utilities
- **LightGBM/XGBoost**: Gradient boosting (signal weighting)
- **Transformers (HuggingFace)**: NLP models for sentiment
- **NLTK/spaCy**: Text processing

#### Technical Analysis
- **TA-Lib**: 200+ technical indicators
- **Pandas-TA**: Alternative TA library
- **Backtrader**: Backtesting framework

### Storage

#### Time-Series Database
- **TimescaleDB**: PostgreSQL extension for time-series
  - Store OHLCV data
  - Store mention counts over time
  - Store indicator values
  - Automatic compression and retention policies

#### Relational Database
- **PostgreSQL**: User data, metadata, configurations
  - User accounts and preferences
  - Stock metadata (company info, sector)
  - Recommendation history
  - Signal definitions

#### Cache & Pub/Sub
- **Redis**:
  - Cache API responses (reduce costs)
  - Real-time signal updates (Pub/Sub)
  - Rate limiting counters
  - Session storage

#### Object Storage
- **AWS S3 / MinIO**:
  - Historical data archives
  - Large datasets (satellite imagery, etc.)
  - Backup storage

#### Search
- **Elasticsearch**: Full-text search
  - News article search
  - SEC filing search
  - Historical signal search

### API Integrations

#### Data APIs (Partial List)
- **Reddit**: PRAW (Python Reddit API Wrapper)
- **Twitter**: Tweepy, Twitter API v2
- **Financial Data**:
  - yfinance (free)
  - Alpha Vantage (free tier, then paid)
  - Polygon.io (real-time market data)
  - IEX Cloud
  - Finnhub
- **Options**: Tradier, CBOE Data Shop
- **News**: NewsAPI, GNews API, Benzinga API
- **Sentiment**: Sentdex, Social Sentiment
- **Congressional Trading**: QuiverQuant API, Capitol Trades API
- **SEC Data**: sec-api.io
- **Alternative Data**: SafeGraph, SimilarWeb

### Infrastructure

#### Deployment
- **Docker**: Containerization
- **Docker Compose**: Local development
- **Kubernetes**: Production orchestration (optional, for scale)
- **GitHub Actions**: CI/CD

#### Monitoring & Logging
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Sentry**: Error tracking
- **ELK Stack** (Elasticsearch, Logstash, Kibana): Log aggregation
- **Datadog** (alternative): All-in-one monitoring

#### Networking
- **Nginx**: Reverse proxy
- **CloudFlare**: CDN and DDoS protection
- **Kong/Traefik**: API Gateway (rate limiting, auth)

---

## Project Structure (Complete)

```
penguin/
├── README.md
├── CLAUDE.md                    # This file
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── setup.py
│
├── penguin/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── logging.py          # Logging setup
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── constants.py        # Global constants
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── base.py             # BaseCollector interface
│   │   ├── registry.py         # Plugin registry
│   │   ├── orchestrator.py     # Data collection orchestration
│   │   ├── streaming.py        # Real-time pipeline
│   │   ├── batch.py            # Batch pipeline
│   │   │
│   │   ├── collectors/         # Data source plugins (1000+ files)
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── social/
│   │   │   │   ├── reddit_wsb.py
│   │   │   │   ├── reddit_pennystocks.py
│   │   │   │   ├── twitter_sentiment.py
│   │   │   │   ├── stocktwits.py
│   │   │   │   ├── discord_wsb.py
│   │   │   │   └── ... (50+ more)
│   │   │   │
│   │   │   ├── news/
│   │   │   │   ├── bloomberg.py
│   │   │   │   ├── reuters.py
│   │   │   │   ├── yahoo_finance.py
│   │   │   │   ├── benzinga.py
│   │   │   │   └── ... (100+ more)
│   │   │   │
│   │   │   ├── market_data/
│   │   │   │   ├── polygon_ohlcv.py
│   │   │   │   ├── iex_cloud.py
│   │   │   │   ├── alpha_vantage.py
│   │   │   │   └── ... (20+ more)
│   │   │   │
│   │   │   ├── options/
│   │   │   │   ├── unusual_whales.py
│   │   │   │   ├── flowalgo.py
│   │   │   │   ├── cheddar_flow.py
│   │   │   │   ├── tradier_options.py
│   │   │   │   └── ... (30+ more)
│   │   │   │
│   │   │   ├── insider/
│   │   │   │   ├── congressional_trades.py
│   │   │   │   ├── sec_form4.py
│   │   │   │   ├── openinsider.py
│   │   │   │   ├── institutional_13f.py
│   │   │   │   └── ... (20+ more)
│   │   │   │
│   │   │   ├── fundamental/
│   │   │   │   ├── financials.py
│   │   │   │   ├── earnings.py
│   │   │   │   ├── sec_filings.py
│   │   │   │   └── ... (30+ more)
│   │   │   │
│   │   │   ├── alternative/
│   │   │   │   ├── web_traffic.py
│   │   │   │   ├── app_analytics.py
│   │   │   │   ├── satellite_imagery.py
│   │   │   │   ├── credit_card.py
│   │   │   │   ├── employment.py
│   │   │   │   ├── supply_chain.py
│   │   │   │   └── ... (100+ more)
│   │   │   │
│   │   │   ├── macro/
│   │   │   │   ├── economic_indicators.py
│   │   │   │   ├── fed_data.py
│   │   │   │   ├── treasury_yields.py
│   │   │   │   └── ... (50+ more)
│   │   │   │
│   │   │   └── crypto/
│   │   │       ├── bitcoin_correlation.py
│   │   │       ├── onchain_data.py
│   │   │       └── ... (20+ more)
│   │   │
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── normalizer.py      # Data normalization
│   │   │   ├── sentiment.py       # Sentiment analysis
│   │   │   ├── aggregator.py      # Time-series aggregation
│   │   │   └── validator.py       # Data quality checks
│   │   │
│   │   └── storage/
│   │       ├── __init__.py
│   │       ├── models.py          # SQLAlchemy models
│   │       ├── timescale.py       # TimescaleDB interface
│   │       ├── postgres.py        # PostgreSQL interface
│   │       ├── redis_cache.py     # Redis interface
│   │       └── s3_storage.py      # S3 interface
│   │
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── base.py                # BaseDetector interface
│   │   ├── registry.py            # Signal registry
│   │   ├── aggregator.py          # Multi-signal aggregation
│   │   │
│   │   ├── detectors/
│   │   │   ├── __init__.py
│   │   │   ├── momentum_spike.py
│   │   │   ├── sentiment_shift.py
│   │   │   ├── volume_anomaly.py
│   │   │   ├── options_flow.py
│   │   │   ├── insider_cluster.py
│   │   │   ├── congressional_buy.py
│   │   │   ├── mean_reversion.py
│   │   │   ├── pattern_breakout.py
│   │   │   ├── earnings_surprise.py
│   │   │   ├── short_squeeze.py
│   │   │   ├── dark_pool.py
│   │   │   ├── gamma_squeeze.py
│   │   │   └── ... (20+ detectors)
│   │   │
│   │   ├── technical/
│   │   │   ├── __init__.py
│   │   │   ├── indicators.py      # TA-Lib wrappers
│   │   │   ├── patterns.py        # Chart pattern detection
│   │   │   └── screeners.py       # Technical screeners
│   │   │
│   │   └── correlation.py         # Signal correlation analysis
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── claude.py              # Claude API client
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── single_signal.py   # Layer 1 prompts
│   │   │   ├── multi_signal.py    # Layer 2 prompts
│   │   │   ├── portfolio.py       # Layer 3 prompts
│   │   │   └── templates.py       # Prompt templates
│   │   │
│   │   ├── analysis.py            # Analysis orchestration
│   │   ├── parsers.py             # Response parsing
│   │   └── cache.py               # Analysis caching
│   │
│   ├── recommender/
│   │   ├── __init__.py
│   │   ├── engine.py              # Recommendation generation
│   │   ├── scoring.py             # Confidence scoring
│   │   ├── ranking.py             # Rank recommendations
│   │   ├── tracker.py             # Performance tracking
│   │   └── backtester.py          # Backtesting framework
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py              # FastAPI app
│   │   ├── deps.py                # Dependencies
│   │   ├── middleware.py          # Middleware
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── recommendations.py # GET /recommendations
│   │   │   ├── signals.py         # GET /signals/{symbol}
│   │   │   ├── stocks.py          # GET /stocks/{symbol}
│   │   │   ├── analysis.py        # POST /analyze
│   │   │   ├── admin.py           # Admin endpoints
│   │   │   └── webhooks.py        # Webhook receivers
│   │   │
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── signal.py
│   │       ├── recommendation.py
│   │       └── stock.py
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py                # CLI entry point
│   │   ├── commands/
│   │   │   ├── scan.py            # Scan for opportunities
│   │   │   ├── analyze.py         # Analyze specific stock
│   │   │   ├── backtest.py        # Backtest signals
│   │   │   └── manage.py          # Manage data sources
│   │
│   ├── alerts/
│   │   ├── __init__.py
│   │   ├── notifier.py            # Notification orchestration
│   │   ├── channels/
│   │   │   ├── email.py
│   │   │   ├── sms.py
│   │   │   ├── push.py
│   │   │   ├── discord.py
│   │   │   └── telegram.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── rate_limiter.py
│       ├── retry.py
│       ├── cache.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_collectors/
│   ├── test_signals/
│   ├── test_ai/
│   └── test_api/
│
├── scripts/
│   ├── init_db.py
│   ├── backfill_data.py
│   ├── generate_api_keys.py
│   └── migrate_data.py
│
├── config/
│   ├── collectors.yaml         # Enable/disable collectors
│   ├── signals.yaml            # Signal configurations
│   ├── prompts.yaml            # Claude prompts
│   └── alerts.yaml             # Alert rules
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── adding_collectors.md
│   ├── deployment.md
│   └── contributing.md
│
└── infra/                      # Infrastructure as Code
    ├── docker/
    │   ├── Dockerfile
    │   ├── Dockerfile.worker
    │   └── nginx.conf
    └── terraform/              # Cloud infrastructure
        ├── aws/
        └── gcp/
```

---

## Development Commands

### Environment Setup
```bash
# Clone repository
git clone <repo-url>
cd penguin

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_db.py

# Run database migrations
alembic upgrade head
```

### Running Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or run individually:

# 1. Start API server
uvicorn penguin.api.server:app --reload --port 8000

# 2. Start Celery worker (data collection)
celery -A penguin.data.batch worker --loglevel=info

# 3. Start Celery beat (scheduler)
celery -A penguin.data.batch beat --loglevel=info

# 4. Start Flower (Celery monitoring)
celery -A penguin.data.batch flower --port=5555

# 5. Start streaming pipeline
python -m penguin.data.streaming
```

### CLI Usage

```bash
# Scan for opportunities
penguin scan --top 10

# Analyze specific stock
penguin analyze AAPL --verbose

# Backtest a signal
penguin backtest --signal momentum_spike --days 90

# List all data sources
penguin sources list

# Enable a data source
penguin sources enable reddit_wsb

# Disable a data source
penguin sources disable twitter_sentiment

# Test a collector
penguin sources test reddit_wsb --symbol GME

# Check data freshness
penguin status --data-sources
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=penguin --cov-report=html

# Run specific test file
pytest tests/test_signals/test_momentum_spike.py

# Run integration tests only
pytest -m integration

# Run unit tests only
pytest -m unit

# Run tests in parallel
pytest -n auto
```

### Data Management

```bash
# Backfill historical data for a stock
python scripts/backfill_data.py --symbol AAPL --start 2024-01-01 --end 2024-12-31

# Backfill for all S&P 500 stocks
python scripts/backfill_data.py --index SP500 --days 365

# Clean old data (retention policy)
python scripts/cleanup_data.py --older-than 90d

# Export data to CSV
penguin export --symbol TSLA --output tsla_data.csv

# Import data from CSV
penguin import --file historical_data.csv
```

### Database Management

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Monitoring

```bash
# Check system health
penguin health

# View metrics
curl http://localhost:9090/metrics  # Prometheus endpoint

# Check Celery tasks
celery -A penguin.data.batch inspect active

# View logs
docker-compose logs -f api
docker-compose logs -f worker
```

---

## Configuration Management

### Collector Configuration (config/collectors.yaml)

```yaml
# Enable/disable collectors without code changes
collectors:
  reddit_wsb:
    enabled: true
    frequency: high  # 1-5 minutes
    symbols: all  # or list of symbols
    config:
      subreddit: wallstreetbets
      min_upvotes: 10

  unusual_whales:
    enabled: true
    frequency: realtime
    requires_subscription: true
    cost_per_month: 50
    config:
      min_premium: 10000  # Only alerts for >$10k premium

  bloomberg_news:
    enabled: false  # Disabled (expensive)
    frequency: medium
    cost_per_request: 0.10
```

### Signal Configuration (config/signals.yaml)

```yaml
signals:
  momentum_spike:
    enabled: true
    threshold: 3.0  # 300% increase
    lookback_hours: 24
    min_baseline: 5  # Ignore if baseline < 5 mentions

  options_flow:
    enabled: true
    min_premium: 50000  # $50k minimum
    types:
      - sweep
      - block
    exclude_earnings_week: true

  short_squeeze:
    enabled: true
    min_short_interest: 20  # 20% SI
    volume_threshold: 2.0  # 2x average volume
```

---

## MVP Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
1. Set up project structure
2. Implement BaseCollector interface
3. Create plugin registry
4. Set up databases (PostgreSQL, TimescaleDB, Redis)
5. Build single collector: Reddit WSB
6. Store data in TimescaleDB
7. Create basic CLI

### Phase 2: Signal Detection (Weeks 3-4)
1. Implement MomentumSpikeDetector
2. Build signal aggregation
3. Add basic technical indicators (RSI, volume)
4. Create signal storage schema
5. CLI command: `penguin scan`

### Phase 3: AI Integration (Weeks 5-6)
1. Claude API client
2. Single-signal prompt (Layer 1)
3. Multi-signal synthesis (Layer 2)
4. Structured output parsing
5. Store recommendations in DB

### Phase 4: Validation (Weeks 7-8)
1. Backfill historical Reddit data (2-3 months)
2. Run signal detection on historical data
3. Generate recommendations
4. Manually validate against actual price movements
5. Calculate accuracy metrics

### Phase 5: Expansion (Weeks 9-12)
1. Add 5-10 more collectors (Twitter, StockTwits, Options Flow, Congressional)
2. Implement 5-10 more signal detectors
3. Build FastAPI REST API
4. Create basic web dashboard
5. Email/SMS alerts

### Phase 6: Iteration (Ongoing)
1. Add more collectors (goal: 100+)
2. Refine signal detection thresholds
3. Improve Claude prompts
4. Build backtesting framework
5. Optimize performance

---

## Key Implementation Patterns

### Adding a New Data Collector

1. Create file: `penguin/data/collectors/social/new_source.py`
2. Implement BaseCollector:

```python
from penguin.data.base import BaseCollector, DataCategory, CollectionFrequency

class NewSourceCollector(BaseCollector):
    name = "new_source"
    category = DataCategory.SOCIAL_SENTIMENT
    frequency = CollectionFrequency.HIGH
    requires_auth = True
    rate_limit = 100  # per minute

    async def collect(self, symbols: List[str], **kwargs) -> List[Dict]:
        data = []
        for symbol in symbols:
            # Fetch data from API
            response = await self.client.get(f"/api/{symbol}")

            # Normalize
            normalized = self.normalize(response)
            data.append(normalized)

        return data

    def normalize(self, raw_data: Dict) -> Dict:
        return {
            "timestamp": raw_data["created_at"],
            "symbol": raw_data["ticker"],
            "source": self.name,
            "category": self.category.value,
            "data_type": "mention",
            "value": raw_data["mention_count"],
            "metadata": {
                "sentiment": raw_data["sentiment_score"]
            }
        }
```

3. Collector is auto-discovered by registry
4. Enable in `config/collectors.yaml`
5. Done! Data collection starts automatically

### Adding a New Signal Detector

1. Create file: `penguin/signals/detectors/new_signal.py`
2. Implement BaseDetector:

```python
from penguin.signals.base import BaseDetector, Signal, SignalType

class NewSignalDetector(BaseDetector):
    signal_type = SignalType.NEW_SIGNAL

    def detect(self, symbol: str) -> Optional[Signal]:
        # Fetch relevant data
        data = self.get_data(symbol)

        # Check conditions
        if self.condition_met(data):
            return Signal(
                type=self.signal_type,
                symbol=symbol,
                strength=self.calculate_strength(data),
                metadata={"key": "value"}
            )

        return None
```

3. Register detector
4. Configure in `config/signals.yaml`
5. Runs automatically on each scan

---

## Performance Considerations

### Rate Limiting Strategy
- Track API calls per source in Redis
- Implement token bucket algorithm
- Queue requests that exceed limits
- Rotate API keys for higher throughput

### Caching Strategy
- Cache API responses (TTL based on data freshness needs)
- Cache computed signals (invalidate on new data)
- Cache Claude analysis (expensive, cache for 1 hour)

### Database Optimization
- Partition TimescaleDB by symbol and time
- Index on (symbol, timestamp, source)
- Compress old data automatically
- Archive data > 1 year to S3

### Scaling Horizontally
- Multiple Celery workers for data collection
- Separate workers for signal detection vs data collection
- Redis cluster for high-throughput caching
- Read replicas for PostgreSQL

---

## Security & Compliance

### API Key Management
- Store in environment variables, never commit
- Use secret management (AWS Secrets Manager, HashiCorp Vault)
- Rotate keys regularly
- Separate keys for dev/staging/prod

### Rate Limiting (User-Facing API)
- Implement per-user rate limits
- Tiered access (free, pro, enterprise)
- DDoS protection via CloudFlare

### Data Privacy
- Anonymize user data
- GDPR compliance (data deletion requests)
- Encrypt sensitive data at rest
- Audit logs for data access

### Legal Compliance
- Clear "not financial advice" disclaimers
- Terms of service
- Review API ToS (don't violate)
- Consult lawyer before monetizing

---

## Monitoring & Alerting

### Key Metrics to Track
- Data collection success rate per source
- API error rates
- Signal detection latency
- Recommendation accuracy (over time)
- Claude API costs
- Database query performance

### Alerts
- Source down (no data collected in N hours)
- API rate limit exceeded
- Database connection failures
- High error rate (>5%)
- Anomalous costs (Claude API)

---

## Cost Estimation

### MVP (Phase 1-4)
- **Claude API**: ~$50-200/month (depends on analysis frequency)
- **Data APIs**: $0-500/month (start with free tiers)
- **Infrastructure**: $50-100/month (AWS/GCP small instance + RDS)
- **Total**: $100-800/month

### Scale (1000+ sources, 10K users)
- **Claude API**: $1,000-5,000/month
- **Data APIs**: $2,000-10,000/month (premium sources)
- **Infrastructure**: $500-2,000/month
- **Total**: $3,500-17,000/month

---

## Future Enhancements

### Short-term (6-12 months)
- Mobile app (React Native)
- Real-time push notifications
- Portfolio tracking & paper trading
- Community features (share recommendations)
- Backtesting framework
- Machine learning for signal weighting

### Medium-term (1-2 years)
- Live trading integration (Alpaca, Interactive Brokers)
- Custom alert builder (no-code)
- Screener builder
- Algo trading (strategy builder)
- Premium subscription tiers

### Long-term (2-5 years)
- Institutional-grade platform
- Hedge fund tools (portfolio optimization)
- API for third-party developers
- White-label solution
- International markets

---

## Getting Started with Development

### Step 1: Set Up Environment
```bash
git clone <repo>
cd penguin
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

### Step 2: Initialize Databases
```bash
docker-compose up -d postgres redis
python scripts/init_db.py
alembic upgrade head
```

### Step 3: Test Reddit Collector
```bash
# Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in .env
penguin sources test reddit_wsb --symbol GME
```

### Step 4: Collect Data
```bash
# Run for 1 hour, collect Reddit mentions
penguin collect --source reddit_wsb --duration 1h
```

### Step 5: Detect Signals
```bash
# Scan for momentum spikes
penguin scan --signal momentum_spike
```

### Step 6: Generate Recommendation
```bash
# Analyze a stock with Claude
penguin analyze GME
```

### Step 7: Iterate
- Adjust signal thresholds in `config/signals.yaml`
- Refine prompts in `penguin/ai/prompts/`
- Add more collectors
- Backtest on historical data

---

## Support & Resources

- **Documentation**: `/docs` directory
- **API Docs**: `http://localhost:8000/docs` (FastAPI auto-generated)
- **Architecture Diagrams**: `/docs/architecture.md`
- **Contribution Guide**: `/docs/contributing.md`

---

## Notes for Future Claude Instances

- **Start with Reddit**: Easiest API, free, high signal
- **Use Claude API sparingly during dev**: Cache aggressively to reduce costs
- **Test on historical data**: Validate signals before going live
- **Modular design**: Each collector/signal is independent
- **Configuration over code**: Enable/disable sources via YAML
- **Monitor costs**: Set up billing alerts on all paid APIs
- **Iterative approach**: Start small, validate, expand

This architecture is designed for infinite scalability. The plugin system means adding new data sources is trivial. Focus on proving value with a small set of high-quality sources, then expand methodically.
