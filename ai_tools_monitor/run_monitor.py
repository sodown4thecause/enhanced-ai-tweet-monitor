import asyncio
import os
from dotenv import load_dotenv
from src.agents.orchestrator import FetcherOrchestrator

async def main():
    # Load environment variables
    load_dotenv()
    
    # Create config from environment variables
    config = {
        'producthunt_access_token': os.getenv('PRODUCTHUNT_ACCESS_TOKEN'),
        # Add other API keys and config as needed
    }
    
    # Create and run orchestrator
    orchestrator = FetcherOrchestrator(config)
    
    try:
        # Run the orchestrator (will run continuously)
        await orchestrator.run(interval_minutes=60)  # Check every hour
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 