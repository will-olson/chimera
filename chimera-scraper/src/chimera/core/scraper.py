import asyncio
import random
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx
from loguru import logger

from chimera.providers.proxies import ProxyProvider
from chimera.utils.logging import configure_logging

configure_logging()

class ChimeraRequestException(Exception):
    """Custom exception for scraper errors."""
    pass

class AsyncScraper:
    def __init__(self, proxy_provider: ProxyProvider, user_agents: List[str]):
        self.proxy_provider = proxy_provider
        self.user_agents = user_agents
        self.client = None
        
    async def __aenter__(self):
        await self._init_client()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
            
    async def _init_client(self):
        """Initialize the HTTP client with a random user agent and proxy."""
        proxy_url = await self.proxy_provider.get_proxy()
        user_agent = random.choice(self.user_agents)
        
        headers = self._generate_headers(user_agent)
        
        # Configure proxy if available
        proxies = None
        if proxy_url:
            proxies = {"http://": proxy_url, "https://": proxy_url}
        
        self.client = httpx.AsyncClient(
            proxies=proxies,
            headers=headers,
            timeout=30.0,
            follow_redirects=True
        )
        
    def _generate_headers(self, user_agent: str) -> Dict[str, str]:
        """Generate realistic headers for a given user agent."""
        base_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        # Browser-specific headers
        if "Chrome" in user_agent:
            base_headers.update({
                "Sec-CH-UA": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
            })
        elif "Firefox" in user_agent:
            base_headers.update({
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            })
            
        base_headers["User-Agent"] = user_agent
        return base_headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ChimeraRequestException)
    )
    async def get(self, url: str) -> str:
        """Make a GET request with retry logic."""
        if not self.client:
            await self._init_client()
            
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            # Check for blocking indicators
            if self._is_blocked(response):
                logger.warning(f"Request to {url} was blocked")
                raise ChimeraRequestException("Request was blocked")
                
            return response.text
        except (httpx.HTTPError, httpx.RequestError) as e:
            logger.error(f"Request failed: {e}")
            # Rotate proxy and user agent on failure
            await self._init_client()
            raise ChimeraRequestException(f"Request failed: {e}") from e
            
    def _is_blocked(self, response: httpx.Response) -> bool:
        """Check if the response indicates a block."""
        blocked_indicators = [
            response.status_code in [403, 429, 503],
            "cloudflare" in response.text.lower(),
            "datadome" in response.text.lower(),
            "access denied" in response.text.lower(),
            "captcha" in response.text.lower(),
        ]
        return any(blocked_indicators)
