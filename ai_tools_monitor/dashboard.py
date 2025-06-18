import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from src.agents.orchestrator import FetcherOrchestrator

async def show_dashboard():
    """Show a simple dashboard of the AI abilities monitor."""
    print("🤖 AI abilities Monitor Dashboard")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Create config from environment variables
    config = {
        'producthunt_access_token': os.getenv('PRODUCTHUNT_ACCESS_TOKEN'),
        'twitter_api_key': os.getenv('TWITTER_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
    }
    
    # Create orchestrator
    orchestrator = FetcherOrchestrator(config)
    
    print(f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Active Fetchers: {len(orchestrator.fetchers)}")
    print()
    
    try:
        print("🔄 Running fetch cycle...")
        results = await orchestrator.fetch_all()
        
        print(f"✅ Fetch completed! Found {len(results)} AI abilities:")
        print("-" * 50)
        
        for i, tool in enumerate(results, 1):
            print(f"{i:2d}. 🔧 {tool['name']}")
            print(f"     📝 {tool['description']}")
            print(f"     🏷️  Category: {tool['category']}")
            print(f"     🌐 URL: {tool['url']}")
            print(f"     📊 Source: {tool['source']}")
            print()
            
    except Exception as e:
        print(f"❌ Error during fetch: {str(e)}")
    
    await orchestrator.cleanup()
    print("🏁 Dashboard session completed!")

if __name__ == "__main__":
    asyncio.run(show_dashboard())