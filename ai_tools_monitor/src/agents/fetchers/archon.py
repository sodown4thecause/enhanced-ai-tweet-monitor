from typing import List, Dict, Any
import aiohttp
from datetime import datetime, timedelta
from .base import BaseFetcher
from ...utils.fetcher_utils import (
    RateLimiter,
    deduplicate_tools,
    enrich_tool_data,
    fetch_with_retry
)

class ArchonFetcher(BaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.api_key = config.get('ARCHON_API_KEY')
        self.endpoint = config.get('ARCHON_ENDPOINT', 'http://localhost:8000')
        self.rate_limiter = RateLimiter(calls_per_second=0.1)  # 10 seconds between requests

    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch AI tools from Archon using MCP."""
        try:
            async with aiohttp.ClientSession() as session:
                # Prepare MCP request
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                # Query Archon for AI tools
                query = {
                    "query": "Find recent AI tools and their details",
                    "context": {
                        "type": "ai_tools",
                        "filters": {
                            "min_date": (datetime.now() - timedelta(days=30)).isoformat(),
                            "categories": ["AI", "Machine Learning", "Deep Learning"]
                        }
                    }
                }
                
                # Make request to Archon MCP endpoint
                async with session.post(
                    f"{self.endpoint}/mcp/query",
                    headers=headers,
                    json=query
                ) as response:
                    if response.status != 200:
                        self.logger.error(f"Error querying Archon: {response.status}")
                        return []
                        
                    data = await response.json()
                    
                    # Process tools from Archon
                    tools = []
                    for item in data.get('results', []):
                        tool = {
                            'name': item.get('title', ''),
                            'description': item.get('description', ''),
                            'url': item.get('url', ''),
                            'raw_data': {
                                'source': 'Archon',
                                'categories': item.get('categories', []),
                                'pricing': item.get('pricing', 'Unknown'),
                                'metrics': {
                                    'views': item.get('views', 0),
                                    'likes': item.get('likes', 0),
                                    'comments': item.get('comments', 0)
                                },
                                'fetched_at': datetime.now().isoformat(),
                                'archon_data': item
                            }
                        }
                        tools.append(enrich_tool_data(tool))
                    
                    return tools
                    
        except Exception as e:
            self.logger.error(f"Error fetching from Archon: {str(e)}")
            return []

    async def close(self):
        """Clean up resources."""
        await super().close() 