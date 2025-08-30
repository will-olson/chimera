"""Enterprise-grade Chimera scraper with comprehensive anti-detection and intelligence capabilities."""

import asyncio
import time
import random
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from pathlib import Path
import json
import yaml

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


class ChimeraEnterpriseScraper:
    """Enterprise-grade scraper with advanced anti-detection that goes beyond benchmark limitations."""
    
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
            RetryConfig(
                max_attempts=self.config.get("retry_attempts", 3),
                base_delay=self.config.get("base_delay", 2.0),
                strategy="exponential_backoff"
            ),
            CircuitBreakerConfig(
                failure_threshold=self.config.get("failure_threshold", 5),
                recovery_timeout=self.config.get("recovery_timeout", 60.0)
            )
        )
        
        self.performance_monitor = PerformanceMonitor({
            "monitor_interval": self.config.get("monitor_interval", 5.0)
        })
        
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
            "total_reviews": 0,
            "start_time": None
        }
        
        # Anti-detection state
        self.anti_detection_events = []
        self.fingerprint_rotations = 0
        self.last_rotation_time = datetime.now()
        
        logger.info("Chimera Enterprise Scraper initialized")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file or use defaults."""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        # Default configuration
        return {
            "scraping_profile": "stealth",
            "retry_attempts": 3,
            "base_delay": 2.0,
            "failure_threshold": 5,
            "recovery_timeout": 60.0,
            "monitor_interval": 5.0,
            "max_reviews_per_target": 25,
            "human_behavior": True,
            "cloudflare_bypass": True,
            "performance_monitoring": True
        }
    
    async def initialize(self):
        """Initialize the scraper with browser and monitoring."""
        try:
            # Start performance monitoring
            if self.config.get("performance_monitoring", True):
                await self.performance_monitor.start_monitoring()
                logger.info("Performance monitoring started")
            
            # Initialize browser
            await self._initialize_browser()
            
            # Load targets
            await self._load_targets()
            
            self.is_initialized = True
            self.scraping_stats["start_time"] = datetime.now()
            
            logger.info("Chimera Enterprise Scraper fully initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize scraper: {e}")
            raise
    
    async def _initialize_browser(self):
        """Initialize Playwright browser with advanced stealth."""
        try:
            playwright = await async_playwright().start()
            
            # Use stealth profile from config
            profile = self.config.get("scraping_profile", "stealth")
            
            self.browser = await playwright.chromium.launch(
                headless=self.config.get("headless", False),
                args=self.fingerprint_manager.get_chrome_args(profile)
            )
            
            # Create stealth context
            self.context = await self.fingerprint_manager.create_stealth_browser_context(
                profile=profile
            )
            
            # Create page
            self.page = await self.context.new_page()
            
            # Apply advanced stealth measures
            await self._apply_advanced_stealth_measures()
            
            # Setup advanced monitoring
            await self._setup_advanced_monitoring()
            
            logger.info("Browser initialized with advanced stealth measures")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise
    
    async def _apply_advanced_stealth_measures(self):
        """Apply comprehensive stealth measures to the page."""
        if not self.page:
            return
        
        try:
            # Inject advanced stealth scripts
            await self.fingerprint_manager._inject_stealth_scripts(self.page)
            
            # Set viewport and user agent
            await self.page.set_viewport_size({
                "width": random.randint(1200, 1920),
                "height": random.randint(800, 1080)
            })
            
            # Set extra headers
            await self.page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            })
            
            logger.info("Advanced stealth measures applied")
            
        except Exception as e:
            logger.warning(f"Failed to apply some stealth measures: {e}")
    
    async def _setup_advanced_monitoring(self):
        """Setup advanced page monitoring and event handling."""
        if not self.page:
            return
        
        try:
            # Monitor for detection events
            await self.page.add_init_script("""
                window.chimeraDetectionEvents = [];
                
                // Monitor for bot detection
                const originalFetch = window.fetch;
                window.fetch = function(...args) {
                    const response = originalFetch.apply(this, args);
                    if (response.url.includes('captcha') || response.url.includes('block')) {
                        window.chimeraDetectionEvents.push({
                            type: 'detection_attempt',
                            url: response.url,
                            timestamp: new Date().toISOString()
                        });
                    }
                    return response;
                };
                
                // Monitor for suspicious behavior detection
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.name.includes('bot') || entry.name.includes('detection')) {
                            window.chimeraDetectionEvents.push({
                                type: 'performance_detection',
                                name: entry.name,
                                timestamp: new Date().toISOString()
                            });
                        }
                    }
                });
                observer.observe({ entryTypes: ['measure'] });
            """)
            
            logger.info("Advanced monitoring setup completed")
            
        except Exception as e:
            logger.warning(f"Failed to setup advanced monitoring: {e}")
    
    async def _load_targets(self):
        """Load and validate scraping targets."""
        try:
            # Load targets from configuration
            targets = self.target_manager.load_targets()
            
            if not targets:
                logger.warning("No targets loaded, using default targets")
                # Create default targets for testing
                targets = self.target_manager.create_default_targets()
            
            self.scraping_stats["total_targets"] = len(targets)
            logger.info(f"Loaded {len(targets)} targets for scraping")
            
        except Exception as e:
            logger.error(f"Failed to load targets: {e}")
            raise
    
    async def scrape_targets(self, target_filter: Optional[Dict[str, Any]] = None) -> List[ReviewBatch]:
        """Scrape multiple targets with enterprise-grade capabilities."""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            # Get targets to scrape
            targets = self.target_manager.get_targets_by_filter(target_filter) if target_filter else self.target_manager.get_all_targets()
            
            logger.info(f"Starting scraping of {len(targets)} targets")
            
            review_batches = []
            
            for target in targets:
                try:
                    self.current_target = target
                    logger.info(f"Scraping target: {target.get('name', 'Unknown')}")
                    
                    # Scrape single target
                    reviews = await self.scrape_target(target)
                    
                    if reviews:
                        # Create review batch
                        batch = ReviewBatch(
                            batch_id=f"batch_{int(time.time())}_{random.randint(1000, 9999)}",
                            source_platform=target.get('platform', 'unknown'),
                            target_company=target.get('name', 'unknown'),
                            extraction_date=datetime.now(),
                            reviews=reviews
                        )
                        
                        # Update batch statistics
                        batch.update_statistics()
                        
                        review_batches.append(batch)
                        
                        # Store batch
                        await self.storage.save_reviews_batch(batch)
                        
                        logger.info(f"Successfully scraped {len(reviews)} reviews from {target.get('name', 'Unknown')}")
                    
                    # Update session
                    self.session_manager.complete_target_scraping(target.get('id', 'unknown'), True)
                    self.scraping_stats["completed_targets"] += 1
                    
                    # Anti-detection delay
                    if self.config.get("human_behavior", True):
                        delay = random.uniform(
                            self.config.get("min_delay", 3.0),
                            self.config.get("max_delay", 8.0)
                        )
                        logger.info(f"Anti-detection delay: {delay:.2f}s")
                        await asyncio.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Failed to scrape target {target.get('name', 'Unknown')}: {e}")
                    self.session_manager.complete_target_scraping(target.get('id', 'unknown'), False)
                    self.scraping_stats["failed_targets"] += 1
                    
                    # Record error in performance monitor
                    self.performance_monitor.record_request(False, 0)
                    
                    continue
            
            # Final statistics
            self.scraping_stats["total_reviews"] = sum(len(batch.reviews) for batch in review_batches)
            
            logger.info(f"Scraping completed. Total reviews: {self.scraping_stats['total_reviews']}")
            
            return review_batches
            
        except Exception as e:
            logger.error(f"Error in bulk scraping: {e}")
            raise
    
    async def scrape_target(self, target: Dict[str, Any]) -> List[EnhancedReview]:
        """Scrape a single target with advanced anti-detection."""
        if not self.page:
            raise RuntimeError("Browser not initialized")
        
        try:
            # Prepare for scraping
            await self._prepare_for_scraping(target)
            
            # Navigate to target URL
            url = target.get('url')
            if not url:
                raise ValueError("Target URL not provided")
            
            # Navigate with stealth
            await self._navigate_with_stealth(url)
            
            # Check for immediate blocking
            if await self._detect_immediate_blocking():
                logger.warning("Immediate blocking detected, attempting recovery")
                await self._attempt_advanced_recovery()
            
            # Handle Cloudflare if needed
            if self.config.get("cloudflare_bypass", True):
                await self.cloudflare_bypass.wait_for_bypass(self.page, target.get('platform', 'unknown'))
            
            # Simulate human behavior
            if self.config.get("human_behavior", True):
                await self._simulate_advanced_human_behavior()
            
            # Extract content robustly
            html_content = await self._extract_content_robustly()
            
            # Parse reviews based on platform
            platform = target.get('platform', 'unknown').lower()
            reviews = await self._parse_reviews_enhanced(html_content, url, platform)
            
            # Post-scraping cleanup
            await self._post_scraping_cleanup()
            
            # Update statistics
            self.scraping_stats["total_reviews"] += len(reviews)
            
            # Record success in performance monitor
            self.performance_monitor.record_request(True, 0)  # Response time not available here
            
            return reviews
            
        except Exception as e:
            logger.error(f"Error scraping target {target.get('name', 'Unknown')}: {e}")
            
            # Record failure in performance monitor
            self.performance_monitor.record_request(False, 0)
            
            # Attempt recovery
            await self._attempt_advanced_recovery()
            
            raise
    
    async def _prepare_for_scraping(self, target: Dict[str, Any]):
        """Prepare the scraper for a new target."""
        try:
            # Rotate fingerprint if needed
            if self._should_rotate_fingerprint():
                await self._rotate_fingerprint_minor()
            
            # Update session
            self.session_manager.start_target_scraping(target.get('id', 'unknown'))
            
            # Reset page state
            if self.page:
                await self.page.evaluate("() => window.chimeraDetectionEvents = []")
            
            logger.info(f"Prepared for scraping target: {target.get('name', 'Unknown')}")
            
        except Exception as e:
            logger.warning(f"Failed to prepare for scraping: {e}")
    
    async def _navigate_with_stealth(self, url: str):
        """Navigate to URL with stealth measures."""
        try:
            # Navigate with retry logic
            await self.retry_manager.execute_with_retry(
                self.page.goto,
                url,
                wait_until="networkidle",
                timeout=30000
            )
            
            # Wait for page to stabilize
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            # Check for successful navigation
            if not self.page.url or "error" in self.page.url.lower():
                raise Exception("Failed to navigate to target URL")
            
            logger.info(f"Successfully navigated to {url}")
            
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            raise
    
    async def _detect_immediate_blocking(self) -> bool:
        """Detect immediate blocking or detection."""
        if not self.page:
            return False
        
        try:
            # Check for common blocking indicators
            blocking_indicators = [
                "access denied",
                "blocked",
                "captcha",
                "robot",
                "bot detected",
                "suspicious activity",
                "rate limit exceeded"
            ]
            
            page_content = await self.page.content()
            page_text = page_content.lower()
            
            for indicator in blocking_indicators:
                if indicator in page_text:
                    logger.warning(f"Blocking indicator detected: {indicator}")
                    return True
            
            # Check for detection events
            detection_events = await self.page.evaluate("() => window.chimeraDetectionEvents || []")
            if detection_events:
                logger.warning(f"Detection events found: {len(detection_events)}")
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error detecting blocking: {e}")
            return False
    
    async def _simulate_advanced_human_behavior(self):
        """Simulate advanced human browsing behavior."""
        try:
            # Get behavior profile
            profile = BehaviorProfile.get_profile("stealth")
            
            # Apply behavior simulation
            await self.behavior_simulator.set_page(self.page)
            await self.behavior_simulator.simulate_human_behavior(profile)
            
            logger.info("Advanced human behavior simulation completed")
            
        except Exception as e:
            logger.warning(f"Failed to simulate human behavior: {e}")
    
    async def _extract_content_robustly(self) -> str:
        """Extract HTML content with robust error handling."""
        try:
            # Wait for content to load
            await self.page.wait_for_load_state("networkidle", timeout=10000)
            
            # Extract content
            content = await self.page.content()
            
            if not content or len(content) < 1000:
                raise Exception("Insufficient content extracted")
            
            logger.info(f"Successfully extracted {len(content)} characters of content")
            return content
            
        except Exception as e:
            logger.error(f"Failed to extract content: {e}")
            raise
    
    async def _parse_reviews_enhanced(self, html_content: str, url: str, platform: str) -> List[EnhancedReview]:
        """Parse reviews using enhanced parsers."""
        try:
            if platform == "g2":
                parser = G2Parser()
                reviews = await parser.extract_reviews(html_content, url)
            elif platform == "capterra":
                parser = CapterraParser()
                reviews = await parser.extract_reviews(html_content, url)
            else:
                # Fallback to G2 parser
                parser = G2Parser()
                reviews = await parser.extract_reviews(html_content, url)
            
            # Enhance reviews with sentiment analysis
            enhanced_reviews = []
            for review in reviews:
                # Advanced sentiment analysis
                sentiment_score, sentiment_label, analysis_details = await self.sentiment_analyzer.analyze_sentiment_advanced(
                    review.content,
                    context={"platform": platform, "url": url}
                )
                
                # Update review with enhanced data
                review.sentiment_score = sentiment_score
                review.sentiment_label = sentiment_label
                
                enhanced_reviews.append(review)
            
            logger.info(f"Successfully parsed {len(enhanced_reviews)} enhanced reviews")
            return enhanced_reviews
            
        except Exception as e:
            logger.error(f"Failed to parse reviews: {e}")
            raise
    
    async def _post_scraping_cleanup(self):
        """Perform post-scraping cleanup and maintenance."""
        try:
            # Clear cookies and storage
            if self.context:
                await self.context.clear_cookies()
            
            # Clear page cache
            if self.page:
                await self.page.evaluate("() => window.localStorage.clear()")
                await self.page.evaluate("() => window.sessionStorage.clear()")
            
            # Record anti-detection event
            self.anti_detection_events.append({
                "timestamp": datetime.now().isoformat(),
                "type": "scraping_completed",
                "target": self.current_target.get('name', 'Unknown') if self.current_target else 'Unknown'
            })
            
            logger.info("Post-scraping cleanup completed")
            
        except Exception as e:
            logger.warning(f"Failed to complete post-scraping cleanup: {e}")
    
    async def _attempt_advanced_recovery(self):
        """Attempt advanced recovery from blocking or errors."""
        try:
            logger.info("Attempting advanced recovery...")
            
            # Minor fingerprint rotation
            await self._rotate_fingerprint_minor()
            
            # Wait for recovery
            await asyncio.sleep(random.uniform(5.0, 15.0))
            
            # Check if recovery was successful
            if await self._detect_immediate_blocking():
                logger.warning("Minor recovery failed, attempting major recovery")
                await self._rotate_fingerprint_major()
            
            logger.info("Advanced recovery completed")
            
        except Exception as e:
            logger.error(f"Advanced recovery failed: {e}")
    
    def _should_rotate_fingerprint(self) -> bool:
        """Determine if fingerprint rotation is needed."""
        time_since_rotation = datetime.now() - self.last_rotation_time
        return time_since_rotation.total_seconds() > 300  # 5 minutes
    
    async def _rotate_fingerprint_minor(self):
        """Perform minor fingerprint rotation."""
        try:
            # Rotate user agent
            new_user_agent = self._get_random_user_agent()
            if self.context:
                await self.context.set_extra_http_headers({
                    "User-Agent": new_user_agent
                })
            
            # Rotate viewport
            if self.page:
                await self.page.set_viewport_size({
                    "width": random.randint(1200, 1920),
                    "height": random.randint(800, 1080)
                })
            
            self.fingerprint_rotations += 1
            self.last_rotation_time = datetime.now()
            
            logger.info("Minor fingerprint rotation completed")
            
        except Exception as e:
            logger.warning(f"Minor fingerprint rotation failed: {e}")
    
    async def _rotate_fingerprint_major(self):
        """Perform major fingerprint rotation."""
        try:
            # Close current context
            if self.context:
                await self.context.close()
            
            # Create new context with different profile
            profiles = ["desktop_chrome", "desktop_firefox", "mac_chrome"]
            new_profile = random.choice(profiles)
            
            self.context = await self.fingerprint_manager.create_stealth_browser_context(
                profile=new_profile
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Apply stealth measures
            await self._apply_advanced_stealth_measures()
            await self._setup_advanced_monitoring()
            
            self.fingerprint_rotations += 1
            self.last_rotation_time = datetime.now()
            
            logger.info("Major fingerprint rotation completed")
            
        except Exception as e:
            logger.error(f"Major fingerprint rotation failed: {e}")
            raise
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        return random.choice(user_agents)
    
    async def close(self):
        """Clean up resources and close the scraper."""
        try:
            # Stop performance monitoring
            if self.performance_monitor:
                await self.performance_monitor.stop_monitoring()
            
            # Close browser
            if self.browser:
                await self.browser.close()
            
            # Export final statistics
            await self._export_final_statistics()
            
            logger.info("Chimera Enterprise Scraper closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing scraper: {e}")
    
    async def _export_final_statistics(self):
        """Export final scraping statistics and performance data."""
        try:
            # Export performance metrics
            if self.performance_monitor:
                metrics_file = f"performance_metrics_{int(time.time())}.json"
                self.performance_monitor.export_metrics(metrics_file)
            
            # Export session summary
            session_summary = self.session_manager.get_session_summary()
            session_file = f"session_summary_{int(time.time())}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session_summary, f, indent=2, default=str)
            
            # Export anti-detection events
            events_file = f"anti_detection_events_{int(time.time())}.json"
            with open(events_file, 'w') as f:
                json.dump(self.anti_detection_events, f, indent=2, default=str)
            
            logger.info("Final statistics exported successfully")
            
        except Exception as e:
            logger.error(f"Failed to export final statistics: {e}")
    
    def get_scraping_summary(self) -> Dict[str, Any]:
        """Get comprehensive scraping summary."""
        return {
            "scraping_stats": self.scraping_stats,
            "session_summary": self.session_manager.get_session_summary(),
            "performance_summary": self.performance_monitor.get_metrics_summary() if self.performance_monitor else {},
            "anti_detection_events": len(self.anti_detection_events),
            "fingerprint_rotations": self.fingerprint_rotations,
            "retry_statistics": self.retry_manager.get_statistics() if self.retry_manager else {},
            "uptime_seconds": (datetime.now() - self.scraping_stats.get("start_time", datetime.now())).total_seconds() if self.scraping_stats.get("start_time") else 0
        }
    
    def get_anti_detection_stats(self) -> Dict[str, Any]:
        """Get anti-detection statistics."""
        return {
            "total_events": len(self.anti_detection_events),
            "fingerprint_rotations": self.fingerprint_rotations,
            "last_rotation": self.last_rotation_time.isoformat(),
            "events_by_type": self._count_events_by_type(),
            "recent_events": self.anti_detection_events[-10:] if self.anti_detection_events else []
        }
    
    def _count_events_by_type(self) -> Dict[str, int]:
        """Count anti-detection events by type."""
        event_counts = {}
        for event in self.anti_detection_events:
            event_type = event.get("type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        return event_counts
