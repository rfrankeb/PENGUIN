
"""
Proof of Concept: Yahoo Finance Stock Data Scraper
Demonstrates fetching real-time stock data and basic analysis
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
import time


class YahooFinanceScraper:
    """Scrape Yahoo Finance for stock data and analysis"""

    def __init__(self):
        """Initialize scraper"""
        self.data_cache = {}

    def get_stock_info(self, ticker: str) -> Dict:
        """Get comprehensive stock information"""
        try:
            time.sleep(1)  # Rate limiting: 1 second between requests
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                'symbol': ticker,
                'name': info.get('longName', ticker),
                'price': info.get('currentPrice', info.get('regularMarketPrice')),
                'previous_close': info.get('previousClose'),
                'open': info.get('open'),
                'day_high': info.get('dayHigh'),
                'day_low': info.get('dayLow'),
                'volume': info.get('volume'),
                'avg_volume': info.get('averageVolume'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'eps': info.get('trailingEps'),
                'dividend_yield': info.get('dividendYield'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'sector': info.get('sector'),
                'industry': info.get('industry')
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def get_historical_data(self, ticker: str, period: str = '1mo') -> pd.DataFrame:
        """
        Get historical price data
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            time.sleep(1)  # Rate limiting: 1 second between requests
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None

    def calculate_momentum(self, ticker: str, days: int = 30) -> Dict:
        """Calculate momentum indicators"""
        hist = self.get_historical_data(ticker, period=f'{days}d')

        if hist is None or hist.empty:
            return None

        current_price = hist['Close'].iloc[-1]
        start_price = hist['Close'].iloc[0]

        # Calculate returns
        total_return = ((current_price - start_price) / start_price) * 100

        # Volume analysis
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].iloc[-5:].mean()
        volume_change = ((recent_volume - avg_volume) / avg_volume) * 100

        # Volatility
        volatility = hist['Close'].pct_change().std() * 100

        return {
            'ticker': ticker,
            'current_price': current_price,
            f'{days}d_return': total_return,
            'avg_volume': avg_volume,
            'recent_volume': recent_volume,
            'volume_change_pct': volume_change,
            'volatility': volatility,
            'days_analyzed': len(hist)
        }

    def analyze_multiple_stocks(self, tickers: List[str]) -> pd.DataFrame:
        """Analyze multiple stocks and compare"""
        results = []

        for ticker in tickers:
            print(f"Analyzing {ticker}...")
            momentum = self.calculate_momentum(ticker)

            if momentum:
                results.append(momentum)

        df = pd.DataFrame(results)
        return df.sort_values('30d_return', ascending=False)

    def detect_signals(self, ticker: str) -> Dict:
        """Detect trading signals based on simple technical analysis"""
        hist = self.get_historical_data(ticker, period='3mo')

        if hist is None or hist.empty:
            return None

        # Calculate moving averages
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()

        current_price = hist['Close'].iloc[-1]
        sma_20 = hist['SMA_20'].iloc[-1]
        sma_50 = hist['SMA_50'].iloc[-1]

        # RSI calculation (simplified)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # Determine signals
        signals = []

        # Moving average crossover
        if sma_20 > sma_50:
            signals.append("Bullish: 20-day MA above 50-day MA")
        else:
            signals.append("Bearish: 20-day MA below 50-day MA")

        # RSI signals
        if current_rsi < 30:
            signals.append("Oversold: RSI < 30 (potential buy)")
        elif current_rsi > 70:
            signals.append("Overbought: RSI > 70 (potential sell)")

        # Volume spike
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].iloc[-1]
        if recent_volume > avg_volume * 1.5:
            signals.append(f"Volume Spike: {recent_volume/avg_volume:.1f}x average")

        return {
            'ticker': ticker,
            'current_price': current_price,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': current_rsi,
            'signals': signals
        }


def main():
    """Main execution - Demo analysis"""
    print("="*70)
    print("PENGUIN Stock Tracker - Yahoo Finance Proof of Concept")
    print("="*70)
    print()

    scraper = YahooFinanceScraper()

    # Popular tickers to analyze (reduced for testing)
    tickers = ['AAPL']  # Just one stock to test

    print("Fetching stock data...\n")

    # 1. Get basic info for a few stocks
    print("-" * 70)
    print("STOCK INFORMATION")
    print("-" * 70)

    for ticker in tickers[:1]:
        print(f"Fetching info for {ticker}...")
        info = scraper.get_stock_info(ticker)
        if info:
            print(f"\n{info['name']} (${ticker})")
            print(f"  Price: ${info['price']:.2f}")
            print(f"  Market Cap: ${info['market_cap']:,}" if info['market_cap'] else "  Market Cap: N/A")
            print(f"  P/E Ratio: {info['pe_ratio']:.2f}" if info['pe_ratio'] else "  P/E Ratio: N/A")
            print(f"  Sector: {info['sector']}")

    # 2. Momentum analysis
    print("\n" + "=" * 70)
    print("MOMENTUM ANALYSIS (30-day returns)")
    print("=" * 70)

    momentum_df = scraper.analyze_multiple_stocks(tickers)
    print(momentum_df.to_string(index=False))

    # 3. Technical signals
    print("\n" + "=" * 70)
    print("TECHNICAL SIGNALS")
    print("=" * 70)

    for ticker in tickers[:1]:
        print(f"Analyzing signals for {ticker}...")
        signals_data = scraper.detect_signals(ticker)
        if signals_data:
            print(f"\n${ticker} - ${signals_data['current_price']:.2f}")
            print(f"  RSI: {signals_data['rsi']:.1f}")
            print(f"  SMA(20): ${signals_data['sma_20']:.2f}")
            print(f"  SMA(50): ${signals_data['sma_50']:.2f}")
            print("  Signals:")
            for signal in signals_data['signals']:
                print(f"    - {signal}")

    print("\n" + "=" * 70)
    print("\n✓ Analysis complete!")
    print("\nThis proof of concept demonstrates:")
    print("  - Yahoo Finance API integration (yfinance library)")
    print("  - Real-time stock price data")
    print("  - Historical data analysis")
    print("  - Momentum calculations (returns, volume, volatility)")
    print("  - Technical indicators (SMA, RSI)")
    print("  - Trading signal detection")
    print("\nNext steps: Integrate into PENGUIN for multi-source analysis!")
    print()


if __name__ == '__main__':
    main()
