"""Specialized scraper for G2 head-to-head comparison pages with focus on AI-generated summaries."""

import asyncio
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
from dataclasses import asdict

from playwright.async_api import Page
from loguru import logger

from .competitive_intelligence_scraper import CompetitiveIntelligenceScraper, CompetitiveTarget, CompetitiveInsight
from ..parsers.head_to_head_comparison import G2HeadToHeadComparisonParser, HeadToHeadComparisonData


class HeadToHeadComparisonScraper:
    """Specialized scraper for G2 head-to-head comparison pages with AI summary focus."""
    
    def __init__(self, competitive_scraper: CompetitiveIntelligenceScraper):
        self.competitive_scraper = competitive_scraper
        self.parser = G2HeadToHeadComparisonParser()
        self.scraping_stats = {
            "total_comparisons": 0,
            "successful_comparisons": 0,
            "failed_comparisons": 0,
            "total_products_analyzed": 0,
            "ai_summaries_extracted": 0,
            "start_time": None
        }
        
        logger.info("Head-to-Head Comparison Scraper initialized with AI summary focus")
    
    async def scrape_all_head_to_head_comparisons(self, targets: List[CompetitiveTarget]) -> List[CompetitiveInsight]:
        """Scrape all head-to-head comparisons from the provided targets."""
        try:
            self.scraping_stats["start_time"] = datetime.now()
            all_insights = []
            
            # Collect all head-to-head comparison URLs
            head_to_head_urls = self._collect_head_to_head_urls(targets)
            self.scraping_stats["total_comparisons"] = len(head_to_head_urls)
            
            logger.info(f"Found {len(head_to_head_urls)} head-to-head comparison URLs to scrape")
            
            # Scrape each comparison
            for url_data in head_to_head_urls:
                try:
                    insight = await self._scrape_single_head_to_head_comparison(url_data)
                    if insight:
                        all_insights.append(insight)
                        self.scraping_stats["successful_comparisons"] += 1
                        self.scraping_stats["total_products_analyzed"] += 2  # Always 2 products in head-to-head
                        
                        # Track AI summary extraction
                        if insight.content.get("ai_generated_summary", {}).get("summary_points"):
                            self.scraping_stats["ai_summaries_extracted"] += 1
                        
                        logger.info(f"Successfully scraped head-to-head comparison: {url_data['url']}")
                    
                    # Anti-detection delay
                    delay = random.uniform(5.0, 12.0)
                    logger.info(f"Anti-detection delay: {delay:.2f}s")
                    await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Failed to scrape head-to-head comparison {url_data['url']}: {e}")
                    self.scraping_stats["failed_comparisons"] += 1
                    continue
            
            logger.info(f"Head-to-head comparison scraping completed. Success: {self.scraping_stats['successful_comparisons']}/{self.scraping_stats['total_comparisons']}")
            logger.info(f"AI summaries extracted: {self.scraping_stats['ai_summaries_extracted']}")
            
            return all_insights
            
        except Exception as e:
            logger.error(f"Error in head-to-head comparison scraping: {e}")
            raise
    
    def _collect_head_to_head_urls(self, targets: List[CompetitiveTarget]) -> List[Dict[str, Any]]:
        """Collect all head-to-head comparison URLs from targets."""
        head_to_head_urls = []
        
        for target in targets:
            if "head_to_head" in target.targets:
                for url in target.targets["head_to_head"]:
                    head_to_head_urls.append({
                        "url": url,
                        "competitor_id": target.competitor_id,
                        "competitor_name": target.name,
                        "platform": target.platform,
                        "category": target.category
                    })
        
        # Remove duplicates while preserving order
        seen_urls = set()
        unique_urls = []
        for url_data in head_to_head_urls:
            if url_data["url"] not in seen_urls:
                seen_urls.add(url_data["url"])
                unique_urls.append(url_data)
        
        logger.info(f"Collected {len(unique_urls)} unique head-to-head comparison URLs")
        return unique_urls
    
    async def _scrape_single_head_to_head_comparison(self, url_data: Dict[str, Any]) -> Optional[CompetitiveInsight]:
        """Scrape a single head-to-head comparison page."""
        try:
            url = url_data["url"]
            
            # Navigate to the comparison page
            await self.competitive_scraper._navigate_with_maximum_stealth(url)
            
            # Handle Cloudflare if needed
            if self.competitive_scraper.config.get("cloudflare_bypass", True):
                await self.competitive_scraper.cloudflare_bypass.wait_for_bypass(
                    self.competitive_scraper.page, 
                    url_data["platform"]
                )
            
            # Simulate competitive research behavior
            if self.competitive_scraper.config.get("human_behavior", True):
                await self.competitive_scraper._simulate_competitive_research_behavior()
            
            # Extract content
            html_content = await self.competitive_scraper._extract_content_robustly()
            
            # Parse the head-to-head comparison
            comparison_data = await self.parser.parse_head_to_head_comparison(html_content, url)
            
            # Create competitive insight
            insight = await self._create_head_to_head_insight(url_data, comparison_data)
            
            return insight
            
        except Exception as e:
            logger.error(f"Failed to scrape head-to-head comparison {url_data['url']}: {e}")
            return None
    
    async def _create_head_to_head_insight(self, url_data: Dict[str, Any], 
                                         comparison_data: HeadToHeadComparisonData) -> CompetitiveInsight:
        """Create a competitive insight from head-to-head comparison data."""
        try:
            # Extract competitive mentions from product names
            competitive_mentions = []
            if comparison_data.product_a.get("name"):
                competitive_mentions.append(comparison_data.product_a["name"])
            if comparison_data.product_b.get("name"):
                competitive_mentions.append(comparison_data.product_b["name"])
            
            # Generate market insights
            market_insights = await self._generate_head_to_head_market_insights(comparison_data)
            
            # Create the insight
            insight = CompetitiveInsight(
                competitor_id=url_data["competitor_id"],
                platform=url_data["platform"],
                extraction_date=datetime.now(),
                data_type="head_to_head_comparison",
                url=url_data["url"],
                content=asdict(comparison_data),
                sentiment_analysis={
                    "score": 0.0,  # Head-to-head comparisons don't have sentiment
                    "label": "neutral",
                    "details": {"type": "comparison_data", "products_compared": 2}
                },
                competitive_mentions=competitive_mentions,
                market_insights=market_insights,
                quality_score=comparison_data.data_quality_score / 100.0,  # Normalize to 0-1
                extraction_confidence=comparison_data.extraction_confidence / 100.0  # Normalize to 0-1
            )
            
            return insight
            
        except Exception as e:
            logger.error(f"Failed to create head-to-head insight: {e}")
            raise
    
    async def _generate_head_to_head_market_insights(self, comparison_data: HeadToHeadComparisonData) -> Dict[str, Any]:
        """Generate market insights from head-to-head comparison data."""
        try:
            insights = {
                "competitive_positioning": {},
                "market_trends": [],
                "feature_analysis": {},
                "pricing_analysis": {},
                "ai_summary_insights": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Analyze competitive positioning
            if comparison_data.product_a and comparison_data.product_b:
                insights["competitive_positioning"] = self._analyze_head_to_head_competitive_positioning(comparison_data)
            
            # Analyze market trends
            insights["market_trends"] = self._analyze_head_to_head_market_trends(comparison_data)
            
            # Analyze features
            insights["feature_analysis"] = self._analyze_head_to_head_feature_competitiveness(comparison_data)
            
            # Analyze pricing
            insights["pricing_analysis"] = self._analyze_head_to_head_pricing_competitiveness(comparison_data)
            
            # Analyze AI summary insights (most valuable)
            insights["ai_summary_insights"] = self._analyze_ai_summary_insights(comparison_data)
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate head-to-head market insights: {e}")
            return {}
    
    def _analyze_head_to_head_competitive_positioning(self, comparison_data: HeadToHeadComparisonData) -> Dict[str, Any]:
        """Analyze competitive positioning from head-to-head comparison data."""
        try:
            positioning = {
                "product_a_advantages": [],
                "product_b_advantages": [],
                "competitive_balance": "balanced",
                "pricing_positioning": {},
                "feature_positioning": {}
            }
            
            # Analyze star ratings and review counts
            if comparison_data.at_a_glance and comparison_data.at_a_glance.get("star_ratings"):
                star_ratings = comparison_data.at_a_glance["star_ratings"]
                
                product_a_name = comparison_data.product_a.get("name", "Product A")
                product_b_name = comparison_data.product_b.get("name", "Product B")
                
                product_a_rating = star_ratings.get(product_a_name, {}).get("rating", 0)
                product_b_rating = star_ratings.get(product_b_name, {}).get("rating", 0)
                
                if product_a_rating > product_b_rating:
                    positioning["competitive_balance"] = f"{product_a_name} advantage"
                elif product_b_rating > product_a_rating:
                    positioning["competitive_balance"] = f"{product_b_name} advantage"
                else:
                    positioning["competitive_balance"] = "balanced"
            
            # Analyze pricing positioning
            if comparison_data.at_a_glance and comparison_data.at_a_glance.get("entry_level_pricing"):
                pricing_data = comparison_data.at_a_glance["entry_level_pricing"]
                
                for product_name, pricing in pricing_data.items():
                    if pricing == "Free":
                        positioning["pricing_positioning"][product_name] = "aggressive"
                    elif pricing.startswith("$") and float(pricing.replace("$", "").replace(",", "")) < 50:
                        positioning["pricing_positioning"][product_name] = "competitive"
                    else:
                        positioning["pricing_positioning"][product_name] = "premium"
            
            return positioning
            
        except Exception as e:
            logger.warning(f"Failed to analyze head-to-head competitive positioning: {e}")
            return {}
    
    def _analyze_head_to_head_market_trends(self, comparison_data: HeadToHeadComparisonData) -> List[str]:
        """Analyze market trends from head-to-head comparison data."""
        try:
            trends = []
            
            # Analyze market segments
            if comparison_data.at_a_glance and comparison_data.at_a_glance.get("market_segments"):
                market_segments = comparison_data.at_a_glance["market_segments"]
                
                enterprise_focus = 0
                mid_market_focus = 0
                
                for product_name, segments in market_segments.items():
                    if segments.get("enterprise", 0) > 50:
                        enterprise_focus += 1
                    if segments.get("mid_market", 0) > 30:
                        mid_market_focus += 1
                
                if enterprise_focus >= 1:
                    trends.append("At least one product heavily focused on enterprise customers")
                if mid_market_focus >= 1:
                    trends.append("At least one product showing mid-market adoption")
            
            # Analyze AI summary insights for trends
            if comparison_data.ai_generated_summary and comparison_data.ai_generated_summary.get("structured_insights"):
                structured_insights = comparison_data.ai_generated_summary["structured_insights"]
                
                if structured_insights.get("competitive_advantages"):
                    trends.append("Clear competitive advantages identified in AI summary")
                if structured_insights.get("competitive_disadvantages"):
                    trends.append("Competitive disadvantages identified in AI summary")
                if structured_insights.get("feature_comparisons"):
                    trends.append("Feature-by-feature comparison available in AI summary")
            
            return trends
            
        except Exception as e:
            logger.warning(f"Failed to analyze head-to-head market trends: {e}")
            return []
    
    def _analyze_head_to_head_feature_competitiveness(self, comparison_data: HeadToHeadComparisonData) -> Dict[str, Any]:
        """Analyze feature competitiveness from head-to-head comparison data."""
        try:
            feature_analysis = {
                "strength_areas": {},
                "weakness_areas": {},
                "competitive_advantages": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Analyze AI summary for feature insights
            if comparison_data.ai_generated_summary and comparison_data.ai_generated_summary.get("structured_insights"):
                structured_insights = comparison_data.ai_generated_summary["structured_insights"]
                
                # Extract feature comparisons from AI summary
                if structured_insights.get("feature_comparisons"):
                    for feature_category, points in structured_insights["feature_comparisons"].items():
                        if points:
                            # Find the best point for this feature category
                            best_point = max(points, key=lambda x: x.get("confidence", 0))
                            
                            if best_point.get("insight_type") == "competitive_advantage":
                                feature_analysis["strength_areas"][feature_category] = {
                                    "insight": best_point.get("text", ""),
                                    "confidence": best_point.get("confidence", 0)
                                }
                            elif best_point.get("insight_type") == "competitive_disadvantage":
                                feature_analysis["weakness_areas"][feature_category] = {
                                    "insight": best_point.get("text", ""),
                                    "confidence": best_point.get("confidence", 0)
                                }
            
            return feature_analysis
            
        except Exception as e:
            logger.warning(f"Failed to analyze head-to-head feature competitiveness: {e}")
            return {}
    
    def _analyze_head_to_head_pricing_competitiveness(self, comparison_data: HeadToHeadComparisonData) -> Dict[str, Any]:
        """Analyze pricing competitiveness from head-to-head comparison data."""
        try:
            pricing_analysis = {
                "pricing_tiers": {},
                "competitive_pricing": {},
                "pricing_strategies": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            if comparison_data.at_a_glance and comparison_data.at_a_glance.get("entry_level_pricing"):
                pricing_data = comparison_data.at_a_glance["entry_level_pricing"]
                
                # Categorize pricing strategies
                for product_name, pricing in pricing_data.items():
                    if pricing == "Free":
                        pricing_analysis["pricing_strategies"][product_name] = "freemium"
                        pricing_analysis["competitive_pricing"][product_name] = "most_competitive"
                    elif pricing.startswith("$"):
                        try:
                            price_value = float(pricing.replace("$", "").replace(",", ""))
                            if price_value <= 30:
                                pricing_analysis["pricing_strategies"][product_name] = "low_cost"
                                pricing_analysis["competitive_pricing"][product_name] = "competitive"
                            elif price_value <= 70:
                                pricing_analysis["pricing_strategies"][product_name] = "mid_tier"
                                pricing_analysis["competitive_pricing"][product_name] = "moderate"
                            else:
                                pricing_analysis["pricing_strategies"][product_name] = "premium"
                                pricing_analysis["competitive_pricing"][product_name] = "least_competitive"
                        except ValueError:
                            pricing_analysis["pricing_strategies"][product_name] = "unknown"
                            pricing_analysis["competitive_pricing"][product_name] = "unknown"
                    else:
                        pricing_analysis["pricing_strategies"][product_name] = "custom"
                        pricing_analysis["competitive_pricing"][product_name] = "unknown"
                
                # Identify pricing tiers
                free_products = [k for k, v in pricing_data.items() if v == "Free"]
                paid_products = [k for k, v in pricing_data.items() if v != "Free"]
                
                if free_products:
                    pricing_analysis["pricing_tiers"]["free_tier"] = free_products
                if paid_products:
                    pricing_analysis["pricing_tiers"]["paid_tier"] = paid_products
            
            return pricing_analysis
            
        except Exception as e:
            logger.warning(f"Failed to analyze head-to-head pricing competitiveness: {e}")
            return {}
    
    def _analyze_ai_summary_insights(self, comparison_data: HeadToHeadComparisonData) -> Dict[str, Any]:
        """Analyze AI summary insights - the most valuable competitive intelligence."""
        try:
            ai_insights = {
                "summary_quality": comparison_data.summary_quality_score,
                "extraction_confidence": comparison_data.ai_generated_summary.get("extraction_confidence", 0),
                "summary_points_count": len(comparison_data.ai_generated_summary.get("summary_points", [])),
                "structured_insights": comparison_data.ai_generated_summary.get("structured_insights", {}),
                "competitive_intelligence_score": 0.0,
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Calculate competitive intelligence score
            if comparison_data.ai_generated_summary.get("summary_points"):
                points = comparison_data.ai_generated_summary["summary_points"]
                
                # Score based on data quality
                score = 0.0
                max_score = 100.0
                
                # Score extraction quality
                score += (comparison_data.summary_quality_score / 100.0) * 40
                
                # Score structured insights
                structured_insights = comparison_data.ai_generated_summary.get("structured_insights", {})
                if structured_insights.get("competitive_advantages"):
                    score += 20
                if structured_insights.get("competitive_disadvantages"):
                    score += 20
                if structured_insights.get("feature_comparisons"):
                    score += 20
                
                ai_insights["competitive_intelligence_score"] = min(score, max_score)
            
            return ai_insights
            
        except Exception as e:
            logger.warning(f"Failed to analyze AI summary insights: {e}")
            return {}
    
    async def export_head_to_head_data(self, insights: List[CompetitiveInsight], 
                                     export_dir: str = "output") -> Dict[str, str]:
        """Export head-to-head comparison data to various formats."""
        try:
            # Ensure export directory exists
            Path(export_dir).mkdir(parents=True, exist_ok=True)
            
            export_files = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export as JSON
            json_file = f"{export_dir}/head_to_head_comparisons_{timestamp}.json"
            with open(json_file, 'w') as f:
                json.dump([asdict(insight) for insight in insights], f, indent=2, default=str)
            export_files["json"] = json_file
            
            # Export summary report
            summary_file = f"{export_dir}/head_to_head_summary_{timestamp}.json"
            summary = self._create_summary_report(insights)
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            export_files["summary"] = summary_file
            
            # Export AI summary insights (most valuable)
            ai_summary_file = f"{export_dir}/ai_summary_insights_{timestamp}.json"
            ai_summary_insights = self._extract_ai_summary_insights(insights)
            with open(ai_summary_file, 'w') as f:
                json.dump(ai_summary_insights, f, indent=2, default=str)
            export_files["ai_summary"] = ai_summary_file
            
            # Export statistics
            stats_file = f"{export_dir}/head_to_head_stats_{timestamp}.json"
            with open(stats_file, 'w') as f:
                json.dump(self.scraping_stats, f, indent=2, default=str)
            export_files["stats"] = stats_file
            
            logger.info(f"Head-to-head comparison data exported to {export_dir}")
            return export_files
            
        except Exception as e:
            logger.error(f"Failed to export head-to-head comparison data: {e}")
            return {}
    
    def _extract_ai_summary_insights(self, insights: List[CompetitiveInsight]) -> Dict[str, Any]:
        """Extract and consolidate AI summary insights from all comparisons."""
        try:
            ai_summary_insights = {
                "extraction_metadata": {
                    "total_comparisons": len(insights),
                    "extraction_date": datetime.now().isoformat(),
                    "total_ai_summaries": 0,
                    "average_summary_quality": 0.0
                },
                "competitive_insights": [],
                "feature_analysis": {},
                "sentiment_analysis": {"positive": 0, "negative": 0, "neutral": 0},
                "score_comparisons": []
            }
            
            total_quality = 0.0
            ai_summary_count = 0
            
            for insight in insights:
                if insight.content.get("ai_generated_summary", {}).get("summary_points"):
                    ai_summary_count += 1
                    
                    # Extract AI summary data
                    ai_summary = insight.content["ai_generated_summary"]
                    quality_score = insight.content.get("summary_quality_score", 0)
                    total_quality += quality_score
                    
                    # Add competitive insights
                    if ai_summary.get("structured_insights"):
                        structured_insights = ai_summary["structured_insights"]
                        
                        # Competitive advantages/disadvantages
                        if structured_insights.get("competitive_advantages"):
                            for advantage in structured_insights["competitive_advantages"]:
                                ai_summary_insights["competitive_insights"].append({
                                    "type": "advantage",
                                    "insight": advantage.get("text", ""),
                                    "feature_category": advantage.get("feature_category", ""),
                                    "confidence": advantage.get("confidence", 0),
                                    "comparison_url": insight.url
                                })
                        
                        if structured_insights.get("competitive_disadvantages"):
                            for disadvantage in structured_insights["competitive_disadvantages"]:
                                ai_summary_insights["competitive_insights"].append({
                                    "type": "disadvantage",
                                    "insight": disadvantage.get("text", ""),
                                    "feature_category": disadvantage.get("feature_category", ""),
                                    "confidence": disadvantage.get("confidence", 0),
                                    "comparison_url": insight.url
                                })
                        
                        # Feature analysis
                        if structured_insights.get("feature_comparisons"):
                            for feature_category, points in structured_insights["feature_comparisons"].items():
                                if feature_category not in ai_summary_insights["feature_analysis"]:
                                    ai_summary_insights["feature_analysis"][feature_category] = []
                                
                                for point in points:
                                    ai_summary_insights["feature_analysis"][feature_category].append({
                                        "insight": point.get("text", ""),
                                        "insight_type": point.get("insight_type", ""),
                                        "sentiment": point.get("sentiment", ""),
                                        "confidence": point.get("confidence", 0),
                                        "comparison_url": insight.url
                                    })
                        
                        # Sentiment analysis
                        if structured_insights.get("sentiment_analysis"):
                            sentiment_data = structured_insights["sentiment_analysis"]
                            for sentiment, count in sentiment_data.items():
                                ai_summary_insights["sentiment_analysis"][sentiment] += count
                        
                        # Score comparisons
                        if structured_insights.get("score_insights"):
                            for score_insight in structured_insights["score_insights"]:
                                ai_summary_insights["score_comparisons"].append({
                                    "feature": score_insight.get("feature", ""),
                                    "product_a_score": score_insight.get("product_a_score", 0),
                                    "product_b_score": score_insight.get("product_b_score", 0),
                                    "difference": score_insight.get("difference", 0),
                                    "comparison_url": insight.url
                                })
            
            # Calculate averages
            if ai_summary_count > 0:
                ai_summary_insights["extraction_metadata"]["total_ai_summaries"] = ai_summary_count
                ai_summary_insights["extraction_metadata"]["average_summary_quality"] = total_quality / ai_summary_count
            
            return ai_summary_insights
            
        except Exception as e:
            logger.error(f"Failed to extract AI summary insights: {e}")
            return {}
    
    def _create_summary_report(self, insights: List[CompetitiveInsight]) -> Dict[str, Any]:
        """Create a summary report of all head-to-head comparisons."""
        try:
            summary = {
                "report_metadata": {
                    "generation_date": datetime.now().isoformat(),
                    "total_comparisons": len(insights),
                    "total_products_analyzed": sum(2 for _ in insights),  # Always 2 products per comparison
                    "scraping_duration": (
                        datetime.now() - self.scraping_stats["start_time"]
                    ).total_seconds() if self.scraping_stats["start_time"] else 0
                },
                "comparison_overview": [],
                "product_analysis": {},
                "ai_summary_analysis": {
                    "total_summaries": 0,
                    "average_quality": 0.0,
                    "quality_distribution": {"high": 0, "medium": 0, "low": 0}
                },
                "data_quality_summary": {
                    "average_quality_score": 0.0,
                    "average_extraction_confidence": 0.0,
                    "quality_distribution": {"high": 0, "medium": 0, "low": 0}
                }
            }
            
            # Analyze each comparison
            all_products = set()
            quality_scores = []
            confidence_scores = []
            ai_summary_qualities = []
            
            for insight in insights:
                comparison_data = insight.content
                
                # Add comparison overview
                summary["comparison_overview"].append({
                    "comparison_id": comparison_data.get("comparison_id"),
                    "url": insight.url,
                    "products": [
                        comparison_data.get("product_a", {}).get("name", "Unknown"),
                        comparison_data.get("product_b", {}).get("name", "Unknown")
                    ],
                    "data_quality_score": comparison_data.get("data_quality_score", 0),
                    "extraction_confidence": comparison_data.get("extraction_confidence", 0),
                    "summary_quality_score": comparison_data.get("summary_quality_score", 0)
                })
                
                # Collect product information
                for product_key in ["product_a", "product_b"]:
                    product = comparison_data.get(product_key, {})
                    product_name = product.get("name")
                    if product_name:
                        all_products.add(product_name)
                        
                        if product_name not in summary["product_analysis"]:
                            summary["product_analysis"][product_name] = {
                                "appearances": 0,
                                "average_rating": 0.0,
                                "total_reviews": 0,
                                "pricing_strategies": set()
                            }
                        
                        product_analysis = summary["product_analysis"][product_name]
                        product_analysis["appearances"] += 1
                        
                        if product.get("star_rating"):
                            product_analysis["average_rating"] += product["star_rating"]
                        if product.get("review_count"):
                            product_analysis["total_reviews"] += product["review_count"]
                        if product.get("entry_level_pricing"):
                            product_analysis["pricing_strategies"].add(product["entry_level_pricing"])
                
                # Collect quality metrics
                if comparison_data.get("data_quality_score"):
                    quality_scores.append(comparison_data["data_quality_score"])
                if comparison_data.get("extraction_confidence"):
                    confidence_scores.append(comparison_data["extraction_confidence"])
                if comparison_data.get("summary_quality_score"):
                    ai_summary_qualities.append(comparison_data["summary_quality_score"])
            
            # Calculate averages and distributions
            if quality_scores:
                summary["data_quality_summary"]["average_quality_score"] = sum(quality_scores) / len(quality_scores)
                
                for score in quality_scores:
                    if score >= 80:
                        summary["data_quality_summary"]["quality_distribution"]["high"] += 1
                    elif score >= 60:
                        summary["data_quality_summary"]["quality_distribution"]["medium"] += 1
                    else:
                        summary["data_quality_summary"]["quality_distribution"]["low"] += 1
            
            if confidence_scores:
                summary["data_quality_summary"]["average_extraction_confidence"] = sum(confidence_scores) / len(confidence_scores)
            
            if ai_summary_qualities:
                summary["ai_summary_analysis"]["total_summaries"] = len(ai_summary_qualities)
                summary["ai_summary_analysis"]["average_quality"] = sum(ai_summary_qualities) / len(ai_summary_qualities)
                
                for score in ai_summary_qualities:
                    if score >= 80:
                        summary["ai_summary_analysis"]["quality_distribution"]["high"] += 1
                    elif score >= 60:
                        summary["ai_summary_analysis"]["quality_distribution"]["medium"] += 1
                    else:
                        summary["ai_summary_analysis"]["quality_distribution"]["low"] += 1
            
            # Convert sets to lists for JSON serialization
            for product_analysis in summary["product_analysis"].values():
                product_analysis["pricing_strategies"] = list(product_analysis["pricing_strategies"])
                
                # Calculate averages
                if product_analysis["appearances"] > 0:
                    product_analysis["average_rating"] /= product_analysis["appearances"]
            
            summary["total_unique_products"] = len(all_products)
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to create summary report: {e}")
            return {}
    
    def get_scraping_summary(self) -> Dict[str, Any]:
        """Get summary of head-to-head comparison scraping."""
        return {
            "scraping_stats": self.scraping_stats,
            "parser_capabilities": self.parser.get_extraction_statistics(),
            "success_rate": (
                self.scraping_stats["successful_comparisons"] / 
                max(1, self.scraping_stats["total_comparisons"])
            ) * 100,
            "ai_summary_extraction_rate": (
                self.scraping_stats["ai_summaries_extracted"] / 
                max(1, self.scraping_stats["successful_comparisons"])
            ) * 100,
            "uptime_seconds": (
                datetime.now() - self.scraping_stats["start_time"]
            ).total_seconds() if self.scraping_stats["start_time"] else 0
        }
