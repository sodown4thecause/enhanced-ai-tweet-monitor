import asyncio
import logging
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
import tweepy
import praw
from producthunt import ProductHunt
from datetime import datetime, timedelta
from ..models import Base, API, APIChange
from sqlalchemy.orm import Session

class SourceFetcher:
    def __init__(self, db: Session, config: Dict[str, Any]):
        self.db = db
        self.config = config
        self.setup_logging()
        self.setup_clients()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='source_fetcher.log'
        )
        self.logger = logging.getLogger('SourceFetcher')

    def setup_clients(self):
        """Initialize API clients for different sources."""
        # Twitter setup
        self.twitter_client = tweepy.Client(
            bearer_token=self.config['twitter_bearer_token'],
            consumer_key=self.config['twitter_api_key'],
            consumer_secret=self.config['twitter_api_secret'],
            access_token=self.config['twitter_access_token'],
            access_token_secret=self.config['twitter_access_token_secret']
        )

        # Reddit setup
        self.reddit_client = praw.Reddit(
            client_id=self.config['reddit_client_id'],
            client_secret=self.config['reddit_client_secret'],
            user_agent=self.config['reddit_user_agent']
        )

        # Product Hunt setup
        self.ph_client = ProductHunt(
            access_token=self.config['producthunt_access_token']
        )

    async def fetch_product_hunt(self) -> List[Dict[str, Any]]:
        """Fetch new AI tools from Product Hunt."""
        try:
            # Get today's posts
            posts = self.ph_client.get_posts()
            ai_tools = []
            
            for post in posts:
                if any(tag in post.tags for tag in ['ai', 'artificial-intelligence', 'machine-learning']):
                    ai_tools.append({
                        'name': post.name,
                        'description': post.tagline,
                        'url': post.redirect_url,
                        'source': 'producthunt',
                        'discovered_at': datetime.utcnow(),
                        'raw_data': post.to_dict()
                    })
            
            self.logger.info(f"Fetched {len(ai_tools)} AI tools from Product Hunt")
            return ai_tools
        except Exception as e:
            self.logger.error(f"Error fetching from Product Hunt: {str(e)}")
            return []

    async def fetch_reddit(self) -> List[Dict[str, Any]]:
        """Fetch AI tool discussions from Reddit."""
        try:
            subreddits = ['ArtificialIntelligence', 'aiTools', 'MachineLearning']
            ai_tools = []
            
            for subreddit_name in subreddits:
                subreddit = self.reddit_client.subreddit(subreddit_name)
                for submission in subreddit.new(limit=50):
                    if any(keyword in submission.title.lower() for keyword in ['ai tool', 'artificial intelligence', 'machine learning']):
                        ai_tools.append({
                            'name': submission.title,
                            'description': submission.selftext,
                            'url': submission.url,
                            'source': f'reddit/{subreddit_name}',
                            'discovered_at': datetime.utcnow(),
                            'raw_data': {
                                'score': submission.score,
                                'num_comments': submission.num_comments,
                                'created_utc': submission.created_utc
                            }
                        })
            
            self.logger.info(f"Fetched {len(ai_tools)} AI tools from Reddit")
            return ai_tools
        except Exception as e:
            self.logger.error(f"Error fetching from Reddit: {str(e)}")
            return []

    async def fetch_twitter(self) -> List[Dict[str, Any]]:
        """Fetch AI tool mentions from Twitter."""
        try:
            query = '(AI tool OR "artificial intelligence" OR "machine learning") -is:retweet'
            tweets = self.twitter_client.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            ai_tools = []
            for tweet in tweets.data or []:
                ai_tools.append({
                    'name': tweet.text[:100],  # Use first 100 chars as name
                    'description': tweet.text,
                    'url': f"https://twitter.com/user/status/{tweet.id}",
                    'source': 'twitter',
                    'discovered_at': datetime.utcnow(),
                    'raw_data': {
                        'metrics': tweet.public_metrics,
                        'created_at': tweet.created_at
                    }
                })
            
            self.logger.info(f"Fetched {len(ai_tools)} AI tools from Twitter")
            return ai_tools
        except Exception as e:
            self.logger.error(f"Error fetching from Twitter: {str(e)}")
            return []

    async def fetch_ai_directories(self) -> List[Dict[str, Any]]:
        """Fetch AI tools from various directories."""
        try:
            directories = [
                'https://www.futuretools.io/',
                'https://www.aitoolkit.org/',
                'https://www.aitoolguide.com/'
            ]
            
            ai_tools = []
            async with aiohttp.ClientSession() as session:
                for directory in directories:
                    try:
                        async with session.get(directory) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                
                                # Extract tools (this will need to be customized per directory)
                                tools = soup.find_all('div', class_='tool-card')  # Example selector
                                for tool in tools:
                                    ai_tools.append({
                                        'name': tool.find('h2').text.strip(),
                                        'description': tool.find('p').text.strip(),
                                        'url': tool.find('a')['href'],
                                        'source': directory,
                                        'discovered_at': datetime.utcnow(),
                                        'raw_data': {
                                            'html': str(tool)
                                        }
                                    })
                    except Exception as e:
                        self.logger.error(f"Error fetching from {directory}: {str(e)}")
            
            self.logger.info(f"Fetched {len(ai_tools)} AI tools from directories")
            return ai_tools
        except Exception as e:
            self.logger.error(f"Error fetching from AI directories: {str(e)}")
            return []

    async def fetch_all_sources(self) -> List[Dict[str, Any]]:
        """Fetch data from all sources concurrently."""
        tasks = [
            self.fetch_product_hunt(),
            self.fetch_reddit(),
            self.fetch_twitter(),
            self.fetch_ai_directories()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and filter out exceptions
        all_tools = []
        for result in results:
            if isinstance(result, list):
                all_tools.extend(result)
            else:
                self.logger.error(f"Error in fetch task: {str(result)}")
        
        # Save to database
        for tool in all_tools:
            try:
                existing_tool = self.db.query(API).filter_by(url=tool['url']).first()
                if existing_tool:
                    # Update existing tool
                    for key, value in tool.items():
                        if hasattr(existing_tool, key):
                            setattr(existing_tool, key, value)
                else:
                    # Create new tool
                    new_tool = API(**tool)
                    self.db.add(new_tool)
                
                self.db.commit()
            except Exception as e:
                self.logger.error(f"Error saving tool {tool.get('name', 'unknown')}: {str(e)}")
                self.db.rollback()
        
        return all_tools 