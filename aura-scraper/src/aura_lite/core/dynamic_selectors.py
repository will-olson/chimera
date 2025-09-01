"""
Dynamic Selector System
Uses extracted selectors from developer tools analysis for precise data extraction
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class DynamicSelectorManager:
    """Manages dynamic selectors extracted from real page analysis"""
    
    def __init__(self, selectors_file: Optional[str] = None):
        self.selectors_file = selectors_file or "output/selectors/combined_capterra_selectors.json"
        self.selectors = self._load_selectors()
        self.fallback_selectors = self._get_fallback_selectors()
    
    def _load_selectors(self) -> Dict[str, Any]:
        """Load extracted selectors from file"""
        try:
            if Path(self.selectors_file).exists():
                with open(self.selectors_file, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Selectors file not found: {self.selectors_file}")
                return {}
        except Exception as e:
            logger.error(f"Error loading selectors: {str(e)}")
            return {}
    
    def _get_fallback_selectors(self) -> Dict[str, str]:
        """Fallback selectors based on common Capterra patterns"""
        return {
            'company_name': 'h1, .company-name, [class*="company"] h1',
            'company_logo': 'img[alt*="logo"], .logo img, [class*="logo"] img',
            'overall_rating': '[class*="rating"], [class*="star"], .rating',
            'review_count': 'p:contains("Based on"), [class*="review-count"]',
            'review_container': 'article, .review, [class*="review"], [data-testid*="review"]',
            'reviewer_name': 'h3, h4, .reviewer-name, [class*="name"]',
            'review_text': 'p, .review-text, [class*="text"]',
            'review_date': 'time, .date, [class*="date"]',
            'pricing': '[class*="price"], [class*="cost"], [class*="pricing"]',
            'alternative_card': '.card, [class*="product"], [class*="alternative"]',
            'rating_categories': '[class*="rating"] [class*="category"]',
            'write_review_button': 'a:contains("Write a review"), button:contains("Write a review")',
            'visit_website_button': 'a:contains("Visit Website"), button:contains("Visit Website")'
        }
    
    def get_selector(self, element_type: str, company: str = None) -> str:
        """Get selector for specific element type, with company-specific fallback"""
        # Try company-specific selector first
        if company and company in self.selectors:
            company_selectors = self.selectors[company]
            
            # Map element type to selector category
            selector_mapping = {
                'company_name': 'company_info.name',
                'company_logo': 'company_info.logo',
                'overall_rating': 'rating_info.overall_rating',
                'review_count': 'rating_info.review_count_element',
                'review_container': 'reviews.container_selector',
                'reviewer_name': 'reviews.reviewer_name_selector',
                'review_text': 'reviews.review_text_selector',
                'review_date': 'reviews.review_date_selector',
                'pricing': 'pricing.pricing_selector',
                'alternative_card': 'alternatives.alternative_card_selector'
            }
            
            if element_type in selector_mapping:
                path_parts = selector_mapping[element_type].split('.')
                selector_value = company_selectors
                
                for part in path_parts:
                    if isinstance(selector_value, dict) and part in selector_value:
                        selector_value = selector_value[part]
                    else:
                        selector_value = None
                        break
                
                if selector_value:
                    return selector_value
        
        # Fall back to generic selectors
        return self.fallback_selectors.get(element_type, f'[class*="{element_type}"]')
    
    def get_company_selectors(self, company: str) -> Dict[str, str]:
        """Get all selectors for a specific company"""
        if company not in self.selectors:
            return self.fallback_selectors
        
        company_data = self.selectors[company]
        selectors = {}
        
        # Extract company info selectors
        if 'company_info' in company_data:
            company_info = company_data['company_info']
            if 'name' in company_info:
                selectors['company_name'] = company_info['name']
            if 'logo' in company_info:
                selectors['company_logo'] = company_info['logo']
        
        # Extract rating selectors
        if 'rating_info' in company_data:
            rating_info = company_data['rating_info']
            if 'overall_rating' in rating_info:
                selectors['overall_rating'] = rating_info['overall_rating']
            if 'review_count_element' in rating_info:
                selectors['review_count'] = rating_info['review_count_element']
        
        # Extract review selectors
        if 'reviews' in company_data:
            reviews = company_data['reviews']
            if 'container_selector' in reviews:
                selectors['review_container'] = reviews['container_selector']
            if 'reviewer_name_selector' in reviews:
                selectors['reviewer_name'] = reviews['reviewer_name_selector']
            if 'review_text_selector' in reviews:
                selectors['review_text'] = reviews['review_text_selector']
            if 'review_date_selector' in reviews:
                selectors['review_date'] = reviews['review_date_selector']
        
        # Extract pricing selectors
        if 'pricing' in company_data:
            pricing = company_data['pricing']
            if 'pricing_selector' in pricing:
                selectors['pricing'] = pricing['pricing_selector']
        
        # Extract alternatives selectors
        if 'alternatives' in company_data:
            alternatives = company_data['alternatives']
            if 'alternative_card_selector' in alternatives:
                selectors['alternative_card'] = alternatives['alternative_card_selector']
        
        # Fill in missing selectors with fallbacks
        for key, fallback in self.fallback_selectors.items():
            if key not in selectors:
                selectors[key] = fallback
        
        return selectors

class PreciseDataExtractor:
    """Precise data extractor using dynamic selectors"""
    
    def __init__(self, page: Page, selector_manager: DynamicSelectorManager):
        self.page = page
        self.selector_manager = selector_manager
        self.extraction_stats = {
            'elements_found': 0,
            'elements_missing': 0,
            'extraction_errors': 0
        }
    
    async def extract_company_data(self, company: str) -> Dict[str, Any]:
        """Extract company data using precise selectors"""
        print(f"🔍 Extracting data for: {company}")
        
        selectors = self.selector_manager.get_company_selectors(company)
        data = {}
        
        try:
            # Extract company name
            company_name = await self._extract_element_text(
                selectors['company_name'], 
                f"company name for {company}"
            )
            data['company_name'] = company_name
            
            # Extract company logo
            logo_url = await self._extract_element_attribute(
                selectors['company_logo'], 
                'src', 
                f"company logo for {company}"
            )
            data['company_logo'] = logo_url
            
            # Extract overall rating
            overall_rating = await self._extract_element_text(
                selectors['overall_rating'], 
                f"overall rating for {company}"
            )
            data['overall_rating'] = overall_rating
            
            # Extract review count
            review_count = await self._extract_element_text(
                selectors['review_count'], 
                f"review count for {company}"
            )
            data['review_count'] = review_count
            
            # Extract pricing
            pricing = await self._extract_element_text(
                selectors['pricing'], 
                f"pricing for {company}"
            )
            data['pricing'] = pricing
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting company data for {company}: {str(e)}")
            self.extraction_stats['extraction_errors'] += 1
            return {'error': str(e)}
    
    async def extract_reviews(self, company: str, max_reviews: int = 10) -> List[Dict[str, Any]]:
        """Extract individual reviews using precise selectors"""
        print(f"📝 Extracting reviews for: {company}")
        
        selectors = self.selector_manager.get_company_selectors(company)
        reviews = []
        
        try:
            # Find review containers
            review_containers = await self.page.query_selector_all(selectors['review_container'])
            
            if not review_containers:
                print(f"   ⚠️ No review containers found for {company}")
                return reviews
            
            print(f"   📊 Found {len(review_containers)} review containers")
            
            # Extract data from each review
            for i, container in enumerate(review_containers[:max_reviews]):
                try:
                    review_data = {}
                    
                    # Extract reviewer name
                    reviewer_name = await self._extract_from_container(
                        container, 
                        selectors['reviewer_name'], 
                        'text'
                    )
                    review_data['reviewer_name'] = reviewer_name
                    
                    # Extract review text
                    review_text = await self._extract_from_container(
                        container, 
                        selectors['review_text'], 
                        'text'
                    )
                    review_data['review_text'] = review_text
                    
                    # Extract review date
                    review_date = await self._extract_from_container(
                        container, 
                        selectors['review_date'], 
                        'text'
                    )
                    review_data['review_date'] = review_date
                    
                    # Extract rating (if available)
                    rating = await self._extract_from_container(
                        container, 
                        selectors['overall_rating'], 
                        'text'
                    )
                    review_data['rating'] = rating
                    
                    if review_data['review_text']:  # Only add if we have review text
                        reviews.append(review_data)
                        self.extraction_stats['elements_found'] += 1
                    
                except Exception as e:
                    logger.error(f"Error extracting review {i}: {str(e)}")
                    self.extraction_stats['extraction_errors'] += 1
                    continue
            
            print(f"   ✅ Successfully extracted {len(reviews)} reviews")
            return reviews
            
        except Exception as e:
            logger.error(f"Error extracting reviews for {company}: {str(e)}")
            self.extraction_stats['extraction_errors'] += 1
            return []
    
    async def extract_alternatives(self, company: str, max_alternatives: int = 5) -> List[Dict[str, Any]]:
        """Extract alternative products using precise selectors"""
        print(f"🔄 Extracting alternatives for: {company}")
        
        selectors = self.selector_manager.get_company_selectors(company)
        alternatives = []
        
        try:
            # Find alternative cards
            alternative_cards = await self.page.query_selector_all(selectors['alternative_card'])
            
            if not alternative_cards:
                print(f"   ⚠️ No alternative cards found for {company}")
                return alternatives
            
            print(f"   📊 Found {len(alternative_cards)} alternative cards")
            
            # Extract data from each alternative
            for i, card in enumerate(alternative_cards[:max_alternatives]):
                try:
                    alternative_data = {}
                    
                    # Extract alternative name
                    alternative_name = await self._extract_from_container(
                        card, 
                        'h3, h4, .product-name, [class*="name"]', 
                        'text'
                    )
                    alternative_data['name'] = alternative_name
                    
                    # Extract alternative rating
                    alternative_rating = await self._extract_from_container(
                        card, 
                        '[class*="rating"], [class*="star"]', 
                        'text'
                    )
                    alternative_data['rating'] = alternative_rating
                    
                    # Extract alternative link
                    alternative_link = await self._extract_from_container(
                        card, 
                        'a', 
                        'href'
                    )
                    alternative_data['link'] = alternative_link
                    
                    if alternative_data['name']:  # Only add if we have a name
                        alternatives.append(alternative_data)
                        self.extraction_stats['elements_found'] += 1
                    
                except Exception as e:
                    logger.error(f"Error extracting alternative {i}: {str(e)}")
                    self.extraction_stats['extraction_errors'] += 1
                    continue
            
            print(f"   ✅ Successfully extracted {len(alternatives)} alternatives")
            return alternatives
            
        except Exception as e:
            logger.error(f"Error extracting alternatives for {company}: {str(e)}")
            self.extraction_stats['extraction_errors'] += 1
            return []
    
    async def _extract_element_text(self, selector: str, description: str) -> str:
        """Extract text from element using selector"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                text = await element.text_content()
                self.extraction_stats['elements_found'] += 1
                return text.strip() if text else ""
            else:
                self.extraction_stats['elements_missing'] += 1
                return ""
        except Exception as e:
            logger.error(f"Error extracting {description}: {str(e)}")
            self.extraction_stats['extraction_errors'] += 1
            return ""
    
    async def _extract_element_attribute(self, selector: str, attribute: str, description: str) -> str:
        """Extract attribute from element using selector"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                value = await element.get_attribute(attribute)
                self.extraction_stats['elements_found'] += 1
                return value if value else ""
            else:
                self.extraction_stats['elements_missing'] += 1
                return ""
        except Exception as e:
            logger.error(f"Error extracting {description}: {str(e)}")
            self.extraction_stats['extraction_errors'] += 1
            return ""
    
    async def _extract_from_container(self, container, selector: str, extract_type: str) -> str:
        """Extract data from within a container element"""
        try:
            element = await container.query_selector(selector)
            if element:
                if extract_type == 'text':
                    text = await element.text_content()
                    return text.strip() if text else ""
                elif extract_type == 'href':
                    return await element.get_attribute('href') or ""
                else:
                    return await element.get_attribute(extract_type) or ""
            else:
                return ""
        except Exception as e:
            logger.error(f"Error extracting from container: {str(e)}")
            return ""
    
    def get_extraction_stats(self) -> Dict[str, int]:
        """Get extraction statistics"""
        return self.extraction_stats.copy()
