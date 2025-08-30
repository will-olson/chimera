#!/usr/bin/env python3
"""Python 3.8 compatible head-to-head comparison parser."""

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
    product_a: Dict
    product_b: Dict
    
    # AI-generated summary (most valuable data)
    ai_generated_summary: Dict
    
    # Comparison sections
    at_a_glance: Dict
    pricing: Dict
    ratings: Dict
    features: Dict
    reviews: Dict
    alternatives: Dict
    
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
    market_segments: Dict
    entry_level_pricing: str
    pricing_details: Dict
    ratings_by_criteria: Dict
    feature_scores: Dict


@dataclass
class AIGeneratedSummary:
    """AI-generated summary data with structured insights."""
    summary_title: str
    summary_subtitle: str
    summary_points: List[Dict]
    extraction_confidence: float
    structured_insights: Dict


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
    """Python 3.8 compatible parser for G2 head-to-head comparison pages."""
    
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
        
        # Known comparison sections
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
        
        # Feature categories
        self.feature_categories = [
            "Data Visualization",
            "Ease of Setup",
            "AI Text Generation",
            "Data Governance",
            "Collaboration and Workflow",
            "Predictive Analytics"
        ]
        
        # AI summary patterns
        self.summary_patterns = {
            "score_comparison": r"scoring\s+(\d+\.?\d*)\s+compared\s+to\s+[^\']*?(\d+\.?\d*)",
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
            comparison_part = url.split('/compare/')[-1]
            comparison_id = comparison_part.replace('-', '_').replace('vs', 'vs')
            return f"head_to_head_{comparison_id}"
        except Exception as e:
            logger.warning(f"Failed to extract comparison ID: {e}")
            return f"head_to_head_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def _extract_products(self, soup: BeautifulSoup) -> List[ProductComparison]:
        """Extract product information from comparison headers."""
        products = []
        
        try:
            # Find product headers
            product_headers = soup.select(self.comparison_selectors["product_headers"])
            
            if not product_headers:
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
            if text_content and len(text_content) < 100:
                return text_content
            
            # Strategy 2: Look for specific product name elements
            name_element = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div'], 
                                      class_=re.compile(r'product.*name|name.*product', re.I))
            if name_element:
                return name_element.get_text(strip=True)
            
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
                rating_match = re.search(r'(\d+\.?\d*)\s+out\s+of\s+5', aria_label)
                if rating_match:
                    star_rating = float(rating_match.group(1))
                    
                    # Extract review count
                    review_match = re.search(r'(\d+(?:,\d+)*)\s*reviews?', aria_label)
                    if review_match:
                        review_count = int(review_match.group(1).replace(',', ''))
                        return star_rating, review_count
            
            return 0.0, 0
            
        except Exception as e:
            logger.warning(f"Failed to extract rating info: {e}")
            return 0.0, 0
    
    def _extract_market_segments(self, element) -> Dict:
        """Extract market segment information."""
        try:
            market_segments = {}
            
            # Look for market segment information in aria-label
            aria_label = element.get('aria-label', '')
            if 'market segment' in aria_label.lower():
                percentage_match = re.search(r'(\d+(?:\.\d+)?)%', aria_label)
                if percentage_match:
                    percentage = float(percentage_match.group(1))
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
    
    async def _extract_summary_points(self, summary_section) -> List[Dict]:
        """Extract individual summary points with structured data."""
        summary_points = []
        
        try:
            # Look for list items containing summary points
            list_items = summary_section.find_all('li')
            
            for item in list_items:
                try:
                    point_text = item.get_text(strip=True)
                    if point_text and len(point_text) > 50:
                        
                        # Parse the summary point
                        summary_point = self._parse_summary_point(point_text)
                        summary_points.append(summary_point)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse summary point: {e}")
                    continue
            
            return summary_points
            
        except Exception as e:
            logger.warning(f"Failed to extract summary points: {e}")
            return []
    
    def _parse_summary_point(self, point_text: str) -> Dict:
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
    
    def _analyze_summary_insights(self, summary_points: List[Dict]) -> Dict:
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
    
    # Placeholder methods for additional data extraction
    async def _extract_at_a_glance(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract 'At a Glance' section data."""
        return {}
    
    async def _extract_pricing(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract comprehensive pricing information."""
        return {}
    
    async def _extract_ratings(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract comprehensive ratings by criteria."""
        return {}
    
    async def _extract_features(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract comprehensive feature comparison data."""
        return {}
    
    async def _extract_reviews(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract comprehensive review data and insights."""
        return {}
    
    async def _extract_alternatives(self, soup: BeautifulSoup, products: List[ProductComparison]) -> Dict:
        """Extract comprehensive alternatives data."""
        return {}
    
    def _calculate_data_quality_score(self, products: List[ProductComparison], 
                                    at_a_glance: Dict, 
                                    pricing: Dict, 
                                    ratings: Dict, 
                                    features: Dict,
                                    reviews: Dict,
                                    alternatives: Dict) -> float:
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
    
    def get_extraction_statistics(self) -> Dict:
        """Get statistics about the extraction process."""
        return {
            "parser_type": "G2 Head-to-Head Comparison Parser (Python 3.8 Compatible)",
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
