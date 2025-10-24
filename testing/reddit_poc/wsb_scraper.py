"""
Proof of Concept: r/wallstreetbets Reddit Scraper
Combs through top posts to extract stock mentions and sentiment
combs thru 100 posts, lists top 20 stocks and their momentum
"""

import praw
import re
from datetime import datetime
import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials (you'll need to create these)
# Visit https://www.reddit.com/prefs/apps to create an app
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', 'your_client_id_here')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret_here')
REDDIT_USER_AGENT = 'PENGUIN Stock Tracker v0.1'


class WSBScraper:
    """Scrape r/wallstreetbets for stock mentions"""

    def __init__(self):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Common stock ticker pattern (1-5 capital letters)
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')

        # Words to exclude (common false positives)
        self.exclude_words = {
            'A', 'I', 'DD', 'YOLO', 'WSB', 'CEO', 'CFO', 'IPO', 'ETF',
            'ATH', 'ATL', 'IMO', 'FYI', 'FOMO', 'TA', 'PE', 'EPS',
            'NYSE', 'NASDAQ', 'SEC', 'IRS', 'US', 'UK', 'EU', 'IT',
            'AM', 'PM', 'EST', 'PST', 'OK', 'LOL', 'OMG', 'WTF',
            'EDIT', 'TLDR', 'TL', 'DR', 'OR', 'AND', 'THE', 'FOR'
        }

    def extract_tickers(self, text: str) -> List[str]:
        """Extract potential stock tickers from text"""
        if not text:
            return []

        # Find all potential tickers
        potential_tickers = self.ticker_pattern.findall(text)

        # Filter out excluded words and duplicates
        tickers = [
            ticker for ticker in potential_tickers
            if ticker not in self.exclude_words
        ]

        return tickers

    def analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis (bullish/bearish/neutral)"""
        if not text:
            return 'neutral'

        text_lower = text.lower()

        # Bullish indicators
        bullish_words = [
            'moon', 'rocket', 'buy', 'calls', 'bullish', 'pump',
            'rally', 'squeeze', 'tendies', 'gains', 'up', 'long',
            'green', 'breakout', 'support', 'diamond hands'
        ]

        # Bearish indicators
        bearish_words = [
            'crash', 'dump', 'puts', 'bearish', 'short', 'down',
            'red', 'sell', 'drop', 'fall', 'tank', 'rekt',
            'rug pull', 'bag holder', 'dead cat'
        ]

        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)

        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'

    def scrape_hot_posts(self, limit: int = 50) -> List[Dict]:
        """Scrape hot posts from r/wallstreetbets"""
        print(f"Fetching top {limit} hot posts from r/wallstreetbets...")

        subreddit = self.reddit.subreddit('wallstreetbets')
        posts = []

        for submission in subreddit.hot(limit=limit):
            # Skip stickied posts
            if submission.stickied:
                continue

            # Extract tickers from title and selftext
            title_tickers = self.extract_tickers(submission.title)
            body_tickers = self.extract_tickers(submission.selftext)
            all_tickers = title_tickers + body_tickers

            # Sentiment analysis
            combined_text = f"{submission.title} {submission.selftext}"
            sentiment = self.analyze_sentiment(combined_text)

            post_data = {
                'title': submission.title,
                'author': str(submission.author),
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'num_comments': submission.num_comments,
                'created_utc': datetime.fromtimestamp(submission.created_utc),
                'url': submission.url,
                'tickers': all_tickers,
                'sentiment': sentiment,
                'awards': submission.total_awards_received
            }

            posts.append(post_data)

        print(f"✓ Scraped {len(posts)} posts")
        return posts

    def analyze_mentions(self, posts: List[Dict]) -> Dict[str, Dict]:
        """Analyze ticker mentions across all posts"""
        ticker_data = {}

        for post in posts:
            for ticker in post['tickers']:
                if ticker not in ticker_data:
                    ticker_data[ticker] = {
                        'mention_count': 0,
                        'total_score': 0,
                        'total_comments': 0,
                        'bullish_count': 0,
                        'bearish_count': 0,
                        'neutral_count': 0,
                        'posts': []
                    }

                ticker_data[ticker]['mention_count'] += 1
                ticker_data[ticker]['total_score'] += post['score']
                ticker_data[ticker]['total_comments'] += post['num_comments']

                # Track sentiment
                if post['sentiment'] == 'bullish':
                    ticker_data[ticker]['bullish_count'] += 1
                elif post['sentiment'] == 'bearish':
                    ticker_data[ticker]['bearish_count'] += 1
                else:
                    ticker_data[ticker]['neutral_count'] += 1

                # Store reference to post
                ticker_data[ticker]['posts'].append({
                    'title': post['title'],
                    'score': post['score'],
                    'sentiment': post['sentiment']
                })

        return ticker_data

    def get_trending_stocks(self, ticker_data: Dict, min_mentions: int = 3) -> List[Tuple[str, Dict]]:
        """Get trending stocks sorted by mention count"""
        # Filter by minimum mentions
        filtered = {
            ticker: data
            for ticker, data in ticker_data.items()
            if data['mention_count'] >= min_mentions
        }

        # Sort by mention count (descending)
        sorted_tickers = sorted(
            filtered.items(),
            key=lambda x: x[1]['mention_count'],
            reverse=True
        )

        return sorted_tickers

    def print_report(self, posts: List[Dict], ticker_data: Dict):
        """Print analysis report"""
        print("\n" + "="*70)
        print("r/WALLSTREETBETS ANALYSIS REPORT")
        print("="*70)
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Posts Analyzed: {len(posts)}")
        print(f"Unique Tickers Found: {len(ticker_data)}")

        # Get trending stocks
        trending = self.get_trending_stocks(ticker_data, min_mentions=3)

        print("\n" + "-"*70)
        print("TOP TRENDING STOCKS (Min 3 mentions)")
        print("-"*70)

        for i, (ticker, data) in enumerate(trending[:20], 1):
            # Calculate sentiment ratio
            total_sentiment = data['bullish_count'] + data['bearish_count'] + data['neutral_count']
            bullish_pct = (data['bullish_count'] / total_sentiment * 100) if total_sentiment > 0 else 0
            bearish_pct = (data['bearish_count'] / total_sentiment * 100) if total_sentiment > 0 else 0

            # Determine overall sentiment
            if bullish_pct > bearish_pct + 20:
                sentiment_indicator = "🚀 BULLISH"
            elif bearish_pct > bullish_pct + 20:
                sentiment_indicator = "🐻 BEARISH"
            else:
                sentiment_indicator = "⚖️  NEUTRAL"

            avg_score = data['total_score'] / data['mention_count']

            print(f"\n{i}. ${ticker}")
            print(f"   Mentions: {data['mention_count']}")
            print(f"   Avg Score: {avg_score:.1f} upvotes")
            print(f"   Sentiment: {sentiment_indicator} ({bullish_pct:.0f}% bull / {bearish_pct:.0f}% bear)")
            print(f"   Total Comments: {data['total_comments']}")

            # Show top post for this ticker
            top_post = max(data['posts'], key=lambda x: x['score'])
            print(f"   Top Post: \"{top_post['title'][:60]}...\" ({top_post['score']} upvotes)")

        print("\n" + "="*70)

        # Momentum analysis
        print("\nMOMENTUM SIGNALS (Stocks mentioned 5+ times):")
        print("-"*70)
        high_momentum = [
            (ticker, data) for ticker, data in trending
            if data['mention_count'] >= 5
        ]

        for ticker, data in high_momentum[:10]:
            bullish_pct = (data['bullish_count'] / data['mention_count'] * 100)
            momentum_score = data['mention_count'] * (1 + bullish_pct/100)
            print(f"${ticker}: {data['mention_count']} mentions, "
                  f"{bullish_pct:.0f}% bullish, "
                  f"Momentum Score: {momentum_score:.1f}")

        print("\n" + "="*70)


def main():
    """Main execution"""
    print("PENGUIN Stock Tracker - WSB Proof of Concept")
    print("="*70)

    # Check if credentials are set
    if REDDIT_CLIENT_ID == 'your_client_id_here':
        print("\n⚠️  WARNING: Reddit API credentials not set!")
        print("\nTo use this script:")
        print("1. Go to https://www.reddit.com/prefs/apps")
        print("2. Click 'Create App' or 'Create Another App'")
        print("3. Choose 'script' as the app type")
        print("4. Set redirect URI to http://localhost:8080")
        print("5. Copy the client ID and secret")
        print("6. Set environment variables:")
        print("   export REDDIT_CLIENT_ID='your_client_id'")
        print("   export REDDIT_CLIENT_SECRET='your_secret'")
        print("\nOr edit this file and replace the placeholder values.\n")
        return

    try:
        # Initialize scraper
        scraper = WSBScraper()

        # Scrape hot posts
        posts = scraper.scrape_hot_posts(limit=100)

        # Analyze mentions
        ticker_data = scraper.analyze_mentions(posts)

        # Print report
        scraper.print_report(posts, ticker_data)

        print("\n✓ Analysis complete!")
        print("\nThis proof of concept demonstrates:")
        print("  - Reddit API integration")
        print("  - Ticker extraction from posts")
        print("  - Basic sentiment analysis")
        print("  - Mention counting and ranking")
        print("  - Momentum signal detection")
        print("\nNext steps: Integrate into PENGUIN architecture with proper storage,")
        print("historical tracking, and Claude AI analysis!\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. You have PRAW installed: pip install praw")
        print("2. Your Reddit API credentials are correct")
        print("3. You have internet connection\n")


if __name__ == '__main__':
    main()
