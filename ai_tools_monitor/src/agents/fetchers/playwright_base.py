from typing import List, Dict, Any
from playwright.async_api import async_playwright, Browser, Page
from .base import BaseFetcher

class PlaywrightBaseFetcher(BaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.browser = None
        self.context = None
        self.page = None

    async def setup(self):
        try:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
        except Exception as e:
            self.logger.error(f"Error setting up Playwright: {str(e)}")
            raise

    async def cleanup(self):
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, '_playwright'):
                await self._playwright.stop()
        except Exception as e:
            self.logger.error(f"Error cleaning up Playwright: {str(e)}")

    async def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Child classes must implement fetch()")

    async def close(self):
        await self.cleanup()
        await super().close() 