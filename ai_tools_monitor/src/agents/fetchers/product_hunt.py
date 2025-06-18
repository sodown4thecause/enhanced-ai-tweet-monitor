from typing import List, Dict, Any
import aiohttp
from datetime import datetime, timedelta
from .base import BaseFetcher

class ProductHuntFetcher(BaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.api_url = "https://api.producthunt.com/v2/api/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.config.get('producthunt_access_token')}",
            "Content-Type": "application/json"
        }

    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch new AI tools from Product Hunt."""
        try:
            # GraphQL query for AI tools
            query = """
            {
              posts(first: 50, order: NEWEST) {
                edges {
                  node {
                    name
                    tagline
                    description
                    url
                    topics {
                      name
                    }
                    votesCount
                    commentsCount
                    createdAt
                  }
                }
              }
            }
            """
            
            session = await self.get_session()
            async with session.post(
                self.api_url,
                headers=self.headers,
                json={"query": query}
            ) as response:
                if response.status != 200:
                    self.logger.error(f"Product Hunt API error: {response.status}")
                    return []
                
                data = await response.json()
                tools = []
                
                for edge in data.get('data', {}).get('posts', {}).get('edges', []):
                    post = edge['node']
                    
                    # Check if it's an AI tool
                    topics = [t['name'].lower() for t in post.get('topics', [])]
                    if any(topic in ['ai', 'artificial-intelligence', 'machine-learning'] for topic in topics):
                        tool = {
                            'name': post['name'],
                            'description': post['tagline'],
                            'url': post['url'],
                            'raw_data': {
                                'votes_count': post['votesCount'],
                                'comments_count': post['commentsCount'],
                                'created_at': post['createdAt'],
                                'topics': topics
                            }
                        }
                        tools.append(self.parse_tool(tool))
                
                self.logger.info(f"Fetched {len(tools)} AI tools from Product Hunt")
                return tools
                
        except Exception as e:
            self.logger.error(f"Error fetching from Product Hunt: {str(e)}")
            return [] 