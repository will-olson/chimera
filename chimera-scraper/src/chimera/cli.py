#!/usr/bin/env python3
"""Command-line interface for the Chimera scraper."""
import asyncio
import argparse
import os
from typing import List
from dotenv import load_dotenv

from chimera.core.scraper import AsyncScraper, ChimeraRequestException
from chimera.providers.proxies import StaticProxyProvider
from chimera.parsers.g2 import G2Parser
from chimera.utils.storage import save_to_json, save_to_csv
from chimera.utils.logging import configure_logging

configure_logging()

# Sample user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
]

async def scrape_g2_reviews(url: str, proxy_provider: StaticProxyProvider) -> List[dict]:
    """Scrape reviews from a G2 product page."""
    async with AsyncScraper(proxy_provider, USER_AGENTS) as scraper:
        try:
            html = await scraper.get(url)
            reviews = G2Parser.extract_reviews(html, url)
            return reviews
        except ChimeraRequestException as e:
            print(f"Failed to scrape {url}: {e}")
            return []

async def main():
    """Main function to run the scraper with CLI arguments."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Chimera - Advanced G2 review scraper")
    parser.add_argument("--url", help="Single URL to scrape")
    parser.add_argument("--urls", nargs="+", help="Multiple URLs to scrape")
    parser.add_argument("--output", default="reviews", help="Output filename prefix (without extension)")
    parser.add_argument("--proxy", help="Proxy server (e.g., http://proxy:port)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests in seconds")
    
    args = parser.parse_args()
    
    # Initialize proxy provider
    proxy_provider = StaticProxyProvider()
    if args.proxy:
        os.environ["PROXY_LIST"] = args.proxy
    
    # Determine URLs to scrape
    urls = []
    if args.url:
        urls = [args.url]
    elif args.urls:
        urls = args.urls
    else:
        # Default URLs if none provided
        urls = [
            "https://www.g2.com/products/salesforce/reviews",
            "https://www.g2.com/products/asana/reviews",
        ]
    
    all_reviews = []
    
    for url in urls:
        print(f"Scraping {url}...")
        reviews = await scrape_g2_reviews(url, proxy_provider)
        all_reviews.extend(reviews)
        print(f"Found {len(reviews)} reviews")
        
        # Be polite - delay between requests
        if len(urls) > 1:
            await asyncio.sleep(args.delay)
    
    # Save results
    if all_reviews:
        json_path = await save_to_json(all_reviews, f"{args.output}.json")
        csv_path = await save_to_csv(all_reviews, f"{args.output}.csv")
        
        print(f"\nSaved {len(all_reviews)} reviews to:")
        print(f"JSON: {json_path}")
        print(f"CSV: {csv_path}")
    else:
        print("No reviews were scraped.")

if __name__ == "__main__":
    asyncio.run(main())
