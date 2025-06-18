import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from src.agents.fetchers.twitter import TwitterFetcher
from src.agents.fetchers.topaitools import TopAIToolsFetcher

def print_tool(tool: dict, source: str):
    """Print a tool's information in a formatted way."""
    print("\n" + "="*80)
    print(f"Source: {source}")
    print(f"Name: {tool['name']}")
    print(f"Description: {tool['description'][:200]}...")  # First 200 chars
    print(f"URL: {tool['url']}")
    
    # Print source-specific data
    if source == "Twitter":
        author = tool['raw_data'].get('author', {})
        if author:
            print(f"Author: @{author.get('username')} ({author.get('name')})")
            print(f"Followers: {author.get('followers', 0):,}")
        metrics = tool['raw_data'].get('metrics', {})
        print(f"Likes: {metrics.get('like_count', 0):,}")
        print(f"Retweets: {metrics.get('retweet_count', 0):,}")
        print(f"Query: {tool['raw_data'].get('query', 'unknown')}")
    
    elif source == "TopAI.tools":
        print(f"Categories: {', '.join(tool['raw_data'].get('categories', []))}")
        print(f"Pricing: {tool['raw_data'].get('pricing', 'Unknown')}")
        metrics = tool['raw_data'].get('metrics', {})
        print(f"Views: {metrics.get('views', 0):,}")
    
    print(f"Fetched at: {tool['raw_data'].get('fetched_at', 'Unknown')}")
    print("="*80)

async def test_fetchers():
    # Load environment variables
    load_dotenv()
    
    # Create config from environment variables
    config = {
        'TWITTER_API_KEY': os.getenv('TWITTER_API_KEY'),
        'TWITTER_API_SECRET': os.getenv('TWITTER_API_SECRET'),
        'TWITTER_ACCESS_TOKEN': os.getenv('TWITTER_ACCESS_TOKEN'),
        'TWITTER_ACCESS_TOKEN_SECRET': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }
    
    # Test Twitter fetcher
    # print("\nTesting Twitter Fetcher...")
    # twitter_fetcher = TwitterFetcher(config)
    # try:
    #     twitter_tools = await twitter_fetcher.fetch()
    #     print(f"\nFound {len(twitter_tools)} unique AI tools on Twitter")
    #     for tool in twitter_tools[:5]:  # Show first 5 tools
    #         print_tool(tool, "Twitter")
    # except Exception as e:
    #     print(f"Error testing Twitter fetcher: {str(e)}")
    # finally:
    #     await twitter_fetcher.close()
    
    # Test TopAI.tools fetcher
    print("\nTesting TopAI.tools Fetcher...")
    topai_fetcher = TopAIToolsFetcher()
    try:
        topai_tools = await topai_fetcher.fetch()
        print(f"\nFound {len(topai_tools)} unique AI tools on TopAI.tools")
        for tool in topai_tools[:5]:  # Show first 5 tools
            print_tool(tool, "TopAI.tools")
    except Exception as e:
        print(f"Error testing TopAI.tools fetcher: {str(e)}")
    finally:
        await topai_fetcher.close()

if __name__ == "__main__":
    print(f"Starting fetcher tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    asyncio.run(test_fetchers()) 