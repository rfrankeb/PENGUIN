"""Global constants for PENGUIN"""

from enum import Enum


class DataCategory(Enum):
    """Categories of data sources"""
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
    """How often to collect data from a source"""
    REALTIME = "realtime"        # WebSocket/streaming
    HIGH = "high"                 # Every 1-5 minutes
    MEDIUM = "medium"             # Every 15-60 minutes
    LOW = "low"                   # Every 1-24 hours
    ON_DEMAND = "on_demand"       # Triggered by events


class SignalType(Enum):
    """Types of investment signals"""
    MOMENTUM_SPIKE = "momentum_spike"
    SENTIMENT_SHIFT = "sentiment_shift"
    VOLUME_ANOMALY = "volume_anomaly"
    OPTIONS_FLOW = "options_flow"
    INSIDER_CLUSTER = "insider_cluster"
    CONGRESSIONAL_BUY = "congressional_buy"
    MEAN_REVERSION = "mean_reversion"
    PATTERN_BREAKOUT = "pattern_breakout"
    EARNINGS_SURPRISE = "earnings_surprise"
    SHORT_SQUEEZE = "short_squeeze"
    DARK_POOL_PRINT = "dark_pool_print"
    CORRELATION_DIVERGENCE = "correlation_divergence"
    GAMMA_SQUEEZE = "gamma_squeeze"
    SECTOR_ROTATION = "sector_rotation"
    FUNDAMENTAL_IMPROVEMENT = "fundamental_improvement"
    ALTERNATIVE_DATA_SPIKE = "alternative_data_spike"


# Stock ticker patterns to exclude (common false positives)
EXCLUDED_WORDS = {
    # Single letters
    'A', 'I', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z',

    # Common abbreviations & trading terms
    'DD', 'YOLO', 'WSB', 'CEO', 'CFO', 'IPO', 'ETF', 'ATH', 'ATL',
    'IMO', 'FYI', 'FOMO', 'TA', 'PE', 'EPS', 'AI', 'ML', 'AR', 'VR',
    'ICO', 'NFT', 'EOD', 'EOW', 'AH', 'PM', 'ITM', 'OTM', 'ATM',
    'IV', 'HV', 'VIX', 'SPY', 'QQQ', 'DIA', 'IWM',

    # Exchanges & organizations
    'NYSE', 'NASDAQ', 'SEC', 'IRS', 'FDA', 'FBI', 'CIA', 'FED',
    'FOMC', 'OPEC', 'IMF', 'WHO', 'UN', 'EU', 'GDP', 'CPI', 'PPI',

    # Countries/regions
    'US', 'UK', 'EU', 'IT', 'FR', 'DE', 'JP', 'CN', 'CA', 'AU',
    'IN', 'BR', 'RU', 'KR', 'MX', 'ES', 'NL', 'CH', 'SE', 'NO',

    # Time/date
    'AM', 'PM', 'EST', 'PST', 'CST', 'MST', 'GMT', 'UTC',
    'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN',
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',

    # Common words that look like tickers
    'OK', 'LOL', 'OMG', 'WTF', 'EDIT', 'TLDR', 'TL', 'DR', 'PS',
    'OR', 'AND', 'THE', 'FOR', 'NOW', 'NEW', 'GET', 'JUST', 'NEXT',
    'LIKE', 'WHEN', 'WHAT', 'ALL', 'OUT', 'SO', 'NO', 'YES', 'GOOD',
    'CAN', 'DO', 'GO', 'NOT', 'BUT', 'ARE', 'WAS', 'IS', 'BE', 'BEING',
    'TO', 'OF', 'IN', 'ON', 'AT', 'BY', 'AS', 'AN', 'IF', 'IT', 'WITH',
    'MY', 'HE', 'SHE', 'WE', 'ME', 'HIM', 'HER', 'WHO', 'WHY', 'THEM',
    'HOW', 'VERY', 'TOO', 'ONLY', 'BOTH', 'EACH', 'FEW', 'MORE', 'MOST',
    'SOME', 'ANY', 'MANY', 'MUCH', 'SUCH', 'SAME', 'THESE', 'THOSE',
    'FROM', 'INTO', 'THAN', 'THEN', 'ONCE', 'HERE', 'THERE', 'WHERE',
    'ALSO', 'BEEN', 'HAVE', 'HAS', 'HAD', 'DOES', 'DID', 'WILL', 'WOULD',
    'COULD', 'SHOULD', 'MAY', 'MIGHT', 'MUST', 'CAN', 'CANT',
    'DONT', 'WONT', 'ISNT', 'ARENT', 'WASNT', 'WERENT',

    # Reddit/WSB specific
    'MOON', 'HOLD', 'BUY', 'SELL', 'CALL', 'PUT', 'BULL', 'BEAR',
    'LONG', 'SHORT', 'PUMP', 'DUMP', 'DIP', 'RIP', 'TANK', 'MEGA',
    'HUGE', 'BIG', 'GAIN', 'LOSS', 'WIN', 'FAIL', 'EPIC', 'LIFE',
    'NEXT', 'NEED', 'WANT', 'HELP', 'MAKE', 'MOVE', 'PLAY', 'WEEK',
    'YEAR', 'LAST', 'BEST', 'WORST', 'EVER', 'STILL', 'WELL', 'BACK',
    'EVEN', 'DOWN', 'TILL', 'OVER', 'BOTH', 'UNDER', 'WHILE', 'ABOUT',
}
