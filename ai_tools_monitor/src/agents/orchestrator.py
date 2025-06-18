import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime
from .fetchers.product_hunt import ProductHuntFetcher
from .fetchers.futuretools import FutureToolsFetcher
from .fetchers.theresanaiforthat import TheresAnAIFetcher
from .fetchers.aivalley import AIValleyFetcher
from .fetchers.topaitools import TopAIToolsFetcher
from .fetchers.insidr import InsidrFetcher
from .fetchers.aitoolsclub import AIToolsClubFetcher
from .fetchers.gadgetai import GadgetAIFetcher
from .fetchers.toolify import ToolifyFetcher
from .fetchers.aitoolhunt import AIToolHuntFetcher
from .fetchers.reddit import RedditFetcher
from .fetchers.twitter import TwitterFetcher

class FetcherOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.setup_logging()
        self.fetchers = [
            ProductHuntFetcher(config),
            FutureToolsFetcher(config),
            TheresAnAIFetcher(config),
            AIValleyFetcher(config),
            TopAIToolsFetcher(config),
            InsidrFetcher(config),
            AIToolsClubFetcher(config),
            GadgetAIFetcher(config),
            ToolifyFetcher(config),
            AIToolHuntFetcher(config),
            RedditFetcher(config),
            TwitterFetcher(config)
        ]

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
            # Create tasks for all fetchers
            tasks = [fetcher.fetch() for fetcher in self.fetchers]
            
            # Run all fetchers concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            all_tools = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"Error in {self.fetchers[i].__class__.__name__}: {str(result)}")
                elif isinstance(result, list):
                    all_tools.extend(result)
                else:
                    self.logger.warning(f"Unexpected result type from {self.fetchers[i].__class__.__name__}")
            
            # Close all fetcher sessions
            await asyncio.gather(*(fetcher.close() for fetcher in self.fetchers))
            
            self.logger.info(f"Total tools fetched: {len(all_tools)}")
            return all_tools
            
        except Exception as e:
            self.logger.error(f"Error in orchestrator: {str(e)}")
            return []

    async def run(self, interval_minutes: int = 60):
        """Run the fetcher continuously at specified intervals."""
        while True:
            try:
                self.logger.info("Starting fetch cycle...")
                tools = await self.fetch_all()
                
                # Here you would typically:
                # 1. Process the tools (deduplication, enrichment, etc.)
                # 2. Store them in your database
                # 3. Trigger any downstream processing
                
                self.logger.info(f"Fetch cycle completed. Found {len(tools)} tools.")
                
                # Wait for next cycle
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                self.logger.error(f"Error in fetch cycle: {str(e)}")
                await asyncio.sleep(60)  # Wait a minute before retrying 