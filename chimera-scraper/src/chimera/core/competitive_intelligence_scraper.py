"""Ultra-optimized competitive intelligence scraper for comprehensive market analysis."""

import asyncio
import time
import random
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from pathlib import Path
import json
import yaml
from dataclasses import dataclass, asdict
from collections import defaultdict

from playwright.async_api import async_playwright, BrowserContext, Page, Browser
from loguru import logger

from .fingerprint import AdvancedFingerprintManager
from .behavior import HumanBehaviorSimulator, BehaviorProfile
from .cloudflare import CloudflareBypass
from .session import ScrapingSession
from .retry import AdvancedRetryManager, RetryConfig, CircuitBreakerConfig
from ..targets.manager import TargetManager
from ..parsers.g2 import G2Parser
from ..parsers.capterra import CapterraParser
from ..analysis.sentiment import AdvancedSentimentAnalyzer
from ..monitoring.performance import PerformanceMonitor
from ..models.review import EnhancedReview, ReviewBatch
from ..utils.storage import DataStorage


@dataclass
class CompetitiveTarget:
    """Comprehensive competitive target definition."""
    competitor_id: str
    name: str
    platform: str
    category: str
    market_position: str
    primary_competitors: List[str]
    targets: Dict[str, Any]
    metadata: Dict[str, Any]
    priority: int = 1


@dataclass
class CompetitiveInsight:
    """Comprehensive competitive insight data."""
    competitor_id: str
    platform: str
    extraction_date: datetime
    data_type: str
    url: str
    content: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    competitive_mentions: List[str]
    market_insights: Dict[str, Any]
    quality_score: float
    extraction_confidence: float


