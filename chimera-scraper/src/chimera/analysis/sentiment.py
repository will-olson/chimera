"""Advanced sentiment analysis for review intelligence."""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from loguru import logger
import asyncio

from chimera.models.review import ReviewSentiment


class AdvancedSentimentAnalyzer:
    """Advanced sentiment analyzer with context-aware analysis and competitive intelligence."""
    
    def __init__(self):
        self.sentiment_lexicons = self._load_sentiment_lexicons()
        self.context_modifiers = self._load_context_modifiers()
        self.competitor_sentiment_patterns = self._load_competitor_patterns()
        self.industry_specific_terms = self._load_industry_terms()
        
    def _load_sentiment_lexicons(self) -> Dict[str, Dict[str, float]]:
        """Load comprehensive sentiment lexicons."""
        return {
            "positive": {
                "excellent": 0.9, "outstanding": 0.9, "amazing": 0.8, "fantastic": 0.8,
                "great": 0.7, "good": 0.6, "nice": 0.5, "decent": 0.4, "satisfactory": 0.4,
                "love": 0.9, "like": 0.6, "enjoy": 0.7, "appreciate": 0.6,
                "recommend": 0.8, "suggest": 0.6, "endorse": 0.8,
                "easy": 0.6, "simple": 0.5, "intuitive": 0.7, "user-friendly": 0.7,
                "fast": 0.6, "quick": 0.6, "efficient": 0.7, "productive": 0.7,
                "reliable": 0.7, "stable": 0.6, "consistent": 0.6, "dependable": 0.7,
                "powerful": 0.7, "robust": 0.7, "comprehensive": 0.6, "complete": 0.6,
                "innovative": 0.7, "modern": 0.6, "advanced": 0.6, "cutting-edge": 0.7,
                "affordable": 0.6, "cost-effective": 0.6, "value": 0.6, "worth": 0.6,
                "support": 0.6, "helpful": 0.6, "responsive": 0.6, "professional": 0.6
            },
            "negative": {
                "terrible": -0.9, "awful": -0.9, "horrible": -0.8, "dreadful": -0.8,
                "bad": -0.6, "poor": -0.7, "mediocre": -0.4, "disappointing": -0.6,
                "hate": -0.9, "dislike": -0.6, "frustrated": -0.7, "annoyed": -0.6,
                "avoid": -0.7, "waste": -0.6, "regret": -0.7,
                "difficult": -0.5, "complicated": -0.5, "confusing": -0.6, "complex": -0.4,
                "slow": -0.5, "laggy": -0.6, "unresponsive": -0.6, "buggy": -0.7,
                "unreliable": -0.7, "unstable": -0.7, "inconsistent": -0.6, "glitchy": -0.7,
                "weak": -0.5, "limited": -0.4, "basic": -0.3, "simple": -0.2,
                "outdated": -0.5, "old": -0.4, "obsolete": -0.6, "archaic": -0.6,
                "expensive": -0.4, "overpriced": -0.6, "costly": -0.4, "waste": -0.5,
                "unhelpful": -0.6, "unresponsive": -0.6, "slow": -0.5, "incompetent": -0.7
            },
            "neutral": {
                "okay": 0.0, "fine": 0.0, "average": 0.0, "standard": 0.0,
                "normal": 0.0, "typical": 0.0, "usual": 0.0, "regular": 0.0,
                "adequate": 0.0, "sufficient": 0.0, "acceptable": 0.0, "tolerable": 0.0,
                "moderate": 0.0, "reasonable": 0.0, "fair": 0.0, "balanced": 0.0
            }
        }
    
    def _load_context_modifiers(self) -> Dict[str, float]:
        """Load context modifiers that affect sentiment intensity."""
        return {
            "very": 1.5, "really": 1.4, "extremely": 1.6, "incredibly": 1.7,
            "absolutely": 1.8, "completely": 1.6, "totally": 1.5, "entirely": 1.5,
            "somewhat": 0.7, "kind of": 0.6, "sort of": 0.6, "a bit": 0.5,
            "slightly": 0.8, "moderately": 0.9, "reasonably": 0.9,
            "not": -1.0, "never": -1.0, "no": -1.0, "none": -1.0,
            "barely": 0.3, "hardly": 0.2, "scarcely": 0.2, "almost": 0.8
        }
    
    def _load_competitor_patterns(self) -> Dict[str, Dict[str, float]]:
        """Load competitor-specific sentiment patterns."""
        return {
            "tableau": {
                "positive": ["beautiful", "visual", "intuitive", "powerful", "enterprise"],
                "negative": ["expensive", "complex", "heavy", "resource-intensive"]
            },
            "power bi": {
                "positive": ["affordable", "microsoft", "integrated", "familiar"],
                "negative": ["limited", "basic", "restrictive", "windows-only"]
            },
            "qlik sense": {
                "positive": ["associative", "fast", "flexible", "innovative"],
                "negative": ["steep learning", "complex", "expensive", "niche"]
            },
            "looker": {
                "positive": ["sql", "data modeling", "enterprise", "scalable"],
                "negative": ["technical", "complex", "expensive", "sql-heavy"]
            }
        }
    
    def _load_industry_terms(self) -> Dict[str, List[str]]:
        """Load industry-specific terminology for context analysis."""
        return {
            "business_intelligence": [
                "dashboard", "report", "analytics", "insights", "kpi", "metrics",
                "data warehouse", "etl", "data modeling", "visualization"
            ],
            "crm": [
                "lead", "opportunity", "pipeline", "sales", "customer", "contact",
                "deal", "forecast", "quota", "conversion"
            ],
            "marketing": [
                "campaign", "lead generation", "email", "social media", "seo",
                "conversion", "funnel", "roi", "engagement", "reach"
            ]
        }
    
    async def analyze_sentiment_advanced(self, text: str, context: Optional[Dict[str, Any]] = None) -> Tuple[float, ReviewSentiment, Dict[str, Any]]:
        """Perform advanced sentiment analysis with context awareness."""
        try:
            # Basic sentiment calculation
            base_sentiment = self._calculate_base_sentiment(text)
            
            # Apply context modifiers
            context_adjusted_sentiment = self._apply_context_modifiers(text, base_sentiment)
            
            # Apply competitor-specific adjustments
            competitor_adjusted_sentiment = self._apply_competitor_context(text, context_adjusted_sentiment)
            
            # Apply industry-specific adjustments
            industry_adjusted_sentiment = self._apply_industry_context(text, competitor_adjusted_sentiment, context)
            
            # Calculate confidence and reliability metrics
            confidence_metrics = self._calculate_confidence_metrics(text, industry_adjusted_sentiment)
            
            # Determine final sentiment label
            sentiment_label = self._determine_sentiment_label(industry_adjusted_sentiment)
            
            # Prepare detailed analysis
            analysis_details = {
                "base_sentiment": base_sentiment,
                "context_adjusted": context_adjusted_sentiment,
                "competitor_adjusted": competitor_adjusted_sentiment,
                "industry_adjusted": industry_adjusted_sentiment,
                "confidence_metrics": confidence_metrics,
                "text_length": len(text),
                "word_count": len(text.split()),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return industry_adjusted_sentiment, sentiment_label, analysis_details
            
        except Exception as e:
            logger.error(f"Error in advanced sentiment analysis: {e}")
            return 0.0, ReviewSentiment.NEUTRAL, {"error": str(e)}
    
    def _calculate_base_sentiment(self, text: str) -> float:
        """Calculate base sentiment score from text."""
        text_lower = text.lower()
        words = text_lower.split()
        
        total_score = 0.0
        word_count = 0
        
        for word in words:
            word_clean = re.sub(r'[^\w\s]', '', word)
            if word_clean:
                # Check positive lexicon
                if word_clean in self.sentiment_lexicons["positive"]:
                    total_score += self.sentiment_lexicons["positive"][word_clean]
                    word_count += 1
                # Check negative lexicon
                elif word_clean in self.sentiment_lexicons["negative"]:
                    total_score += self.sentiment_lexicons["negative"][word_clean]
                    word_count += 1
                # Check neutral lexicon
                elif word_clean in self.sentiment_lexicons["neutral"]:
                    word_count += 1
        
        if word_count == 0:
            return 0.0
        
        return total_score / word_count
    
    def _apply_context_modifiers(self, text: str, base_sentiment: float) -> float:
        """Apply context modifiers to adjust sentiment intensity."""
        text_lower = text.lower()
        words = text_lower.split()
        
        modified_sentiment = base_sentiment
        modifier_count = 0
        
        for i, word in enumerate(words):
            if word in self.context_modifiers:
                modifier = self.context_modifiers[word]
                
                # Look for the next word to modify
                if i + 1 < len(words):
                    next_word = words[i + 1]
                    next_word_clean = re.sub(r'[^\w\s]', '', next_word)
                    
                    # Check if next word is a sentiment word
                    sentiment_value = 0.0
                    if next_word_clean in self.sentiment_lexicons["positive"]:
                        sentiment_value = self.sentiment_lexicons["positive"][next_word_clean]
                    elif next_word_clean in self.sentiment_lexicons["negative"]:
                        sentiment_value = self.sentiment_lexicons["negative"][next_word_clean]
                    
                    if sentiment_value != 0.0:
                        # Apply modifier
                        if modifier == -1.0:  # Negation
                            modified_sentiment = -sentiment_value
                        else:
                            modified_sentiment = sentiment_value * modifier
                        modifier_count += 1
        
        # If no modifiers found, return base sentiment
        if modifier_count == 0:
            return base_sentiment
        
        return modified_sentiment
    
    def _apply_competitor_context(self, text: str, sentiment: float) -> float:
        """Apply competitor-specific sentiment adjustments."""
        text_lower = text.lower()
        adjusted_sentiment = sentiment
        
        for competitor, patterns in self.competitor_sentiment_patterns.items():
            if competitor.lower() in text_lower:
                # Check for positive patterns
                positive_matches = sum(1 for pattern in patterns["positive"] if pattern in text_lower)
                negative_matches = sum(1 for pattern in patterns["negative"] if pattern in text_lower)
                
                # Adjust sentiment based on pattern matches
                if positive_matches > negative_matches:
                    adjusted_sentiment += 0.1 * (positive_matches - negative_matches)
                elif negative_matches > positive_matches:
                    adjusted_sentiment -= 0.1 * (negative_matches - positive_matches)
        
        return max(-1.0, min(1.0, adjusted_sentiment))
    
    def _apply_industry_context(self, text: str, sentiment: float, context: Optional[Dict[str, Any]] = None) -> float:
        """Apply industry-specific sentiment adjustments."""
        text_lower = text.lower()
        adjusted_sentiment = sentiment
        
        # Determine industry context
        industry = context.get("industry", "business_intelligence") if context else "business_intelligence"
        
        if industry in self.industry_specific_terms:
            industry_terms = self.industry_specific_terms[industry]
            term_matches = sum(1 for term in industry_terms if term in text_lower)
            
            # Adjust sentiment based on industry term usage
            if term_matches > 0:
                # More industry terms suggest more informed review
                confidence_boost = min(0.1, term_matches * 0.02)
                adjusted_sentiment += confidence_boost
        
        return max(-1.0, min(1.0, adjusted_sentiment))
    
    def _calculate_confidence_metrics(self, text: str, sentiment: float) -> Dict[str, Any]:
        """Calculate confidence and reliability metrics for sentiment analysis."""
        text_lower = text.lower()
        words = text_lower.split()
        
        # Count sentiment words
        sentiment_words = 0
        for word in words:
            word_clean = re.sub(r'[^\w\s]', '', word)
            if (word_clean in self.sentiment_lexicons["positive"] or 
                word_clean in self.sentiment_lexicons["negative"] or
                word_clean in self.sentiment_lexicons["neutral"]):
                sentiment_words += 1
        
        # Calculate confidence based on sentiment word density
        sentiment_density = sentiment_words / len(words) if words else 0
        
        # Calculate text quality indicators
        has_punctuation = any(char in text for char in "!?.,;:")
        has_capitalization = any(word[0].isupper() for word in words if word)
        has_numbers = any(char.isdigit() for char in text)
        
        # Overall confidence score
        confidence_score = min(1.0, (
            sentiment_density * 0.4 +
            (0.2 if has_punctuation else 0) +
            (0.2 if has_capitalization else 0) +
            (0.1 if has_numbers else 0) +
            (0.1 if len(text) > 50 else 0)
        ))
        
        return {
            "sentiment_word_count": sentiment_words,
            "sentiment_density": sentiment_density,
            "text_quality": {
                "has_punctuation": has_punctuation,
                "has_capitalization": has_capitalization,
                "has_numbers": has_numbers,
                "length_adequate": len(text) > 50
            },
            "confidence_score": confidence_score,
            "reliability": "high" if confidence_score > 0.7 else "medium" if confidence_score > 0.4 else "low"
        }
    
    def _determine_sentiment_label(self, sentiment_score: float) -> ReviewSentiment:
        """Determine sentiment label from sentiment score."""
        if sentiment_score >= 0.3:
            return ReviewSentiment.POSITIVE
        elif sentiment_score <= -0.3:
            return ReviewSentiment.NEGATIVE
        else:
            return ReviewSentiment.NEUTRAL
    
    async def analyze_batch_sentiment(self, texts: List[str], context: Optional[Dict[str, Any]] = None) -> List[Tuple[float, ReviewSentiment, Dict[str, Any]]]:
        """Analyze sentiment for a batch of texts."""
        results = []
        
        for text in texts:
            result = await self.analyze_sentiment_advanced(text, context)
            results.append(result)
        
        return results
    
    async def get_sentiment_summary(self, texts: List[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get sentiment summary for a collection of texts."""
        if not texts:
            return {"error": "No texts provided"}
        
        # Analyze all texts
        sentiment_results = await self.analyze_batch_sentiment(texts, context)
        
        # Calculate summary statistics
        sentiment_scores = [result[0] for result in sentiment_results]
        sentiment_labels = [result[1] for result in sentiment_results]
        
        # Count sentiment distribution
        sentiment_distribution = {
            "positive": sentiment_labels.count(ReviewSentiment.POSITIVE),
            "negative": sentiment_labels.count(ReviewSentiment.NEGATIVE),
            "neutral": sentiment_labels.count(ReviewSentiment.NEUTRAL)
        }
        
        # Calculate average sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # Calculate confidence metrics
        confidence_scores = [result[2].get("confidence_score", 0) for result in sentiment_results]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            "total_texts": len(texts),
            "average_sentiment": avg_sentiment,
            "sentiment_distribution": sentiment_distribution,
            "average_confidence": avg_confidence,
            "sentiment_range": {
                "min": min(sentiment_scores) if sentiment_scores else 0,
                "max": max(sentiment_scores) if sentiment_scores else 0
            },
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    # Backward compatibility method
    def analyze_sentiment(self, text: str) -> Tuple[float, ReviewSentiment]:
        """Legacy method for backward compatibility."""
        sentiment_score, sentiment_label, _ = asyncio.run(self.analyze_sentiment_advanced(text))
        return sentiment_score, sentiment_label
