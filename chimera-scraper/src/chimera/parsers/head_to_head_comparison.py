"""Specialized parser for G2 head-to-head comparison pages with focus on AI-generated summaries."""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from loguru import logger

from .base import BaseParser


@dataclass
class HeadToHeadComparisonData:
    """Structured data for head-to-head comparison analysis."""
    comparison_id: str
    extraction_date: datetime
    url: str
    
    # Product information
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    
    # AI-generated summary (most valuable data)
    ai_generated_summary: Dict[str, Any]
    
    # Comparison sections
    at_a_glance: Dict[str, Any]
    pricing: Dict[str, Any]
    ratings: Dict[str, Any]
    features: Dict[str, Any]
    reviews: Dict[str, Any]
    alternatives: Dict[str, Any]
    
    # Metadata
    data_quality_score: float
    extraction_confidence: float
    summary_quality_score: float


@dataclass
class ProductComparison:
    """Individual product data within a head-to-head comparison."""
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


@dataclass
class AIGeneratedSummary:
    """AI-generated summary data with structured insights."""
    summary_title: str
    summary_subtitle: str
    summary_points: List[Dict[str, Any]]
    extraction_confidence: float
    structured_insights: Dict[str, Any]


@dataclass
class SummaryPoint:
    """Individual summary point with structured data."""
    text: str
    product_a_score: Optional[float]
    product_b_score: Optional[float]
    feature_category: str
    insight_type: str
    sentiment: str
    confidence: float