class CompetitiveIntelligenceScraper:
    """Ultra-optimized scraper for comprehensive competitive intelligence."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.fingerprint_manager = AdvancedFingerprintManager()
        self.behavior_simulator = HumanBehaviorSimulator()
        self.cloudflare_bypass = CloudflareBypass()
        self.session_manager = ScrapingSession()
        self.target_manager = TargetManager()
        self.sentiment_analyzer = AdvancedSentimentAnalyzer()
        self.storage = DataStorage()
        
        # Advanced components
        self.retry_manager = AdvancedRetryManager(
            RetryConfig(max_attempts=5, base_delay=3.0, strategy="adaptive_backoff"),
            CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0)
        )
        
        self.performance_monitor = PerformanceMonitor({
            "monitor_interval": 3.0
        })
        
        # Competitive intelligence state
        self.competitive_targets: List[CompetitiveTarget] = []
        self.competitive_insights: List[CompetitiveInsight] = []
        self.market_analysis: Dict[str, Any] = {}
        
        # Browser management
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Scraping state
        self.is_initialized = False
        self.current_target = None
        self.scraping_stats = {
            "total_targets": 0,
            "completed_targets": 0,
            "failed_targets": 0,
            "total_insights": 0,
            "start_time": None
        }
        
        logger.info("Competitive Intelligence Scraper initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration with competitive intelligence focus."""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        # Default competitive intelligence configuration
        return {
            "scraping_profile": "stealth",
            "retry_attempts": 5,
            "base_delay": 3.0,
            "failure_threshold": 3,
            "recovery_timeout": 30.0,
            "monitor_interval": 3.0,
            "max_reviews_per_target": 50,  # Increased for comprehensive coverage
            "max_comparisons_per_target": 10,
            "max_alternatives_per_target": 20,
            "human_behavior": True,
            "cloudflare_bypass": True,
            "performance_monitoring": True,
            "competitive_analysis": True,
            "market_intelligence": True
        }
    
    async def initialize(self):
        """Initialize with competitive intelligence focus."""
        try:
            # Start performance monitoring
            if self.config.get("performance_monitoring", True):
                await self.performance_monitor.start_monitoring()
                logger.info("Performance monitoring started")
            
            # Initialize browser
            await self._initialize_browser()
            
            # Load competitive targets
            await self._load_competitive_targets()
            
            self.is_initialized = True
            self.scraping_stats["start_time"] = datetime.now()
            
            logger.info("Competitive Intelligence Scraper fully initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize scraper: {e}")
            raise
    
    async def _initialize_browser(self):
        """Initialize browser with maximum stealth for competitive intelligence."""
        try:
            playwright = await async_playwright().start()
            
            profile = self.config.get("scraping_profile", "stealth")
            
            self.browser = await playwright.chromium.launch(
                headless=self.config.get("headless", False),
                args=self.fingerprint_manager.get_chrome_args(profile)
            )
            
            self.context = await self.fingerprint_manager.create_stealth_browser_context(
                profile=profile
            )
            
            self.page = await self.context.new_page()
            
            await self._apply_maximum_stealth_measures()
            await self._setup_competitive_monitoring()
            
            logger.info("Browser initialized with maximum stealth for competitive intelligence")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise
    
    async def _apply_maximum_stealth_measures(self):
        """Apply maximum stealth measures for competitive intelligence scraping."""
        if not self.page:
            return
        
        try:
            # Inject advanced stealth scripts
            await self.fingerprint_manager._inject_stealth_scripts(self.page)
            
            # Set randomized viewport
            await self.page.set_viewport_size({
                "width": random.randint(1366, 1920),
                "height": random.randint(768, 1080)
            })
            
            # Set comprehensive headers
            await self.page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9,en-GB;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            })
            
            # Additional stealth measures
            await self.page.add_init_script("""
                // Override additional detection methods
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                
                // Override performance timing
                const originalGetEntries = Performance.prototype.getEntries;
                Performance.prototype.getEntries = function() {
                    const entries = originalGetEntries.call(this);
                    return entries.filter(entry => !entry.name.includes('bot'));
                };
                
                // Override console methods
                const originalLog = console.log;
                console.log = function(...args) {
                    if (args[0] && typeof args[0] === 'string' && args[0].includes('bot')) {
                        return;
                    }
                    return originalLog.apply(this, args);
                };
            """)
            
            logger.info("Maximum stealth measures applied")
            
        except Exception as e:
            logger.warning(f"Failed to apply some stealth measures: {e}")
    
    async def _setup_competitive_monitoring(self):
        """Setup monitoring specifically for competitive intelligence."""
        if not self.page:
            return
        
        try:
            await self.page.add_init_script("""
                window.chimeraCompetitiveEvents = [];
                
                // Monitor for competitive intelligence opportunities
                const observer = new MutationObserver((mutations) => {
                    mutations.forEach((mutation) => {
                        if (mutation.type === 'childList') {
                            mutation.addedNodes.forEach((node) => {
                                if (node.nodeType === Node.ELEMENT_NODE) {
                                    // Look for competitor mentions
                                    const text = node.textContent || '';
                                    const competitors = ['tableau', 'power bi', 'qlik', 'looker', 'snowflake'];
                                    competitors.forEach(competitor => {
                                        if (text.toLowerCase().includes(competitor)) {
                                            window.chimeraCompetitiveEvents.push({
                                                type: 'competitor_mention',
                                                competitor: competitor,
                                                context: text.substring(0, 100),
                                                timestamp: new Date().toISOString()
                                            });
                                        }
                                    });
                                }
                            });
                        }
                    });
                });
                
                observer.observe(document.body, { childList: true, subtree: true });
            """)
            
            logger.info("Competitive monitoring setup completed")
            
        except Exception as e:
            logger.warning(f"Failed to setup competitive monitoring: {e}")
    
    async def _load_competitive_targets(self):
        """Load comprehensive competitive targets from benchmark data."""
        try:
            # Load G2 targets
            g2_targets = self._load_g2_competitive_targets()
            
            # Load Capterra targets
            capterra_targets = self._load_capterra_competitive_targets()
            
            # Combine and prioritize targets
            self.competitive_targets = g2_targets + capterra_targets
            
            # Sort by priority and market position
            self.competitive_targets.sort(key=lambda x: (x.priority, x.market_position == "leader", x.name))
            
            self.scraping_stats["total_targets"] = len(self.competitive_targets)
            logger.info(f"Loaded {len(self.competitive_targets)} competitive targets")
            
        except Exception as e:
            logger.error(f"Failed to load competitive targets: {e}")
            raise
    
    def _load_g2_competitive_targets(self) -> List[CompetitiveTarget]:
        """Load G2 competitive targets with comprehensive coverage."""
        try:
            g2_file = Path("benchmarkSRCs/g2_sentiment_targets.json")
            if not g2_file.exists():
                logger.warning("G2 targets file not found, using default targets")
                return self._get_default_g2_targets()
            
            with open(g2_file, 'r') as f:
                g2_data = json.load(f)
            
            targets = []
            for competitor_id, competitor_data in g2_data["competitors"].items():
                target = CompetitiveTarget(
                    competitor_id=competitor_id,
                    name=competitor_data["name"],
                    platform="g2",
                    category=competitor_data["metadata"]["category"],
                    market_position=competitor_data["metadata"]["market_position"],
                    primary_competitors=competitor_data["metadata"]["primary_competitors"],
                    targets=competitor_data["targets"],
                    metadata=competitor_data["metadata"],
                    priority=self._calculate_priority(competitor_data["metadata"])
                )
                targets.append(target)
            
            return targets
            
        except Exception as e:
            logger.error(f"Failed to load G2 targets: {e}")
            return self._get_default_g2_targets()
    
    def _load_capterra_competitive_targets(self) -> List[CompetitiveTarget]:
        """Load Capterra competitive targets."""
        try:
            capterra_file = Path("benchmarkSRCs/capterra_sentiment_targets.json")
            if not capterra_file.exists():
                logger.warning("Capterra targets file not found, using default targets")
                return self._get_default_capterra_targets()
            
            with open(capterra_file, 'r') as f:
                capterra_data = json.load(f)
            
            targets = []
            for competitor_id, competitor_data in capterra_data["competitors"].items():
                target = CompetitiveTarget(
                    competitor_id=competitor_id,
                    name=competitor_data["name"],
                    platform="capterra",
                    category=competitor_data["metadata"]["category"],
                    market_position=competitor_data["metadata"]["market_position"],
                    primary_competitors=competitor_data["metadata"]["primary_competitors"],
                    targets=competitor_data["targets"],
                    metadata=competitor_data["metadata"],
                    priority=self._calculate_priority(competitor_data["metadata"])
                )
                targets.append(target)
            
            return targets
            
        except Exception as e:
            logger.error(f"Failed to load Capterra targets: {e}")
            return self._get_default_capterra_targets()
    
    def _calculate_priority(self, metadata: Dict[str, Any]) -> int:
        """Calculate target priority based on market position and category."""
        priority = 1
        
        # Market position priority
        if metadata.get("market_position") == "leader":
            priority += 3
        elif metadata.get("market_position") == "established":
            priority += 2
        elif metadata.get("market_position") == "emerging":
            priority += 1
        
        # Category priority
        if metadata.get("category") in ["business_intelligence", "data_visualization"]:
            priority += 2
        elif metadata.get("category") in ["cloud_data_warehouse", "unified_data_platform"]:
            priority += 1
        
        return priority
    
    def _get_default_g2_targets(self) -> List[CompetitiveTarget]:
        """Get default G2 targets if file loading fails."""
        return [
            CompetitiveTarget(
                competitor_id="tableau",
                name="Tableau",
                platform="g2",
                category="data_visualization",
                market_position="leader",
                primary_competitors=["power_bi", "qlik_sense", "looker"],
                targets={
                    "product_reviews": "https://www.g2.com/products/tableau/reviews",
                    "head_to_head": [
                        "https://www.g2.com/compare/tableau-vs-power-bi",
                        "https://www.g2.com/compare/tableau-vs-qlik-sense"
                    ]
                },
                metadata={"category": "data_visualization", "market_position": "leader"},
                priority=5
            )
        ]
    
    def _get_default_capterra_targets(self) -> List[CompetitiveTarget]:
        """Get default Capterra targets if file loading fails."""
        return [
            CompetitiveTarget(
                competitor_id="tableau",
                name="Tableau",
                platform="capterra",
                category="data_visualization",
                market_position="leader",
                primary_competitors=["power_bi", "qlik_sense", "looker"],
                targets={
                    "product_reviews": "https://www.capterra.com/p/208764/Tableau/reviews/",
                    "product_profile": "https://www.capterra.com/p/208764/Tableau/"
                },
                metadata={"category": "data_visualization", "market_position": "leader"},
                priority=5
            )
        ]
    
    async def scrape_competitive_intelligence(self) -> Dict[str, Any]:
        """Scrape comprehensive competitive intelligence data."""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            logger.info(f"Starting comprehensive competitive intelligence scraping of {len(self.competitive_targets)} targets")
            
            all_insights = []
            market_analysis = {}
            
            for target in self.competitive_targets:
                try:
                    self.current_target = target
                    logger.info(f"Scraping competitive intelligence for: {target.name} ({target.platform})")
                    
                    # Scrape comprehensive data for this competitor
                    insights = await self._scrape_competitor_intelligence(target)
                    
                    if insights:
                        all_insights.extend(insights)
                        
                        # Analyze market position
                        market_analysis[target.competitor_id] = await self._analyze_market_position(target, insights)
                        
                        logger.info(f"Successfully extracted {len(insights)} insights from {target.name}")
                    
                    # Update session
                    self.session_manager.complete_target_scraping(target.competitor_id, True)
                    self.scraping_stats["completed_targets"] += 1
                    
                    # Anti-detection delay
                    if self.config.get("human_behavior", True):
                        delay = random.uniform(
                            self.config.get("min_delay", 5.0),
                            self.config.get("max_delay", 12.0)
                        )
                        logger.info(f"Anti-detection delay: {delay:.2f}s")
                        await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Failed to scrape {target.name}: {e}")
                    self.session_manager.complete_target_scraping(target.competitor_id, False)
                    self.scraping_stats["failed_targets"] += 1
                    continue
            
            # Final analysis
            self.competitive_insights = all_insights
            self.market_analysis = market_analysis
            self.scraping_stats["total_insights"] = len(all_insights)
            
            # Generate comprehensive report
            comprehensive_report = await self._generate_comprehensive_report()
            
            logger.info(f"Competitive intelligence scraping completed. Total insights: {len(all_insights)}")
            
            return comprehensive_report
            
        except Exception as e:
            logger.error(f"Error in competitive intelligence scraping: {e}")
            raise
    
    async def _scrape_competitor_intelligence(self, target: CompetitiveTarget) -> List[CompetitiveInsight]:
        """Scrape comprehensive intelligence for a single competitor."""
        insights = []
        
        try:
            # Scrape product reviews
            if "product_reviews" in target.targets:
                review_insights = await self._scrape_product_reviews(target)
                insights.extend(review_insights)
            
            # Scrape head-to-head comparisons
            if "head_to_head" in target.targets:
                comparison_insights = await self._scrape_head_to_head_comparisons(target)
                insights.extend(comparison_insights)
            
            # Scrape four-way comparisons
            if "four_way" in target.targets:
                four_way_insights = await self._scrape_four_way_comparisons(target)
                insights.extend(four_way_insights)
            
            # Scrape alternatives
            if "alternatives" in target.targets:
                alternative_insights = await self._scrape_alternatives(target)
                insights.extend(alternative_insights)
            
            # Scrape product profiles
            if "product_profile" in target.targets:
                profile_insights = await self._scrape_product_profile(target)
                insights.extend(profile_insights)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to scrape competitor intelligence for {target.name}: {e}")
            return []
    
    async def _scrape_product_reviews(self, target: CompetitiveTarget) -> List[CompetitiveInsight]:
        """Scrape product reviews with enhanced competitive analysis."""
        try:
            url = target.targets["product_reviews"]
            
            # Navigate with stealth
            await self._navigate_with_maximum_stealth(url)
            
            # Handle Cloudflare if needed
            if self.config.get("cloudflare_bypass", True):
                await self.cloudflare_bypass.wait_for_bypass(self.page, target.platform)
            
            # Simulate human behavior
            if self.config.get("human_behavior", True):
                await self._simulate_competitive_research_behavior()
            
            # Extract content
            html_content = await self._extract_content_robustly()
            
            # Parse reviews based on platform
            if target.platform == "g2":
                parser = G2Parser()
                reviews = await parser.extract_reviews(html_content, url)
            else:
                parser = CapterraParser()
                reviews = await parser.extract_reviews(html_content, url)
            
            # Convert to competitive insights
            insights = []
            for review in reviews:
                insight = await self._create_review_insight(target, review, url, "product_review")
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to scrape product reviews for {target.name}: {e}")
            return []
    
    async def _scrape_comparisons(self, target: CompetitiveTarget) -> List[CompetitiveInsight]:
        """Scrape head-to-head and multi-way comparisons."""
        insights = []
        
        try:
            for comparison_url in target.targets["head_to_head"]:
                try:
                    # Navigate to comparison page
                    await self._navigate_with_maximum_stealth(comparison_url)
                    
                    # Handle Cloudflare
                    if self.config.get("cloudflare_bypass", True):
                        await self.cloudflare_bypass.wait_for_bypass(self.page, target.platform)
                    
                    # Extract comparison data
                    comparison_data = await self._extract_comparison_data()
                    
                    # Create comparison insight
                    insight = CompetitiveInsight(
                        competitor_id=target.competitor_id,
                        platform=target.platform,
                        extraction_date=datetime.now(),
                        data_type="head_to_head_comparison",
                        url=comparison_url,
                        content=comparison_data,
                        sentiment_analysis={},
                        competitive_mentions=comparison_data.get("competitors", []),
                        market_insights=comparison_data.get("market_insights", {}),
                        quality_score=0.9,
                        extraction_confidence=0.95
                    )
                    
                    insights.append(insight)
                    
                    # Anti-detection delay
                    await asyncio.sleep(random.uniform(3.0, 8.0))
                    
                except Exception as e:
                    logger.warning(f"Failed to scrape comparison {comparison_url}: {e}")
                    continue
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to scrape comparisons for {target.name}: {e}")
            return []
    
    async def _scrape_head_to_head_comparisons(self, target: CompetitiveTarget) -> List[CompetitiveInsight]:
        """Scrape head-to-head comparison data with focus on AI-generated summaries."""
        insights = []
        
        try:
            for comparison_url in target.targets.get("head_to_head", []):
                try:
                    logger.info(f"Scraping head-to-head comparison: {comparison_url}")
                    
                    # Navigate to comparison page
                    await self._navigate_with_maximum_stealth(comparison_url)
                    
                    # Handle Cloudflare
                    if self.config.get("cloudflare_bypass", True):
                        await self.cloudflare_bypass.wait_for_bypass(self.page, target.platform)
                    
                    # Simulate competitive research behavior
                    if self.config.get("human_behavior", True):
                        await self._simulate_competitive_research_behavior()
                    
                    # Extract content
                    html_content = await self._extract_content_robustly()
                    
                    # Parse head-to-head comparison using specialized parser
                    from ..parsers.head_to_head_comparison import G2HeadToHeadComparisonParser
                    head_to_head_parser = G2HeadToHeadComparisonParser()
                    comparison_data = await head_to_head_parser.parse_head_to_head_comparison(html_content, comparison_url)
                    
                    # Create comprehensive insight
                    insight = CompetitiveInsight(
                        competitor_id=target.competitor_id,
                        platform=target.platform,
                        extraction_date=datetime.now(),
                        data_type="head_to_head_comparison",
                        url=comparison_url,
                        content=asdict(comparison_data),
                        sentiment_analysis={
                            "score": 0.0,  # Head-to-head comparisons don't have sentiment
                            "label": "neutral",
                            "details": {"type": "comparison_data", "products_compared": 2}
                        },
                        competitive_mentions=[
                            comparison_data.product_a.get("name", ""),
                            comparison_data.product_b.get("name", "")
                        ],
                        market_insights=await self._generate_head_to_head_market_insights(comparison_data, target),
                        quality_score=comparison_data.data_quality_score / 100.0,  # Normalize to 0-1
                        extraction_confidence=comparison_data.extraction_confidence / 100.0  # Normalize to 0-1
                    )
                    
                    insights.append(insight)
                    
                    # Log AI summary extraction success
                    if comparison_data.ai_generated_summary and comparison_data.ai_generated_summary.get("summary_points"):
                        logger.info(f"Successfully extracted AI-generated summary with {len(comparison_data.ai_generated_summary['summary_points'])} points")
                    else:
                        logger.warning("No AI-generated summary found in head-to-head comparison")
                    
                    logger.info(f"Successfully scraped head-to-head comparison with {len(comparison_data.product_a) if comparison_data.product_a else 0} + {len(comparison_data.product_b) if comparison_data.product_b else 0} products")
                    
                    # Anti-detection delay for head-to-head comparisons
                    delay = random.uniform(5.0, 12.0)
                    logger.info(f"Head-to-head comparison anti-detection delay: {delay:.2f}s")
                    await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.warning(f"Failed to scrape head-to-head comparison {comparison_url}: {e}")
                    continue
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to scrape head-to-head comparisons for {target.name}: {e}")
            return []
    
    async def _scrape_four_way_comparisons(self, target: CompetitiveTarget) -> List[CompetitiveInsight]:
        """Scrape four-way comparison data for comprehensive competitive analysis."""
        insights = []
        
        try:
            for comparison_url in target.targets.get("four_way", []):
                try:
                    logger.info(f"Scraping four-way comparison: {comparison_url}")
                    
                    # Navigate to comparison page
                    await self._navigate_with_maximum_stealth(comparison_url)
                    
                    # Handle Cloudflare
                    if self.config.get("cloudflare_bypass", True):
                        await self.cloudflare_bypass.wait_for_bypass(self.page, target.platform)
                    
                    # Simulate competitive research behavior
                    if self.config.get("human_behavior", True):
                        await self._simulate_competitive_research_behavior()
                    
                    # Extract content
                    html_content = await self._extract_content_robustly()
                    
                    # Parse four-way comparison using specialized parser
                    from ..parsers.four_way_comparison import G2FourWayComparisonParser
                    four_way_parser = G2FourWayComparisonParser()
                    comparison_data = await four_way_parser.parse_four_way_comparison(html_content, comparison_url)
                    
                    # Create comprehensive insight
                    insight = CompetitiveInsight(
                        competitor_id=target.competitor_id,
                        platform=target.platform,
                        extraction_date=datetime.now(),
                        data_type="four_way_comparison",
                        url=comparison_url,
                        content=asdict(comparison_data),
                        sentiment_analysis={
                            "score": 0.0,  # Four-way comparisons don't have sentiment
                            "label": "neutral",
                            "details": {"type": "comparison_data", "products_compared": len(comparison_data.products)}
                        },
                        competitive_mentions=[p.get("name", "") for p in comparison_data.products if p.get("name")],
                        market_insights=await self._generate_four_way_market_insights(comparison_data, target),
                        quality_score=comparison_data.data_quality_score / 100.0,  # Normalize to 0-1
                        extraction_confidence=comparison_data.extraction_confidence / 100.0  # Normalize to 0-1
                    )
                    
                    insights.append(insight)
                    
                    logger.info(f"Successfully scraped four-way comparison with {len(comparison_data.products)} products")
                    
                    # Anti-detection delay for four-way comparisons
                    delay = random.uniform(8.0, 15.0)
                    logger.info(f"Four-way comparison anti-detection delay: {delay:.2f}s")
                    await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.warning(f"Failed to scrape four-way comparison {comparison_url}: {e}")
                    continue
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to scrape four-way comparisons for {target.name}: {e}")
            return []
    
    async def _extract_comparison_data(self) -> Dict[str, Any]:
        """Extract comprehensive comparison data."""
        try:
            # Extract competitor names
            competitors = await self.page.evaluate("""
                () => {
                    const competitorElements = document.querySelectorAll('[class*="competitor"], [class*="product"], [class*="vs"]');
                    const competitors = [];
                    competitorElements.forEach(el => {
                        const text = el.textContent || '';
                        if (text.includes('vs') || text.includes('compare')) {
                            competitors.push(text.trim());
                        }
                    });
                    return competitors;
                }
            """)
            
            # Extract comparison metrics
            metrics = await self.page.evaluate("""
                () => {
                    const metricElements = document.querySelectorAll('[class*="score"], [class*="rating"], [class*="metric"]');
                    const metrics = {};
                    metricElements.forEach(el => {
                        const label = el.querySelector('[class*="label"]')?.textContent || 'Unknown';
                        const value = el.querySelector('[class*="value"]')?.textContent || '0';
                        metrics[label.trim()] = value.trim();
                    });
                    return metrics;
                }
            """)
            
            return {
                "competitors": competitors,
                "metrics": metrics,
                "extraction_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract comparison data: {e}")
            return {"competitors": [], "metrics": {}, "extraction_timestamp": datetime.now().isoformat()}
    
    async def _create_review_insight(self, target: CompetitiveTarget, review: EnhancedReview, url: str, data_type: str) -> CompetitiveInsight:
        """Create competitive insight from review data."""
        try:
            # Advanced sentiment analysis with competitive context
            sentiment_score, sentiment_label, analysis_details = await self.sentiment_analyzer.analyze_sentiment_advanced(
                review.content,
                context={
                    "platform": target.platform,
                    "competitor": target.name,
                    "category": target.category,
                    "url": url
                }
            )
            
            # Extract competitive mentions
            competitive_mentions = self._extract_competitive_mentions(review.content, target)
            
            # Generate market insights
            market_insights = await self._generate_market_insights(review, target, sentiment_score)
            
            return CompetitiveInsight(
                competitor_id=target.competitor_id,
                platform=target.platform,
                extraction_date=datetime.now(),
                data_type=data_type,
                url=url,
                content=asdict(review),
                sentiment_analysis={
                    "score": sentiment_score,
                    "label": sentiment_label,
                    "details": analysis_details
                },
                competitive_mentions=competitive_mentions,
                market_insights=market_insights,
                quality_score=review.review_quality_score or 0.8,
                extraction_confidence=review.extraction_confidence or 0.9
            )
            
        except Exception as e:
            logger.error(f"Failed to create review insight: {e}")
            # Return basic insight on error
            return CompetitiveInsight(
                competitor_id=target.competitor_id,
                platform=target.platform,
                extraction_date=datetime.now(),
                data_type=data_type,
                url=url,
                content=asdict(review),
                sentiment_analysis={},
                competitive_mentions=[],
                market_insights={},
                quality_score=0.5,
                extraction_confidence=0.5
            )
    
    def _extract_competitive_mentions(self, content: str, target: CompetitiveTarget) -> List[str]:
        """Extract mentions of competitors from content."""
        mentions = []
        content_lower = content.lower()
        
        # Check for mentions of primary competitors
        for competitor in target.primary_competitors:
            if competitor.lower() in content_lower:
                mentions.append(competitor)
        
        # Check for mentions of other major competitors
        major_competitors = [
            "tableau", "power bi", "qlik", "looker", "snowflake", "databricks",
            "thoughtspot", "sigma", "hex", "omni", "domo", "sisense"
        ]
        
        for competitor in major_competitors:
            if competitor.lower() in content_lower and competitor not in mentions:
                mentions.append(competitor)
        
        return mentions
    
    async def _generate_market_insights(self, review: EnhancedReview, target: CompetitiveTarget, sentiment_score: float) -> Dict[str, Any]:
        """Generate market insights from review data."""
        try:
            insights = {
                "competitor_strengths": [],
                "competitor_weaknesses": [],
                "market_trends": [],
                "competitive_positioning": {}
            }
            
            # Analyze sentiment for market insights
            if sentiment_score > 0.6:
                insights["competitor_strengths"].append("High user satisfaction")
            elif sentiment_score < -0.6:
                insights["competitor_weaknesses"].append("User dissatisfaction")
            
            # Analyze content for specific insights
            content_lower = review.content.lower()
            
            if "easy to use" in content_lower or "intuitive" in content_lower:
                insights["competitor_strengths"].append("User experience")
            
            if "expensive" in content_lower or "cost" in content_lower:
                insights["market_trends"].append("Pricing sensitivity")
            
            if "integration" in content_lower or "api" in content_lower:
                insights["market_trends"].append("Integration focus")
            
            # Competitive positioning
            insights["competitive_positioning"] = {
                "category": target.category,
                "market_position": target.market_position,
                "sentiment_score": sentiment_score,
                "review_quality": review.review_quality_score or 0.8
            }
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate market insights: {e}")
            return {}
    
    async def _generate_head_to_head_market_insights(self, comparison_data, target: CompetitiveTarget) -> Dict[str, Any]:
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
            insights["ai_summary_insights"] = self._analyze_head_to_head_ai_summary_insights(comparison_data)
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate head-to-head market insights: {e}")
            return {}
    
    async def _generate_four_way_market_insights(self, comparison_data, target: CompetitiveTarget) -> Dict[str, Any]:
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
                insights["competitive_positioning"] = self._analyze_four_way_competitive_positioning(comparison_data)
            
            # Analyze market trends
            insights["market_trends"] = self._analyze_four_way_market_trends(comparison_data)
            
            # Analyze features
            insights["feature_analysis"] = self._analyze_four_way_feature_competitiveness(comparison_data)
            
            # Analyze pricing
            insights["pricing_analysis"] = self._analyze_four_way_pricing_competitiveness(comparison_data)
            
            return insights
            
        except Exception as e:
            logger.warning(f"Failed to generate four-way market insights: {e}")
            return {}
    
    def _analyze_head_to_head_competitive_positioning(self, comparison_data) -> Dict[str, Any]:
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
    
    def _analyze_head_to_head_market_trends(self, comparison_data) -> List[str]:
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
    
    def _analyze_head_to_head_feature_competitiveness(self, comparison_data) -> Dict[str, Any]:
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
    
    def _analyze_head_to_head_pricing_competitiveness(self, comparison_data) -> Dict[str, Any]:
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
    
    def _analyze_head_to_head_ai_summary_insights(self, comparison_data) -> Dict[str, Any]:
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
            logger.warning(f"Failed to analyze head-to-head AI summary insights: {e}")
            return {}
    
    def _analyze_four_way_competitive_positioning(self, comparison_data) -> Dict[str, Any]:
        """Analyze competitive positioning from four-way comparison data."""
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
            logger.warning(f"Failed to analyze four-way competitive positioning: {e}")
            return {}
    
    def _analyze_four_way_market_trends(self, comparison_data) -> List[str]:
        """Analyze market trends from four-way comparison data."""
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
            logger.warning(f"Failed to analyze four-way market trends: {e}")
            return []
    
    def _analyze_four_way_feature_competitiveness(self, comparison_data) -> Dict[str, Any]:
        """Analyze feature competitiveness from four-way comparison data."""
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
            logger.warning(f"Failed to analyze four-way feature competitiveness: {e}")
            return {}
    
    def _analyze_four_way_pricing_competitiveness(self, comparison_data) -> Dict[str, Any]:
        """Analyze pricing competitiveness from four-way comparison data."""
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
            logger.warning(f"Failed to analyze four-way pricing competitiveness: {e}")
            return {}
    
    async def _navigate_with_maximum_stealth(self, url: str):
        """Navigate with maximum stealth measures."""
        try:
            # Navigate with retry logic
            await self.retry_manager.execute_with_retry(
                self.page.goto,
                url,
                wait_until="networkidle",
                timeout=45000
            )
            
            # Wait for page to stabilize
            await asyncio.sleep(random.uniform(3.0, 6.0))
            
            # Check for successful navigation
            if not self.page.url or "error" in self.page.url.lower():
                raise Exception("Failed to navigate to target URL")
            
            logger.info(f"Successfully navigated to {url}")
            
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            raise
    
    async def _simulate_competitive_research_behavior(self):
        """Simulate human competitive research behavior."""
        try:
            # Get competitive research behavior profile
            profile = BehaviorProfile.get_profile("competitive_research")
            
            # Apply behavior simulation
            await self.behavior_simulator.set_page(self.page)
            await self.behavior_simulator.simulate_human_behavior(profile)
            
            # Additional competitive research behaviors
            await self._simulate_competitive_analysis_behavior()
            
            logger.info("Competitive research behavior simulation completed")
            
        except Exception as e:
            logger.warning(f"Failed to simulate competitive research behavior: {e}")
    
    async def _simulate_competitive_analysis_behavior(self):
        """Simulate specific competitive analysis behaviors."""
        try:
            # Scroll through comparison tables
            await self.page.evaluate("""
                () => {
                    const tables = document.querySelectorAll('table, [class*="comparison"], [class*="vs"]');
                    tables.forEach(table => {
                        // Simulate reading comparison data
                        const rows = table.querySelectorAll('tr');
                        rows.forEach((row, index) => {
                            if (index > 0) { // Skip header
                                setTimeout(() => {
                                    row.style.backgroundColor = '#f0f0f0';
                                    setTimeout(() => {
                                        row.style.backgroundColor = '';
                                    }, 500);
                                }, index * 200);
                            }
                        });
                    });
                }
            """)
            
            # Wait for behavior simulation
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
        except Exception as e:
            logger.warning(f"Failed to simulate competitive analysis behavior: {e}")
    
    async def _extract_content_robustly(self) -> str:
        """Extract HTML content with robust error handling."""
        try:
            # Wait for content to load
            await self.page.wait_for_load_state("networkidle", timeout=15000)
            
            # Extract content
            content = await self.page.content()
            
            if not content or len(content) < 1000:
                raise Exception("Insufficient content extracted")
            
            logger.info(f"Successfully extracted {len(content)} characters of content")
            return content
            
        except Exception as e:
            logger.error(f"Failed to extract content: {e}")
            raise
    
    async def _analyze_market_position(self, target: CompetitiveTarget, insights: List[CompetitiveInsight]) -> Dict[str, Any]:
        """Analyze market position based on collected insights."""
        try:
            if not insights:
                return {"status": "no_data", "confidence": 0.0}
            
            # Calculate average sentiment
            sentiment_scores = [
                insight.sentiment_analysis.get("score", 0) 
                for insight in insights 
                if insight.sentiment_analysis.get("score") is not None
            ]
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            # Analyze competitive mentions
            all_mentions = []
            for insight in insights:
                all_mentions.extend(insight.competitive_mentions)
            
            mention_frequency = defaultdict(int)
            for mention in all_mentions:
                mention_frequency[mention] += 1
            
            # Determine market position strength
            if avg_sentiment > 0.5:
                position_strength = "strong"
            elif avg_sentiment > 0:
                position_strength = "moderate"
            else:
                position_strength = "weak"
            
            return {
                "status": "analyzed",
                "confidence": len(insights) / 10,  # Confidence based on data volume
                "average_sentiment": avg_sentiment,
                "position_strength": position_strength,
                "competitive_mentions": dict(mention_frequency),
                "insight_count": len(insights),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze market position for {target.name}: {e}")
            return {"status": "error", "confidence": 0.0, "error": str(e)}
    
    async def _generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive competitive intelligence report."""
        try:
            report = {
                "report_metadata": {
                    "generation_date": datetime.now().isoformat(),
                    "total_competitors": len(self.competitive_targets),
                    "total_insights": len(self.competitive_insights),
                    "scraping_duration": (datetime.now() - self.scraping_stats["start_time"]).total_seconds(),
                    "success_rate": self.scraping_stats["completed_targets"] / self.scraping_stats["total_targets"] if self.scraping_stats["total_targets"] > 0 else 0
                },
                "competitive_landscape": {
                    "market_leaders": [t for t in self.competitive_targets if t.market_position == "leader"],
                    "established_players": [t for t in self.competitive_targets if t.market_position == "established"],
                    "emerging_competitors": [t for t in self.competitive_targets if t.market_position == "emerging"]
                },
                "market_analysis": self.market_analysis,
                "competitive_insights": [
                    {
                        "competitor_id": insight.competitor_id,
                        "platform": insight.platform,
                        "data_type": insight.data_type,
                        "sentiment_score": insight.sentiment_analysis.get("score", 0),
                        "competitive_mentions": insight.competitive_mentions,
                        "quality_score": insight.quality_score
                    }
                    for insight in self.competitive_insights
                ],
                "scraping_statistics": self.scraping_stats,
                "recommendations": await self._generate_strategic_recommendations()
            }
            
            # Save comprehensive report
            report_file = f"competitive_intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Comprehensive report saved to {report_file}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate comprehensive report: {e}")
            raise
    
    async def _generate_strategic_recommendations(self) -> List[str]:
        """Generate strategic recommendations based on competitive intelligence."""
        try:
            recommendations = []
            
            # Analyze market gaps
            if self.market_analysis:
                avg_sentiments = []
                for competitor_id, analysis in self.market_analysis.items():
                    if analysis.get("status") == "analyzed":
                        avg_sentiments.append(analysis.get("average_sentiment", 0))
                
                if avg_sentiments:
                    overall_sentiment = sum(avg_sentiments) / len(avg_sentiments)
                    
                    if overall_sentiment < 0:
                        recommendations.append("Market shows overall dissatisfaction - opportunity for disruption")
                    elif overall_sentiment > 0.5:
                        recommendations.append("Market is well-served - focus on differentiation and innovation")
            
            # Analyze competitive positioning
            leader_count = len([t for t in self.competitive_targets if t.market_position == "leader"])
            if leader_count > 5:
                recommendations.append("Highly competitive market with multiple leaders - focus on niche positioning")
            
            # Analyze data quality
            if self.competitive_insights:
                avg_quality = sum(insight.quality_score for insight in self.competitive_insights) / len(self.competitive_insights)
                if avg_quality < 0.7:
                    recommendations.append("Data quality needs improvement - refine extraction strategies")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate strategic recommendations: {e}")
            return ["Unable to generate recommendations due to data processing error"]
    
    async def close(self):
        """Clean up resources and close the scraper."""
        try:
            # Stop performance monitoring
            if self.performance_monitor:
                await self.performance_monitor.stop_monitoring()
            
            # Close browser
            if self.browser:
                await self.browser.close()
            
            # Export final competitive intelligence data
            await self._export_competitive_intelligence()
            
            logger.info("Competitive Intelligence Scraper closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing scraper: {e}")
    
    async def _export_competitive_intelligence(self):
        """Export competitive intelligence data."""
        try:
            # Export insights
            insights_file = f"competitive_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(insights_file, 'w') as f:
                json.dump([asdict(insight) for insight in self.competitive_insights], f, indent=2, default=str)
            
            # Export market analysis
            market_file = f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(market_file, 'w') as f:
                json.dump(self.market_analysis, f, indent=2, default=str)
            
            logger.info("Competitive intelligence data exported successfully")
            
        except Exception as e:
            logger.error(f"Failed to export competitive intelligence data: {e}")
    
    def get_competitive_summary(self) -> Dict[str, Any]:
        """Get comprehensive competitive intelligence summary."""
        return {
            "scraping_stats": self.scraping_stats,
            "session_summary": self.session_manager.get_session_summary(),
            "performance_summary": self.performance_monitor.get_metrics_summary() if self.performance_monitor else {},
            "competitive_targets": len(self.competitive_targets),
            "competitive_insights": len(self.competitive_insights),
            "market_analysis": len(self.market_analysis),
            "uptime_seconds": (datetime.now() - self.scraping_stats.get("start_time", datetime.now())).total_seconds() if self.scraping_stats.get("start_time") else 0
        }
