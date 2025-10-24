"""
Multi-Subreddit Stock Scraper
Aggregates stock mentions across top investment subreddits
"""

import praw
import re
import time
from datetime import datetime
from typing import List, Dict
from collections import defaultdict
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', 'your_client_id_here')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret_here')
REDDIT_USER_AGENT = 'PENGUIN Stock Tracker v0.2 - Multi-Subreddit'


class MultiSubredditScraper:
    """Scrape multiple investment subreddits for stock mentions"""

    def __init__(self):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        # Top investment subreddits (from CLAUDE.md)
        self.subreddits = [
            'wallstreetbets',
            'pennystocks',
            'stocks',
            'investing',
            'options',
            'Daytrading',
            'SecurityAnalysis',
            'ValueInvesting',
            'Dividends',
            'StockMarket'
        ]

        # Common stock ticker pattern (1-5 capital letters)
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')

        # Words to exclude (common false positives)
        self.exclude_words = {
            # Single letters
            'A', 'I', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z',
            # Common abbreviations
            'DD', 'YOLO', 'WSB', 'CEO', 'CFO', 'IPO', 'ETF', 'ATH', 'ATL',
            'IMO', 'FYI', 'FOMO', 'TA', 'PE', 'EPS', 'AI', 'ML', 'AR', 'VR',
            'NYSE', 'NASDAQ', 'SEC', 'IRS', 'FDA', 'FBI', 'CIA',
            # Countries/regions
            'US', 'UK', 'EU', 'IT', 'FR', 'DE', 'JP', 'CN', 'CA', 'AU',
            # Time/date
            'AM', 'PM', 'EST', 'PST', 'CST', 'MST', 'GMT', 'UTC',
            # Common words
            'OK', 'LOL', 'OMG', 'WTF', 'EDIT', 'TLDR', 'TL', 'DR',
            'OR', 'AND', 'THE', 'FOR', 'NOW', 'NEW', 'GET', 'JUST',
            'LIKE', 'WHEN', 'WHAT', 'ALL', 'OUT', 'SO', 'NO', 'YES',
            'CAN', 'DO', 'GO', 'NOT', 'BUT', 'ARE', 'WAS', 'IS', 'BE',
            'TO', 'OF', 'IN', 'ON', 'AT', 'BY', 'AS', 'AN', 'IF', 'IT',
            'MY', 'HE', 'SHE', 'WE', 'ME', 'HIM', 'HER', 'WHO', 'WHY',
            'HOW', 'VERY', 'TOO', 'ONLY', 'BOTH', 'EACH', 'FEW', 'MORE',
            'MOST', 'SOME', 'SUCH', 'THAN', 'THAT', 'THESE', 'THOSE',
            'WILL', 'WITH', 'BEEN', 'HAVE', 'HAS', 'HAD', 'DOES', 'DID',
            'MADE', 'MAKE', 'MAY', 'MUST', 'NEED', 'ONLY', 'OWN', 'SAID',
            'SAME', 'SEE', 'SEEM', 'SHOULD', 'SINCE', 'STILL', 'TAKE',
            'THAN', 'THEM', 'THEN', 'THERE', 'THEY', 'THIS', 'THUS',
            'VERY', 'WANT', 'WELL', 'WERE', 'WHAT', 'WHEN', 'WHERE',
            'WHICH', 'WHILE', 'WOULD', 'YEAR', 'YOUR','COVID', 'USA',
            # Financial terms
            'ROI', 'ROE', 'FCF', 'EBITDA', 'YOY', 'QOQ', 'ATM', 'OTM', 'ITM',
            'DIV', 'YTD', 'USD', 'EUR', 'GBP', 'JPY', 'RMB', 'IRA', 'PT',
            # Reddit/Internet slang
            'AMA', 'ELI5', 'TIL', 'NSFW', 'SFW', 'OP', 'OC', 'FTFY',
            'IIRC', 'AFAIK', 'IMHO', 'IMO', 'SMH', 'TBH', 'LPT', 'EV',
            'UP'
        }

    def extract_tickers(self, text: str) -> List[str]:
        """Extract potential stock tickers from text"""
        if not text:
            return []

        potential_tickers = self.ticker_pattern.findall(text)
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

        bullish_words = [
            'moon', 'rocket', 'buy', 'calls', 'bullish', 'pump',
            'rally', 'squeeze', 'tendies', 'gains', 'up', 'long',
            'green', 'breakout', 'support', 'diamond hands', 'hodl',
            'to the moon', 'undervalued', 'great buy'
        ]

        bearish_words = [
            'crash', 'dump', 'puts', 'bearish', 'short', 'down',
            'red', 'sell', 'drop', 'fall', 'tank', 'rekt',
            'rug pull', 'bag holder', 'dead cat', 'overvalued'
        ]

        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)

        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'

    def scrape_subreddit(self, subreddit_name: str, limit: int = 100) -> List[Dict]:
        """Scrape posts from a single subreddit"""
        posts = []

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            for submission in subreddit.hot(limit=limit):
                # Skip stickied posts
                if submission.stickied:
                    continue

                post_text = f"{submission.title} {submission.selftext}"
                tickers = self.extract_tickers(post_text)

                if tickers:  # Only store posts with stock mentions
                    posts.append({
                        'subreddit': subreddit_name,
                        'title': submission.title,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'created_utc': submission.created_utc,
                        'tickers': tickers,
                        'sentiment': self.analyze_sentiment(post_text),
                        'url': f"https://reddit.com{submission.permalink}"
                    })

        except Exception as e:
            print(f"  ⚠️  Error scraping r/{subreddit_name}: {e}")

        return posts

    def scrape_all_subreddits(self, posts_per_sub: int = 100) -> Dict:
        """Scrape all configured subreddits"""
        print(f"🔍 Scraping {len(self.subreddits)} subreddits ({posts_per_sub} posts each)...")
        print("=" * 70)

        all_posts = []

        for idx, subreddit in enumerate(self.subreddits, 1):
            print(f"[{idx}/{len(self.subreddits)}] Scraping r/{subreddit}...", end=" ")

            posts = self.scrape_subreddit(subreddit, limit=posts_per_sub)
            all_posts.extend(posts)

            print(f"✓ Found {len(posts)} posts with stock mentions")

            # Rate limiting: sleep between requests to be respectful
            if idx < len(self.subreddits):
                time.sleep(3)  # 3 second delay between subreddits (safe for API limits)

        print()
        print(f"✓ Total posts collected: {len(all_posts)}")
        print("=" * 70)
        print()

        return all_posts

    def aggregate_stock_data(self, posts: List[Dict]) -> List[Dict]:
        """Aggregate all mentions of each stock across subreddits"""
        stock_data = defaultdict(lambda: {
            'mentions': 0,
            'total_score': 0,
            'total_comments': 0,
            'bullish_count': 0,
            'bearish_count': 0,
            'neutral_count': 0,
            'subreddits': set(),
            'top_post': None,
            'top_post_score': 0
        })

        # Aggregate data
        for post in posts:
            for ticker in post['tickers']:
                data = stock_data[ticker]
                data['mentions'] += 1
                data['total_score'] += post['score']
                data['total_comments'] += post['num_comments']
                data['subreddits'].add(post['subreddit'])

                # Track sentiment
                if post['sentiment'] == 'bullish':
                    data['bullish_count'] += 1
                elif post['sentiment'] == 'bearish':
                    data['bearish_count'] += 1
                else:
                    data['neutral_count'] += 1

                # Track top post
                if post['score'] > data['top_post_score']:
                    data['top_post_score'] = post['score']
                    data['top_post'] = {
                        'title': post['title'],
                        'score': post['score'],
                        'subreddit': post['subreddit'],
                        'url': post['url']
                    }

        # Calculate derived metrics
        results = []
        for ticker, data in stock_data.items():
            total_sentiment = data['bullish_count'] + data['bearish_count'] + data['neutral_count']

            bullish_pct = (data['bullish_count'] / total_sentiment * 100) if total_sentiment > 0 else 0
            bearish_pct = (data['bearish_count'] / total_sentiment * 100) if total_sentiment > 0 else 0

            # Momentum score: mentions × bullish% × subreddit diversity
            subreddit_multiplier = len(data['subreddits'])
            momentum_score = data['mentions'] * (bullish_pct / 100) * subreddit_multiplier

            results.append({
                'ticker': ticker,
                'mentions': data['mentions'],
                'avg_score': data['total_score'] / data['mentions'],
                'total_comments': data['total_comments'],
                'bullish_pct': bullish_pct,
                'bearish_pct': bearish_pct,
                'subreddit_count': len(data['subreddits']),
                'subreddits': list(data['subreddits']),
                'momentum_score': momentum_score,
                'top_post': data['top_post']
            })

        # Sort by momentum score
        results.sort(key=lambda x: x['momentum_score'], reverse=True)

        return results

    def get_sentiment_emoji(self, bullish_pct: float, bearish_pct: float) -> str:
        """Get emoji based on sentiment"""
        if bullish_pct >= 60:
            return "🚀 BULLISH"
        elif bearish_pct >= 60:
            return "🐻 BEARISH"
        else:
            return "⚖️  NEUTRAL"

    def print_report(self, top_stocks: List[Dict], top_n: int = 10):
        """Print formatted report of top stocks"""
        print("=" * 70)
        print("🐧 PENGUIN MULTI-SUBREDDIT STOCK ANALYSIS")
        print("=" * 70)
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Subreddits Analyzed: {len(self.subreddits)}")
        print(f"Unique Stocks Found: {len(top_stocks)}")
        print()
        print("-" * 70)
        print(f"TOP {top_n} STOCKS BY MOMENTUM")
        print("-" * 70)
        print()

        for idx, stock in enumerate(top_stocks[:top_n], 1):
            sentiment = self.get_sentiment_emoji(stock['bullish_pct'], stock['bearish_pct'])

            print(f"{idx}. ${stock['ticker']}")
            print(f"   Mentions: {stock['mentions']} across {stock['subreddit_count']} subreddits")
            print(f"   Subreddits: {', '.join(['r/' + s for s in stock['subreddits'][:5]])}")
            print(f"   Avg Score: {stock['avg_score']:.1f} upvotes")
            print(f"   Sentiment: {sentiment} ({stock['bullish_pct']:.0f}% bull / {stock['bearish_pct']:.0f}% bear)")
            print(f"   Total Comments: {stock['total_comments']:,}")
            print(f"   Momentum Score: {stock['momentum_score']:.1f}")

            if stock['top_post']:
                print(f"   Top Post: \"{stock['top_post']['title'][:60]}...\" ({stock['top_post']['score']} upvotes, r/{stock['top_post']['subreddit']})")

            print()

        print("=" * 70)
        print()
        print("✓ Analysis complete!")
        print()

    def print_summary_metrics(self, all_posts: List[Dict], top_stocks: List[Dict]):
        """Print summary metrics about the scraping session"""
        print("=" * 70)
        print("📊 SUMMARY METRICS")
        print("=" * 70)
        print()

        # Calculate metrics
        total_posts = len(all_posts)
        total_stocks = len(top_stocks)
        total_mentions = sum(stock['mentions'] for stock in top_stocks)
        total_upvotes = sum(post['score'] for post in all_posts)
        total_comments = sum(post['num_comments'] for post in all_posts)

        # Sentiment breakdown
        bullish_posts = sum(1 for post in all_posts if post['sentiment'] == 'bullish')
        bearish_posts = sum(1 for post in all_posts if post['sentiment'] == 'bearish')
        neutral_posts = sum(1 for post in all_posts if post['sentiment'] == 'neutral')

        # Stocks by sentiment
        highly_bullish = [s for s in top_stocks if s['bullish_pct'] >= 70]
        highly_bearish = [s for s in top_stocks if s['bearish_pct'] >= 70]

        # Subreddit distribution
        subreddit_post_counts = defaultdict(int)
        for post in all_posts:
            subreddit_post_counts[post['subreddit']] += 1

        # Top mentioned stocks
        top_5_stocks = top_stocks[:5]

        # Cross-subreddit stocks (mentioned in 5+ subreddits)
        cross_subreddit = [s for s in top_stocks if s['subreddit_count'] >= 5]

        print("📈 DATA COLLECTION:")
        print(f"   Total Posts Scraped: {total_posts:,}")
        print(f"   Total Stock Mentions: {total_mentions:,}")
        print(f"   Unique Stocks Found: {total_stocks:,}")
        print(f"   Total Upvotes: {total_upvotes:,}")
        print(f"   Total Comments: {total_comments:,}")
        print()

        print("🎭 SENTIMENT DISTRIBUTION:")
        print(f"   Bullish Posts: {bullish_posts} ({bullish_posts/total_posts*100:.1f}%)")
        print(f"   Bearish Posts: {bearish_posts} ({bearish_posts/total_posts*100:.1f}%)")
        print(f"   Neutral Posts: {neutral_posts} ({neutral_posts/total_posts*100:.1f}%)")
        print()
        print(f"   Highly Bullish Stocks (≥70%): {len(highly_bullish)}")
        print(f"   Highly Bearish Stocks (≥70%): {len(highly_bearish)}")
        print()

        print("🌐 SUBREDDIT BREAKDOWN:")
        for subreddit, count in sorted(subreddit_post_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   r/{subreddit}: {count} posts")
        print()

        print("🔥 TOP 5 MOST MENTIONED:")
        for idx, stock in enumerate(top_5_stocks, 1):
            print(f"   {idx}. ${stock['ticker']}: {stock['mentions']} mentions, {stock['bullish_pct']:.0f}% bullish")
        print()

        print("🌍 CROSS-SUBREDDIT TRENDING:")
        print(f"   Stocks mentioned in 5+ subreddits: {len(cross_subreddit)}")
        if cross_subreddit:
            for stock in cross_subreddit[:5]:
                print(f"   ${stock['ticker']}: {stock['subreddit_count']} subreddits, momentum: {stock['momentum_score']:.0f}")
        print()

        print("=" * 70)
        print()
        print("💡 KEY INSIGHTS:")
        print("  ✓ Multi-subreddit stock mention tracking")
        print("  ✓ Cross-community sentiment analysis")
        print("  ✓ Momentum scoring with subreddit diversity weighting")
        print("  ✓ Comprehensive data aggregation across investment communities")
        print()


def main():
    """Main execution"""
    print()
    print("=" * 70)
    print("🐧 PENGUIN Stock Tracker - Multi-Subreddit Aggregator")
    print("=" * 70)
    print()

    # Initialize scraper
    scraper = MultiSubredditScraper()

    # Scrape all subreddits
    all_posts = scraper.scrape_all_subreddits(posts_per_sub=100)

    # Aggregate stock data
    print("📊 Aggregating stock mentions across all subreddits...")
    top_stocks = scraper.aggregate_stock_data(all_posts)
    print(f"✓ Aggregated data for {len(top_stocks)} unique stocks")
    print()

    # Print report
    scraper.print_report(top_stocks, top_n=10)

    # Print summary metrics
    scraper.print_summary_metrics(all_posts, top_stocks)

    print("Next steps: Integrate with Yahoo Finance for price data,")
    print("add Claude AI analysis, and build momentum detection signals!")
    print()


if __name__ == '__main__':
    main()
