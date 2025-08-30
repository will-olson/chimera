from bs4 import BeautifulSoup
from typing import List, Any, Optional
import re
from datetime import datetime
import time
from loguru import logger
import asyncio

from chimera.models.review import Review, EnhancedReview
from .base import BaseParser


class G2Parser(BaseParser):
    """Enhanced G2 parser with benchmark-level capabilities and advanced anti-detection."""
    
    def __init__(self):
        super().__init__()
        self.known_competitors = [
            "tableau", "power bi", "qlik sense", "looker", "snowflake", 
            "databricks", "thoughtspot", "sigma", "hex", "omni", "domo",
            "sisense", "microstrategy", "oracle", "sap", "ibm cognos"
        ]
        self.last_extraction_time = datetime.now()
    
    async def extract_reviews(self, html: str, source_url: str) -> List[EnhancedReview]:
        """Extract reviews with enhanced features matching benchmark capabilities."""
        start_time = time.time()
        reviews = []
        
        try:
            # Extract using multiple selector strategies
            review_elements = await self._extract_review_elements(html)
            
            for element in review_elements:
                review = await self._parse_single_review_enhanced(element, source_url)
                if review:
                    reviews.append(review)
                    
                    # Update extraction stats
                    extraction_time = time.time() - start_time
                    self.update_extraction_stats("g2_review_selector", True, extraction_time)
            
            # Validate and enhance reviews
            validated_reviews = self.validate_extraction(reviews)
            
            # Enhance with competitive intelligence
            enhanced_reviews = await self._enhance_reviews_with_intelligence(validated_reviews)
            
            self.last_extraction_time = datetime.now()
            return enhanced_reviews
            
        except Exception as e:
            logger.error(f"Error in enhanced G2 review extraction: {e}")
            return []
    
    async def _extract_review_elements(self, html: str) -> List[Any]:
        """Extract review elements using multiple strategies."""
        soup = BeautifulSoup(html, 'lxml')
        
        # Primary selectors from benchmark
        primary_selectors = [
            'div[itemprop="reviewBody"]',
            'div[itemprop="review"]',
            '.review',
            '.review-item'
        ]
        
        # Fallback selectors from benchmark
        fallback_selectors = [
            '.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base',
            'p.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base'
        ]
        
        # Try primary selectors first
        for selector in primary_selectors:
            elements = soup.select(selector)
            if elements:
                self.cache_selectors({"g2_review_selector": selector})
                logger.info(f"Found {len(elements)} review elements with primary selector: {selector}")
                return elements
        
        # Try fallback selectors
        for selector in fallback_selectors:
            elements = soup.select(selector)
            if elements:
                self.cache_selectors({"g2_review_selector": selector})
                logger.info(f"Found {len(elements)} review elements with fallback selector: {selector}")
                return elements
        
        # Pattern matching fallback (from benchmark)
        return self._extract_by_pattern_matching(soup)
    
    def _extract_by_pattern_matching(self, soup: BeautifulSoup) -> List[Any]:
        """Extract reviews using pattern matching from benchmark."""
        potential_reviews = []
        
        # Look for review-like patterns
        all_elements = soup.find_all(['div', 'p', 'span'])
        
        for element in all_elements:
            text = element.get_text().strip()
            if text and len(text) > 30:
                if any(phrase in text.lower() for phrase in [
                    'what do you like best about',
                    'what do you dislike about',
                    'what problems are you solving',
                    'experience of working on',
                    'several features in',
                    'associative model',
                    'data visualization',
                    'dashboard management'
                ]):
                    potential_reviews.append(element)
        
        logger.info(f"Found {len(potential_reviews)} potential review elements using pattern matching")
        return potential_reviews[:30]  # Limit to avoid detection
    
    async def _parse_single_review_enhanced(self, element: Any, source_url: str) -> Optional[EnhancedReview]:
        """Parse single review with enhanced features."""
        try:
            # Basic extraction
            text = self._extract_text_content(element)
            rating = self._extract_rating(element)
            date = self._extract_date(element)
            author = self._extract_author(element)
            
            if not text or len(text.strip()) < 20:
                return None
            
            # Enhanced features
            sentiment_score, sentiment_label = self.analyze_sentiment(text)
            competitor_mentions = self.extract_competitor_mentions(text, self.known_competitors)
            features, pain_points = self.extract_features_and_pain_points(text)
            pros, cons = self.extract_pros_and_cons(text)
            
            # Calculate quality metrics
            review_quality_score = self.calculate_review_quality_score(text)
            extraction_confidence = self._calculate_extraction_confidence(element)
            
            # Create enhanced review
            review = EnhancedReview(
                id=f"g2_{hash(f'{author}_{date}_{text[:50]}')}",
                source="G2",
                title=text[:100] + "..." if len(text) > 100 else text,
                content=text,
                rating=rating,
                author=author,
                date=date,
                url=source_url,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                competitor_mentions=competitor_mentions,
                feature_mentions=features,
                pain_points=pain_points,
                pros=pros,
                cons=cons,
                review_quality_score=review_quality_score,
                extraction_confidence=extraction_confidence,
                word_count=len(text.split()),
                extraction_method="enhanced_g2_parser",
                extraction_timestamp=datetime.now()
            )
            
            return review
            
        except Exception as e:
            logger.warning(f"Error parsing enhanced review: {e}")
            return None
    
    def _extract_text_content(self, element: Any) -> str:
        """Extract text content from review element."""
        # Try multiple text extraction strategies
        text_selectors = [
            'p', 'span', 'div', '.review-text', '.review-content', '.review-body'
        ]
        
        for selector in text_selectors:
            try:
                text_elements = element.select(selector)
                for text_element in text_elements:
                    text = text_element.get_text().strip()
                    if text and len(text) > 20:
                        return text
            except:
                continue
        
        # Fallback to element text
        return element.get_text().strip()
    
    def _extract_rating(self, element: Any) -> float:
        """Extract rating from review element."""
        try:
            # Multiple rating extraction strategies
            rating_selectors = [
                '[class*="rating"]', '.stars', '.score', '[data-testid="rating"]',
                '.review__rating', '.review-item__rating'
            ]
            
            for selector in rating_selectors:
                try:
                    rating_element = element.select_one(selector)
                    if rating_element:
                        rating_text = rating_element.get_text()
                        rating_match = re.search(r"(\d+\.?\d?)", rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                            if 0 <= rating <= 5:
                                return rating
                except:
                    continue
            
            # Look for rating in text content
            text = element.get_text()
            rating_match = re.search(r"(\d+\.?\d?)\s*out\s*of\s*5", text)
            if rating_match:
                rating = float(rating_match.group(1))
                if 0 <= rating <= 5:
                    return rating
            
            return 0.0
            
        except Exception as e:
            logger.debug(f"Error extracting rating: {e}")
            return 0.0
    
    def _extract_date(self, element: Any) -> datetime:
        """Extract date from review element."""
        try:
            # Multiple date extraction strategies
            date_selectors = [
                'time', '[class*="date"]', '.timestamp', '[data-testid="date"]',
                '.review__date', '.review-item__date'
            ]
            
            for selector in date_selectors:
                try:
                    date_element = element.select_one(selector)
                    if date_element:
                        date_str = date_element.get('datetime') or date_element.get_text().strip()
                        if date_str:
                            parsed_date = self._parse_date_string(date_str)
                            if parsed_date:
                                return parsed_date
                except:
                    continue
            
            # Look for date patterns in text
            text = element.get_text()
            date_patterns = [
                r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
                r'\d{4}-\d{2}-\d{2}',      # YYYY-MM-DD
                r'[A-Za-z]+\s+\d{1,2},?\s+\d{4}'  # Month DD, YYYY
            ]
            
            for pattern in date_patterns:
                date_match = re.search(pattern, text)
                if date_match:
                    parsed_date = self._parse_date_string(date_match.group(0))
                    if parsed_date:
                        return parsed_date
            
            return datetime.now()
            
        except Exception as e:
            logger.debug(f"Error extracting date: {e}")
            return datetime.now()
    
    def _extract_author(self, element: Any) -> str:
        """Extract author from review element."""
        try:
            # Multiple author extraction strategies
            author_selectors = [
                '[class*="author"]', '.reviewer-name', '.user-name', '[data-testid="reviewer"]',
                '.review__author', '.review-item__author'
            ]
            
            for selector in author_selectors:
                try:
                    author_element = element.select_one(selector)
                    if author_element:
                        author = author_element.get_text().strip()
                        if author and len(author) > 2 and author.lower() != 'anonymous':
                            return author
                except:
                    continue
            
            # Look for author patterns in text
            text = element.get_text()
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) < 50:
                    if not any(word in line.lower() for word in ['what', 'about', 'experience', 'several', 'associative']):
                        if not any(char.isdigit() for char in line):
                            if re.match(r'^[A-Z][a-z]+\s+[A-Z]\.?$', line):  # Pattern like "John D."
                                return line
            
            return "Anonymous"
            
        except Exception as e:
            logger.debug(f"Error extracting author: {e}")
            return "Anonymous"
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        """Parse date string into datetime object."""
        try:
            # Try various date formats
            date_formats = [
                "%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d/%m/%Y", "%m/%d/%Y",
                "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception as e:
            logger.debug(f"Error parsing date string '{date_str}': {e}")
            return None
    
    def _calculate_extraction_confidence(self, element: Any) -> float:
        """Calculate confidence in extraction."""
        confidence = 0.0
        
        # Check if we have text content
        if element.get_text().strip():
            confidence += 0.3
        
        # Check if we have rating
        if self._extract_rating(element) > 0:
            confidence += 0.2
        
        # Check if we have author
        author = self._extract_author(element)
        if author and author != "Anonymous":
            confidence += 0.2
        
        # Check if we have date
        date = self._extract_date(element)
        if date and date != datetime.now():
            confidence += 0.1
        
        # Check element structure
        if element.name in ['div', 'p', 'span']:
            confidence += 0.1
        
        # Check for review-like content
        text = element.get_text().lower()
        if any(phrase in text for phrase in ['like', 'dislike', 'experience', 'feature']):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    async def _enhance_reviews_with_intelligence(self, reviews: List[EnhancedReview]) -> List[EnhancedReview]:
        """Enhance reviews with competitive intelligence."""
        try:
            for review in reviews:
                # Add sentiment analysis if not present
                if review.sentiment_score is None:
                    review.sentiment_score, review.sentiment_label = self.analyze_sentiment(review.content)
                
                # Add competitor mentions if not present
                if not review.competitor_mentions:
                    review.competitor_mentions = self.extract_competitor_mentions(review.content, self.known_competitors)
                
                # Add features and pain points if not present
                if not review.feature_mentions and not review.pain_points:
                    review.feature_mentions, review.pain_points = self.extract_features_and_pain_points(review.content)
                
                # Add pros and cons if not present
                if not review.pros and not review.cons:
                    review.pros, review.cons = self.extract_pros_and_cons(review.content)
                
                # Calculate quality score if not present
                if review.review_quality_score is None:
                    review.review_quality_score = self.calculate_review_quality_score(review.content)
                
                # Add word count if not present
                if review.word_count is None:
                    review.word_count = len(review.content.split())
            
            return reviews
            
        except Exception as e:
            logger.error(f"Error enhancing reviews with intelligence: {e}")
            return reviews
    
    # Backward compatibility methods
    @staticmethod
    def extract_reviews(html: str, source_url: str) -> List[Review]:
        """Legacy method for backward compatibility."""
        parser = G2Parser()
        # Convert EnhancedReview to Review for backward compatibility
        enhanced_reviews = asyncio.run(parser.extract_reviews(html, source_url))
        return [Review(
            review_id=review.id,
            source=review.source,
            title=review.title,
            content=review.content,
            rating=review.rating,
            author=review.author,
            date=review.date,
            url=review.url
        ) for review in enhanced_reviews]
    
    @staticmethod
    def _parse_review_element(review_element, source_url):
        """Legacy method for backward compatibility."""
        parser = G2Parser()
        # This is a simplified version for backward compatibility
        return parser._parse_single_review_enhanced(review_element, source_url)
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Legacy method for backward compatibility."""
        parser = G2Parser()
        parsed_date = parser._parse_date_string(date_str)
        return parsed_date if parsed_date else datetime.now()
