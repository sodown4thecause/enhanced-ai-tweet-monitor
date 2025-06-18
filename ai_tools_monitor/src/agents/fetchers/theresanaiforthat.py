from typing import List, Dict, Any
from bs4 import BeautifulSoup
from .base import BaseFetcher

class TheresAnAIFetcher(BaseFetcher):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.base_url = "https://theresanaiforthat.com"
        self.tools_url = f"{self.base_url}/ai-tools/"

    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch AI tools from There's An AI For That."""
        try:
            html = await self.fetch_with_retry(self.tools_url)
            if not html:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            tools = []
            
            # Find all tool cards
            tool_cards = soup.find_all('div', class_='tool-card')  # Adjust selector based on actual HTML
            
            for card in tool_cards:
                try:
                    # Extract tool information
                    name_elem = card.find('h3')  # Adjust selector
                    desc_elem = card.find('p', class_='description')  # Adjust selector
                    url_elem = card.find('a', href=True)
                    
                    if not all([name_elem, desc_elem, url_elem]):
                        continue
                    
                    name = self.clean_text(name_elem.text)
                    description = self.clean_text(desc_elem.text)
                    url = url_elem['href']
                    
                    # Make URL absolute if it's relative
                    if url.startswith('/'):
                        url = f"{self.base_url}{url}"
                    
                    # Extract categories
                    categories = []
                    category_elems = card.find_all('span', class_='category')  # Adjust selector
                    for cat in category_elems:
                        categories.append(self.clean_text(cat.text))
                    
                    # Extract pricing if available
                    pricing = None
                    pricing_elem = card.find('span', class_='pricing')  # Adjust selector
                    if pricing_elem:
                        pricing = self.clean_text(pricing_elem.text)
                    
                    tool = {
                        'name': name,
                        'description': description,
                        'url': url,
                        'raw_data': {
                            'categories': categories,
                            'pricing': pricing,
                            'html': str(card)
                        }
                    }
                    
                    tools.append(self.parse_tool(tool))
                    
                except Exception as e:
                    self.logger.error(f"Error parsing tool card: {str(e)}")
                    continue
            
            self.logger.info(f"Fetched {len(tools)} AI tools from There's An AI For That")
            return tools
            
        except Exception as e:
            self.logger.error(f"Error fetching from There's An AI For That: {str(e)}")
            return [] 