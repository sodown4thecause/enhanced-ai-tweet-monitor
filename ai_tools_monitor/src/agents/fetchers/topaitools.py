from typing import List, Dict, Any
from .playwright_base import PlaywrightBaseFetcher
from ...utils.fetcher_utils import (
    RateLimiter,
    PaginationHelper,
    deduplicate_tools,
    enrich_tool_data,
    fetch_with_retry
)

class TopAIToolsFetcher(PlaywrightBaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.base_url = "https://topai.tools"
        self.tools_url = f"{self.base_url}/tools"
        self.rate_limiter = RateLimiter(calls_per_second=0.5)  # 2 seconds between requests
        self.pagination = PaginationHelper(max_pages=5)  # Fetch up to 5 pages

    async def fetch_page(self, page_num: int) -> List[Dict[str, Any]]:
        """Fetch a single page of tools."""
        tools = []
        page_url = f"{self.tools_url}?page={page_num}"
        
        try:
            assert self.page is not None
            await self.page.goto(page_url, wait_until='networkidle', timeout=60000)
            await self.page.wait_for_selector('.tool-card', timeout=30000)
            
            tool_cards = await self.page.query_selector_all('.tool-card')
            
            for card in tool_cards:
                try:
                    # Extract tool information
                    name = await card.query_selector('h3')
                    name_text = await name.inner_text() if name else "Unknown"
                    
                    description = await card.query_selector('.description')
                    desc_text = await description.inner_text() if description else ""
                    
                    url_elem = await card.query_selector('a')
                    url = await url_elem.get_attribute('href') if url_elem else None
                    
                    if url and not url.startswith('http'):
                        url = f"{self.base_url}{url}"
                    
                    # Extract categories
                    categories = []
                    category_elems = await card.query_selector_all('.category')
                    for cat in category_elems:
                        cat_text = await cat.inner_text()
                        categories.append(cat_text)
                    
                    # Extract pricing if available
                    pricing = None
                    pricing_elem = await card.query_selector('.pricing')
                    if pricing_elem:
                        pricing = await pricing_elem.inner_text()
                    
                    # Extract metrics if available
                    metrics = {}
                    views_elem = await card.query_selector('.views')
                    if views_elem:
                        metrics['views'] = int(await views_elem.inner_text() or 0)
                    
                    tool = {
                        'name': name_text.strip(),
                        'description': desc_text.strip(),
                        'url': url,
                        'raw_data': {
                            'categories': categories,
                            'pricing': pricing,
                            'metrics': metrics,
                            'source': 'TopAI.tools',
                            'page': page_num
                        }
                    }
                    
                    tools.append(enrich_tool_data(tool))
                    
                except Exception as e:
                    self.logger.error(f"Error parsing tool card: {str(e)}")
                    continue
            
            return tools
            
        except Exception as e:
            self.logger.error(f"Error fetching page {page_num}: {str(e)}")
            return []

    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch AI tools from TopAI.tools using Playwright with pagination."""
        try:
            await self.setup()
            all_tools = []
            
            while self.pagination.has_next_page():
                page_tools = await fetch_with_retry(
                    self.fetch_page,
                    self.pagination.current_page,
                    rate_limiter=self.rate_limiter
                )
                
                if not page_tools:
                    break
                    
                all_tools.extend(page_tools)
                self.pagination.next_page()
            
            # Deduplicate tools
            unique_tools = deduplicate_tools(all_tools)
            
            self.logger.info(
                f"Fetched {len(unique_tools)} unique AI tools from TopAI.tools "
                f"(from {len(all_tools)} total tools)"
            )
            return unique_tools
            
        except Exception as e:
            self.logger.error(f"Error fetching from TopAI.tools: {str(e)}")
            return []
        finally:
            await self.cleanup()
            self.pagination.reset() 