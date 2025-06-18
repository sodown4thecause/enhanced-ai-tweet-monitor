import asyncio
from src.agents.fetchers.topaitools import TopAIToolsFetcher

async def test_topaitools():
    # Create fetcher
    fetcher = TopAIToolsFetcher()
    try:
        tools = await fetcher.fetch()
        print(f"\nFound {len(tools)} AI tools on TopAI.tools:")
        for tool in tools:
            print(f"\nName: {tool['name']}")
            print(f"Description: {tool['description']}")
            print(f"URL: {tool['url']}")
            print(f"Categories: {tool['raw_data']['categories']}")
            print(f"Pricing: {tool['raw_data']['pricing']}")
            print("-" * 80)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await fetcher.close()

if __name__ == "__main__":
    asyncio.run(test_topaitools()) 