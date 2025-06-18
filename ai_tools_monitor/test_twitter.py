import asyncio
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.agents.fetchers.twitter import TwitterFetcher

async def test_twitter():
    # Load environment variables
    load_dotenv()
    
    # Create config from environment variables
    config = {
        'TWITTER_API_KEY': os.getenv('TWITTER_API_KEY'),
        'TWITTER_API_SECRET': os.getenv('TWITTER_API_SECRET'),
        'TWITTER_ACCESS_TOKEN': os.getenv('TWITTER_ACCESS_TOKEN'),
        'TWITTER_ACCESS_TOKEN_SECRET': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }
    
    # Create and run fetcher
    fetcher = TwitterFetcher(config)
    try:
        tools = await fetcher.fetch()
        print(f"\nFound {len(tools)} AI tools on Twitter:")
        for tool in tools:
            print(f"\nName: {tool['name']}")
            print(f"Description: {tool['description']}")
            print(f"URL: {tool['url']}")
            print("-" * 80)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await fetcher.close()

if __name__ == "__main__":
    asyncio.run(test_twitter()) 