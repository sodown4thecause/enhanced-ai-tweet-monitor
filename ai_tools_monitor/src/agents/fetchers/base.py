import logging
from typing import List, Dict, Any
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import asyncio

class BaseFetcher:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.setup_logging()
        self.session = None

    def setup_logging(self):
        """Setup logging for the fetcher."""
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def fetch(self) -> List[Dict[str, Any]]:
        """Main fetch method to be implemented by each fetcher."""
        raise NotImplementedError("Each fetcher must implement the fetch method")

    def parse_tool(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw data into a standardized tool format."""
        return {
            'name': raw_data.get('name', ''),
            'description': raw_data.get('description', ''),
            'url': raw_data.get('url', ''),
            'source': self.__class__.__name__.replace('Fetcher', '').lower(),
            'discovered_at': datetime.utcnow(),
            'raw_data': raw_data
        }

    async def fetch_with_retry(self, url: str, max_retries: int = 3) -> str:
        """Fetch URL with retry logic."""
        session = await self.get_session()
        for attempt in range(max_retries):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    self.logger.warning(f"Attempt {attempt + 1}: Status {response.status}")
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        return ""

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        return " ".join(text.split()) 