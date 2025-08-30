#!/usr/bin/env python3
"""Standalone head-to-head comparison parser for immediate testing."""

import re
import json
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class HeadToHeadComparisonData:
    """Structured data for head-to-head comparison analysis."""
    comparison_id: str
    extraction_date: datetime
    url: str
    
    # Product information
    product_a: dict
    product_b: dict
    
    # AI-generated summary (most valuable data)
    ai_generated_summary: dict
    
    # Comparison sections
    at_a_glance: dict
    pricing: dict
    ratings: dict
    features: dict
    reviews: dict
    alternatives: dict
    
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
    market_segments: dict
    entry_level_pricing: str
    pricing_details: dict
    ratings_by_criteria: dict
    feature_scores: dict


@dataclass
class AIGeneratedSummary:
    """AI-generated summary data with structured insights."""
    summary_title: str
    summary_subtitle: str
    summary_points: list
    extraction_confidence: float
    structured_insights: dict


@dataclass
class SummaryPoint:
    """Individual summary point with structured data."""
    text: str
    product_a_score: float
    product_b_score: float
    feature_category: str
    insight_type: str
    sentiment: str
    confidence: float


class StandaloneHeadToHeadParser:
    """Standalone parser for G2 head-to-head comparison pages."""
    
    def __init__(self):
        self.known_sections = [
            "At a Glance",
            "Pricing", 
            "Ratings",
            "Features",
            "Reviews",
            "Alternatives",
            "Discussions"
        ]
        
        self.feature_categories = [
            "Data Visualization",
            "Ease of Setup",
            "AI Text Generation",
            "Data Governance",
            "Collaboration and Workflow",
            "Predictive Analytics"
        ]
        
        self.summary_patterns = {
            "score_comparison": r"scoring\s+(\d+\.?\d*)\s+compared\s+to\s+[^\']*?(\d+\.?\d*)",
            "feature_mention": r"(?:excel|excels|superior|stronger|better|trails|behind)\s+(?:in|at)\s+([^,]+)",
            "sentiment_indicators": r"(?:excellent|fantastic|superior|better|trails|behind|lower|stronger|weaker)",
            "product_names": r"(?:Microsoft Power BI|Power BI|Domo|Tableau|Qlik|Snowflake|Databricks)"
        }
    
    def parse_head_to_head_comparison(self, html: str, url: str) -> HeadToHeadComparisonData:
        """Parse a G2 head-to-head comparison page comprehensively."""
        try:
            # Extract basic comparison info
            comparison_id = self._extract_comparison_id(url)
            
            # Extract products information
            products = self._extract_products(html)
            if len(products) != 2:
                raise ValueError(f"Expected 2 products, found {len(products)}")
            
            product_a, product_b = products[0], products[1]
            
            # Extract AI-generated summary (highest priority)
            ai_summary = self._extract_ai_generated_summary(html)
            
            # Extract comparison sections
            at_a_glance = self._extract_at_a_glance(html, products)
            pricing = self._extract_pricing(html, products)
            ratings = self._extract_ratings(html, products)
            features = self._extract_features(html, products)
            reviews = self._extract_reviews(html, products)
            alternatives = self._extract_alternatives(html, products)
            
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
                extraction_confidence=self._calculate_extraction_confidence(html),
                summary_quality_score=summary_quality_score
            )
            
            print(f"Successfully parsed head-to-head comparison with AI summary quality: {summary_quality_score:.1f}")
            return comparison_data
            
        except Exception as e:
            print(f"Failed to parse head-to-head comparison: {e}")
            raise
    
    def _extract_comparison_id(self, url: str) -> str:
        """Extract unique comparison ID from URL."""
        try:
            comparison_part = url.split('/compare/')[-1]
            comparison_id = comparison_part.replace('-', '_').replace('vs', 'vs')
            return f"head_to_head_{comparison_id}"
        except Exception as e:
            print(f"Failed to extract comparison ID: {e}")
            return f"head_to_head_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _extract_products(self, html: str) -> list:
        """Extract product information from comparison headers."""
        products = []
        
        try:
            # Look for product names in the HTML
            product_names = self._extract_product_names_from_html(html)
            
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
            
            print(f"Extracted {len(products)} products from head-to-head comparison")
            return products
            
        except Exception as e:
            print(f"Failed to extract products: {e}")
            return []
    
    def _extract_product_names_from_html(self, html: str) -> list:
        """Extract product names from HTML content."""
        known_products = [
            'Microsoft Power BI', 'Power BI', 'Qlik Sense', 'Tableau', 'Domo',
            'Snowflake', 'Databricks', 'Amazon Redshift', 'Google BigQuery',
            'Looker', 'Sisense', 'ThoughtSpot'
        ]
        
        found_products = []
        for product in known_products:
            if product.lower() in html.lower():
                found_products.append(product)
        
        # If no known products found, try to extract from HTML structure
        if not found_products:
            # Look for common patterns
            if 'comparison-container-v2_header' in html:
                # Extract text between these tags
                import re
                headers = re.findall(r'comparison-container-v2_header[^>]*>([^<]+)', html)
                found_products.extend(headers[:2])  # Take first 2
        
        return found_products[:2]  # Ensure we only return 2 products
    
    def _extract_ai_generated_summary(self, html: str) -> AIGeneratedSummary:
        """Extract AI-generated summary - the most valuable data."""
        try:
            # Look for summary section
            if 'Comparison Summary' in html or 'AI Generated Summary' in html:
                # Extract summary points
                summary_points = self._extract_summary_points(html)
                
                # Generate structured insights
                structured_insights = self._analyze_summary_insights(summary_points)
                
                summary = AIGeneratedSummary(
                    summary_title="AI Generated Summary",
                    summary_subtitle="AI-generated. Powered by real user reviews.",
                    summary_points=summary_points,
                    extraction_confidence=self._calculate_summary_extraction_confidence(html),
                    structured_insights=structured_insights
                )
                
                print(f"Successfully extracted AI-generated summary with {len(summary_points)} points")
                return summary
            
            # If no summary section found, create empty summary
            print("No AI-generated summary section found")
            return AIGeneratedSummary(
                summary_title="No Summary Found",
                summary_subtitle="",
                summary_points=[],
                extraction_confidence=0.0,
                structured_insights={}
            )
            
        except Exception as e:
            print(f"Failed to extract AI-generated summary: {e}")
            return AIGeneratedSummary(
                summary_title="Extraction Failed",
                summary_subtitle="",
                summary_points=[],
                extraction_confidence=0.0,
                structured_insights={}
            )
    
    def _extract_summary_points(self, html: str) -> list:
        """Extract individual summary points with structured data."""
        summary_points = []
        
        try:
            # Look for list items containing summary points
            import re
            list_items = re.findall(r'<li[^>]*>([^<]+)</li>', html)
            
            for item in list_items:
                try:
                    point_text = item.strip()
                    if point_text and len(point_text) > 50:
                        
                        # Parse the summary point
                        summary_point = self._parse_summary_point(point_text)
                        summary_points.append(summary_point)
                        
                except Exception as e:
                    print(f"Failed to parse summary point: {e}")
                    continue
            
            return summary_points
            
        except Exception as e:
            print(f"Failed to extract summary points: {e}")
            return []
    
    def _parse_summary_point(self, point_text: str) -> dict:
        """Parse individual summary point to extract structured data."""
        try:
            # Extract scores if present
            import re
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
                product_a_score=product_a_score or 0.0,
                product_b_score=product_b_score or 0.0,
                feature_category=feature_category,
                insight_type=insight_type,
                sentiment=sentiment,
                confidence=confidence
            )
            
            return asdict(summary_point)
            
        except Exception as e:
            print(f"Failed to parse summary point: {e}")
            return {
                "text": point_text,
                "product_a_score": 0.0,
                "product_b_score": 0.0,
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
    
    def _calculate_point_confidence(self, text: str, score_a: float, score_b: float) -> float:
        """Calculate confidence in the extracted summary point data."""
        confidence = 0.0
        
        # Base confidence from text quality
        if len(text) > 100:
            confidence += 30
        elif len(text) > 50:
            confidence += 20
        
        # Confidence from score extraction
        if score_a and score_b:
            confidence += 40
        
        # Confidence from structured data
        if any(word in text.lower() for word in ["scoring", "compared", "versus"]):
            confidence += 20
        
        # Confidence from feature identification
        if self._extract_feature_category(text) != "other":
            confidence += 10
        
        return min(confidence, 100.0)
    
    def _analyze_summary_insights(self, summary_points: list) -> dict:
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
            print(f"Failed to analyze summary insights: {e}")
            return {}
    
    def _calculate_summary_extraction_confidence(self, html: str) -> float:
        """Calculate confidence in summary extraction."""
        try:
            confidence = 0.0
            
            # Check for key structural elements
            if 'Comparison Summary' in html:
                confidence += 40
            if 'AI Generated Summary' in html:
                confidence += 30
            if '<li>' in html:
                confidence += 20
            if 'AI-generated' in html:
                confidence += 10
            
            return min(confidence, 100.0)
            
        except Exception as e:
            print(f"Failed to calculate summary extraction confidence: {e}")
            return 0.0
    
    # Placeholder methods for additional data extraction
    def _extract_at_a_glance(self, html: str, products: list) -> dict:
        """Extract 'At a Glance' section data."""
        return {}
    
    def _extract_pricing(self, html: str, products: list) -> dict:
        """Extract comprehensive pricing information."""
        return {}
    
    def _extract_ratings(self, html: str, products: list) -> dict:
        """Extract comprehensive ratings by criteria."""
        return {}
    
    def _extract_features(self, html: str, products: list) -> dict:
        """Extract comprehensive feature comparison data."""
        return {}
    
    def _extract_reviews(self, html: str, products: list) -> dict:
        """Extract comprehensive review data and insights."""
        return {}
    
    def _extract_alternatives(self, html: str, products: list) -> dict:
        """Extract comprehensive alternatives data."""
        return {}
    
    def _calculate_data_quality_score(self, products: list, 
                                    at_a_glance: dict, 
                                    pricing: dict, 
                                    ratings: dict, 
                                    features: dict,
                                    reviews: dict,
                                    alternatives: dict) -> float:
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
            print(f"Failed to calculate data quality score: {e}")
            return 0.0
    
    def _calculate_extraction_confidence(self, html: str) -> float:
        """Calculate confidence in the extraction process."""
        try:
            confidence = 0.0
            
            # Check for key structural elements
            if 'data-eventscope="Comparison Table"' in html:
                confidence += 30
            if 'id="comparison-table"' in html:
                confidence += 20
            if 'comparison' in html and 'container' in html:
                confidence += 25
            if 'out of' in html:
                confidence += 25
            
            return min(confidence, 100.0)
            
        except Exception as e:
            print(f"Failed to calculate extraction confidence: {e}")
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
            print(f"Failed to calculate summary quality score: {e}")
            return 0.0
    
    def get_extraction_statistics(self) -> dict:
        """Get statistics about the extraction process."""
        return {
            "parser_type": "Standalone Head-to-Head Comparison Parser",
            "supported_sections": self.known_sections,
            "feature_categories": self.feature_categories,
            "summary_patterns": list(self.summary_patterns.keys()),
            "extraction_methods": [
                "HTML text parsing",
                "AI summary extraction",
                "fallback text extraction"
            ]
        }


def test_standalone_parser():
    """Test the standalone parser with sample data."""
    print("🧪 Testing Standalone Parser")
    print("=" * 50)
    
    # Create parser
    parser = StandaloneHeadToHeadParser()
    print(f"✅ Parser created: {type(parser).__name__}")
    print(f"   - Known sections: {len(parser.known_sections)}")
    print(f"   - Feature categories: {len(parser.feature_categories)}")
    
    # Test HTML
    test_html = """
    <html>
    <body>
        <div class="comparison-container-v2_header">Microsoft Power BI</div>
        <div class="comparison-container-v2_header">Tableau</div>
        <div aria-label="Comparison Summary" class="compare-container-v2_summary">
            <div>AI Generated Summary</div>
            <ul>
                <li>Microsoft Power BI excels in data visualization, scoring 9.2 compared to Tableau's 8.7.</li>
                <li>Tableau has better ease of setup with 8.5 vs Power BI's 7.8.</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    # Parse
    try:
        result = parser.parse_head_to_head_comparison(test_html, "https://example.com/test")
        print(f"✅ Parsing successful: {type(result).__name__}")
        print(f"   - Products: {result.product_a.get('name', 'Unknown')} vs {result.product_b.get('name', 'Unknown')}")
        print(f"   - AI Summary Quality: {result.summary_quality_score:.1f}")
        print(f"   - Data Quality: {result.data_quality_score:.1f}")
        print(f"   - Summary Points: {len(result.ai_generated_summary.get('summary_points', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 STANDALONE PARSER TEST")
    print("=" * 60)
    
    success = test_standalone_parser()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PARSER TEST SUCCESSFUL!")
        print("   Next: Integrate with scraping system")
    else:
        print("💥 PARSER TEST FAILED!")
        print("   Next: Debug and fix issues")
    
    print("=" * 60)
