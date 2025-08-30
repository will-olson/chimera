"""Specialized scraper for G2 four-way comparison pages with comprehensive data capture."""

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
from ..parsers.four_way_comparison import G2FourWayComparisonParser, FourWayComparisonData


class FourWayComparisonScraper:
    """Specialized scraper for G2 four-way comparison pages."""
    
    def __init__(self, competitive_scraper: CompetitiveIntelligenceScraper):
        self.competitive_scraper = competitive_scraper
        self.parser = G2FourWayComparisonParser()
        self.scraping_stats = {
            "total_comparisons": 0,
            "successful_comparisons": 0,
            "failed_comparisons": 0,
            "total_products_analyzed": 0,
            "start_time": None
        }
        
        logger.info("Four-Way Comparison Scraper initialized")
    
    async def scrape_all_four_way_comparisons(self, targets: List[CompetitiveTarget]) -> List[CompetitiveInsight]:
        """Scrape all four-way comparisons from the provided targets."""
        try:
            self.scraping_stats["start_time"] = datetime.now()
            all_insights = []
            
            # Collect all four-way comparison URLs
            four_way_urls = self._collect_four_way_urls(targets)
            self.scraping_stats["total_comparisons"] = len(four_way_urls)
            
            logger.info(f"Found {len(four_way_urls)} four-way comparison URLs to scrape")
            
            # Scrape each comparison
            for url_data in four_way_urls:
                try:
                    insight = await self._scrape_single_four_way_comparison(url_data)
                    if insight:
                        all_insights.append(insight)
                        self.scraping_stats["successful_comparisons"] += 1
                        self.scraping_stats["total_products_analyzed"] += insight.content.get("total_products", 0)
                        
                        logger.info(f"Successfully scraped four-way comparison: {url_data['url']}")
                    
                    # Anti-detection delay
                    delay = random.uniform(8.0, 15.0)
                    logger.info(f"Anti-detection delay: {delay:.2f}s")
                    await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Failed to scrape four-way comparison {url_data['url']}: {e}")
                    self.scraping_stats["failed_comparisons"] += 1
                    continue
            
            logger.info(f"Four-way comparison scraping completed. Success: {self.scraping_stats['successful_comparisons']}/{self.scraping_stats['total_comparisons']}")
            
            return all_insights
            
        except Exception as e:
            logger.error(f"Error in four-way comparison scraping: {e}")
            raise
    
    def _collect_four_way_urls(self, targets: List[CompetitiveTarget]) -> List[Dict[str, Any]]:
        """Collect all four-way comparison URLs from targets."""
        four_way_urls = []
        
        for target in targets:
            if "four_way" in target.targets:
                for url in target.targets["four_way"]:
                    four_way_urls.append({
                        "url": url,
                        "competitor_id": target.competitor_id,
                        "competitor_name": target.name,
                        "platform": target.platform,
                        "category": target.category
                    })
        
        # Remove duplicates while preserving order
        seen_urls = set()
        unique_urls = []
        for url_data in four_way_urls:
            if url_data["url"] not in seen_urls:
                seen_urls.add(url_data["url"])
                unique_urls.append(url_data)
        
        logger.info(f"Collected {len(unique_urls)} unique four-way comparison URLs")
        return unique_urls
    
    async def _scrape_single_four_way_comparison(self, url_data: Dict[str, Any]) -> Optional[CompetitiveInsight]:
        """Scrape a single four-way comparison page."""
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
            
            # Parse the four-way comparison
            comparison_data = await self.parser.parse_four_way_comparison(html_content, url)
            
            # Create competitive insight
            insight = await self._create_four_way_insight(url_data, comparison_data)
            
            return insight
            
        except Exception as e:
            logger.error(f"Failed to scrape four-way comparison {url_data['url']}: {e}")
            return None
    
    async def _create_four_way_insight(self, url_data: Dict[str, Any], 
                                     comparison_data: FourWayComparisonData) -> CompetitiveInsight:
        """Create a competitive insight from four-way comparison data."""
        try:
            # Extract competitive mentions from product names
            competitive_mentions = []
            for product in comparison_data.products:
                if product.get("name"):
                    competitive_mentions.append(product["name"])
            
            # Generate market insights
            market_insights = await self._generate_four_way_market_insights(comparison_data)
            
            # Create the insight
            insight = CompetitiveInsight(
                competitor_id=url_data["competitor_id"],
                platform=url_data["platform"],
                extraction_date=datetime.now(),
                data_type="four_way_comparison",
                url=url_data["url"],
                content=asdict(comparison_data),
                sentiment_analysis={
                    "score": 0.0,  # Four-way comparisons don't have sentiment
                    "label": "neutral",
                    "details": {"type": "comparison_data", "products_compared": len(comparison_data.products)}
                },
                competitive_mentions=competitive_mentions,
                market_insights=market_insights,
                quality_score=comparison_data.data_quality_score / 100.0,  # Normalize to 0-1
                extraction_confidence=comparison_data.extraction_confidence / 100.0  # Normalize to 0-1
            )
            
            return insight
            
        except Exception as e:
            logger.error(f"Failed to create four-way insight: {e}")
            raise
    
    async def _generate_four_way_market_insights(self, comparison_data: FourWayComparisonData) -> Dict[str, Any]:
        """Generate market insights from four-way comparison data."""
        try:
            insights = {
                "competitive_positioning": {},
                "market_trends": [],
                "feature_analysis": {},
                "pricing_analysis": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            # Analyze competitive positioning
            if comparison_data.products:
                insights["competitive_positioning"] = self._analyze_competitive_positioning(comparison_data)
            
            # Analyze market trends
            insights["market_trends"] = self._analyze_market_trends(comparison_data)
            
            # Analyze features
            insights["feature_analysis"] = self._analyze_feature_competitiveness(comparison_data)
            
            # Analyze pricing
            insights["pricing_analysis"] = self._analyze_pricing_competitiveness(comparison_data)
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate four-way market insights: {e}")
            return {}
    
    def _analyze_competitive_positioning(self, comparison_data: FourWayComparisonData) -> Dict[str, Any]:
        """Analyze competitive positioning from comparison data."""
        try:
            positioning = {
                "market_leaders": [],
                "emerging_players": [],
                "pricing_positioning": {},
                "feature_positioning": {}
            }
            
            # Analyze star ratings and review counts
            if comparison_data.at_a_glance and comparison_data.at_a_glance.get("star_ratings"):
                star_ratings = comparison_data.at_a_glance["star_ratings"]
                
                # Find market leaders (highest ratings with significant review counts)
                sorted_products = sorted(
                    star_ratings.items(),
                    key=lambda x: (x[1]["rating"], x[1]["review_count"]),
                    reverse=True
                )
                
                if sorted_products:
                    # Top 2 products with high ratings are market leaders
                    for product_name, data in sorted_products[:2]:
                        if data["rating"] >= 4.0 and data["review_count"] >= 1000:
                            positioning["market_leaders"].append({
                                "name": product_name,
                                "rating": data["rating"],
                                "review_count": data["review_count"]
                            })
                    
                    # Products with lower ratings or fewer reviews are emerging
                    for product_name, data in sorted_products[2:]:
                        if data["rating"] < 4.0 or data["review_count"] < 500:
                            positioning["emerging_players"].append({
                                "name": product_name,
                                "rating": data["rating"],
                                "review_count": data["review_count"]
                            })
            
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
            logger.warning(f"Failed to analyze competitive positioning: {e}")
            return {}
    
    def _analyze_market_trends(self, comparison_data: FourWayComparisonData) -> List[str]:
        """Analyze market trends from comparison data."""
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
                
                if enterprise_focus >= 3:
                    trends.append("Market heavily focused on enterprise customers")
                if mid_market_focus >= 2:
                    trends.append("Growing mid-market adoption")
            
            # Analyze feature categories
            if comparison_data.features_by_category and comparison_data.features_by_category.get("category_ratings"):
                category_ratings = comparison_data.features_by_category["category_ratings"]
                
                # Check for emerging feature categories
                emerging_categories = []
                for category, ratings in category_ratings.items():
                    if "Not enough data" in ratings.values():
                        emerging_categories.append(category)
                
                if emerging_categories:
                    trends.append(f"Emerging feature categories: {', '.join(emerging_categories)}")
            
            return trends
            
        except Exception as e:
            logger.warning(f"Failed to analyze market trends: {e}")
            return []
    
    def _analyze_feature_competitiveness(self, comparison_data: FourWayComparisonData) -> Dict[str, Any]:
        """Analyze feature competitiveness from comparison data."""
        try:
            feature_analysis = {
                "strength_areas": {},
                "weakness_areas": {},
                "competitive_advantages": {},
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            if comparison_data.features_by_category and comparison_data.features_by_category.get("category_ratings"):
                category_ratings = comparison_data.features_by_category["category_ratings"]
                
                for category, ratings in category_ratings.items():
                    # Find products with highest ratings in each category
                    valid_ratings = {k: v for k, v in ratings.items() if isinstance(v, (int, float)) and v > 0}
                    
                    if valid_ratings:
                        max_rating = max(valid_ratings.values())
                        max_rating_products = [k for k, v in valid_ratings.items() if v == max_rating]
                        
                        if max_rating >= 8.5:
                            feature_analysis["strength_areas"][category] = {
                                "rating": max_rating,
                                "leading_products": max_rating_products
                            }
                        elif max_rating <= 7.0:
                            feature_analysis["weakness_areas"][category] = {
                                "rating": max_rating,
                                "products": list(valid_ratings.keys())
                            }
                        
                        # Identify competitive advantages
                        for product_name, rating in valid_ratings.items():
                            if rating >= 8.0:
                                if product_name not in feature_analysis["competitive_advantages"]:
                                    feature_analysis["competitive_advantages"][product_name] = []
                                feature_analysis["competitive_advantages"][product_name].append({
                                    "category": category,
                                    "rating": rating
                                })
            
            return feature_analysis
            
        except Exception as e:
            logger.warning(f"Failed to analyze feature competitiveness: {e}")
            return {}
    
    def _analyze_pricing_competitiveness(self, comparison_data: FourWayComparisonData) -> Dict[str, Any]:
        """Analyze pricing competitiveness from comparison data."""
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
            logger.warning(f"Failed to analyze pricing competitiveness: {e}")
            return {}
    
    async def export_four_way_data(self, insights: List[CompetitiveInsight], 
                                 export_dir: str = "output") -> Dict[str, str]:
        """Export four-way comparison data to various formats."""
        try:
            # Ensure export directory exists
            Path(export_dir).mkdir(parents=True, exist_ok=True)
            
            export_files = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export as JSON
            json_file = f"{export_dir}/four_way_comparisons_{timestamp}.json"
            with open(json_file, 'w') as f:
                json.dump([asdict(insight) for insight in insights], f, indent=2, default=str)
            export_files["json"] = json_file
            
            # Export summary report
            summary_file = f"{export_dir}/four_way_summary_{timestamp}.json"
            summary = self._create_summary_report(insights)
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            export_files["summary"] = summary_file
            
            # Export statistics
            stats_file = f"{export_dir}/four_way_stats_{timestamp}.json"
            with open(stats_file, 'w') as f:
                json.dump(self.scraping_stats, f, indent=2, default=str)
            export_files["stats"] = stats_file
            
            logger.info(f"Four-way comparison data exported to {export_dir}")
            return export_files
            
        except Exception as e:
            logger.error(f"Failed to export four-way comparison data: {e}")
            return {}
    
    def _create_summary_report(self, insights: List[CompetitiveInsight]) -> Dict[str, Any]:
        """Create a summary report of all four-way comparisons."""
        try:
            summary = {
                "report_metadata": {
                    "generation_date": datetime.now().isoformat(),
                    "total_comparisons": len(insights),
                    "total_products_analyzed": sum(
                        insight.content.get("total_products", 0) for insight in insights
                    ),
                    "scraping_duration": (
                        datetime.now() - self.scraping_stats["start_time"]
                    ).total_seconds() if self.scraping_stats["start_time"] else 0
                },
                "comparison_overview": [],
                "product_analysis": {},
                "market_insights": {},
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
            
            for insight in insights:
                comparison_data = insight.content
                
                # Add comparison overview
                summary["comparison_overview"].append({
                    "comparison_id": comparison_data.get("comparison_id"),
                    "url": insight.url,
                    "products": [p["name"] for p in comparison_data.get("products", [])],
                    "total_products": comparison_data.get("total_products", 0),
                    "data_quality_score": comparison_data.get("data_quality_score", 0),
                    "extraction_confidence": comparison_data.get("extraction_confidence", 0)
                })
                
                # Collect product information
                for product in comparison_data.get("products", []):
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
        """Get summary of four-way comparison scraping."""
        return {
            "scraping_stats": self.scraping_stats,
            "parser_capabilities": self.parser.get_extraction_statistics(),
            "success_rate": (
                self.scraping_stats["successful_comparisons"] / 
                max(1, self.scraping_stats["total_comparisons"])
            ) * 100,
            "uptime_seconds": (
                datetime.now() - self.scraping_stats["start_time"]
            ).total_seconds() if self.scraping_stats["start_time"] else 0
        }
