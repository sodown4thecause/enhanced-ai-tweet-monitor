from typing import List, Dict, Any
import tweepy
from .base import BaseFetcher
import logging
from ...utils.fetcher_utils import (
    RateLimiter,
    PaginationHelper,
    deduplicate_tools,
    enrich_tool_data,
    fetch_with_retry
)

class TwitterFetcher(BaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.setup_twitter_client()
        self.rate_limiter = RateLimiter(calls_per_second=0.1)  # 10 seconds between requests

    def setup_twitter_client(self):
        """Initialize Twitter API client."""
        try:
            auth = tweepy.OAuthHandler(
                self.config.get('TWITTER_API_KEY'),
                self.config.get('TWITTER_API_SECRET')
            )
            auth.set_access_token(
                self.config.get('TWITTER_ACCESS_TOKEN'),
                self.config.get('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            self.client = tweepy.Client(
                consumer_key=self.config.get('TWITTER_API_KEY'),
                consumer_secret=self.config.get('TWITTER_API_SECRET'),
                access_token=self.config.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=self.config.get('TWITTER_ACCESS_TOKEN_SECRET')
            )
        except Exception as e:
            self.logger.error(f"Error setting up Twitter client: {str(e)}")
            raise

    async def fetch_query(self, query: str) -> List[Dict[str, Any]]:
        """Fetch tweets for a specific query."""
        try:
            tweets = await fetch_with_retry(
                self.client.search_recent_tweets,
                query=query,
                max_results=100,
                tweet_fields=['created_at', 'public_metrics', 'entities', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'public_metrics'],
                rate_limiter=self.rate_limiter
            )
            
            if not tweets.data:
                return []
                
            tools = []
            for tweet in tweets.data:
                # Skip retweets and replies
                if tweet.text.startswith('RT @') or tweet.text.startswith('@'):
                    continue
                    
                # Extract URLs from tweet
                urls = []
                if tweet.entities and 'urls' in tweet.entities:
                    urls = [url['expanded_url'] for url in tweet.entities['urls']]
                
                # Get author info
                author = next(
                    (user for user in tweets.includes['users'] 
                     if user.id == tweet.author_id),
                    None
                )
                
                # Create tool entry
                tool = {
                    'name': tweet.text[:100],  # Use first 100 chars as name
                    'description': tweet.text,
                    'url': urls[0] if urls else None,
                    'raw_data': {
                        'tweet_id': tweet.id,
                        'created_at': tweet.created_at.isoformat(),
                        'metrics': tweet.public_metrics,
                        'urls': urls,
                        'author': {
                            'username': author.username if author else None,
                            'name': author.name if author else None,
                            'followers': author.public_metrics['followers_count'] if author else 0
                        } if author else None,
                        'source': 'Twitter',
                        'query': query
                    }
                }
                
                tools.append(enrich_tool_data(tool))
            
            return tools
            
        except Exception as e:
            self.logger.error(f"Error processing query '{query}': {str(e)}")
            return []

    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch AI tool-related tweets."""
        try:
            tools = []
            
            # Search queries for AI tools
            search_queries = [
                "new AI tool",
                "AI tool launch",
                "just launched AI",
                "check out my AI",
                "introducing AI",
                "AI tool that",
                "built an AI",
                "created an AI",
                "AI tool for",
                "best AI tool",
                "free AI tool",
                "AI tool review"
            ]
            
            for query in search_queries:
                query_tools = await self.fetch_query(query)
                tools.extend(query_tools)
            
            # Deduplicate tools
            unique_tools = deduplicate_tools(tools)
            
            self.logger.info(
                f"Fetched {len(unique_tools)} unique AI tools from Twitter "
                f"(from {len(tools)} total tweets)"
            )
            return unique_tools
            
        except Exception as e:
            self.logger.error(f"Error fetching from Twitter: {str(e)}")
            return [] 