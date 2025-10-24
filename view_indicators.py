"""
Script to view all 98 technical indicators from Yahoo Finance collector
"""

import asyncio
from penguin.data.registry import registry

async def main():
    print("="*80)
    print("YAHOO FINANCE - 98 TECHNICAL INDICATORS")
    print("="*80)

    # Discover collectors
    registry.auto_discover()

    # Get Yahoo Finance collector
    collector = registry.get_collector('yahoo_finance')

    # Collect data with technical indicators
    print("\nFetching data from Yahoo Finance...")
    data = await collector.collect(
        symbols=['AAPL'],
        period='3mo',
        interval='1d',
        include_technicals=True,
        include_info=False
    )

    print(f"Collected {len(data)} total data points\n")

    # Find technical analysis data point
    for point in data:
        if point.get('data_type') == 'technical_analysis':
            symbol = point['symbol']
            price = point['value']
            indicators = point['metadata']

            print("="*80)
            print(f"TECHNICAL ANALYSIS FOR {symbol}")
            print("="*80)
            print(f"Current Price: ${price:.2f}")
            print(f"Total Indicators: {len(indicators)}")
            print()

            # Show all indicators organized by category
            print("📈 TREND INDICATORS")
            print("-"*80)
            for key in ['sma_5', 'sma_10', 'sma_20', 'sma_50', 'sma_200', 'ema_9', 'ema_12', 'ema_26', 'price_vs_sma20', 'macd', 'macd_signal', 'adx']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n⚡ MOMENTUM INDICATORS")
            print("-"*80)
            for key in ['rsi_14', 'rsi_status', 'stoch_k', 'stoch_d', 'williams_r', 'cci']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n📊 VOLATILITY INDICATORS")
            print("-"*80)
            for key in ['bb_upper', 'bb_middle', 'bb_lower', 'bb_percent_b', 'bb_squeeze', 'atr_14', 'volatility_level']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n📦 VOLUME INDICATORS")
            print("-"*80)
            for key in ['volume_current', 'volume_ratio_10day', 'volume_spike', 'obv_trend', 'cmf', 'vwap']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n📍 PRICE PATTERNS")
            print("-"*80)
            for key in ['support_level', 'resistance_level', 'distance_to_support', 'distance_to_resistance']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n📉 RETURNS & STATISTICS")
            print("-"*80)
            for key in ['return_1d', 'return_5d', 'return_20d', 'volatility_10d', 'z_score']:
                if key in indicators:
                    print(f"  {key:20s}: {indicators[key]}")

            print("\n" + "="*80)
            print("ALL INDICATOR KEYS:")
            print("="*80)
            for i, key in enumerate(sorted(indicators.keys()), 1):
                print(f"  {i:2d}. {key}")

            print("\n" + "="*80)
            print("CODE LOCATIONS:")
            print("="*80)
            print("  Yahoo collector:    penguin/data/collectors/market_data/yahoo_finance.py")
            print("  Technical analysis: penguin/data/collectors/market_data/technical_analysis.py")
            print("  This script:        view_indicators.py")

            break

if __name__ == '__main__':
    asyncio.run(main())