class G2HeadToHeadComparisonParser(BaseParser):
    """Specialized parser for G2 head-to-head comparison pages with AI summary focus."""
    
    def __init__(self):
        super().__init__()
        self.comparison_selectors = {
            "main_container": '[data-eventscope="Comparison Table"], #comparison-table',
            "product_headers": '.comparison-container-v2_header, .comparison-container_header',
            "comparison_sections": '.comparison-container-v2_block, .comparison-container_block',
            "rating_elements": '[aria-label*="out of 10"], [aria-label*="out of 5"]',
            "pricing_elements": '[class*="pricing"], [class*="price"]',
            "feature_elements": '[class*="feature"], [class*="category"]',
            "summary_section": '[aria-label="Comparison Summary"], .compare-container-v2_summary',
            "ai_summary_title": '.mb-1\\/4, [class*="mb-1/4"]',
            "summary_points": '.compare-container-v2_summary li, .comparison-container li'
        }
        
        # Known comparison sections from screenshots
        self.known_sections = [
            "At a Glance",
            "Pricing", 
            "Ratings",
            "Features",
            "Reviews",
            "Alternatives",
            "Discussions"
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
            "Data Visualization",
            "Ease of Setup",
            "AI Text Generation",
            "Data Governance",
            "Collaboration and Workflow",
            "Predictive Analytics"
        ]
        
        # AI summary patterns for extraction
        self.summary_patterns = {
            "score_comparison": r"scoring\s+(\d+\.?\d*)\s+compared\s+to\s+[^']*?(\d+\.?\d*)",
            "feature_mention": r"(?:excel|excels|superior|stronger|better|trails|behind)\s+(?:in|at)\s+([^,]+)",
            "sentiment_indicators": r"(?:excellent|fantastic|superior|better|trails|behind|lower|stronger|weaker)",
            "product_names": r"(?:Microsoft Power BI|Power BI|Domo|Tableau|Qlik|Snowflake|Databricks)"
        }
    
    async def parse_head_to_head_comparison(self, html: str, url: str) -> HeadToHeadComparisonData:
        """Parse a G2 head-to-head comparison page comprehensively."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract basic comparison info
            comparison_id = self._extract_comparison_id(url)
            
            # Extract products information
            products = await self._extract_products(soup)
            if len(products) != 2:
                raise ValueError(f"Expected 2 products, found {len(products)}")
            
            product_a, product_b = products[0], products[1]
            
            # Extract AI-generated summary (highest priority)
            ai_summary = await self._extract_ai_generated_summary(soup)
            
            # Extract comparison sections
            at_a_glance = await self._extract_at_a_glance(soup, products)
            pricing = await self._extract_pricing(soup, products)
            ratings = await self._extract_ratings(soup, products)
            features = await self._extract_features(soup, products)
            reviews = await self._extract_reviews(soup, products)
            alternatives = await self._extract_alternatives(soup, products)
            
            # Calculate data quality metrics
            data_quality_score = self._calculate_data_quality_score(
                products, at_a_glance, pricing, ratings, features, reviews, alternatives
            )
            
            # Calculate summary quality score
            summary_quality_score = self._calculate_summary_quality_score(ai_summary)
            
            # Create comparison data
            comparison_data = HeadToHeadComparisonData(
                comparison_id=comparison_id,
                extraction_date=datetime.now(),
                url=url,
                product_a=asdict(product_a),
                product_b=asdict(product_b),
                ai_generated_summary=asdict(ai_summary),
                at_a_glance=at_a_glance,
                pricing=pricing,
                ratings=ratings,
                features=features,
                reviews=reviews,
                alternatives=alternatives,
                data_quality_score=data_quality_score,
                extraction_confidence=self._calculate_extraction_confidence(soup),
                summary_quality_score=summary_quality_score
            )
            
            logger.info(f"Successfully parsed head-to-head comparison with AI summary quality: {summary_quality_score:.1f}")
            return comparison_data
            
        except Exception as e:
            logger.error(f"Failed to parse head-to-head comparison: {e}")
            raise
    
    def _extract_comparison_id(self, url: str) -> str:
        """Extract unique comparison ID from URL."""
        try:
            # Extract the comparison part from URL
            # Example: g2.com/compare/domo-vs-microsoft-microsoft-power-bi
            comparison_part = url.split('/compare/')[-1]
            # Clean and create ID
            comparison_id = comparison_part.replace('-', '_').replace('vs', 'vs')
            return f"head_to_head_{comparison_id}"
        except Exception as e:
            logger.warning(f"Failed to extract comparison ID: {e}")
            return f"head_to_head_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
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
            
            logger.info(f"Extracted {len(products)} products from head-to-head comparison")
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
    
    async def _extract_ai_generated_summary(self, soup: BeautifulSoup) -> AIGeneratedSummary:
        """Extract AI-generated summary - the most valuable data."""
        try:
            # Look for summary section
            summary_section = soup.find('div', attrs={'aria-label': 'Comparison Summary'})
            if not summary_section:
                summary_section = soup.find('div', class_='compare-container-v2_summary')
            
            if not summary_section:
                # Try alternative selectors
                summary_section = soup.find('div', class_=re.compile(r'summary'))
            
            if summary_section:
                # Extract summary title
                title_element = summary_section.find('div', class_=re.compile(r'mb-1/4'))
                if not title_element:
                    title_element = summary_section.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                
                title = title_element.get_text(strip=True) if title_element else "AI Generated Summary"
                
                # Extract subtitle
                subtitle_element = summary_section.find(string=re.compile(r'AI-generated\. Powered by real user reviews'))
                subtitle = subtitle_element.strip() if subtitle_element else ""
                
                # Extract summary points
                summary_points = await self._extract_summary_points(summary_section)
                
                # Generate structured insights
                structured_insights = self._analyze_summary_insights(summary_points)
                
                summary = AIGeneratedSummary(
                    summary_title=title,
                    summary_subtitle=subtitle,
                    summary_points=summary_points,
                    extraction_confidence=self._calculate_summary_extraction_confidence(summary_section),
                    structured_insights=structured_insights
                )
                
                logger.info(f"Successfully extracted AI-generated summary with {len(summary_points)} points")
                return summary
            
            # If no summary section found, create empty summary
            logger.warning("No AI-generated summary section found")
            return AIGeneratedSummary(
                summary_title="No Summary Found",
                summary_subtitle="",
                summary_points=[],
                extraction_confidence=0.0,
                structured_insights={}
            )
            
        except Exception as e:
            logger.error(f"Failed to extract AI-generated summary: {e}")
            return AIGeneratedSummary(
                summary_title="Extraction Failed",
                summary_subtitle="",
                summary_points=[],
                extraction_confidence=0.0,
                structured_insights={}
            )
    
    async def _extract_summary_points(self, summary_section) -> List[Dict[str, Any]]:
        """Extract individual summary points with structured data."""
        summary_points = []
        
        try:
            # Look for list items containing summary points
            list_items = summary_section.find_all('li')
            
            for item in list_items:
                try:
                    point_text = item.get_text(strip=True)
                    if point_text and len(point_text) > 50:  # Reasonable summary point length
                        
                        # Parse the summary point
                        summary_point = self._parse_summary_point(point_text)
                        summary_points.append(summary_point)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse summary point: {e}")
                    continue
            
            # If no list items found, try alternative extraction
            if not summary_points:
                summary_points = self._extract_summary_points_alternative(summary_section)
            
            return summary_points
            
        except Exception as e:
            logger.warning(f"Failed to extract summary points: {e}")
            return []
    
    def _parse_summary_point(self, point_text: str) -> Dict[str, Any]:
        """Parse individual summary point to extract structured data."""
        try:
            # Extract scores if present
            score_match = re.search(self.summary_patterns["score_comparison"], point_text)
            product_a_score = None
            product_b_score = None
            
            if score_match:
                product_a_score = float(score_match.group(1))
                product_b_score = float(score_match.group(2))
            
            # Extract feature category
            feature_category = self._extract_feature_category(point_text)
            
            # Determine insight type
            insight_type = self._determine_insight_type(point_text)
            
            # Determine sentiment
            sentiment = self._determine_sentiment(point_text)
            
            # Calculate confidence based on data extraction
            confidence = self._calculate_point_confidence(point_text, product_a_score, product_b_score)
            
            summary_point = SummaryPoint(
                text=point_text,
                product_a_score=product_a_score,
                product_b_score=product_b_score,
                feature_category=feature_category,
                insight_type=insight_type,
                sentiment=sentiment,
                confidence=confidence
            )
            
            return asdict(summary_point)
            
        except Exception as e:
            logger.warning(f"Failed to parse summary point: {e}")
            return {
                "text": point_text,
                "product_a_score": None,
                "product_b_score": None,
                "feature_category": "unknown",
                "insight_type": "unknown",
                "sentiment": "neutral",
                "confidence": 0.0
            }
    
    def _extract_feature_category(self, text: str) -> str:
        """Extract feature category from summary point text."""
        text_lower = text.lower()
        
        # Map text to feature categories
        category_mapping = {
            "data visualization": ["data visualization", "visualizations", "dashboards"],
            "ease of setup": ["ease of setup", "setup", "onboarding"],
            "ai text generation": ["ai text generation", "ai capabilities", "ai"],
            "data governance": ["data governance", "data access", "compliance"],
            "collaboration and workflow": ["collaboration", "workflow", "teamwork", "sharing"],
            "predictive analytics": ["predictive analytics", "forecasting", "trend analysis"]
        }
        
        for category, keywords in category_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return "other"
    
    def _determine_insight_type(self, text: str) -> str:
        """Determine the type of insight from summary point."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["excel", "excels", "superior", "better"]):
            return "competitive_advantage"
        elif any(word in text_lower for word in ["trails", "behind", "lower", "weaker"]):
            return "competitive_disadvantage"
        elif any(word in text_lower for word in ["compared", "versus", "vs"]):
            return "comparative_analysis"
        else:
            return "general_insight"
    
    def _determine_sentiment(self, text: str) -> str:
        """Determine sentiment from summary point."""
        text_lower = text.lower()
        
        positive_words = ["excellent", "fantastic", "superior", "better", "stronger", "excels"]
        negative_words = ["trails", "behind", "lower", "weaker", "needs development"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _calculate_point_confidence(self, text: str, score_a: Optional[float], score_b: Optional[float]) -> float:
        """Calculate confidence in the extracted summary point data."""
        confidence = 0.0
        
        # Base confidence from text quality
        if len(text) > 100:
            confidence += 30
        elif len(text) > 50:
            confidence += 20
        
        # Confidence from score extraction
        if score_a is not None and score_b is not None:
            confidence += 40
        
        # Confidence from structured data
        if any(word in text.lower() for word in ["scoring", "compared", "versus"]):
            confidence += 20
        
        # Confidence from feature identification
        if self._extract_feature_category(text) != "other":
            confidence += 10
        
        return min(confidence, 100.0)
    
    def _extract_summary_points_alternative(self, summary_section) -> List[Dict[str, Any]]:
        """Alternative method to extract summary points if primary method fails."""
        summary_points = []
        
        try:
            # Look for paragraphs or divs that might contain summary content
            text_elements = summary_section.find_all(['p', 'div'], string=re.compile(r'.{50,}'))
            
            for element in text_elements:
                text = element.get_text(strip=True)
                if text and len(text) > 50:
                    summary_point = self._parse_summary_point(text)
                    summary_points.append(summary_point)
            
            return summary_points
            
        except Exception as e:
            logger.warning(f"Alternative summary point extraction failed: {e}")
            return []
    
    def _analyze_summary_insights(self, summary_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze summary points to generate structured insights."""
        try:
            insights = {
                "competitive_advantages": [],
                "competitive_disadvantages": [],
                "feature_comparisons": {},
                "sentiment_analysis": {"positive": 0, "negative": 0, "neutral": 0},
                "score_insights": [],
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            for point in summary_points:
                # Categorize by insight type
                if point.get("insight_type") == "competitive_advantage":
                    insights["competitive_advantages"].append(point)
                elif point.get("insight_type") == "competitive_disadvantage":
                    insights["competitive_disadvantages"].append(point)
                
                # Categorize by feature
                feature_category = point.get("feature_category", "other")
                if feature_category not in insights["feature_comparisons"]:
                    insights["feature_comparisons"][feature_category] = []
                insights["feature_comparisons"][feature_category].append(point)
                
                # Sentiment analysis
                sentiment = point.get("sentiment", "neutral")
                insights["sentiment_analysis"][sentiment] += 1
                
                # Score insights
                if point.get("product_a_score") and point.get("product_b_score"):
                    insights["score_insights"].append({
                        "feature": feature_category,
                        "product_a_score": point["product_a_score"],
                        "product_b_score": point["product_b_score"],
                        "difference": abs(point["product_a_score"] - point["product_b_score"])
                    })
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to analyze summary insights: {e}")
            return {}
    
    def _calculate_summary_extraction_confidence(self, summary_section) -> float:
        """Calculate confidence in summary extraction."""
        try:
            confidence = 0.0
            
            # Check for key structural elements
            if summary_section.find('div', attrs={'aria-label': 'Comparison Summary'}):
                confidence += 40
            if summary_section.find('div', class_=re.compile(r'summary')):
                confidence += 30
            if summary_section.find('li'):
                confidence += 20
            if summary_section.find(string=re.compile(r'AI-generated')):
                confidence += 10
            
            return min(confidence, 100.0)
            
        except Exception as e:
            logger.warning(f"Failed to calculate summary extraction confidence: {e}")
            return 0.0
    
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
        """Extract comprehensive ratings by criteria."""
        try:
            ratings_data = {
                "criteria_ratings": {},
                "rating_breakdowns": {},
                "rating_insights": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for ratings section
            ratings_section = soup.find('div', attrs={'aria-label': re.compile(r'Ratings', re.I)})
            if not ratings_section:
                ratings_section = soup.find('div', string=re.compile(r'Ratings', re.I))
            
            if ratings_section:
                # Extract ratings for each criterion
                for criterion_key, criterion_names in self.rating_criteria.items():
                    try:
                        criterion_data = await self._extract_criterion_ratings(
                            ratings_section, criterion_names, products
                        )
                        
                        if criterion_data:
                            ratings_data["criteria_ratings"][criterion_key] = criterion_data
                            
                    except Exception as e:
                        logger.warning(f"Failed to extract {criterion_key} ratings: {e}")
                        continue
            
            # Extract rating breakdowns from visual elements
            rating_breakdowns = await self._extract_rating_breakdowns(soup, products)
            ratings_data["rating_breakdowns"] = rating_breakdowns
            
            # Extract rating insights from AI summary
            rating_insights = await self._extract_rating_insights_from_ai_summary(soup, products)
            ratings_data["rating_insights"] = rating_insights
            
            return ratings_data
            
        except Exception as e:
            logger.warning(f"Failed to extract ratings data: {e}")
            return {}
    
    async def _extract_criterion_ratings(self, ratings_section, criterion_names: List[str], products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract ratings for a specific criterion."""
        try:
            criterion_data = {
                "criterion_name": criterion_names[0],
                "product_ratings": {},
                "extraction_confidence": 0.0
            }
            
            # Look for rating elements with aria-label containing the criterion
            for criterion_name in criterion_names:
                rating_elements = ratings_section.find_all(
                    'div', 
                    attrs={'aria-label': re.compile(f'.*{re.escape(criterion_name)}.*', re.I)}
                )
                
                if rating_elements:
                    for element in rating_elements:
                        aria_label = element.get('aria-label', '')
                        
                        # Extract rating from aria-label
                        rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+10', aria_label)
                        if rating_match:
                            rating = float(rating_match.group(1))
                            
                            # Determine which product this rating belongs to
                            for product in products:
                                if product.name.lower() in aria_label.lower():
                                    criterion_data["product_ratings"][product.name] = {
                                        "rating": rating,
                                        "aria_label": aria_label,
                                        "extraction_confidence": 90.0
                                    }
                                    break
                    
                    # If we found ratings for this criterion, break
                    if criterion_data["product_ratings"]:
                        break
            
            # Calculate extraction confidence
            if criterion_data["product_ratings"]:
                criterion_data["extraction_confidence"] = min(
                    90.0, 
                    len(criterion_data["product_ratings"]) * 30.0
                )
            
            return criterion_data
            
        except Exception as e:
            logger.warning(f"Failed to extract criterion ratings: {e}")
            return {}
    
    async def _extract_rating_breakdowns(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract rating breakdowns from visual elements."""
        try:
            rating_breakdowns = {
                "star_ratings": {},
                "rating_distributions": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Extract star ratings for each product
            for product in products:
                product_name = product.name
                
                # Look for star rating elements
                star_rating_elements = soup.find_all(
                    'div', 
                    attrs={'aria-label': re.compile(f'{re.escape(product_name)}.*star rating', re.I)}
                )
                
                for element in star_rating_elements:
                    aria_label = element.get('aria-label', '')
                    rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', aria_label)
                    
                    if rating_match:
                        rating = float(rating_match.group(1))
                        rating_breakdowns["star_ratings"][product_name] = {
                            "rating": rating,
                            "aria_label": aria_label,
                            "extraction_confidence": 95.0
                        }
                        break
            
            return rating_breakdowns
            
        except Exception as e:
            logger.warning(f"Failed to extract rating breakdowns: {e}")
            return {}
    
    async def _extract_rating_insights_from_ai_summary(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract rating insights from AI-generated summary."""
        try:
            rating_insights = {
                "rating_comparisons": {},
                "rating_advantages": {},
                "extraction_confidence": 0.0
            }
            
            # Look for AI summary section
            summary_section = soup.find('div', attrs={'aria-label': 'Comparison Summary'})
            if not summary_section:
                summary_section = soup.find('div', class_='compare-container-v2_summary')
            
            if summary_section:
                # Extract rating-related insights from summary points
                summary_points = summary_section.find_all('li')
                
                for point in summary_points:
                    try:
                        point_text = point.get_text(strip=True)
                        
                        # Check if this point mentions ratings or scoring
                        if any(word in point_text.lower() for word in ["scoring", "score", "rating", "out of"]):
                            # Extract rating comparison
                            rating_match = re.search(r'scoring\s+(\d+\.?\d*)\s+compared\s+to\s+[^']*?(\d+\.?\d*)', point_text)
                            
                            if rating_match:
                                score_a = float(rating_match.group(1))
                                score_b = float(rating_match.group(2))
                                
                                # Determine which product has the advantage
                                if score_a > score_b:
                                    advantage_product = "Product A"
                                    advantage_score = score_a
                                else:
                                    advantage_product = "Product B"
                                    advantage_score = score_b
                                
                                rating_insights["rating_comparisons"][len(rating_insights["rating_comparisons"])] = {
                                    "text": point_text,
                                    "score_a": score_a,
                                    "score_b": score_b,
                                    "advantage_product": advantage_product,
                                    "advantage_score": advantage_score,
                                    "extraction_confidence": 90.0
                                }
                                
                                # Track rating advantages
                                if advantage_product not in rating_insights["rating_advantages"]:
                                    rating_insights["rating_advantages"][advantage_product] = []
                                rating_insights["rating_advantages"][advantage_product].append({
                                    "insight": point_text,
                                    "score": advantage_score
                                })
                                
                    except Exception as e:
                        logger.warning(f"Failed to extract rating insight from summary point: {e}")
                        continue
                
                # Calculate extraction confidence
                if rating_insights["rating_comparisons"]:
                    total_insights = len(rating_insights["rating_comparisons"])
                    rating_insights["extraction_confidence"] = min(90.0, total_insights * 20.0)
            
            return rating_insights
            
        except Exception as e:
            logger.warning(f"Failed to extract rating insights from AI summary: {e}")
            return {}
    
    async def _extract_features(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract comprehensive feature comparison data."""
        try:
            features_data = {
                "feature_categories": {},
                "feature_ratings": {},
                "feature_comparisons": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for features section
            features_section = soup.find('div', attrs={'aria-label': re.compile(r'Features', re.I)})
            if not features_section:
                features_section = soup.find('div', string=re.compile(r'Features', re.I))
            
            if features_section:
                # Extract feature categories and ratings
                for feature_category in self.feature_categories:
                    try:
                        category_data = await self._extract_feature_category_data(
                            features_section, feature_category, products
                        )
                        
                        if category_data:
                            features_data["feature_categories"][feature_category] = category_data
                            
                    except Exception as e:
                        logger.warning(f"Failed to extract {feature_category} data: {e}")
                        continue
            
            # Extract feature comparisons from AI summary if available
            if soup.find(string=re.compile(r'AI Generated Summary', re.I)):
                ai_summary_features = await self._extract_features_from_ai_summary(soup, products)
                features_data["ai_summary_features"] = ai_summary_features
            
            return features_data
            
        except Exception as e:
            logger.warning(f"Failed to extract features data: {e}")
            return {}
    
    async def _extract_feature_category_data(self, features_section, feature_category: str, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract data for a specific feature category."""
        try:
            category_data = {
                "category_name": feature_category,
                "product_ratings": {},
                "extraction_confidence": 0.0
            }
            
            # Look for elements with aria-label containing the feature category
            category_elements = features_section.find_all(
                'div', 
                attrs={'aria-label': re.compile(f'.*{re.escape(feature_category)}.*', re.I)}
            )
            
            if category_elements:
                for element in category_elements:
                    aria_label = element.get('aria-label', '')
                    
                    # Extract rating from aria-label
                    rating_match = re.search(r'(\d+\.?\d*)', aria_label)
                    if rating_match:
                        rating = float(rating_match.group(1))
                        
                        # Determine which product this rating belongs to
                        for product in products:
                            if product.name.lower() in aria_label.lower():
                                category_data["product_ratings"][product.name] = {
                                    "rating": rating,
                                    "aria_label": aria_label,
                                    "extraction_confidence": 90.0
                                }
                                break
                
                # Calculate extraction confidence based on data completeness
                if category_data["product_ratings"]:
                    category_data["extraction_confidence"] = min(
                        90.0, 
                        len(category_data["product_ratings"]) * 30.0
                    )
            
            return category_data
            
        except Exception as e:
            logger.warning(f"Failed to extract {feature_category} category data: {e}")
            return {}
    
    async def _extract_features_from_ai_summary(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract feature insights from AI-generated summary."""
        try:
            ai_summary_features = {
                "feature_insights": {},
                "competitive_advantages": {},
                "extraction_confidence": 0.0
            }
            
            # Look for AI summary section
            summary_section = soup.find('div', attrs={'aria-label': 'Comparison Summary'})
            if not summary_section:
                summary_section = soup.find('div', class_='compare-container-v2_summary')
            
            if summary_section:
                # Extract feature-related insights from summary points
                summary_points = summary_section.find_all('li')
                
                for point in summary_points:
                    try:
                        point_text = point.get_text(strip=True)
                        
                        # Check if this point mentions any of our feature categories
                        for feature_category in self.feature_categories:
                            if feature_category.lower() in point_text.lower():
                                if feature_category not in ai_summary_features["feature_insights"]:
                                    ai_summary_features["feature_insights"][feature_category] = []
                                
                                # Extract competitive advantage/disadvantage
                                insight_type = "neutral"
                                if any(word in point_text.lower() for word in ["excel", "excels", "superior", "better"]):
                                    insight_type = "competitive_advantage"
                                elif any(word in point_text.lower() for word in ["trails", "behind", "lower", "weaker"]):
                                    insight_type = "competitive_disadvantage"
                                
                                feature_insight = {
                                    "text": point_text,
                                    "insight_type": insight_type,
                                    "extraction_confidence": 85.0
                                }
                                
                                ai_summary_features["feature_insights"][feature_category].append(feature_insight)
                                
                                # Track competitive advantages
                                if insight_type == "competitive_advantage":
                                    if feature_category not in ai_summary_features["competitive_advantages"]:
                                        ai_summary_features["competitive_advantages"][feature_category] = []
                                    ai_summary_features["competitive_advantages"][feature_category].append(point_text)
                                
                                break
                                
                    except Exception as e:
                        logger.warning(f"Failed to extract feature insight from summary point: {e}")
                        continue
                
                # Calculate extraction confidence
                if ai_summary_features["feature_insights"]:
                    total_insights = sum(len(insights) for insights in ai_summary_features["feature_insights"].values())
                    ai_summary_features["extraction_confidence"] = min(90.0, total_insights * 15.0)
            
            return ai_summary_features
            
        except Exception as e:
            logger.warning(f"Failed to extract features from AI summary: {e}")
            return {}
    
    async def _extract_reviews(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract comprehensive review data and insights."""
        try:
            reviews_data = {
                "reviewers_company_size": {},
                "reviewers_industry": {},
                "most_helpful_reviews": {},
                "review_statistics": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Extract reviewers company size data
            company_size_data = await self._extract_reviewers_company_size(soup, products)
            reviews_data["reviewers_company_size"] = company_size_data
            
            # Extract reviewers industry data
            industry_data = await self._extract_reviewers_industry(soup, products)
            reviews_data["reviewers_industry"] = industry_data
            
            # Extract most helpful reviews
            helpful_reviews = await self._extract_most_helpful_reviews(soup, products)
            reviews_data["most_helpful_reviews"] = helpful_reviews
            
            # Extract review statistics
            review_stats = await self._extract_review_statistics(soup, products)
            reviews_data["review_statistics"] = review_stats
            
            return reviews_data
            
        except Exception as e:
            logger.warning(f"Failed to extract reviews data: {e}")
            return {}
    
    async def _extract_reviewers_company_size(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract reviewers company size breakdown."""
        try:
            company_size_data = {
                "small_business": {},
                "mid_market": {},
                "enterprise": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for company size section
            company_size_section = soup.find('div', attrs={'aria-label': re.compile(r'Reviewers Company Size', re.I)})
            if not company_size_section:
                company_size_section = soup.find('div', string=re.compile(r'Reviewers.*Company Size', re.I))
            
            if company_size_section:
                # Extract data for each company size category
                categories = ["small_business", "mid_market", "enterprise"]
                category_labels = ["Small-Business (50 or fewer emp.)", "Mid-Market (51-1000 emp.)", "Enterprise (> 1000 emp.)"]
                
                for i, (category, label) in enumerate(zip(categories, category_labels)):
                    try:
                        # Look for elements with aria-label containing the category
                        category_elements = company_size_section.find_all(
                            'div', 
                            attrs={'aria-label': re.compile(f'.*{label}.*', re.I)}
                        )
                        
                        for element in category_elements:
                            # Extract percentage from aria-label
                            aria_label = element.get('aria-label', '')
                            percentage_match = re.search(r'(\d+(?:\.\d+)?)%', aria_label)
                            
                            if percentage_match:
                                percentage = float(percentage_match.group(1))
                                
                                # Determine which product this percentage belongs to
                                for product in products:
                                    if product.name.lower() in aria_label.lower():
                                        company_size_data[category][product.name] = {
                                            "percentage": percentage,
                                            "aria_label": aria_label,
                                            "extraction_confidence": 90.0
                                        }
                                        break
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract {category} data: {e}")
                        continue
            
            return company_size_data
            
        except Exception as e:
            logger.warning(f"Failed to extract reviewers company size: {e}")
            return {}
    
    async def _extract_reviewers_industry(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract reviewers industry breakdown."""
        try:
            industry_data = {
                "industries": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for industry section
            industry_section = soup.find('div', attrs={'aria-label': re.compile(r'Reviewers.*Industry', re.I)})
            if not industry_section:
                industry_section = soup.find('div', string=re.compile(r'Reviewers.*Industry', re.I))
            
            if industry_section:
                # Common industries from screenshots
                common_industries = [
                    "Computer Software", "Marketing and Advertising", "Information Technology and Services",
                    "Hospital & Health Care", "Financial Services", "Other"
                ]
                
                for industry in common_industries:
                    try:
                        # Look for elements with aria-label containing the industry
                        industry_elements = industry_section.find_all(
                            'div', 
                            attrs={'aria-label': re.compile(f'.*{re.escape(industry)}.*', re.I)}
                        )
                        
                        for element in industry_elements:
                            aria_label = element.get('aria-label', '')
                            percentage_match = re.search(r'(\d+(?:\.\d+)?)%', aria_label)
                            
                            if percentage_match:
                                percentage = float(percentage_match.group(1))
                                
                                # Determine which product this percentage belongs to
                                for product in products:
                                    if product.name.lower() in aria_label.lower():
                                        if industry not in industry_data["industries"]:
                                            industry_data["industries"][industry] = {}
                                        
                                        industry_data["industries"][industry][product.name] = {
                                            "percentage": percentage,
                                            "aria_label": aria_label,
                                            "extraction_confidence": 90.0
                                        }
                                        break
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract {industry} data: {e}")
                        continue
            
            return industry_data
            
        except Exception as e:
            logger.warning(f"Failed to extract reviewers industry: {e}")
            return {}
    
    async def _extract_most_helpful_reviews(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract most helpful reviews for each product."""
        try:
            helpful_reviews_data = {
                "reviews": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for most helpful reviews section
            reviews_section = soup.find('div', attrs={'aria-label': re.compile(r'Most Helpful Reviews', re.I)})
            if not reviews_section:
                reviews_section = soup.find('div', string=re.compile(r'Most Helpful Reviews', re.I))
            
            if reviews_section:
                # Extract reviews for each product
                for product in products:
                    product_name = product.name
                    helpful_reviews_data["reviews"][product_name] = []
                    
                    try:
                        # Look for review elements
                        review_elements = reviews_section.find_all(['p', 'div'], class_=re.compile(r'review|comment'))
                        
                        for review_element in review_elements:
                            try:
                                review_text = review_element.get_text(strip=True)
                                
                                # Check if this review belongs to the current product
                                if len(review_text) > 50 and any(word in review_text.lower() for word in product_name.lower().split()):
                                    # Extract reviewer information if available
                                    reviewer_info = self._extract_reviewer_info(review_element)
                                    
                                    review_data = {
                                        "text": review_text,
                                        "reviewer_info": reviewer_info,
                                        "extraction_confidence": 85.0,
                                        "review_length": len(review_text)
                                    }
                                    
                                    helpful_reviews_data["reviews"][product_name].append(review_data)
                                    
                                    # Limit to 3 most helpful reviews per product
                                    if len(helpful_reviews_data["reviews"][product_name]) >= 3:
                                        break
                                        
                            except Exception as e:
                                logger.warning(f"Failed to extract individual review: {e}")
                                continue
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract reviews for {product_name}: {e}")
                        continue
            
            return helpful_reviews_data
            
        except Exception as e:
            logger.warning(f"Failed to extract most helpful reviews: {e}")
            return {}
    
    def _extract_reviewer_info(self, review_element) -> Dict[str, Any]:
        """Extract reviewer information from review element."""
        try:
            reviewer_info = {
                "name": "Unknown",
                "verification_status": "Unknown",
                "industry": "Unknown",
                "company_size": "Unknown"
            }
            
            # Look for reviewer name
            name_element = review_element.find_previous(['span', 'div'], class_=re.compile(r'name|user'))
            if name_element:
                reviewer_info["name"] = name_element.get_text(strip=True)
            
            # Look for verification status
            verification_element = review_element.find_previous(['span', 'div'], string=re.compile(r'Verified User', re.I))
            if verification_element:
                reviewer_info["verification_status"] = "Verified"
            
            # Look for industry information
            industry_element = review_element.find_previous(['span', 'div'], string=re.compile(r'in .*', re.I))
            if industry_element:
                industry_text = industry_element.get_text(strip=True)
                if 'in ' in industry_text:
                    reviewer_info["industry"] = industry_text.split('in ')[-1]
            
            return reviewer_info
            
        except Exception as e:
            logger.warning(f"Failed to extract reviewer info: {e}")
            return {"name": "Unknown", "verification_status": "Unknown", "industry": "Unknown", "company_size": "Unknown"}
    
    async def _extract_review_statistics(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract review statistics and metrics."""
        try:
            review_stats = {
                "total_reviews": {},
                "average_ratings": {},
                "review_distribution": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Extract total reviews for each product
            for product in products:
                product_name = product.name
                
                # Look for review count elements
                review_count_elements = soup.find_all(
                    'a', 
                    attrs={'aria-label': re.compile(f'{re.escape(product_name)}.*reviews?', re.I)}
                )
                
                for element in review_count_elements:
                    aria_label = element.get('aria-label', '')
                    review_count_match = re.search(r'(\d+(?:,\d+)*)', aria_label)
                    
                    if review_count_match:
                        review_count = int(review_count_match.group(1).replace(',', ''))
                        review_stats["total_reviews"][product_name] = {
                            "count": review_count,
                            "aria_label": aria_label,
                            "extraction_confidence": 95.0
                        }
                        break
                
                # Extract average rating if available
                rating_elements = soup.find_all(
                    'div', 
                    attrs={'aria-label': re.compile(f'{re.escape(product_name)}.*star rating', re.I)}
                )
                
                for element in rating_elements:
                    aria_label = element.get('aria-label', '')
                    rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', aria_label)
                    
                    if rating_match:
                        rating = float(rating_match.group(1))
                        review_stats["average_ratings"][product_name] = {
                            "rating": rating,
                            "aria_label": aria_label,
                            "extraction_confidence": 95.0
                        }
                        break
            
            return review_stats
            
        except Exception as e:
            logger.warning(f"Failed to extract review statistics: {e}")
            return {}
    
    async def _extract_alternatives(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict[str, Any]:
        """Extract comprehensive alternatives data."""
        try:
            alternatives_data = {
                "alternative_products": {},
                "competitor_mentions": {},
                "market_positioning": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Look for alternatives section
            alternatives_section = soup.find('div', attrs={'aria-label': re.compile(r'Alternatives', re.I)})
            if not alternatives_section:
                alternatives_section = soup.find('div', string=re.compile(r'Alternatives', re.I))
            
            if alternatives_section:
                # Extract alternative products for each main product
                for product in products:
                    product_name = product.name
                    alternatives_data["alternative_products"][product_name] = []
                    
                    try:
                        # Look for alternative product links
                        alternative_links = alternatives_section.find_all('a', href=re.compile(r'/products/'))
                        
                        for link in alternative_links:
                            try:
                                href = link.get('href', '')
                                if '/products/' in href:
                                    # Extract product name from link text or href
                                    alt_product_name = link.get_text(strip=True)
                                    if not alt_product_name:
                                        alt_product_name = href.split('/products/')[-1].replace('-', ' ').title()
                                    
                                    # Skip if it's the same as the main product
                                    if alt_product_name.lower() != product_name.lower():
                                        alternative_data = {
                                            "name": alt_product_name,
                                            "url": href,
                                            "extraction_confidence": 85.0
                                        }
                                        alternatives_data["alternative_products"][product_name].append(alternative_data)
                                        
                                        # Limit to 10 alternatives per product
                                        if len(alternatives_data["alternative_products"][product_name]) >= 10:
                                            break
                                            
                            except Exception as e:
                                logger.warning(f"Failed to extract individual alternative: {e}")
                                continue
                        
                    except Exception as e:
                        logger.warning(f"Failed to extract alternatives for {product_name}: {e}")
                        continue
            
            # Extract competitor mentions from AI summary and other content
            for product in products:
                product_name = product.name
                alternatives_data["competitor_mentions"][product_name] = []
                
                # Look for competitor mentions in the page content
                page_text = soup.get_text()
                competitor_products = [
                    "Tableau", "Qlik", "Snowflake", "Databricks", "Amazon Redshift", 
                    "Google BigQuery", "Looker", "Sisense", "ThoughtSpot", "Power BI"
                ]
                
                for competitor in competitor_products:
                    if competitor.lower() in page_text.lower() and competitor.lower() != product_name.lower():
                        alternatives_data["competitor_mentions"][product_name].append({
                            "competitor": competitor,
                            "mention_context": "page_content",
                            "extraction_confidence": 80.0
                        })
            
            return alternatives_data
            
        except Exception as e:
            logger.warning(f"Failed to extract alternatives data: {e}")
            return {}
    
    def _calculate_data_quality_score(self, products: List[ProductComparison], 
                                    at_a_glance: Dict[str, Any], 
                                    pricing: Dict[str, Any], 
                                    ratings: Dict[str, Any], 
                                    features: Dict[str, Any],
                                    reviews: Dict[str, Any],
                                    alternatives: Dict[str, Any]) -> float:
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
                
                score += (product_score / len(products)) * 0.3  # 30% weight
            
            # Section data completeness
            section_score = 0.0
            if at_a_glance: section_score += 20
            if pricing: section_score += 20
            if ratings: section_score += 20
            if features: section_score += 20
            if reviews: section_score += 20
            
            score += section_score * 0.7  # 70% weight
            
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
    
    def _calculate_summary_quality_score(self, ai_summary: AIGeneratedSummary) -> float:
        """Calculate quality score for AI-generated summary."""
        try:
            score = 0.0
            max_score = 100.0
            
            # Title and subtitle presence
            if ai_summary.summary_title and ai_summary.summary_title != "No Summary Found":
                score += 20
            if ai_summary.summary_subtitle:
                score += 10
            
            # Summary points quality
            if ai_summary.summary_points:
                points_score = 0.0
                for point in ai_summary.summary_points:
                    point_quality = 0.0
                    if point.get("text"): point_quality += 20
                    if point.get("product_a_score"): point_quality += 20
                    if point.get("product_b_score"): point_quality += 20
                    if point.get("feature_category") != "other": point_quality += 20
                    if point.get("insight_type") != "unknown": point_quality += 20
                    points_score += point_quality
                
                score += (points_score / len(ai_summary.summary_points)) * 0.5  # 50% weight
            
            # Structured insights
            if ai_summary.structured_insights:
                insights_score = 0.0
                if ai_summary.structured_insights.get("competitive_advantages"): insights_score += 25
                if ai_summary.structured_insights.get("competitive_disadvantages"): insights_score += 25
                if ai_summary.structured_insights.get("feature_comparisons"): insights_score += 25
                if ai_summary.structured_insights.get("sentiment_analysis"): insights_score += 25
                score += insights_score * 0.2  # 20% weight
            
            return min(score, max_score)
            
        except Exception as e:
            logger.warning(f"Failed to calculate summary quality score: {e}")
            return 0.0
    
    def get_extraction_statistics(self) -> Dict[str, Any]:
        """Get statistics about the extraction process."""
        return {
            "parser_type": "G2 Head-to-Head Comparison Parser",
            "supported_sections": self.known_sections,
            "rating_criteria": list(self.rating_criteria.keys()),
            "feature_categories": self.feature_categories,
            "summary_patterns": list(self.summary_patterns.keys()),
            "extraction_methods": [
                "aria-label parsing",
                "structured HTML parsing", 
                "AI summary extraction",
                "fallback text extraction"
            ]
        }
