# Chimera Scraper

An advanced web scraping framework with fingerprinting and proxy support, designed for review aggregation and data extraction.

## Features

- **Async HTTP Scraping**: High-performance asynchronous scraping using httpx
- **Proxy Rotation**: Support for static proxy lists and Bright Data (Luminati) proxies
- **Browser Fingerprinting**: Stealth browser contexts using Playwright
- **Retry Logic**: Intelligent retry mechanisms with exponential backoff
- **Header Spoofing**: Realistic browser headers for different user agents
- **Block Detection**: Automatic detection of blocking mechanisms
- **Data Models**: Structured data extraction using Pydantic models
- **Storage**: Flexible storage options (JSON, database, S3)

## Installation

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chimera-scraper
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Install Playwright browsers:
```bash
poetry run playwright install
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Proxy Configuration
PROXY_LIST=http://proxy1:8080,http://proxy2:8080
LUMINATI_USERNAME=your_username
LUMINATI_PASSWORD=your_password
LUMINATI_HOST=zproxy.lum-superproxy.io
LUMINATI_PORT=22225

# Scraping Configuration
REQUEST_DELAY=1.0
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

## Usage

### Basic Usage

```python
import asyncio
from chimera.core.scraper import AsyncScraper
from chimera.providers.proxies import StaticProxyProvider

async def main():
    proxy_provider = StaticProxyProvider()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ]
    
    async with AsyncScraper(proxy_provider, user_agents) as scraper:
        html = await scraper.get("https://example.com")
        print(f"Fetched {len(html)} characters")

asyncio.run(main())
```

### Command Line Interface

#### Simple Usage (main.py)
```bash
# Run with default URLs
poetry run python src/chimera/main.py

# Or make it executable and run directly
chmod +x src/chimera/main.py
./src/chimera/main.py
```

#### Advanced CLI (cli.py)
```bash
# Single URL
poetry run python src/chimera/cli.py --url "https://g2.com/products/salesforce/reviews"

# Multiple URLs
poetry run python src/chimera/cli.py --urls "https://g2.com/products/salesforce/reviews" "https://g2.com/products/asana/reviews"

# With custom proxy
poetry run python src/chimera/cli.py --url "https://g2.com/products/salesforce/reviews" --proxy "http://proxy:8080"

# Custom output filename
poetry run python src/chimera/cli.py --url "https://g2.com/products/salesforce/reviews" --output "salesforce_reviews"

# Custom delay between requests
poetry run python src/chimera/cli.py --urls "url1" "url2" --delay 5.0
```

### Using Different Proxy Providers

```python
from chimera.providers.proxies import StaticProxyProvider, LuminatiProxyProvider

# Static proxy list
static_provider = StaticProxyProvider()

# Bright Data (Luminati) proxies
luminati_provider = LuminatiProxyProvider()
```

### Browser Fingerprinting

```python
from chimera.core.fingerprint import create_stealth_browser_context

async def use_stealth_browser():
    context = await create_stealth_browser_context(
        proxy="http://proxy:8080",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    
    page = await context.new_page()
    await page.goto("https://example.com")
    # ... your scraping logic
```

## Architecture

```
chimera-scraper/
├── src/chimera/
│   ├── core/           # Core scraping functionality
│   ├── providers/      # Proxy and service providers
│   ├── models/         # Data models and schemas
│   ├── parsers/        # HTML and data parsers
│   ├── utils/          # Utility functions
│   ├── main.py         # Simple script entry point
│   └── cli.py          # Advanced CLI with arguments
└── tests/              # Test suite
```

### Core Components

- **AsyncScraper**: Main scraping class with retry logic and proxy rotation
- **ProxyProvider**: Abstract base for different proxy implementations
- **Review**: Pydantic model for structured review data
- **G2Parser**: Parser for G2.com review pages
- **Storage Utilities**: Functions for saving data to JSON and CSV formats

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/

# Sort imports
poetry run isort src/ tests/

# Lint code
poetry run flake8 src/ tests/
```

### Adding New Parsers

1. Create a new parser class in `src/chimera/parsers/`
2. Implement the parsing logic for your target website
3. Add tests in `tests/`
4. Update the main CLI to support your parser

Example:

```python
from chimera.parsers.base import BaseParser
from chimera.models.review import Review

class MySiteParser(BaseParser):
    def parse_reviews(self, html: str) -> List[Review]:
        # Your parsing logic here
        pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review existing issues and discussions
