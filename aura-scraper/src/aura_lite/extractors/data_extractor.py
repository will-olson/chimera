"""
CapterraDataExtractor - Data extraction system
Adapted from Chimera-Ultimate's precision extraction
"""

import asyncio
import re
import random
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class CapterraDataExtractor:
    """Data extraction system adapted from Chimera-Ultimate's precision extraction"""
    
    def __init__(self, page: Page):
        self.page = page
        self.selector_cache = {}
        self.extraction_stats = {
            'reviews_extracted': 0,
            'ratings_extracted': 0,
            'pricing_extracted': 0,
            'alternatives_found': 0,
            'extraction_attempts': 0,
            'successful_extractions': 0,
            'failed_extractions': 0
        }
        self.extraction_history = []
    
    async def extract_product_reviews(self, url: str, company_name: str) -> Dict[str, Any]:
        """Extract reviews using precise selectors from screenshots"""
        extraction_start = datetime.now()
        self.extraction_stats['extraction_attempts'] += 1
        
        try:
            logger.info(f"Scraping {company_name} from {url}")
            await self.page.goto(url, wait_until='domcontentloaded')
            
            # Wait for page to load
            await asyncio.sleep(2)
            
            # Extract data using precise selectors
            overall_rating = await self._extract_overall_rating()
            review_count = await self._extract_review_count()
            reviews = await self._extract_individual_reviews()
            pricing_info = await self._extract_pricing()
            rating_categories = await self._extract_rating_categories()
            
            result = {
                'company': company_name,
                'overall_rating': overall_rating,
                'review_count': review_count,
                'pricing_info': pricing_info,
                'rating_categories': rating_categories,
                'reviews': reviews,
                'scraped_at': datetime.now().isoformat(),
                'source_url': url,
                'extraction_duration': (datetime.now() - extraction_start).total_seconds()
            }
            
            # Update statistics
            self.extraction_stats['successful_extractions'] += 1
            self.extraction_stats['reviews_extracted'] += len(reviews)
            if overall_rating != 'N/A':
                self.extraction_stats['ratings_extracted'] += 1
            if pricing_info != 'N/A':
                self.extraction_stats['pricing_extracted'] += 1
            
            # Record extraction
            self.extraction_history.append({
                'company': company_name,
                'url': url,
                'success': True,
                'reviews_count': len(reviews),
                'rating': overall_rating,
                'duration': result['extraction_duration'],
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"Successfully scraped {len(reviews)} reviews for {company_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error scraping {company_name} from {url}: {str(e)}"
            logger.error(error_msg)
            
            # Update statistics
            self.extraction_stats['failed_extractions'] += 1
            
            # Record failed extraction
            self.extraction_history.append({
                'company': company_name,
                'url': url,
                'success': False,
                'error': str(e),
                'duration': (datetime.now() - extraction_start).total_seconds(),
                'timestamp': datetime.now().isoformat()
            })
            
            return {'error': str(e), 'company': company_name}
    
    async def _extract_overall_rating(self) -> str:
        """Extract overall rating using precise selectors"""
        try:
            # Method 1: Look for rating pattern in text
            page_text = await self.page.content()
            rating_match = re.search(r'Overall Rating:\s*(\d+\.\d+)\s*\((\d+)\)', page_text)
            if rating_match:
                logger.debug(f"Found rating using regex: {rating_match.group(1)}")
                return rating_match.group(1)
            
            # Method 2: Use precise selectors from screenshots
            rating_selectors = [
                'span[data-testid="star-rating-count"]',
                '.star-rating-label',
                '.sb.type-40.star-rating-label',
                '[data-testid="rating"]',
                '.rating-value',
                '.overall-rating'
            ]
            
            for selector in rating_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        for element in elements:
                            text = await element.text_content()
                            if text and re.match(r'\d+\.\d+', text.strip()):
                                logger.debug(f"Found rating using selector '{selector}': {text.strip()}")
                                return text.strip()
                except Exception as e:
                    logger.debug(f"Selector '{selector}' failed: {str(e)}")
                    continue
            
            logger.warning("No overall rating found")
            return 'N/A'
            
        except Exception as e:
            logger.error(f"Error extracting overall rating: {str(e)}")
            return 'N/A'
    
    async def _extract_review_count(self) -> str:
        """Extract review count"""
        try:
            page_text = await self.page.content()
            
            # Look for pattern like "Overall Rating: 4.6 (1848)"
            count_match = re.search(r'Overall Rating:\s*\d+\.\d+\s*\((\d+)\)', page_text)
            if count_match:
                return count_match.group(1)
            
            # Look for standalone review count patterns
            count_patterns = [
                r'(\d+)\s+reviews?',
                r'(\d+)\s+ratings?',
                r'\((\d+)\)'
            ]
            
            for pattern in count_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    # Return the largest number found (likely the total review count)
                    numbers = [int(m) for m in matches if m.isdigit()]
                    if numbers:
                        return str(max(numbers))
            
            return 'N/A'
            
        except Exception as e:
            logger.error(f"Error extracting review count: {str(e)}")
            return 'N/A'
    
    async def _extract_individual_reviews(self) -> List[Dict[str, Any]]:
        """Extract individual reviews using precise selectors"""
        reviews = []
        
        try:
            # PRECISE SELECTORS from screenshots
            review_selectors = [
                'div[data-testid="review-summary-item"]',
                '.sb.card.padding-medium',
                '.rounded-xl.border.border-neutral-20.bg-card',
                '.review-item',
                '.review-card',
                '.review-container',
                '[data-testid="review"]'
            ]
            
            review_elements = []
            for selector in review_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        review_elements = elements
                        logger.debug(f"Found {len(elements)} review elements with selector '{selector}'")
                        break
                except Exception as e:
                    logger.debug(f"Selector '{selector}' failed: {str(e)}")
                    continue
            
            if not review_elements:
                # Pattern matching fallback
                logger.debug("No review elements found with standard selectors, trying pattern matching")
                all_elements = await self.page.query_selector_all('div, p, span')
                potential_reviews = []
                
                for element in all_elements:
                    try:
                        text = await element.text_content()
                        if text and len(text) > 30:
                            if any(phrase in text.lower() for phrase in [
                                'what do you like best about',
                                'what do you dislike about',
                                'powerful tool that empowers',
                                'blended data feature',
                                'experience of working',
                                'recommend this product'
                            ]):
                                potential_reviews.append(element)
                    except:
                        continue
                
                if potential_reviews:
                    review_elements = potential_reviews[:20]
                    logger.debug(f"Found {len(potential_reviews)} potential review elements using pattern matching")
            
            # Extract review data
            max_reviews = 25  # Limit to avoid detection
            for i, element in enumerate(review_elements[:max_reviews]):
                try:
                    review_data = await self._extract_single_review(element)
                    if review_data and review_data.get('text'):
                        reviews.append(review_data)
                        await asyncio.sleep(random.uniform(0.2, 0.4))
                        
                except Exception as e:
                    logger.warning(f"Error extracting review {i}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(reviews)} individual reviews")
            return reviews
            
        except Exception as e:
            logger.error(f"Error extracting individual reviews: {str(e)}")
            return []
    
    async def _extract_single_review(self, element) -> Optional[Dict[str, Any]]:
        """Extract data from a single review element"""
        try:
            text = await element.text_content()
            if not text or len(text) < 20:
                return None
            
            # Extract rating
            rating_match = re.search(r'(\d+\.\d+)', text)
            rating = rating_match.group(1) if rating_match else 'N/A'
            
            # Extract date
            date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', text)
            date = date_match.group(0) if date_match else 'N/A'
            
            # Extract reviewer name
            reviewer = 'Anonymous'
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) < 50:
                    if not any(word in line.lower() for word in ['what', 'about', 'powerful', 'tool', 'experience', 'recommend']):
                        if not any(char.isdigit() for char in line):
                            if re.match(r'^[A-Z][a-z]+\s+[A-Z]\.?$', line):
                                reviewer = line
                                break
            
            # Extract pros/cons if present
            pros = []
            cons = []
            
            if '+ Pros' in text:
                pros_section = text.split('+ Pros')[1].split('- Cons')[0] if '- Cons' in text else text.split('+ Pros')[1]
                pros = [line.strip() for line in pros_section.split('\n') if line.strip() and len(line.strip()) > 10]
            
            if '- Cons' in text:
                cons_section = text.split('- Cons')[1]
                cons = [line.strip() for line in cons_section.split('\n') if line.strip() and len(line.strip()) > 10]
            
            return {
                'text': text,
                'rating': rating,
                'date': date,
                'reviewer': reviewer,
                'pros': pros,
                'cons': cons
            }
            
        except Exception as e:
            logger.warning(f"Error extracting single review: {str(e)}")
            return None
    
    async def _extract_pricing(self) -> str:
        """Extract pricing information"""
        try:
            page_text = await self.page.content()
            
            # Look for pricing patterns
            pricing_patterns = [
                r'Starting from:\s*\$?(\d+)/?Per Month',
                r'From\s*\$?(\d+)/?month',
                r'Pricing starts at\s*\$?(\d+)',
                r'\$(\d+)/?month',
                r'\$(\d+)\s*per\s*month'
            ]
            
            for pattern in pricing_patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    price = match.group(1)
                    return f"${price}/Per Month"
            
            return 'N/A'
            
        except Exception as e:
            logger.error(f"Error extracting pricing: {str(e)}")
            return 'N/A'
    
    async def _extract_rating_categories(self) -> Dict[str, str]:
        """Extract rating categories"""
        try:
            rating_categories = {}
            page_text = await self.page.content()
            
            # Look for patterns like "Ease of Use: 4.1"
            category_pattern = r'([^:]+):\s*(\d+\.\d+)'
            matches = re.findall(category_pattern, page_text)
            
            for category, rating in matches:
                category_name = category.strip()
                if any(word in category_name.lower() for word in ['ease', 'customer', 'features', 'value', 'support', 'usability']):
                    rating_categories[category_name] = rating
            
            return rating_categories
            
        except Exception as e:
            logger.error(f"Error extracting rating categories: {str(e)}")
            return {}
    
    async def extract_alternatives(self, url: str, company_name: str) -> List[Dict[str, Any]]:
        """Extract competitor alternatives"""
        try:
            logger.info(f"Scraping alternatives for {company_name} from {url}")
            await self.page.goto(url, wait_until='domcontentloaded')
            await asyncio.sleep(2)
            
            # Extract alternatives using precise selectors
            alternatives = []
            card_selectors = [
                'div[data-testid="alternative-card"]',
                '.sb.card.padding-medium',
                '.product-card',
                '.alternative-card',
                '.competitor-card'
            ]
            
            product_cards = []
            for selector in card_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        product_cards = elements
                        logger.debug(f"Found {len(elements)} product cards with selector '{selector}'")
                        break
                except Exception as e:
                    logger.debug(f"Selector '{selector}' failed: {str(e)}")
                    continue
            
            if not product_cards:
                logger.warning("No product cards found for alternatives")
                return alternatives
            
            # Extract data from each product card
            max_alternatives = 10  # Limit to avoid detection
            for i, card in enumerate(product_cards[:max_alternatives]):
                try:
                    product_data = await self._extract_product_card_data(card)
                    if product_data:
                        alternatives.append(product_data)
                        await asyncio.sleep(random.uniform(0.2, 0.4))
                except Exception as e:
                    logger.warning(f"Error extracting product card {i}: {str(e)}")
                    continue
            
            self.extraction_stats['alternatives_found'] += len(alternatives)
            logger.info(f"Found {len(alternatives)} alternatives for {company_name}")
            return alternatives
            
        except Exception as e:
            logger.error(f"Error extracting alternatives for {company_name}: {str(e)}")
            return []
    
    async def _extract_product_card_data(self, card_element) -> Optional[Dict[str, Any]]:
        """Extract data from a product card"""
        try:
            # Extract product name
            name_selectors = ['h3', 'h4', '.product-name', '.card-title', '[data-testid="product-name"]']
            product_name = 'Unknown'
            
            for selector in name_selectors:
                try:
                    elements = await card_element.query_selector_all(selector)
                    if elements:
                        product_name = await elements[0].text_content()
                        if product_name:
                            product_name = product_name.strip()
                            break
                except:
                    continue
            
            # Extract rating
            rating_selectors = [
                'span[data-testid="star-rating-count"]',
                '.star-rating-label',
                '.sb.type-40.star-rating-label',
                '.rating-value',
                '[data-testid="rating"]'
            ]
            
            rating = 'N/A'
            for selector in rating_selectors:
                try:
                    elements = await card_element.query_selector_all(selector)
                    if elements:
                        for element in elements:
                            text = await element.text_content()
                            if text and re.match(r'\d+\.\d+', text.strip()):
                                rating = text.strip()
                                break
                        if rating != 'N/A':
                            break
                except:
                    continue
            
            # Extract review count
            review_count = 'N/A'
            if rating != 'N/A':
                card_text = await card_element.text_content()
                count_match = re.search(r'\((\d+)\)', card_text)
                if count_match:
                    review_count = count_match.group(1)
            
            # Extract pricing
            pricing = 'N/A'
            card_text = await card_element.text_content()
            pricing_match = re.search(r'Starting from:\s*\$?(\d+)/?Per Month', card_text)
            if pricing_match:
                pricing = f"${pricing_match.group(1)}/Per Month"
            
            return {
                'product_name': product_name,
                'rating': rating,
                'review_count': review_count,
                'pricing': pricing
            }
            
        except Exception as e:
            logger.warning(f"Error extracting product card data: {str(e)}")
            return None
    
    def get_extraction_statistics(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        total_attempts = self.extraction_stats['extraction_attempts']
        success_rate = self.extraction_stats['successful_extractions'] / max(total_attempts, 1)
        
        return {
            'extraction_attempts': total_attempts,
            'successful_extractions': self.extraction_stats['successful_extractions'],
            'failed_extractions': self.extraction_stats['failed_extractions'],
            'success_rate': success_rate,
            'reviews_extracted': self.extraction_stats['reviews_extracted'],
            'ratings_extracted': self.extraction_stats['ratings_extracted'],
            'pricing_extracted': self.extraction_stats['pricing_extracted'],
            'alternatives_found': self.extraction_stats['alternatives_found'],
            'recent_extractions': self.extraction_history[-5:] if self.extraction_history else []
        }
