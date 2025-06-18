from typing import List, Dict, Any
from .fetchers.base import BaseFetcher
from .fetchers.twitter import TwitterFetcher
from .fetchers.topaitools import TopAIToolsFetcher
from .fetchers.archon import ArchonFetcher

class EnhancedFetcherAgent:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.fetchers: List[BaseFetcher] = []
        self.setup_fetchers()

    def setup_fetchers(self):
        """Initialize fetchers with enhanced capabilities."""
        try:
            # Initialize Twitter fetcher
            twitter_fetcher = TwitterFetcher(self.config)
            self.fetchers.append(twitter_fetcher)

            # Initialize TopAI.tools fetcher
            topai_fetcher = TopAIToolsFetcher()
            self.fetchers.append(topai_fetcher)

            # Initialize Archon fetcher
            if self.config.get('ARCHON_API_KEY'):
                archon_fetcher = ArchonFetcher(self.config)
                self.fetchers.append(archon_fetcher)

        except Exception as e:
            print(f"Error setting up fetchers: {str(e)}")
            raise

    async def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetch tools from all sources with enhanced capabilities."""
        try:
            all_tools = []
            for fetcher in self.fetchers:
                try:
                    tools = await fetcher.fetch()
                    all_tools.extend(tools)
                except Exception as e:
                    print(f"Error fetching from {fetcher.__class__.__name__}: {str(e)}")
                    continue

            return all_tools

        except Exception as e:
            print(f"Error fetching tools: {str(e)}")
            return []

    async def close(self):
        """Clean up resources."""
        try:
            for fetcher in self.fetchers:
                await fetcher.close()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    async def analyze_tools(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the fetched tools for insights."""
        try:
            analysis = {
                "total_tools": len(tools),
                "sources": {},
                "categories": {},
                "pricing_distribution": {},
                "trends": []
            }

            # Analyze by source
            for tool in tools:
                source = tool['raw_data'].get('source', 'Unknown')
                analysis['sources'][source] = analysis['sources'].get(source, 0) + 1

                # Analyze categories
                if 'categories' in tool['raw_data']:
                    for category in tool['raw_data']['categories']:
                        analysis['categories'][category] = analysis['categories'].get(category, 0) + 1

                # Analyze pricing
                pricing = tool['raw_data'].get('pricing', 'Unknown')
                analysis['pricing_distribution'][pricing] = analysis['pricing_distribution'].get(pricing, 0) + 1

            # Identify trends
            if tools:
                # Sort categories by frequency
                sorted_categories = sorted(
                    analysis['categories'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                analysis['trends'] = [
                    f"Top category: {category} ({count} tools)"
                    for category, count in sorted_categories[:3]
                ]

            return analysis

        except Exception as e:
            print(f"Error analyzing tools: {str(e)}")
            return {} 