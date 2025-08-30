"""Tests for the core scraper functionality."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from chimera.core.scraper import AsyncScraper, ChimeraRequestException
from chimera.providers.proxies import StaticProxyProvider


@pytest.fixture
def proxy_provider():
    """Create a mock proxy provider."""
    provider = StaticProxyProvider()
    provider.proxies = ["http://proxy1:8080", "http://proxy2:8080"]
    return provider


@pytest.fixture
def user_agents():
    """Create a list of test user agents."""
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]


@pytest.mark.asyncio
async def test_scraper_initialization(proxy_provider, user_agents):
    """Test scraper initialization."""
    scraper = AsyncScraper(proxy_provider, user_agents)
    assert scraper.proxy_provider == proxy_provider
    assert scraper.user_agents == user_agents
    assert scraper.client is None


@pytest.mark.asyncio
async def test_scraper_context_manager(proxy_provider, user_agents):
    """Test scraper as async context manager."""
    async with AsyncScraper(proxy_provider, user_agents) as scraper:
        assert scraper.client is not None
    # Client should be closed after context exit
    assert scraper.client.is_closed


@pytest.mark.asyncio
async def test_g2_parser_extract_reviews():
    """Test G2 parser review extraction."""
    from chimera.parsers.g2 import G2Parser
    
    # Mock HTML content
    html = """
    <div data-purpose="review">
        <div class="rating">5.0</div>
        <h3>Great Product</h3>
        <p>This is an amazing product!</p>
        <div class="author">John Doe</div>
        <time datetime="2023-01-15">January 15, 2023</time>
    </div>
    """
    
    reviews = G2Parser.extract_reviews(html, "https://g2.com/test")
    
    assert len(reviews) == 1
    review = reviews[0]
    assert review.title == "Great Product"
    assert review.content == "This is an amazing product!"
    assert review.rating == 5.0
    assert review.author == "John Doe"
    assert review.source == "G2"


@pytest.mark.asyncio
async def test_generate_headers_chrome(proxy_provider, user_agents):
    """Test header generation for Chrome user agent."""
    scraper = AsyncScraper(proxy_provider, user_agents)
    chrome_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    headers = scraper._generate_headers(chrome_ua)
    
    assert headers["User-Agent"] == chrome_ua
    assert "Sec-CH-UA" in headers
    assert "Sec-CH-UA-Mobile" in headers
    assert "Sec-CH-UA-Platform" in headers


@pytest.mark.asyncio
async def test_generate_headers_firefox(proxy_provider, user_agents):
    """Test header generation for Firefox user agent."""
    scraper = AsyncScraper(proxy_provider, user_agents)
    firefox_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    
    headers = scraper._generate_headers(firefox_ua)
    
    assert headers["User-Agent"] == firefox_ua
    assert "Sec-Fetch-Dest" in headers
    assert "Sec-Fetch-Mode" in headers
