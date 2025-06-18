import asyncio
import hashlib
from typing import List, Dict, Any, Callable
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

class RateLimiter:
    def __init__(self, calls_per_second: float = 1.0):
        self.calls_per_second = calls_per_second
        self.last_call = datetime.min
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = datetime.now()
            time_since_last_call = (now - self.last_call).total_seconds()
            if time_since_last_call < 1.0 / self.calls_per_second:
                await asyncio.sleep(1.0 / self.calls_per_second - time_since_last_call)
            self.last_call = datetime.now()

def generate_tool_hash(tool: Dict[str, Any]) -> str:
    """Generate a unique hash for a tool based on its name and URL."""
    key = f"{tool['name']}:{tool['url']}"
    return hashlib.md5(key.encode()).hexdigest()

def deduplicate_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate tools based on name and URL."""
    seen = set()
    unique_tools = []
    
    for tool in tools:
        tool_hash = generate_tool_hash(tool)
        if tool_hash not in seen:
            seen.add(tool_hash)
            unique_tools.append(tool)
    
    return unique_tools

def enrich_tool_data(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich tool data with additional metadata."""
    enriched = tool.copy()
    
    # Add timestamp
    enriched['raw_data']['fetched_at'] = datetime.utcnow().isoformat()
    
    # Add source-specific metadata
    if 'source' not in enriched['raw_data']:
        enriched['raw_data']['source'] = 'unknown'
    
    # Add popularity metrics if available
    if 'metrics' not in enriched['raw_data']:
        enriched['raw_data']['metrics'] = {
            'views': 0,
            'likes': 0,
            'shares': 0
        }
    
    return enriched

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def fetch_with_retry(
    fetch_func: Callable,
    *args,
    rate_limiter: RateLimiter = None,
    **kwargs
) -> Any:
    """Execute a fetch function with retries and rate limiting."""
    if rate_limiter:
        await rate_limiter.acquire()
    return await fetch_func(*args, **kwargs)

class PaginationHelper:
    def __init__(self, max_pages: int = 10):
        self.max_pages = max_pages
        self.current_page = 1

    def has_next_page(self) -> bool:
        return self.current_page < self.max_pages

    def next_page(self):
        if self.has_next_page():
            self.current_page += 1
            return True
        return False

    def reset(self):
        self.current_page = 1 