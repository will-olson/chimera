"""Base parser infrastructure for HTML and data parsing."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from loguru import logger

from chimera.models.review import EnhancedReview, ReviewSentiment


class BaseParser(ABC):
    """Abstract base class for all parsers with advanced features."""
    
    def __init__(self):
        self.selector_cache = {}
        self.extraction_stats = {
            'total_attempts': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'selector_success_rates': {},
            'extraction_times': []
        }
        self.last_extraction_time = None
        
    @abstractmethod
    def extract_reviews(self, html: str, source_url: str) -> List[EnhancedReview]:
        """Extract reviews from HTML content."""
        pass
    
    def validate_extraction(self, reviews: List[EnhancedReview]) -> List[EnhancedReview]:
        """Validate extracted reviews for quality."""
        validated_reviews = []
        
        for review in reviews:
            if self._is_valid_review(review):
                validated_reviews.append(review)
            else:
                self.extraction_stats['failed_extractions'] += 1
                logger.debug(f"Review validation failed: {review.id}")
        
        self.extraction_stats['successful_extractions'] = len(validated_reviews)
        return validated_reviews
    
    def _is_valid_review(self, review: EnhancedReview) -> bool:
        """Check if a review meets quality standards."""
        # Basic validation
        if not review.content or len(review.content.strip()) < 20:
            return False
        
        if not review.author or review.author.strip() == "":
            return False
        
        # Rating validation
        if review.rating and (review.rating < 0 or review.rating > 5):
            return False
        
        # Content quality check
        if len(review.content.split()) < 10:  # At least 10 words
            return False
        
        return True
    
    def cache_selectors(self, selectors: Dict[str, str]):
        """Cache successful selectors for future use."""
        for selector_type, selector in selectors.items():
            if selector_type not in self.selector_cache:
                self.selector_cache[selector_type] = []
            
            if selector not in self.selector_cache[selector_type]:
                self.selector_cache[selector_type].append(selector)
                logger.debug(f"Cached selector: {selector_type} -> {selector}")
    
    def get_cached_selectors(self, selector_type: str) -> List[str]:
        """Get cached selectors for a specific type."""
        return self.selector_cache.get(selector_type, [])
    
    def update_extraction_stats(self, selector: str, success: bool, extraction_time: float):
        """Update extraction statistics."""
        self.extraction_stats['total_attempts'] += 1
        
        if success:
            self.extraction_stats['successful_extractions'] += 1
            
            # Update selector success rate
            if selector not in self.extraction_stats['selector_success_rates']:
                self.extraction_stats['selector_success_rates'][selector] = {'success': 0, 'total': 0}
            
            self.extraction_stats['selector_success_rates'][selector]['success'] += 1
            self.extraction_stats['selector_success_rates'][selector]['total'] += 1
            
        else:
            self.extraction_stats['failed_extractions'] += 1
            
            if selector in self.extraction_stats['selector_success_rates']:
                self.extraction_stats['selector_success_rates'][selector]['total'] += 1
        
        # Record extraction time
        self.extraction_stats['extraction_times'].append(extraction_time)
        
        # Keep only last 100 extraction times
        if len(self.extraction_stats['extraction_times']) > 100:
            self.extraction_stats['extraction_times'] = self.extraction_stats['extraction_times'][-100:]
    
    def get_extraction_stats(self) -> Dict[str, Any]:
        """Get comprehensive extraction statistics."""
        stats = self.extraction_stats.copy()
        
        # Calculate success rate
        if stats['total_attempts'] > 0:
            stats['overall_success_rate'] = stats['successful_extractions'] / stats['total_attempts']
        else:
            stats['overall_success_rate'] = 0.0
        
        # Calculate average extraction time
        if stats['extraction_times']:
            stats['average_extraction_time'] = sum(stats['extraction_times']) / len(stats['extraction_times'])
        else:
            stats['average_extraction_time'] = 0.0
        
        # Calculate selector success rates
        for selector, data in stats['selector_success_rates'].items():
            if data['total'] > 0:
                data['success_rate'] = data['success'] / data['total']
            else:
                data['success_rate'] = 0.0
        
        return stats
    
    def analyze_sentiment(self, text: str) -> tuple[float, ReviewSentiment]:
        """Basic sentiment analysis for review text."""
        if not text:
            return 0.0, ReviewSentiment.NEUTRAL
        
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = [
            'excellent', 'great', 'amazing', 'outstanding', 'fantastic', 'wonderful',
            'love', 'perfect', 'best', 'awesome', 'brilliant', 'superb', 'terrific'
        ]
        
        # Negative indicators
        negative_words = [
            'terrible', 'awful', 'horrible', 'worst', 'bad', 'poor', 'disappointing',
            'hate', 'useless', 'broken', 'frustrating', 'annoying', 'difficult'
        ]
        
        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate sentiment score (-1 to 1)
        total_words = len(text.split())
        if total_words == 0:
            return 0.0, ReviewSentiment.NEUTRAL
        
        sentiment_score = (positive_count - negative_count) / max(total_words, 10)
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Categorize sentiment
        if sentiment_score > 0.1:
            sentiment_label = ReviewSentiment.POSITIVE
        elif sentiment_score < -0.1:
            sentiment_label = ReviewSentiment.NEGATIVE
        else:
            sentiment_label = ReviewSentiment.NEUTRAL
        
        return sentiment_score, sentiment_label
    
    def extract_competitor_mentions(self, text: str, known_competitors: List[str]) -> List[str]:
        """Extract mentions of known competitors from review text."""
        if not text or not known_competitors:
            return []
        
        text_lower = text.lower()
        mentioned_competitors = []
        
        for competitor in known_competitors:
            competitor_lower = competitor.lower()
            
            # Check for exact matches and variations
            if competitor_lower in text_lower:
                mentioned_competitors.append(competitor)
            elif competitor_lower.replace(' ', '') in text_lower.replace(' ', ''):
                mentioned_competitors.append(competitor)
            elif competitor_lower.replace('-', ' ') in text_lower:
                mentioned_competitors.append(competitor)
        
        return mentioned_competitors
    
    def extract_features_and_pain_points(self, text: str) -> tuple[List[str], List[str]]:
        """Extract features and pain points from review text."""
        if not text:
            return [], []
        
        text_lower = text.lower()
        
        # Feature indicators
        feature_indicators = [
            'feature', 'functionality', 'capability', 'tool', 'option', 'setting',
            'dashboard', 'report', 'analytics', 'integration', 'api', 'workflow'
        ]
        
        # Pain point indicators
        pain_indicators = [
            'problem', 'issue', 'bug', 'error', 'crash', 'slow', 'difficult',
            'confusing', 'complicated', 'frustrating', 'annoying', 'broken'
        ]
        
        features = []
        pain_points = []
        
        # Extract sentences containing indicators
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if not sentence_lower:
                continue
            
            # Check for features
            if any(indicator in sentence_lower for indicator in feature_indicators):
                if len(sentence.strip()) > 10:
                    features.append(sentence.strip())
            
            # Check for pain points
            if any(indicator in sentence_lower for indicator in pain_indicators):
                if len(sentence.strip()) > 10:
                    pain_points.append(sentence.strip())
        
        return features, pain_points
    
    def calculate_review_quality_score(self, review: EnhancedReview) -> float:
        """Calculate a quality score for a review."""
        score = 0.0
        
        # Content length score (0-0.3)
        if review.content:
            word_count = len(review.content.split())
            if word_count >= 50:
                score += 0.3
            elif word_count >= 25:
                score += 0.2
            elif word_count >= 10:
                score += 0.1
        
        # Rating presence score (0-0.2)
        if review.rating and review.rating > 0:
            score += 0.2
        
        # Author information score (0-0.2)
        if review.author and review.author != "Anonymous":
            score += 0.2
        
        # Date presence score (0-0.1)
        if review.date:
            score += 0.1
        
        # Sentiment analysis score (0-0.1)
        if review.sentiment_score is not None:
            score += 0.1
        
        # Additional metadata score (0-0.1)
        if review.pros or review.cons or review.use_case:
            score += 0.1
        
        return min(1.0, score)
    
    def extract_pros_and_cons(self, text: str) -> tuple[List[str], List[str]]:
        """Extract pros and cons from review text."""
        if not text:
            return [], []
        
        pros = []
        cons = []
        
        # Look for explicit pros/cons sections
        if '+ Pros' in text or 'Pros:' in text:
            pros_section = self._extract_section(text, ['+ Pros', 'Pros:', 'Advantages:'])
            if pros_section:
                pros = [line.strip() for line in pros_section.split('\n') if line.strip() and len(line.strip()) > 5]
        
        if '- Cons' in text or 'Cons:' in text:
            cons_section = self._extract_section(text, ['- Cons', 'Cons:', 'Disadvantages:'])
            if cons_section:
                cons = [line.strip() for line in cons_section.split('\n') if line.strip() and len(line.strip()) > 5]
        
        return pros, cons
    
    def _extract_section(self, text: str, markers: List[str]) -> str:
        """Extract a section of text based on markers."""
        for marker in markers:
            if marker in text:
                parts = text.split(marker)
                if len(parts) > 1:
                    section = parts[1]
                    # Look for next section marker
                    for next_marker in ['+ Pros', '- Cons', 'Pros:', 'Cons:', 'Advantages:', 'Disadvantages:']:
                        if next_marker in section:
                            section = section.split(next_marker)[0]
                            break
                    return section.strip()
        return ""
    
    def get_parser_info(self) -> Dict[str, Any]:
        """Get information about the parser."""
        return {
            'parser_type': self.__class__.__name__,
            'selector_cache_size': sum(len(selectors) for selectors in self.selector_cache.values()),
            'extraction_stats': self.get_extraction_stats(),
            'last_extraction': self.last_extraction_time.isoformat() if self.last_extraction_time else None
        }
