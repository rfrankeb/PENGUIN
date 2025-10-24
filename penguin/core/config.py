"""
Configuration management for PENGUIN
Loads settings from environment variables and config files
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


class Config:
    """Central configuration class"""

    # Project paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CONFIG_DIR = BASE_DIR / "config"

    # Reddit API
    # IMPORTANT: Set these in .env file, NOT here!
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PENGUIN Stock Tracker v0.1')

    # Options Flow APIs
    # IMPORTANT: Set these in .env file, NOT here!
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', '')
    UNUSUAL_WHALES_API_KEY = os.getenv('UNUSUAL_WHALES_API_KEY', '')
    TRADIER_API_KEY = os.getenv('TRADIER_API_KEY', '')

    # Insider & Congressional Trading APIs
    # IMPORTANT: Set these in .env file, NOT here!
    SEC_API_KEY = os.getenv('SEC_API_KEY', '')  # SEC-API.io for Form 4 filings
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')  # Finnhub congressional trades
    FMP_API_KEY = os.getenv('FMP_API_KEY', '')  # Financial Modeling Prep
    QUIVERQUANT_API_KEY = os.getenv('QUIVERQUANT_API_KEY', '')  # QuiverQuant (paid)

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/penguin')
    TIMESCALE_URL = os.getenv('TIMESCALE_URL', DATABASE_URL)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Claude AI
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

    # Data collection
    DEFAULT_COLLECTION_LIMIT = int(os.getenv('COLLECTION_LIMIT', '100'))
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'

    # Storage
    DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', '365'))
    CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', '300'))

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        required = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
        missing = [key for key in required if not getattr(cls, key)]

        if missing:
            print(f"Missing required configuration: {', '.join(missing)}")
            return False
        return True


config = Config()
