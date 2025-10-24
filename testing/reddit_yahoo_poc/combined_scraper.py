"""
PENGUIN Combined Reddit + Yahoo Finance Scraper
Aggregates Reddit sentiment and Yahoo Finance fundamentals
"""

import sys
import os
import time
from datetime import datetime
from typing import List, Dict

# Add parent directories to path to import from other PoCs
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'reddit_poc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'yahoo_poc'))

# Import Reddit scraper
from multi_subreddit_scraper import MultiSubredditScraper

# Import Yahoo scraper components
import yfinance as yf
import pandas as pd


class CombinedRedditYahooScraper:
    """Combine Reddit sentiment with Yahoo Finance fundamentals"""

    def __init__(self):
        """Initialize both scrapers"""
        self.reddit_scraper = MultiSubredditScraper()

    def verify_ticker(self, ticker: str) -> bool:
        """Verify if a ticker is valid via Yahoo Finance (quick check)"""
        try:
            time.sleep(1)  # Brief rate limit
            stock = yf.Ticker(ticker)
            # Try to get current price - if it fails, ticker is invalid
            info = stock.info
            if info.get('regularMarketPrice') or info.get('currentPrice'):
                return True
            return False
        except:
            return False

    def get_reddit_top_stocks(self, limit: int = 10) -> List[Dict]:
        """Get top stocks from Reddit analysis with ticker verification"""
        print()
        print("=" * 70)
        print("🐧 PHASE 1: REDDIT SENTIMENT ANALYSIS")
        print("=" * 70)
        print()

        # Scrape Reddit
        all_posts = self.reddit_scraper.scrape_all_subreddits(posts_per_sub=100)

        # Aggregate stocks
        print("📊 Aggregating stock mentions across all subreddits...")
        top_stocks = self.reddit_scraper.aggregate_stock_data(all_posts)
        print(f"✓ Aggregated data for {len(top_stocks)} unique stocks")
        print()

        # Verify tickers and get valid top N
        print("🔍 Verifying tickers via Yahoo Finance...")
        verified_stocks = []
        idx = 0
        checked = 0

        while len(verified_stocks) < limit and idx < len(top_stocks):
            stock = top_stocks[idx]
            ticker = stock['ticker']
            checked += 1

            print(f"  [{checked}] Checking ${ticker}...", end=" ")

            if self.verify_ticker(ticker):
                verified_stocks.append(stock)
                print(f"✓ Valid (#{len(verified_stocks)} in top {limit})")
            else:
                print(f"✗ Invalid ticker, skipping")

            idx += 1

        print()
        print(f"✓ Verified {len(verified_stocks)} valid tickers out of {checked} checked")
        print()

        return verified_stocks

    def get_yahoo_data(self, ticker: str) -> Dict:
        """Get comprehensive Yahoo Finance data including mean reversion indicators"""
        try:
            # Rate limiting: 2 seconds between Yahoo requests
            time.sleep(2)

            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period='3mo')  # Get 3 months for better analysis

            if hist.empty:
                return None

            # Basic price metrics
            current_price = hist['Close'].iloc[-1]
            start_price_30d = hist['Close'].iloc[-30] if len(hist) >= 30 else hist['Close'].iloc[0]
            price_change_30d = ((current_price - start_price_30d) / start_price_30d) * 100

            # Moving averages for mean reversion
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            sma_20 = hist['SMA_20'].iloc[-1]
            sma_50 = hist['SMA_50'].iloc[-1] if len(hist) >= 50 else None

            # Bollinger Bands (for mean reversion)
            std_20 = hist['Close'].rolling(window=20).std()
            upper_band = hist['SMA_20'] + (std_20 * 2)
            lower_band = hist['SMA_20'] - (std_20 * 2)
            bb_upper = upper_band.iloc[-1]
            bb_lower = lower_band.iloc[-1]

            # Calculate where price is relative to Bollinger Bands (0-100 scale)
            bb_position = ((current_price - bb_lower) / (bb_upper - bb_lower)) * 100 if bb_upper != bb_lower else 50

            # RSI (Relative Strength Index) - mean reversion indicator
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]

            # Mean reversion signals
            oversold = current_rsi < 30  # RSI < 30 = oversold (potential buy)
            overbought = current_rsi > 70  # RSI > 70 = overbought (potential sell)
            at_lower_bb = current_price < bb_lower * 1.02  # Within 2% of lower Bollinger Band
            at_upper_bb = current_price > bb_upper * 0.98  # Within 2% of upper Bollinger Band

            # Distance from mean (for mean reversion)
            distance_from_sma20 = ((current_price - sma_20) / sma_20) * 100

            # Volume analysis
            avg_volume = hist['Volume'].mean()
            recent_volume = hist['Volume'].iloc[-5:].mean()
            volume_change_pct = ((recent_volume - avg_volume) / avg_volume) * 100

            # Volatility
            volatility = hist['Close'].pct_change().std() * 100

            # 52-week range position
            week_52_high = info.get('fiftyTwoWeekHigh')
            week_52_low = info.get('fiftyTwoWeekLow')
            range_position = None
            if week_52_high and week_52_low and week_52_high != week_52_low:
                range_position = ((current_price - week_52_low) / (week_52_high - week_52_low)) * 100

            return {
                'ticker': ticker,
                'current_price': current_price,
                'price_change_30d': price_change_30d,
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'volume_change': volume_change_pct,
                'volatility': volatility,
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                '52w_high': week_52_high,
                '52w_low': week_52_low,
                '52w_range_position': range_position,
                # Mean reversion indicators
                'sma_20': sma_20,
                'sma_50': sma_50,
                'distance_from_sma20': distance_from_sma20,
                'rsi': current_rsi,
                'bb_upper': bb_upper,
                'bb_lower': bb_lower,
                'bb_position': bb_position,
                # Trading signals
                'is_oversold': oversold,
                'is_overbought': overbought,
                'at_lower_bb': at_lower_bb,
                'at_upper_bb': at_upper_bb,
                # Additional fundamentals
                'avg_volume': avg_volume,
                'beta': info.get('beta'),
                'forward_pe': info.get('forwardPE'),
                'price_to_book': info.get('priceToBook'),
                'dividend_yield': info.get('dividendYield'),
            }

        except Exception as e:
            print(f"  ⚠️  Error fetching Yahoo data for ${ticker}: {str(e)[:50]}")
            return None

    def combine_data(self, reddit_stocks: List[Dict]) -> List[Dict]:
        """Combine Reddit and Yahoo data"""
        print()
        print("=" * 70)
        print("💰 PHASE 2: YAHOO FINANCE FUNDAMENTAL ANALYSIS")
        print("=" * 70)
        print()
        print(f"Fetching Yahoo Finance data for top {len(reddit_stocks)} stocks...")
        print("(2-second delay between requests to respect rate limits)")
        print()

        combined_data = []

        for idx, reddit_stock in enumerate(reddit_stocks, 1):
            ticker = reddit_stock['ticker']
            print(f"[{idx}/{len(reddit_stocks)}] Fetching ${ticker}...", end=" ")

            yahoo_data = self.get_yahoo_data(ticker)

            if yahoo_data:
                # Combine Reddit and Yahoo data
                combined = {
                    **reddit_stock,  # Reddit data (mentions, sentiment, etc.)
                    **yahoo_data,    # Yahoo data (price, fundamentals, etc.)
                }
                combined_data.append(combined)
                print(f"✓ ${yahoo_data['current_price']:.2f}")
            else:
                print("✗ No data")

        print()
        print(f"✓ Successfully fetched data for {len(combined_data)}/{len(reddit_stocks)} stocks")
        print()

        return combined_data

    def calculate_combined_score(self, stock: Dict) -> float:
        """Calculate a combined momentum score using both Reddit and Yahoo data"""

        # Reddit metrics (0-100 scale)
        reddit_score = stock['momentum_score']  # Already calculated

        # Yahoo metrics
        price_momentum = max(0, min(100, stock.get('price_change_30d', 0) * 2))  # Price change (capped)
        volume_momentum = max(0, min(100, stock.get('volume_change', 0)))  # Volume change

        # Volatility penalty (high volatility = higher risk)
        volatility_penalty = stock.get('volatility', 0) * 0.5

        # Combine scores with weights
        # 40% Reddit sentiment, 30% price momentum, 20% volume, 10% volatility penalty
        combined_score = (
            (reddit_score * 0.4) +
            (price_momentum * 0.3) +
            (volume_momentum * 0.2) -
            (volatility_penalty * 0.1)
        )

        return max(0, combined_score)  # Ensure non-negative

    def rank_stocks(self, combined_data: List[Dict]) -> List[Dict]:
        """Rank stocks by combined score"""
        for stock in combined_data:
            stock['combined_score'] = self.calculate_combined_score(stock)

        # Sort by combined score
        combined_data.sort(key=lambda x: x['combined_score'], reverse=True)

        return combined_data

    def print_detailed_stock_analysis(self, stock: Dict):
        """Print comprehensive analysis for a single stock"""
        print("=" * 70)
        print(f"🏆 #1 STOCK: ${stock['ticker']} - DETAILED ANALYSIS")
        print("=" * 70)
        print()

        # Basic info
        print(f"💰 CURRENT PRICE: ${stock['current_price']:.2f}")
        if stock.get('market_cap'):
            market_cap_b = stock['market_cap'] / 1e9
            print(f"📊 MARKET CAP: ${market_cap_b:.2f}B")
        print(f"🏢 SECTOR: {stock.get('sector', 'N/A')}")
        print(f"🏭 INDUSTRY: {stock.get('industry', 'N/A')}")
        print()

        # Reddit metrics
        print("📱 REDDIT SOCIAL METRICS:")
        sentiment = "🚀 BULLISH" if stock['bullish_pct'] >= 60 else "🐻 BEARISH" if stock['bearish_pct'] >= 60 else "⚖️  NEUTRAL"
        print(f"   Mentions: {stock['mentions']} across {stock['subreddit_count']} subreddits")
        print(f"   Sentiment: {sentiment} ({stock['bullish_pct']:.0f}% bull / {stock['bearish_pct']:.0f}% bear)")
        print(f"   Reddit Momentum Score: {stock['momentum_score']:.1f}")
        print(f"   Subreddits: {', '.join(['r/' + s for s in stock['subreddits'][:5]])}")
        print()

        # Price momentum
        print("📈 PRICE MOMENTUM:")
        print(f"   30-Day Change: {stock['price_change_30d']:+.2f}%")
        print(f"   20-Day SMA: ${stock['sma_20']:.2f}")
        if stock.get('sma_50'):
            print(f"   50-Day SMA: ${stock['sma_50']:.2f}")
            trend = "Bullish" if stock['current_price'] > stock['sma_50'] else "Bearish"
            print(f"   Trend (vs 50-SMA): {trend}")
        print(f"   Distance from 20-SMA: {stock['distance_from_sma20']:+.2f}%")
        print()

        # Mean reversion indicators
        print("🎯 MEAN REVERSION ANALYSIS:")
        print(f"   RSI (14): {stock['rsi']:.1f}", end="")
        if stock['is_oversold']:
            print(" ⚠️  OVERSOLD (<30) - Potential Buy Signal!")
        elif stock['is_overbought']:
            print(" ⚠️  OVERBOUGHT (>70) - Potential Sell Signal!")
        else:
            print(" (Neutral)")

        print(f"   Bollinger Band Position: {stock['bb_position']:.0f}%", end="")
        if stock['at_lower_bb']:
            print(" ⚠️  At Lower Band - Oversold!")
        elif stock['at_upper_bb']:
            print(" ⚠️  At Upper Band - Overbought!")
        else:
            print()

        print(f"   Upper Bollinger Band: ${stock['bb_upper']:.2f}")
        print(f"   Lower Bollinger Band: ${stock['bb_lower']:.2f}")
        print()

        # Trading signal
        print("🚦 TRADING SIGNAL:")
        if stock['is_oversold'] or stock['at_lower_bb']:
            print("   ✅ MEAN REVERSION BUY SIGNAL")
            print("   Strategy: Stock appears oversold, may bounce back to mean")
            print("   Entry: Near current price")
            print(f"   Target: ${stock['sma_20']:.2f} (20-SMA)")
            print(f"   Stop Loss: ${stock['bb_lower'] * 0.98:.2f} (2% below lower BB)")
        elif stock['is_overbought'] or stock['at_upper_bb']:
            print("   ⛔ OVERBOUGHT - AVOID OR SELL")
            print("   Strategy: Stock appears overbought, may revert to mean")
        else:
            print("   ⚖️  NEUTRAL - No clear mean reversion signal")
        print()

        # Volume & volatility
        print("📊 VOLUME & VOLATILITY:")
        print(f"   Volume Change: {stock['volume_change']:+.2f}%")
        print(f"   Average Volume: {stock['avg_volume']:,.0f}")
        print(f"   Volatility: {stock['volatility']:.2f}%")
        if stock.get('beta'):
            print(f"   Beta: {stock['beta']:.2f}")
        print()

        # 52-week range
        print("📅 52-WEEK RANGE:")
        if stock.get('52w_high') and stock.get('52w_low'):
            print(f"   High: ${stock['52w_high']:.2f}")
            print(f"   Low: ${stock['52w_low']:.2f}")
            if stock.get('52w_range_position'):
                print(f"   Current Position: {stock['52w_range_position']:.0f}% of range")
        print()

        # Valuation
        print("💎 VALUATION METRICS:")
        if stock.get('pe_ratio'):
            print(f"   P/E Ratio (TTM): {stock['pe_ratio']:.2f}")
        if stock.get('forward_pe'):
            print(f"   Forward P/E: {stock['forward_pe']:.2f}")
        if stock.get('price_to_book'):
            print(f"   Price/Book: {stock['price_to_book']:.2f}")
        if stock.get('dividend_yield'):
            print(f"   Dividend Yield: {stock['dividend_yield']*100:.2f}%")
        print()

        print("=" * 70)
        print()

    def print_combined_report(self, ranked_stocks: List[Dict]):
        """Print final ranked report with detailed #1 stock analysis"""
        print("=" * 70)
        print("🚀 PHASE 3: COMBINED RANKING & RECOMMENDATIONS")
        print("=" * 70)
        print()
        print("Ranking Methodology:")
        print("  • 40% Reddit Momentum (mentions × sentiment × diversity)")
        print("  • 30% Price Momentum (30-day price change)")
        print("  • 20% Volume Momentum (volume increase)")
        print("  • -10% Volatility Penalty (risk adjustment)")
        print()

        # Print detailed analysis for #1 stock
        if ranked_stocks:
            top_stock = ranked_stocks[0]
            self.print_detailed_stock_analysis(top_stock)

        print("=" * 70)
        print("TOP 10 STOCKS - COMBINED ANALYSIS")
        print("=" * 70)
        print()

        for idx, stock in enumerate(ranked_stocks, 1):
            sentiment = self.reddit_scraper.get_sentiment_emoji(
                stock['bullish_pct'],
                stock['bearish_pct']
            )

            print(f"{idx}. ${stock['ticker']} - Combined Score: {stock['combined_score']:.1f}")
            print(f"   Current Price: ${stock['current_price']:.2f}")

            if stock.get('market_cap'):
                market_cap_b = stock['market_cap'] / 1e9
                print(f"   Market Cap: ${market_cap_b:.2f}B")

            print(f"   Sector: {stock.get('sector', 'N/A')} | Industry: {stock.get('industry', 'N/A')}")
            print()

            print(f"   📊 REDDIT METRICS:")
            print(f"      Mentions: {stock['mentions']} across {stock['subreddit_count']} subreddits")
            print(f"      Sentiment: {sentiment} ({stock['bullish_pct']:.0f}% bull / {stock['bearish_pct']:.0f}% bear)")
            print(f"      Reddit Momentum: {stock['momentum_score']:.1f}")
            print()

            print(f"   💰 YAHOO FINANCE METRICS:")
            print(f"      30-Day Price Change: {stock['price_change_30d']:+.2f}%")
            print(f"      Volume Change: {stock['volume_change']:+.2f}%")
            print(f"      Volatility: {stock['volatility']:.2f}%")

            if stock.get('pe_ratio'):
                print(f"      P/E Ratio: {stock['pe_ratio']:.2f}")

            if stock.get('52w_high') and stock.get('52w_low'):
                current = stock['current_price']
                high = stock['52w_high']
                low = stock['52w_low']
                range_pct = ((current - low) / (high - low)) * 100
                print(f"      52-Week Range: ${low:.2f} - ${high:.2f} (currently at {range_pct:.0f}%)")

            print()

        print("=" * 70)
        print()

    def generate_summary(self, ranked_stocks: List[Dict]):
        """Generate executive summary"""
        print("=" * 70)
        print("📋 EXECUTIVE SUMMARY")
        print("=" * 70)
        print()

        # Best momentum stock
        best_momentum = ranked_stocks[0]
        print(f"🏆 BEST COMBINED MOMENTUM: ${best_momentum['ticker']}")
        print(f"   Score: {best_momentum['combined_score']:.1f}")
        print(f"   {best_momentum['bullish_pct']:.0f}% bullish on Reddit, {best_momentum['price_change_30d']:+.1f}% price change")
        print()

        # Most mentioned
        most_mentioned = max(ranked_stocks, key=lambda x: x['mentions'])
        print(f"🔥 MOST MENTIONED: ${most_mentioned['ticker']}")
        print(f"   {most_mentioned['mentions']} mentions across {most_mentioned['subreddit_count']} subreddits")
        print()

        # Best price performer
        best_price = max(ranked_stocks, key=lambda x: x.get('price_change_30d', -999))
        print(f"📈 BEST PRICE PERFORMANCE: ${best_price['ticker']}")
        print(f"   {best_price['price_change_30d']:+.2f}% in last 30 days")
        print()

        # Highest sentiment
        best_sentiment = max(ranked_stocks, key=lambda x: x['bullish_pct'])
        print(f"🚀 HIGHEST BULLISH SENTIMENT: ${best_sentiment['ticker']}")
        print(f"   {best_sentiment['bullish_pct']:.0f}% bullish on Reddit")
        print()

        print("=" * 70)
        print()


def main():
    """Main execution"""
    print()
    print("=" * 70)
    print("🐧 PENGUIN: Combined Reddit + Yahoo Finance Analysis")
    print("=" * 70)
    print()

    # Initialize scraper
    scraper = CombinedRedditYahooScraper()

    # Phase 1: Get top stocks from Reddit
    reddit_top_stocks = scraper.get_reddit_top_stocks(limit=10)

    # Phase 2: Get Yahoo Finance data
    combined_data = scraper.combine_data(reddit_top_stocks)

    # Phase 3: Rank by combined score
    ranked_stocks = scraper.rank_stocks(combined_data)

    # Print report
    scraper.print_combined_report(ranked_stocks)

    # Print summary
    scraper.generate_summary(ranked_stocks)

    print("✓ Analysis complete!")
    print()
    print("Next steps:")
    print("  • Integrate Claude AI for thesis generation")
    print("  • Add technical indicators (RSI, MACD, etc.)")
    print("  • Build real-time monitoring dashboard")
    print("  • Implement backtesting framework")
    print()


if __name__ == '__main__':
    main()
