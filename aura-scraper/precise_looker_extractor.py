#!/usr/bin/env python3
"""
Precise Looker Review Extractor
Uses the exact selectors extracted from the HTML analysis to extract comprehensive review data.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreciseLookerExtractor:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
        # Precise selectors from HTML analysis
        self.selectors = {
            'company_info': {
                'name': 'h1.text-typo-70.lg:text-typo-95.font-bold.text-neutral-100',
                'logo': 'img.mr-2.object-contain.w-6.h-6.lg:w-8.lg:h-8.inline-flex.align-baseline'
            },
            'rating_info': {
                'overall_rating': 'div.flex.items-center.gap-1.mr-1',  # Star rating container
                'review_count': 'span.text-typo-0.text-neutral-90'  # Review count text
            },
            'reviews': {
                'container': 'div.flex.md:flex-row.md:items-start.gap-3.mb-2',
                'title': 'h4.text-typo-20.font-semibold.text-neutral-99.flex-1',
                'reviewer_name': 'span.text-typo-0.text-neutral-90',  # Pattern: "EGErika G."
                'reviewer_role': 'span.text-typo-0.text-neutral-90',  # Pattern: "Data Analyst"
                'reviewer_company': 'span.text-typo-0.text-neutral-90',  # Pattern: "Information Technology and Services"
                'review_date': 'span.text-typo-0.text-neutral-90',  # Pattern: "August 9, 2025"
                'star_rating': 'div.flex.items-center.gap-1.mr-1',  # Star rating
                'review_text': 'p.text-typo-20.text-neutral-90',  # Main review text
                'pros': 'div.flex.items-center.gap-2.mb-2',  # Pros section
                'cons': 'div.flex.items-center.gap-2.mb-2',  # Cons section
                'continue_reading': 'button.inline-flex.items-center.justify-center.rounded-lg.font-semibold.transition-colors'  # Continue reading button
            }
        }
    
    async def setup_browser(self) -> bool:
        """Setup browser with stealth measures"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-dev-shm-usage',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images',
                    '--disable-javascript',
                    '--disable-gpu'
                ]
            )
            
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self.page = await self.context.new_page()
            
            # Apply stealth measures
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
            """)
            
            return True
        except Exception as e:
            logger.error(f"Failed to setup browser: {e}")
            return False
    
    async def extract_looker_data(self, url: str) -> Dict[str, Any]:
        """Extract comprehensive data from Looker Capterra page"""
        try:
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for page to load
            await asyncio.sleep(3)
            
            # Extract company info
            company_info = await self._extract_company_info()
            
            # Extract rating info
            rating_info = await self._extract_rating_info()
            
            # Extract all reviews
            reviews = await self._extract_all_reviews()
            
            return {
                'company_info': company_info,
                'rating_info': rating_info,
                'reviews': reviews,
                'extraction_metadata': {
                    'url': url,
                    'total_reviews_found': len(reviews),
                    'extraction_timestamp': asyncio.get_event_loop().time()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return {}
    
    async def _extract_company_info(self) -> Dict[str, Any]:
        """Extract company information"""
        company_info = {}
        
        try:
            # Company name
            name_element = await self.page.query_selector(self.selectors['company_info']['name'])
            if name_element:
                company_info['name'] = await name_element.text_content()
            
            # Company logo
            logo_element = await self.page.query_selector(self.selectors['company_info']['logo'])
            if logo_element:
                company_info['logo_url'] = await logo_element.get_attribute('src')
            
        except Exception as e:
            logger.error(f"Failed to extract company info: {e}")
        
        return company_info
    
    async def _extract_rating_info(self) -> Dict[str, Any]:
        """Extract rating information"""
        rating_info = {}
        
        try:
            # Overall rating
            rating_element = await self.page.query_selector(self.selectors['rating_info']['overall_rating'])
            if rating_element:
                rating_info['overall_rating'] = await rating_element.text_content()
            
            # Review count
            count_elements = await self.page.query_selector_all(self.selectors['rating_info']['review_count'])
            for element in count_elements:
                text = await element.text_content()
                if 'Based on' in text and 'reviews' in text:
                    rating_info['review_count'] = text
                    break
            
        except Exception as e:
            logger.error(f"Failed to extract rating info: {e}")
        
        return rating_info
    
    async def _extract_all_reviews(self) -> List[Dict[str, Any]]:
        """Extract all reviews from the page"""
        reviews = []
        
        try:
            # Find all review containers
            review_containers = await self.page.query_selector_all(self.selectors['reviews']['container'])
            logger.info(f"Found {len(review_containers)} review containers")
            
            for i, container in enumerate(review_containers):
                try:
                    review_data = await self._extract_single_review(container, i)
                    if review_data:
                        reviews.append(review_data)
                except Exception as e:
                    logger.error(f"Failed to extract review {i}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Failed to extract reviews: {e}")
        
        return reviews
    
    async def _extract_single_review(self, container, index: int) -> Dict[str, Any]:
        """Extract data from a single review container"""
        review_data = {
            'index': index,
            'title': '',
            'reviewer_name': '',
            'reviewer_role': '',
            'reviewer_company': '',
            'review_date': '',
            'star_rating': '',
            'review_text': '',
            'pros': '',
            'cons': '',
            'continue_reading_available': False
        }
        
        try:
            # Extract review title
            title_element = await container.query_selector(self.selectors['reviews']['title'])
            if title_element:
                review_data['title'] = await title_element.text_content()
            
            # Extract reviewer information
            reviewer_elements = await container.query_selector_all(self.selectors['reviews']['reviewer_name'])
            for element in reviewer_elements:
                text = await element.text_content()
                if text:
                    # Check if it's a name pattern (e.g., "EGErika G.")
                    if len(text.split()) == 2 and text.split()[1].endswith('.'):
                        review_data['reviewer_name'] = text
                    # Check if it's a role pattern
                    elif any(word in text.lower() for word in ['analyst', 'manager', 'director', 'engineer', 'developer', 'consultant']):
                        review_data['reviewer_role'] = text
                    # Check if it's a company pattern
                    elif any(word in text.lower() for word in ['services', 'technology', 'marketing', 'software', 'health', 'financial']):
                        review_data['reviewer_company'] = text
                    # Check if it's a date pattern
                    elif any(word in text.lower() for word in ['august', 'july', 'june', 'may', 'april', 'march', 'february', 'january', '2024', '2023', '2022']):
                        review_data['review_date'] = text
            
            # Extract star rating
            rating_element = await container.query_selector(self.selectors['reviews']['star_rating'])
            if rating_element:
                review_data['star_rating'] = await rating_element.text_content()
            
            # Extract review text
            text_elements = await container.query_selector_all(self.selectors['reviews']['review_text'])
            for element in text_elements:
                text = await element.text_content()
                if text and len(text) > 50 and not text.startswith('Pros') and not text.startswith('Cons'):
                    review_data['review_text'] = text
                    break
            
            # Extract pros and cons
            pros_cons_elements = await container.query_selector_all(self.selectors['reviews']['pros'])
            for element in pros_cons_elements:
                text = await element.text_content()
                if text:
                    if 'Pros' in text:
                        review_data['pros'] = text
                    elif 'Cons' in text:
                        review_data['cons'] = text
            
            # Check for continue reading button
            continue_button = await container.query_selector(self.selectors['reviews']['continue_reading'])
            if continue_button:
                review_data['continue_reading_available'] = True
            
        except Exception as e:
            logger.error(f"Failed to extract single review {index}: {e}")
        
        return review_data
    
    async def close(self):
        """Close browser and cleanup"""
        try:
            if self.browser:
                await self.browser.close()
        except Exception as e:
            logger.error(f"Failed to close browser: {e}")

async def main():
    """Main function to test the precise extractor"""
    extractor = PreciseLookerExtractor()
    
    try:
        if await extractor.setup_browser():
            logger.info("Browser setup successful")
            
            # Test with Looker page
            url = "https://www.capterra.com/p/169053/Looker/"
            data = await extractor.extract_looker_data(url)
            
            # Save results
            output_file = "output/looker_precise_extraction.json"
            Path("output").mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Extraction complete. Results saved to {output_file}")
            logger.info(f"Extracted {len(data.get('reviews', []))} reviews")
            
        else:
            logger.error("Failed to setup browser")
    
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
    
    finally:
        await extractor.close()

if __name__ == "__main__":
    asyncio.run(main())
