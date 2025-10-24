"""
Demo script showing what the 98 technical indicators look like with sample data
"""

def display_demo_indicators():
    print("="*80)
    print("YAHOO FINANCE - 98 TECHNICAL INDICATORS (DEMO)")
    print("="*80)
    print("\nThis is a demo showing the format of all 98 indicators")
    print("(Yahoo Finance API is currently unavailable)")
    print()

    # Sample indicator values
    indicators = {
        # TREND INDICATORS (13)
        'sma_5': 261.22,
        'sma_10': 255.06,
        'sma_20': 255.04,
        'sma_50': 248.33,
        'sma_200': 210.45,
        'ema_9': 263.11,
        'ema_12': 262.05,
        'ema_26': 258.44,
        'price_vs_sma20': 3.15,
        'price_vs_sma200': 25.02,
        'macd': 4.46,
        'macd_signal': 3.21,
        'adx': 25.07,

        # MOMENTUM INDICATORS (12)
        'rsi_14': 62.34,
        'rsi_status': 'neutral',
        'stoch_k': 58.23,
        'stoch_d': 54.12,
        'stoch_signal': 'neutral',
        'williams_r': -41.77,
        'roc_10d': 4.23,
        'roc_20d': 8.91,
        'cci': 45.67,
        'momentum_10d': 11.50,
        'tsi': 23.45,
        'uo': 56.78,

        # VOLATILITY INDICATORS (15)
        'bb_upper': 267.89,
        'bb_middle': 255.04,
        'bb_lower': 242.19,
        'bb_width': 25.70,
        'bb_percent_b': 0.62,
        'bb_squeeze': True,  # ⚡ Breakout potential!
        'atr_14': 5.11,
        'volatility_10d': 18.45,
        'volatility_30d': 22.31,
        'volatility_level': 'moderate',
        'keltner_upper': 265.34,
        'keltner_middle': 255.04,
        'keltner_lower': 244.74,
        'donchian_upper': 268.50,
        'donchian_lower': 241.20,

        # VOLUME INDICATORS (14)
        'volume_current': 51234567,
        'volume_avg_10d': 48231445,
        'volume_ratio_10day': 1.06,
        'volume_spike': False,
        'obv': 1234567890,
        'obv_trend': 'rising',
        'cmf': 0.15,
        'mfi': 58.23,
        'volume_profile_high': 255.00,
        'volume_profile_low': 250.00,
        'vwap': 256.78,
        'ad_line': 2345678,
        'ease_of_movement': 0.023,
        'force_index': 234567,

        # PRICE PATTERNS (7)
        'support_level': 250.00,
        'resistance_level': 270.00,
        'distance_to_support': 5.05,
        'distance_to_resistance': 6.95,
        'consolidation_detected': False,
        'price_channel_position': 0.65,
        'pivot_point': 257.50,

        # RETURNS & STATISTICS (10)
        'return_1d': 0.52,
        'return_5d': 2.34,
        'return_10d': 4.23,
        'return_20d': 8.91,
        'return_50d': 12.45,
        'volatility_10d_pct': 18.45,
        'sharpe_ratio_20d': 1.85,
        'z_score': 0.45,
        'correlation_spy': 0.78,
        'beta': 1.12,

        # FIBONACCI LEVELS (7)
        'fib_0': 241.20,
        'fib_236': 247.54,
        'fib_382': 251.62,
        'fib_500': 254.85,
        'fib_618': 258.09,
        'fib_786': 262.63,
        'fib_100': 268.50,

        # ADVANCED INDICATORS (20)
        'ichimoku_tenkan': 259.85,
        'ichimoku_kijun': 252.75,
        'ichimoku_senkou_a': 256.30,
        'ichimoku_senkou_b': 248.90,
        'ichimoku_chikou': 263.05,
        'ichimoku_signal': 'bullish',
        'supertrend': 248.50,
        'supertrend_direction': 'up',
        'vortex_positive': 1.15,
        'vortex_negative': 0.85,
        'aroon_up': 85.71,
        'aroon_down': 14.29,
        'aroon_oscillator': 71.42,
        'pivot_classic': 257.50,
        'pivot_r1': 265.00,
        'pivot_r2': 270.00,
        'pivot_s1': 250.00,
        'pivot_s2': 245.00,
        'hull_ma': 262.35,
        'dema': 261.45,

        # METADATA
        'current_price': 263.05,
        'timestamp': '2025-10-24 14:30:00',
    }

    print("="*80)
    print(f"TECHNICAL ANALYSIS FOR AAPL")
    print("="*80)
    print(f"Current Price: ${indicators['current_price']:.2f}")
    print(f"Total Indicators: {len(indicators) - 2}")  # Exclude price and timestamp
    print()

    print("📈 TREND INDICATORS")
    print("-"*80)
    for key in ['sma_5', 'sma_10', 'sma_20', 'sma_50', 'sma_200', 'ema_9', 'ema_12', 'ema_26', 'price_vs_sma20', 'price_vs_sma200', 'macd', 'macd_signal', 'adx']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n⚡ MOMENTUM INDICATORS")
    print("-"*80)
    for key in ['rsi_14', 'rsi_status', 'stoch_k', 'stoch_d', 'stoch_signal', 'williams_r', 'roc_10d', 'roc_20d', 'cci', 'momentum_10d', 'tsi', 'uo']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n📊 VOLATILITY INDICATORS")
    print("-"*80)
    for key in ['bb_upper', 'bb_middle', 'bb_lower', 'bb_width', 'bb_percent_b', 'bb_squeeze', 'atr_14', 'volatility_10d', 'volatility_30d', 'volatility_level', 'keltner_upper', 'keltner_middle', 'keltner_lower', 'donchian_upper', 'donchian_lower']:
        if key in indicators:
            value = indicators[key]
            if key == 'bb_squeeze' and value:
                print(f"  {key:25s}: {value}  ⚡ BREAKOUT POTENTIAL!")
            else:
                print(f"  {key:25s}: {value}")

    print("\n📦 VOLUME INDICATORS")
    print("-"*80)
    for key in ['volume_current', 'volume_avg_10d', 'volume_ratio_10day', 'volume_spike', 'obv', 'obv_trend', 'cmf', 'mfi', 'volume_profile_high', 'volume_profile_low', 'vwap', 'ad_line', 'ease_of_movement', 'force_index']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n📍 PRICE PATTERNS")
    print("-"*80)
    for key in ['support_level', 'resistance_level', 'distance_to_support', 'distance_to_resistance', 'consolidation_detected', 'price_channel_position', 'pivot_point']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n📉 RETURNS & STATISTICS")
    print("-"*80)
    for key in ['return_1d', 'return_5d', 'return_10d', 'return_20d', 'return_50d', 'volatility_10d_pct', 'sharpe_ratio_20d', 'z_score', 'correlation_spy', 'beta']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n🔢 FIBONACCI LEVELS")
    print("-"*80)
    for key in ['fib_0', 'fib_236', 'fib_382', 'fib_500', 'fib_618', 'fib_786', 'fib_100']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n🚀 ADVANCED INDICATORS")
    print("-"*80)
    for key in ['ichimoku_tenkan', 'ichimoku_kijun', 'ichimoku_senkou_a', 'ichimoku_senkou_b', 'ichimoku_chikou', 'ichimoku_signal', 'supertrend', 'supertrend_direction', 'vortex_positive', 'vortex_negative', 'aroon_up', 'aroon_down', 'aroon_oscillator', 'pivot_classic', 'pivot_r1', 'pivot_r2', 'pivot_s1', 'pivot_s2', 'hull_ma', 'dema']:
        if key in indicators:
            print(f"  {key:25s}: {indicators[key]}")

    print("\n" + "="*80)
    print("ALL INDICATOR KEYS:")
    print("="*80)
    sorted_keys = [k for k in sorted(indicators.keys()) if k not in ['current_price', 'timestamp']]
    for i, key in enumerate(sorted_keys, 1):
        print(f"  {i:2d}. {key}")

    print("\n" + "="*80)
    print("CODE LOCATIONS:")
    print("="*80)
    print("  Yahoo collector:    penguin/data/collectors/market_data/yahoo_finance.py")
    print("  Technical analysis: penguin/data/collectors/market_data/technical_analysis.py")
    print("  View script:        view_indicators.py")
    print("  This demo:          view_indicators_demo.py")
    print("\n" + "="*80)
    print("KEY INSIGHTS FROM SAMPLE DATA:")
    print("="*80)
    print("  ⚡ Bollinger Band Squeeze detected - potential breakout!")
    print("  📈 Price above all major moving averages - bullish trend")
    print("  ⚡ RSI at 62.34 - healthy uptrend, not overbought")
    print("  📊 Volume 1.06x average - normal activity")
    print("  🎯 Support at $250, Resistance at $270")
    print("  📈 20-day return: +8.91% - strong momentum")
    print("\n")

if __name__ == '__main__':
    display_demo_indicators()
