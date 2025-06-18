import asyncio
import os
from dotenv import load_dotenv
from src.agents.orchestrator import FetcherOrchestrator

async def test_monitor():
    # Load environment variables
    load_dotenv()
    
    # Create config from environment variables
    config = {
        'producthunt_access_token': os.getenv('PRODUCTHUNT_ACCESS_TOKEN'),
        'twitter_api_key': os.getenv('TWITTER_API_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
    }
    
    # Create and test orchestrator
    orchestrator = FetcherOrchestrator(config)
    
    print("🤖 Testing AI abilities monitor...")
    
    try:
        # Run one fetch cycle
        results = await orchestrator.fetch_all()
        print(f"✅ Test completed! Found {len(results)} AI abilities.")
        
        # Show the results
        for tool in results:
            print(f"  🔧 {tool['name']}: {tool['description']}")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
    
    await orchestrator.cleanup()
    print("🏁 Test finished!")

if __name__ == "__main__":
    asyncio.run(test_monitor())