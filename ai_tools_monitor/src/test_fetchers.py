import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from agents.mcp_agent import EnhancedFetcherAgent

def print_tool(tool: dict, source: str):
    print("\n" + "="*80)
    print(f"Source: {source}")
    print(f"Name: {tool['name']}")
    print(f"Description: {tool['description'][:200]}...")
    print(f"URL: {tool['url']}")
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
    # Hardcoded config for testing
    config = {
        'TWITTER_API_KEY': 'GcYxXIDIqPSxtxRPe1941XKdo',
        'TWITTER_API_SECRET': 'BMDWR7RBxVPlqeepuWPDz2mC7kXtqtk9ZgQ0OinI7IlnVyHWSa',
        'TWITTER_ACCESS_TOKEN': 'AAAAAAAAAAAAAAAAAAAAADf02AEAAAAA2%2BFJY3Icc%2Bz%2FX%2FjzQzPrySV7M7g%3D22dIjxRV3E0VZB9jLDLSoMiDOjtd4Ni0EyqcRqPr8BiCfc6d6L',
        'TWITTER_ACCESS_TOKEN_SECRET': 'WEl8VIoDXH1zAKtfIUzJKXDPeMIv7SAIf1b4rEu8adk9U'
    }
    
    print("\nInitializing Enhanced Fetcher Agent...")
    agent = EnhancedFetcherAgent(config)
    
    try:
        print("\nFetching tools from all sources...")
        tools = await agent.fetch_all()
        print(f"\nFound {len(tools)} unique AI tools")
        
        # Print first 5 tools from each source
        twitter_tools = [t for t in tools if t['raw_data'].get('source') == 'Twitter']
        topai_tools = [t for t in tools if t['raw_data'].get('source') == 'TopAI.tools']
        
        print(f"\nTwitter Tools ({len(twitter_tools)}):")
        for tool in twitter_tools[:5]:
            print_tool(tool, "Twitter")
            
        print(f"\nTopAI.tools ({len(topai_tools)}):")
        for tool in topai_tools[:5]:
            print_tool(tool, "TopAI.tools")
            
        # Analyze tools
        print("\nAnalyzing tools...")
        analysis = await agent.analyze_tools(tools)
        print("\nAnalysis Results:")
        print(f"Total Tools: {analysis['total_tools']}")
        print("\nSources:")
        for source, count in analysis['sources'].items():
            print(f"- {source}: {count} tools")
        print("\nTop Categories:")
        for trend in analysis['trends']:
            print(f"- {trend}")
        print("\nPricing Distribution:")
        for pricing, count in analysis['pricing_distribution'].items():
            print(f"- {pricing}: {count} tools")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
    finally:
        await agent.close()

if __name__ == "__main__":
    print(f"Starting fetcher tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    asyncio.run(test_fetchers()) 