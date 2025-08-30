#!/usr/bin/env python3
import asyncio
import json
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

async def scrape_g2_reviews(url: str) -> List[dict]:
    """Scrape reviews from a G2 product page."""
    proxy_provider = StaticProxyProvider()
    
    async with AsyncScraper(proxy_provider, USER_AGENTS) as scraper:
        try:
            html = await scraper.get(url)
            reviews = G2Parser.extract_reviews(html, url)
            return reviews
        except ChimeraRequestException as e:
            print(f"Failed to scrape {url}: {e}")
            return []

async def main():
    """Main function to run the scraper."""
    load_dotenv()
    
    # Example URLs to scrape
    urls = [
        "https://www.g2.com/products/salesforce/reviews",
        "https://www.g2.com/products/asana/reviews",
        # Add more URLs here
    ]
    
    all_reviews = []
    
    for url in urls:
        print(f"Scraping {url}...")
        reviews = await scrape_g2_reviews(url)
        all_reviews.extend(reviews)
        print(f"Found {len(reviews)} reviews")
        # Be polite - delay between requests
        await asyncio.sleep(2)
    
    # Save results
    if all_reviews:
        json_path = await save_to_json(all_reviews)
        csv_path = await save_to_csv(all_reviews)
        
        print(f"Saved {len(all_reviews)} reviews to:")
        print(f"JSON: {json_path}")
        print(f"CSV: {csv_path}")
    else:
        print("No reviews were scraped.")

if __name__ == "__main__":
    asyncio.run(main())
