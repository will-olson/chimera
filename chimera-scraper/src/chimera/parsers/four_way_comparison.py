"""Specialized parser for G2 four-way comparison pages with comprehensive data extraction."""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from loguru import logger

from .base import BaseParser


@dataclass
class FourWayComparisonData:
    """Structured data for four-way comparison analysis."""
    comparison_id: str
    extraction_date: datetime
    url: str
    
    # Product information
    products: List[Dict[str, Any]]
    
    # Comparison sections
    at_a_glance: Dict[str, Any]
    pricing: Dict[str, Any]
    ratings: Dict[str, Any]
    features_by_category: Dict[str, Any]
    
    # Metadata
    total_products: int
    comparison_categories: List[str]
    data_quality_score: float
    extraction_confidence: float


@dataclass
class ProductComparison:
    """Individual product data within a four-way comparison."""
    name: str
    g2_product_id: str
    vendor_id: str
    star_rating: float
    review_count: int
    market_segments: Dict[str, float]
    entry_level_pricing: str
    pricing_details: Dict[str, Any]
    ratings_by_criteria: Dict[str, float]
    feature_scores: Dict[str, float]


class G2FourWayComparisonParser(BaseParser):
    """Specialized parser for G2 four-way comparison pages."""
    
    def __init__(self):
        super().__init__()
        self.comparison_selectors = {
            "main_container": '[data-eventscope="Comparison Table"], #comparison-table',
            "product_headers": '.comparison-container-v2_header, .comparison-container_header',
            "comparison_sections": '.comparison-container-v2_block, .comparison-container_block',
            "rating_elements": '[aria-label*="out of 10"], [aria-label*="out of 5"]',
            "pricing_elements": '[class*="pricing"], [class*="price"]',
            "feature_elements": '[class*="feature"], [class*="category"]'
        }
        
        # Known comparison sections from screenshots
        self.known_sections = [
            "At a Glance",
            "Featured Products", 
            "Compare Products",
            "Pricing",
            "Ratings",
            "Features by Category"
        ]
        
        # Rating criteria mapping
        self.rating_criteria = {
            "meets_requirements": ["Meets Requirements", "meets requirements"],
            "ease_of_use": ["Ease of Use", "ease of use"],
            "ease_of_setup": ["Ease of Setup", "ease of setup"],
            "ease_of_admin": ["Ease of Admin", "ease of admin"],
            "quality_of_support": ["Quality of Support", "quality of support"],
            "business_partner": ["Has the product been a good partner in doing business?", "good partner"],
            "product_direction": ["Product Direction", "product direction"]
        }
        
        # Feature categories from screenshots
        self.feature_categories = [
            "Business Intelligence",
            "Analytics Platforms", 
            "Embedded Business Intelligence",
            "Location Intelligence",
            "Data Preparation",
            "Insurance Analytics",
            "Data Governance"
        ]
    
    async def parse_four_way_comparison(self, html: str, url: str) -> FourWayComparisonData:
        """Parse a G2 four-way comparison page comprehensively."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract basic comparison info
            comparison_id = self._extract_comparison_id(url)
            
            # Extract products information
            products = await self._extract_products(soup)
            
            # Extract comparison sections
            at_a_glance = await self._extract_at_a_glance(soup, products)
            pricing = await self._extract_pricing(soup, products)
            ratings = await self._extract_ratings(soup, products)
            features_by_category = await self._extract_features_by_category(soup, products)
            
            # Calculate data quality metrics
            data_quality_score = self._calculate_data_quality_score(
                products, at_a_glance, pricing, ratings, features_by_category
            )
            
            # Create comparison data
            comparison_data = FourWayComparisonData(
                comparison_id=comparison_id,
                extraction_date=datetime.now(),
                url=url,
                products=[asdict(product) for product in products],
                at_a_glance=at_a_glance,
                pricing=pricing,
                ratings=ratings,
                features_by_category=features_by_category,
                total_products=len(products),
                comparison_categories=self._identify_comparison_categories(soup),
                data_quality_score=data_quality_score,
                extraction_confidence=self._calculate_extraction_confidence(soup)
            )
            
            logger.info(f"Successfully parsed four-way comparison with {len(products)} products")
            return comparison_data
            
        except Exception as e:
            logger.error(f"Failed to parse four-way comparison: {e}")
            raise
    
    def _extract_comparison_id(self, url: str) -> str:
        """Extract unique comparison ID from URL."""
        try:
            # Extract the comparison part from URL
            # Example: g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense-vs-tableau-vs-domo
            comparison_part = url.split('/compare/')[-1]
            # Clean and create ID
            comparison_id = comparison_part.replace('-', '_').replace('vs', 'vs')
            return f"four_way_{comparison_id}"
        except Exception as e:
            logger.warning(f"Failed to extract comparison ID: {e}")
            return f"four_way_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def _extract_products(self, soup: BeautifulSoup) -> List[ProductComparison]:
        """Extract product information from comparison headers."""
        products = []
        
        try:
            # Find product headers using multiple selector strategies
            product_headers = soup.select(self.comparison_selectors["product_headers"])
            
            if not product_headers:
                # Fallback: look for product names in comparison structure
                product_headers = soup.find_all('div', class_=re.compile(r'comparison.*header'))
            
            for header in product_headers:
                try:
                    product = await self._extract_single_product(header)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.warning(f"Failed to extract product from header: {e}")
                    continue
            
            # If we still don't have products, try alternative extraction
            if not products:
                products = await self._extract_products_alternative(soup)
            
            logger.info(f"Extracted {len(products)} products from comparison")
            return products
            
        except Exception as e:
            logger.error(f"Failed to extract products: {e}")
            return []
    
    async def _extract_single_product(self, header_element) -> Optional[ProductComparison]:
        """Extract information for a single product from header element."""
        try:
            # Extract product name
            product_name = self._extract_product_name(header_element)
            if not product_name:
                return None
            
            # Extract G2 product ID and vendor ID
            g2_product_id, vendor_id = self._extract_product_identifiers(header_element)
            
            # Extract star rating and review count
            star_rating, review_count = self._extract_rating_info(header_element)
            
            # Extract market segments
            market_segments = self._extract_market_segments(header_element)
            
            # Extract entry level pricing
            entry_level_pricing = self._extract_entry_level_pricing(header_element)
            
            # Create product comparison object
            product = ProductComparison(
                name=product_name,
                g2_product_id=g2_product_id,
                vendor_id=vendor_id,
                star_rating=star_rating,
                review_count=review_count,
                market_segments=market_segments,
                entry_level_pricing=entry_level_pricing,
                pricing_details={},
                ratings_by_criteria={},
                feature_scores={}
            )
            
            return product
            
        except Exception as e:
            logger.warning(f"Failed to extract single product: {e}")
            return None
    
    def _extract_product_name(self, element) -> Optional[str]:
        """Extract product name from header element."""
        try:
            # Strategy 1: Look for product name in text content
            text_content = element.get_text(strip=True)
            if text_content and len(text_content) < 100:  # Reasonable product name length
                return text_content
            
            # Strategy 2: Look for specific product name elements
            name_element = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div'], 
                                      class_=re.compile(r'product.*name|name.*product', re.I))
            if name_element:
                return name_element.get_text(strip=True)
            
            # Strategy 3: Look for aria-label with product name
            aria_label = element.get('aria-label', '')
            if aria_label and any(name in aria_label for name in ['Power BI', 'Tableau', 'Qlik', 'Domo', 'Snowflake']):
                # Extract product name from aria-label
                for name in ['Power BI', 'Tableau', 'Qlik', 'Domo', 'Snowflake']:
                    if name in aria_label:
                        return name
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to extract product name: {e}")
            return None
    
    def _extract_product_identifiers(self, element) -> Tuple[str, str]:
        """Extract G2 product ID and vendor ID."""
        try:
            # Strategy 1: Look for data attributes
            data_event_options = element.find('a', attrs={'data-event-options': True})
            if data_event_options:
                try:
                    event_data = json.loads(data_event_options['data-event-options'])
                    product_id = event_data.get('product', '').lower().replace(' ', '-')
                    vendor_id = str(event_data.get('vendor_id', ''))
                    return product_id, vendor_id
                except json.JSONDecodeError:
                    pass
            
            # Strategy 2: Look for href patterns
            href_links = element.find_all('a', href=True)
            for link in href_links:
                href = link['href']
                if '/products/' in href:
                    # Extract product ID from href
                    product_id = href.split('/products/')[-1].split('/')[0]
                    return product_id, ''
            
            # Strategy 3: Generate from product name
            product_name = self._extract_product_name(element)
            if product_name:
                product_id = product_name.lower().replace(' ', '-').replace('microsoft-', '')
                return product_id, ''
            
            return '', ''
            
        except Exception as e:
            logger.warning(f"Failed to extract product identifiers: {e}")
            return '', ''
    
    def _extract_rating_info(self, element) -> Tuple[float, int]:
        """Extract star rating and review count."""
        try:
            # Strategy 1: Look for star rating in aria-label
            aria_label = element.get('aria-label', '')
            if 'star rating' in aria_label.lower():
                # Extract rating from aria-label
                rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', aria_label)
                if rating_match:
                    star_rating = float(rating_match.group(1))
                    
                    # Extract review count
                    review_match = re.search(r'(\d+(?:,\d+)*)\s*reviews?', aria_label)
                    if review_match:
                        review_count = int(review_match.group(1).replace(',', ''))
                        return star_rating, review_count
            
            # Strategy 2: Look for rating elements
            rating_elements = element.find_all(['span', 'div'], class_=re.compile(r'star|rating'))
            for rating_elem in rating_elements:
                text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+\.?\d*)', text)
                if rating_match:
                    star_rating = float(rating_match.group(1))
                    # Try to find review count nearby
                    review_count = self._extract_review_count_nearby(rating_elem)
                    return star_rating, review_count
            
            return 0.0, 0
            
        except Exception as e:
            logger.warning(f"Failed to extract rating info: {e}")
            return 0.0, 0
    
    def _extract_review_count_nearby(self, rating_element) -> int:
        """Extract review count from elements near rating."""
        try:
            # Look for review count in parent or sibling elements
            parent = rating_element.parent
            if parent:
                # Look for review count in parent text
                parent_text = parent.get_text()
                review_match = re.search(r'\((\d+(?:,\d+)*)\)', parent_text)
                if review_match:
                    return int(review_match.group(1).replace(',', ''))
                
                # Look for review count in siblings
                for sibling in parent.find_next_siblings():
                    sibling_text = sibling.get_text()
                    review_match = re.search(r'(\d+(?:,\d+)*)', sibling_text)
                    if review_match:
                        return int(review_match.group(1).replace(',', ''))
            
            return 0
            
        except Exception as e:
            logger.warning(f"Failed to extract review count nearby: {e}")
            return 0
    
    def _extract_market_segments(self, element) -> Dict[str, float]:
        """Extract market segment information."""
        try:
            market_segments = {}
            
            # Look for market segment information in aria-label or text
            aria_label = element.get('aria-label', '')
            if 'market segment' in aria_label.lower():
                # Extract percentage from aria-label
                percentage_match = re.search(r'(\d+(?:\.\d+)?)%', aria_label)
                if percentage_match:
                    percentage = float(percentage_match.group(1))
                    # Determine segment type
                    if 'enterprise' in aria_label.lower():
                        market_segments['enterprise'] = percentage
                    elif 'mid-market' in aria_label.lower():
                        market_segments['mid_market'] = percentage
                    elif 'small business' in aria_label.lower():
                        market_segments['small_business'] = percentage
            
            return market_segments
            
        except Exception as e:
            logger.warning(f"Failed to extract market segments: {e}")
            return {}
    
    def _extract_entry_level_pricing(self, element) -> str:
        """Extract entry level pricing information."""
        try:
            # Look for pricing information in text or aria-label
            text_content = element.get_text()
            aria_label = element.get('aria-label', '')
            
            # Combine text sources
            full_text = f"{text_content} {aria_label}"
            
            # Look for pricing patterns
            pricing_patterns = [
                r'\$[\d,]+(?:\.\d{2})?',
                r'Free',
                r'Contact Sales',
                r'Free Trial'
            ]
            
            for pattern in pricing_patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    return match.group(0)
            
            return "Not specified"
            
        except Exception as e:
            logger.warning(f"Failed to extract entry level pricing: {e}")
            return "Not specified"
    
    async def _extract_products_alternative(self, soup: BeautifulSoup) -> List[ProductComparison]:
        """Alternative method to extract products if primary method fails."""
        products = []
        
        try:
            # Look for product names in the page title or URL
            title = soup.find('title')
            if title:
                title_text = title.get_text()
                # Extract product names from title
                product_names = self._extract_product_names_from_text(title_text)
                
                for name in product_names:
                    product = ProductComparison(
                        name=name,
                        g2_product_id=name.lower().replace(' ', '-'),
                        vendor_id='',
                        star_rating=0.0,
                        review_count=0,
                        market_segments={},
                        entry_level_pricing="Not specified",
                        pricing_details={},
                        ratings_by_criteria={},
                        feature_scores={}
                    )
                    products.append(product)
            
            return products
            
        except Exception as e:
            logger.warning(f"Alternative product extraction failed: {e}")
            return []
    
    def _extract_product_names_from_text(self, text: str) -> List[str]:
        """Extract product names from text content."""
        known_products = [
            'Microsoft Power BI', 'Power BI', 'Qlik Sense', 'Tableau', 'Domo',
            'Snowflake', 'Databricks', 'Amazon Redshift', 'Google BigQuery',
            'Looker', 'Sisense', 'ThoughtSpot'
        ]
        
        found_products = []
        for product in known_products:
            if product.lower() in text.lower():
                found_products.append(product)
        
        return found_products
    
    async def _extract_at_a_glance(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract 'At a Glance' section data."""
        try:
            at_a_glance = {
                "star_ratings": {},
                "market_segments": {},
                "entry_level_pricing": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Extract data for each product
            for product in products:
                product_name = product.name
                
                # Star ratings
                at_a_glance["star_ratings"][product_name] = {
                    "rating": product.star_rating,
                    "review_count": product.review_count
                }
                
                # Market segments
                at_a_glance["market_segments"][product_name] = product.market_segments
                
                # Entry level pricing
                at_a_glance["entry_level_pricing"][product_name] = product.entry_level_pricing
            
            return at_a_glance
            
        except Exception as e:
            logger.warning(f"Failed to extract at a glance data: {e}")
            return {}
    
    async def _extract_pricing(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract comprehensive pricing information."""
        try:
            pricing_data = {
                "entry_level_pricing": {},
                "free_trials": {},
                "pricing_details": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for pricing section
            pricing_section = soup.find('div', string=re.compile(r'pricing', re.I))
            if not pricing_section:
                pricing_section = soup.find('div', id='pricing')
            
            if pricing_section:
                # Extract pricing for each product
                for product in products:
                    product_name = product.name
                    
                    # Look for pricing information in the section
                    pricing_info = self._extract_product_pricing(pricing_section, product_name)
                    pricing_data["entry_level_pricing"][product_name] = pricing_info.get("entry_level", "Not specified")
                    pricing_data["free_trials"][product_name] = pricing_info.get("free_trial", "Not specified")
                    pricing_data["pricing_details"][product_name] = pricing_info.get("details", {})
            
            return pricing_data
            
        except Exception as e:
            logger.warning(f"Failed to extract pricing data: {e}")
            return {}
    
    def _extract_product_pricing(self, pricing_section, product_name: str) -> Dict[str, Any]:
        """Extract pricing information for a specific product."""
        try:
            pricing_info = {
                "entry_level": "Not specified",
                "free_trial": "Not specified",
                "details": {}
            }
            
            # Look for pricing information in the section
            # This is a simplified extraction - in practice, you'd need more sophisticated logic
            # based on the actual HTML structure
            
            return pricing_info
            
        except Exception as e:
            logger.warning(f"Failed to extract product pricing: {e}")
            return {}
    
    async def _extract_ratings(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract detailed ratings by criteria."""
        try:
            ratings_data = {
                "criteria_ratings": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for ratings section
            ratings_section = soup.find('div', string=re.compile(r'ratings', re.I))
            if not ratings_section:
                ratings_section = soup.find('div', id='ratings')
            
            if ratings_section:
                # Extract ratings for each criterion
                for criterion_key, criterion_names in self.rating_criteria.items():
                    criterion_ratings = {}
                    
                    for product in products:
                        product_name = product.name
                        rating = self._extract_criterion_rating(ratings_section, product_name, criterion_names)
                        criterion_ratings[product_name] = rating
                    
                    ratings_data["criteria_ratings"][criterion_key] = criterion_ratings
            
            return ratings_data
            
        except Exception as e:
            logger.warning(f"Failed to extract ratings data: {e}")
            return {}
    
    def _extract_criterion_rating(self, ratings_section, product_name: str, criterion_names: List[str]) -> float:
        """Extract rating for a specific criterion and product."""
        try:
            # Look for rating elements with aria-label containing the criterion and product
            for criterion_name in criterion_names:
                # Look for elements with aria-label containing both product name and criterion
                rating_elements = ratings_section.find_all(
                    'div', 
                    attrs={'aria-label': re.compile(f'{product_name}.*{criterion_name}|{criterion_name}.*{product_name}', re.I)}
                )
                
                for element in rating_elements:
                    aria_label = element.get('aria-label', '')
                    # Extract rating from aria-label
                    rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+10', aria_label)
                    if rating_match:
                        return float(rating_match.group(1))
            
            return 0.0
            
        except Exception as e:
            logger.warning(f"Failed to extract criterion rating: {e}")
            return 0.0
    
    async def _extract_features_by_category(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract features by category ratings."""
        try:
            features_data = {
                "category_ratings": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for features section
            features_section = soup.find('div', string=re.compile(r'features.*category|category.*features', re.I))
            
            if features_section:
                # Extract ratings for each feature category
                for category in self.feature_categories:
                    category_ratings = {}
                    
                    for product in products:
                        product_name = product.name
                        rating = self._extract_feature_category_rating(features_section, product_name, category)
                        category_ratings[product_name] = rating
                    
                    features_data["category_ratings"][category] = category_ratings
            
            return features_data
            
        except Exception as e:
            logger.warning(f"Failed to extract features by category: {e}")
            return {}
    
    def _extract_feature_category_rating(self, features_section, product_name: str, category: str) -> float:
        """Extract rating for a specific feature category and product."""
        try:
            # Look for rating elements with aria-label containing the category and product
            rating_elements = features_section.find_all(
                'div', 
                attrs={'aria-label': re.compile(f'{product_name}.*{category}|{category}.*{product_name}', re.I)}
            )
            
            for element in rating_elements:
                aria_label = element.get('aria-label', '')
                # Extract rating from aria-label
                rating_match = re.search(r'(\d+\.?\d*)', aria_label)
                if rating_match:
                    return float(rating_match.group(1))
            
            return 0.0
            
        except Exception as e:
            logger.warning(f"Failed to extract feature category rating: {e}")
            return 0.0
    
    def _identify_comparison_categories(self, soup: BeautifulSoup) -> List[str]:
        """Identify all comparison categories present on the page."""
        try:
            categories = []
            
            # Look for section headers
            section_headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], 
                                          string=re.compile(r'|'.join(self.known_sections), re.I))
            
            for header in section_headers:
                category = header.get_text(strip=True)
                if category:
                    categories.append(category)
            
            return categories
            
        except Exception as e:
            logger.warning(f"Failed to identify comparison categories: {e}")
            return self.known_sections
    
    def _calculate_data_quality_score(self, products: List[ProductComparison], 
                                    at_a_glance: Dict[str, Any], 
                                    pricing: Dict[str, Any], 
                                    ratings: Dict[str, Any], 
                                    features_by_category: Dict[str, Any]) -> float:
        """Calculate overall data quality score."""
        try:
            score = 0.0
            max_score = 100.0
            
            # Product information completeness
            if products:
                product_score = 0.0
                for product in products:
                    product_completeness = 0.0
                    if product.name: product_completeness += 20
                    if product.star_rating > 0: product_completeness += 20
                    if product.review_count > 0: product_completeness += 20
                    if product.entry_level_pricing != "Not specified": product_completeness += 20
                    if product.market_segments: product_completeness += 20
                    product_score += product_completeness
                
                score += (product_score / len(products)) * 0.4  # 40% weight
            
            # Section data completeness
            section_score = 0.0
            if at_a_glance: section_score += 25
            if pricing: section_score += 25
            if ratings: section_score += 25
            if features_by_category: section_score += 25
            
            score += section_score * 0.6  # 60% weight
            
            return min(score, max_score)
            
        except Exception as e:
            logger.warning(f"Failed to calculate data quality score: {e}")
            return 0.0
    
    def _calculate_extraction_confidence(self, soup: BeautifulSoup) -> float:
        """Calculate confidence in the extraction process."""
        try:
            confidence = 0.0
            
            # Check for key structural elements
            if soup.find('div', attrs={'data-eventscope': 'Comparison Table'}):
                confidence += 30
            if soup.find('div', id='comparison-table'):
                confidence += 20
            if soup.find('div', class_=re.compile(r'comparison.*container')):
                confidence += 25
            if soup.find('div', attrs={'aria-label': re.compile(r'out of \d+')}):
                confidence += 25
            
            return min(confidence, 100.0)
            
        except Exception as e:
            logger.warning(f"Failed to calculate extraction confidence: {e}")
            return 0.0
    
    def get_extraction_statistics(self) -> Dict[str, Any]:
        """Get statistics about the extraction process."""
        return {
            "parser_type": "G2 Four-Way Comparison Parser",
            "supported_sections": self.known_sections,
            "rating_criteria": list(self.rating_criteria.keys()),
            "feature_categories": self.feature_categories,
            "extraction_methods": [
                "aria-label parsing",
                "structured HTML parsing", 
                "fallback text extraction"
            ]
        }
