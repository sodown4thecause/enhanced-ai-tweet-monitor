import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

class SimpleFetcher:
    """A simple fetcher for testing purposes."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch some sample AI abilities data."""
        self.logger.info("Fetching sample AI abilities data...")
        
        # Return some sample data for testing
        sample_tools = [
            {
                "name": "ChatGPT",
                "description": "AI-powered conversational assistant",
                "category": "Conversational AI",
                "url": "https://chat.openai.com",
                "source": "sample_data",
                "fetched_at": datetime.now().isoformat()
            },
            {
                "name": "Claude",
                "description": "AI assistant by Anthropic",
                "category": "Conversational AI", 
                "url": "https://claude.ai",
                "source": "sample_data",
                "fetched_at": datetime.now().isoformat()
            },
            {
                "name": "Midjourney",
                "description": "AI image generation tool",
                "category": "Image Generation",
                "url": "https://midjourney.com",
                "source": "sample_data",
                "fetched_at": datetime.now().isoformat()
            }
        ]
        
        # Simulate some async work
        await asyncio.sleep(1)
        
        self.logger.info(f"Successfully fetched {len(sample_tools)} sample AI abilities")
        return sample_tools

class FetcherOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.setup_logging()
        
        # Start with a simple fetcher for testing
        self.fetchers = [SimpleFetcher(config)]
        self.logger.info(f"Initialized orchestrator with {len(self.fetchers)} fetchers")

    def setup_logging(self):
        """Setup logging for the orchestrator."""
        self.logger = logging.getLogger('FetcherOrchestrator')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetch data from all sources concurrently."""
        try:
            self.logger.info(f"Starting fetch from {len(self.fetchers)} sources")
            
            # Create tasks for all fetchers
            tasks = []
            for fetcher in self.fetchers:
                try:
                    task = asyncio.create_task(fetcher.fetch())
                    tasks.append((fetcher.__class__.__name__, task))
                except Exception as e:
                    self.logger.error(f"Error creating task for {fetcher.__class__.__name__}: {e}")
            
            # Wait for all tasks to complete
            results = []
            for fetcher_name, task in tasks:
                try:
                    result = await task
                    if result:
                        results.extend(result)
                        self.logger.info(f"Successfully fetched {len(result)} items from {fetcher_name}")
                    else:
                        self.logger.warning(f"No data returned from {fetcher_name}")
                except Exception as e:
                    self.logger.error(f"Error fetching from {fetcher_name}: {e}")
            
            self.logger.info(f"Total items fetched: {len(results)}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in fetch_all: {e}")
            return []

    async def run(self, interval_minutes: int = 60):
        """Run the orchestrator continuously."""
        self.logger.info(f"🤖 Starting AI abilities monitor with {interval_minutes} minute intervals")
        
        while True:
            try:
                self.logger.info("🔄 Starting fetch cycle...")
                results = await self.fetch_all()
                
                if results:
                    self.logger.info(f"✅ Fetch cycle completed. Found {len(results)} AI abilities.")
                    # Log the tools found
                    for tool in results:
                        self.logger.info(f"🔧 Found: {tool.get('name', 'Unknown')} - {tool.get('description', 'No description')}")
                else:
                    self.logger.warning("⚠️ No AI abilities found in this cycle")
                
                # Wait for the specified interval
                self.logger.info(f"⏰ Waiting {interval_minutes} minutes until next fetch...")
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Received interrupt signal, shutting down...")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in run loop: {e}")
                self.logger.info("⏳ Waiting 5 minutes before retrying...")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
        
        # Cleanup
        await self.cleanup()

    async def cleanup(self):
        """Cleanup resources."""
        self.logger.info("🧹 Cleaning up resources...")
        for fetcher in self.fetchers:
            try:
                if hasattr(fetcher, 'cleanup'):
                    await fetcher.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up {fetcher.__class__.__name__}: {e}")
        self.logger.info("✅ Cleanup completed")