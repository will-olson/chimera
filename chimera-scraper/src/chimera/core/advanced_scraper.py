"""Advanced Chimera scraper with enterprise-grade anti-detection capabilities."""
import asyncio
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from playwright.async_api import async_playwright, BrowserContext, Page, Browser
from loguru import logger
import json
import os

from .fingerprint import AdvancedFingerprintManager
from .behavior import HumanBehaviorSimulator, BehaviorProfile
from .cloudflare import CloudflareBypass
from .session import ScrapingSession
from ..targets.manager import TargetManager
from ..parsers.base import BaseParser
from ..models.review import EnhancedReview, ReviewBatch


class AdvancedChimeraScraper:
    """Enterprise-grade scraper with advanced anti-detection that goes beyond benchmark limitations."""
    
    def __init__(self, profile: str = "stealth", config_path: str = None):
        self.profile = profile
        self.config_path = config_path
        self.fingerprint_manager = AdvancedFingerprintManager()
        self.behavior_simulator = None
        self.cloudflare_bypass = None
        self.session_manager = ScrapingSession(f"Chimera_Advanced_{profile}")
        self.target_manager = TargetManager(config_path) if config_path else None
        
        # Advanced anti-detection components
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Anti-detection state tracking
        self.anti_detection_state = {
            'fingerprint_rotation_count': 0,
            'last_fingerprint_change': None,
            'blocking_indicators_seen': [],
            'successful_bypasses': 0,
            'failed_bypasses': 0
        }
        
        # Advanced retry and recovery
        self.retry_strategies = {
            'fingerprint_rotation': 3,
            'browser_restart': 2,
            'proxy_rotation': 5,
            'session_renewal': 2
        }
        
        logger.info(f"Initialized AdvancedChimeraScraper with profile: {profile}")
    
    async def initialize_browser(self, profile: str = None) -> bool:
        """Initialize browser with advanced anti-detection that goes beyond benchmarks."""
        try:
            if profile:
                self.profile = profile
            
            # Create stealth browser context with enhanced fingerprinting
            self.context = await self.fingerprint_manager.create_stealth_browser_context(
                profile=self.profile,
                browser_type="chromium"
            )
            
            # Create new page with additional stealth measures
            self.page = await self.context.new_page()
            
            # Apply additional stealth measures that benchmarks didn't use
            await self._apply_advanced_stealth_measures()
            
            # Initialize behavior simulator
            self.behavior_simulator = HumanBehaviorSimulator(self.context)
            self.behavior_simulator.set_page(self.page)
            
            # Initialize Cloudflare bypass
            self.cloudflare_bypass = CloudflareBypass(self.page)
            
            # Set up advanced monitoring
            await self._setup_advanced_monitoring()
            
            logger.info("Browser initialized with advanced anti-detection measures")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            return False
    
    async def _apply_advanced_stealth_measures(self):
        """Apply stealth measures that go beyond benchmark implementations."""
        try:
            # Advanced viewport spoofing
            await self.page.set_viewport_size({
                'width': random.randint(1366, 1920),
                'height': random.randint(768, 1080)
            })
            
            # Advanced timezone and locale spoofing
            await self.context.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            })
            
            # Advanced JavaScript injection for stealth
            await self.page.add_init_script("""
                // Advanced stealth measures that benchmarks didn't implement
                
                // Override performance timing
                const originalGetEntries = performance.getEntries;
                performance.getEntries = function() {
                    const entries = originalGetEntries.apply(this, arguments);
                    return entries.map(entry => ({
                        ...entry,
                        duration: entry.duration + Math.random() * 10,
                        startTime: entry.startTime + Math.random() * 5
                    }));
                };
                
                // Override battery API
                if (navigator.getBattery) {
                    navigator.getBattery = function() {
                        return Promise.resolve({
                            charging: true,
                            chargingTime: Infinity,
                            dischargingTime: Infinity,
                            level: 0.8 + Math.random() * 0.2
                        });
                    };
                }
                
                // Override connection API
                if (navigator.connection) {
                    Object.defineProperty(navigator.connection, 'effectiveType', {
                        get: () => '4g'
                    });
                    Object.defineProperty(navigator.connection, 'rtt', {
                        get: () => 50 + Math.random() * 100
                    });
                }
                
                // Override media devices
                if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                    navigator.mediaDevices.enumerateDevices = function() {
                        return Promise.resolve([
                            { deviceId: 'default', kind: 'audioinput', label: 'Default - Microphone' },
                            { deviceId: 'default', kind: 'audiooutput', label: 'Default - Speaker' },
                            { deviceId: 'default', kind: 'videoinput', label: 'Default - Camera' }
                        ]);
                    };
                }
                
                // Override permissions
                if (navigator.permissions) {
                    navigator.permissions.query = function(permissionDesc) {
                        return Promise.resolve({
                            state: 'granted',
                            onchange: null
                        });
                    };
                }
                
                // Override geolocation
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition = function(success) {
                        success({
                            coords: {
                                latitude: 40.7128 + (Math.random() - 0.5) * 0.1,
                                longitude: -74.0060 + (Math.random() - 0.5) * 0.1,
                                accuracy: 100 + Math.random() * 900
                            },
                            timestamp: Date.now()
                        });
                    };
                }
            """)
            
            logger.info("Applied advanced stealth measures beyond benchmark implementations")
            
        except Exception as e:
            logger.warning(f"Error applying advanced stealth measures: {e}")
    
    async def _setup_advanced_monitoring(self):
        """Set up advanced monitoring for anti-detection."""
        try:
            # Monitor for blocking indicators
            await self.page.add_init_script("""
                window.chimeraBlockingDetected = false;
                window.chimeraBlockingIndicators = [];
                
                // Monitor DOM changes for blocking indicators
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'childList') {
                            mutation.addedNodes.forEach(function(node) {
                                if (node.nodeType === Node.ELEMENT_NODE) {
                                    const text = node.textContent || '';
                                    const blockingPatterns = [
                                        'checking your browser', 'cloudflare', 'ray id',
                                        'please wait', 'ddos protection', 'security check',
                                        'access denied', 'blocked', 'unusual activity',
                                        'automated access', 'bot detection', 'captcha',
                                        'challenge page', 'verify you are human'
                                    ];
                                    
                                    blockingPatterns.forEach(pattern => {
                                        if (text.toLowerCase().includes(pattern)) {
                                            window.chimeraBlockingDetected = true;
                                            window.chimeraBlockingIndicators.push({
                                                pattern: pattern,
                                                timestamp: Date.now(),
                                                element: node.outerHTML.substring(0, 200)
                                            });
                                        }
                                    });
                                }
                            });
                        }
                    });
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
            """)
            
            logger.info("Advanced monitoring setup completed")
            
        except Exception as e:
            logger.warning(f"Error setting up advanced monitoring: {e}")
    
    async def scrape_target(self, target_id: str, url: str, company_name: str, 
                           parser: BaseParser) -> List[EnhancedReview]:
        """Scrape a single target with advanced anti-detection that goes beyond benchmarks."""
        start_time = time.time()
        
        try:
            # Add target to session
            self.session_manager.add_target(target_id, company_name, url)
            
            # Pre-scraping anti-detection preparation
            await self._prepare_for_scraping()
            
            # Navigate with advanced stealth
            navigation_success = await self._navigate_with_stealth(url)
            if not navigation_success:
                raise Exception("Failed to navigate to target URL")
            
            # Advanced Cloudflare handling
            if await self._detect_advanced_blocking():
                await self._handle_advanced_blocking()
            
            # Simulate advanced human behavior
            await self._simulate_advanced_human_behavior()
            
            # Extract content with multiple strategies
            content = await self._extract_content_robustly()
            
            # Parse reviews with enhanced capabilities
            reviews = await self._parse_reviews_enhanced(content, url, company_name, parser)
            
            # Post-scraping cleanup and rotation
            await self._post_scraping_cleanup()
            
            # Update session
            self.session_manager.complete_target_scraping(
                target_id, True, len(reviews)
            )
            
            logger.info(f"Successfully scraped {len(reviews)} reviews from {company_name}")
            return reviews
            
        except Exception as e:
            error_msg = f"Failed to scrape {company_name}: {str(e)}"
            logger.error(error_msg)
            
            # Advanced error recovery
            recovery_success = await self._attempt_advanced_recovery(target_id, url, company_name, parser)
            if recovery_success:
                return await self.scrape_target(target_id, url, company_name, parser)
            
            # Update session with failure
            self.session_manager.complete_target_scraping(target_id, False, 0, [error_msg])
            return []
    
    async def _prepare_for_scraping(self):
        """Prepare for scraping with advanced anti-detection measures."""
        try:
            # Randomize fingerprint slightly
            if random.random() < 0.3:
                await self._rotate_fingerprint_minor()
            
            # Clear any existing data
            await self.context.clear_cookies()
            
            # Set random viewport
            await self.page.set_viewport_size({
                'width': random.randint(1366, 1920),
                'height': random.randint(768, 1080)
            })
            
            # Random delay
            await asyncio.sleep(random.uniform(1, 3))
            
        except Exception as e:
            logger.warning(f"Error in scraping preparation: {e}")
    
    async def _navigate_with_stealth(self, url: str) -> bool:
        """Navigate to URL with advanced stealth measures."""
        try:
            # Pre-navigation behavior
            await self.behavior_simulator.simulate_human_behavior(intensity="medium")
            
            # Navigate with custom options
            response = await self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
            
            if not response or response.status >= 400:
                logger.warning(f"Navigation failed with status: {response.status if response else 'No response'}")
                return False
            
            # Wait for page to stabilize
            await asyncio.sleep(random.uniform(2, 4))
            
            # Check for immediate blocking
            if await self._detect_immediate_blocking():
                logger.warning("Immediate blocking detected after navigation")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False
    
    async def _detect_advanced_blocking(self) -> bool:
        """Detect blocking using advanced methods beyond benchmarks."""
        try:
            # Check for blocking indicators in page content
            content = await self.page.content()
            content_lower = content.lower()
            
            # Advanced blocking patterns
            advanced_blocking_patterns = [
                'checking your browser', 'cloudflare', 'ray id', 'please wait',
                'ddos protection', 'security check', 'access denied', 'blocked',
                'unusual activity', 'automated access', 'bot detection', 'captcha',
                'challenge page', 'verify you are human', 'suspicious activity',
                'rate limited', 'too many requests', 'temporary block'
            ]
            
            for pattern in advanced_blocking_patterns:
                if pattern in content_lower:
                    self.anti_detection_state['blocking_indicators_seen'].append({
                        'pattern': pattern,
                        'timestamp': datetime.now(),
                        'url': self.page.url
                    })
                    return True
            
            # Check JavaScript variables for blocking
            blocking_detected = await self.page.evaluate("""
                () => {
                    return window.chimeraBlockingDetected || false;
                }
            """)
            
            if blocking_detected:
                return True
            
            # Check for suspicious page characteristics
            if len(content) < 1000 or 'error' in content_lower[:2000]:
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error in advanced blocking detection: {e}")
            return False
    
    async def _detect_immediate_blocking(self) -> bool:
        """Detect immediate blocking after navigation."""
        try:
            # Quick check for obvious blocking
            title = await self.page.title()
            if any(indicator in title.lower() for indicator in ['blocked', 'error', 'access denied']):
                return True
            
            # Check for Cloudflare indicators
            content = await self.page.content()
            if 'checking your browser' in content.lower():
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error in immediate blocking detection: {e}")
            return False
    
    async def _handle_advanced_blocking(self):
        """Handle blocking with advanced strategies beyond benchmarks."""
        try:
            logger.info("Advanced blocking detected, implementing enhanced bypass strategies")
            
            # Strategy 1: Enhanced Cloudflare bypass
            if await self.cloudflare_bypass.detect_cloudflare():
                logger.info("Cloudflare detected, attempting comprehensive bypass")
                bypass_success = await self.cloudflare_bypass.wait_for_bypass(
                    max_wait=60, strategy="comprehensive"
                )
                
                if bypass_success:
                    self.anti_detection_state['successful_bypasses'] += 1
                    logger.info("Cloudflare bypass successful")
                else:
                    self.anti_detection_state['failed_bypasses'] += 1
                    logger.warning("Cloudflare bypass failed")
            
            # Strategy 2: Advanced fingerprint rotation
            if self.anti_detection_state['failed_bypasses'] > 2:
                await self._rotate_fingerprint_major()
            
            # Strategy 3: Session renewal
            if self.anti_detection_state['failed_bypasses'] > 5:
                await self._renew_session()
            
            # Strategy 4: Advanced human behavior simulation
            await self._simulate_advanced_human_behavior()
            
        except Exception as e:
            logger.error(f"Error in advanced blocking handling: {e}")
    
    async def _simulate_advanced_human_behavior(self):
        """Simulate advanced human behavior that goes beyond benchmarks."""
        try:
            # Get behavior profile
            behavior_config = BehaviorProfile.get_profile(self.profile)
            
            # Advanced mouse movements with acceleration simulation
            await self._simulate_accelerated_mouse_movements()
            
            # Realistic scrolling with pauses
            await self._simulate_realistic_scrolling()
            
            # Page interaction simulation
            await self._simulate_page_interactions()
            
            # Reading behavior simulation
            await self._simulate_reading_behavior()
            
            # Random delays with human-like patterns
            await self._simulate_human_delays()
            
        except Exception as e:
            logger.warning(f"Error in advanced human behavior simulation: {e}")
    
    async def _simulate_accelerated_mouse_movements(self):
        """Simulate mouse movements with realistic acceleration."""
        try:
            viewport = await self.page.viewport_size()
            if not viewport:
                return
            
            # Generate realistic mouse movement path
            points = self._generate_realistic_mouse_path(viewport)
            
            for i, point in enumerate(points):
                # Move with acceleration/deceleration
                await self.page.mouse.move(point['x'], point['y'])
                
                # Variable delays based on movement distance
                if i > 0:
                    prev_point = points[i-1]
                    distance = ((point['x'] - prev_point['x'])**2 + (point['y'] - prev_point['y'])**2)**0.5
                    delay = min(0.5, distance / 1000)  # Faster for longer distances
                    await asyncio.sleep(delay)
                
                # Sometimes pause (like human thinking)
                if random.random() < 0.2:
                    await asyncio.sleep(random.uniform(0.5, 2.0)
                    
        except Exception as e:
            logger.debug(f"Error in accelerated mouse movements: {e}")
    
    def _generate_realistic_mouse_path(self, viewport: Dict[str, int]) -> List[Dict[str, int]]:
        """Generate realistic mouse movement path."""
        points = []
        current_x = viewport['width'] // 2
        current_y = viewport['height'] // 2
        
        for _ in range(random.randint(5, 12)):
            # Generate next point with realistic constraints
            target_x = max(50, min(viewport['width'] - 50, 
                                 current_x + random.randint(-200, 200)))
            target_y = max(50, min(viewport['height'] - 50, 
                                 current_y + random.randint(-200, 200)))
            
            # Add intermediate points for smooth movement
            steps = random.randint(3, 8)
            for step in range(1, steps + 1):
                x = current_x + (target_x - current_x) * step / steps
                y = current_y + (target_y - current_y) * step / steps
                points.append({'x': int(x), 'y': int(y)})
            
            current_x, current_y = target_x, target_y
        
        return points
    
    async def _simulate_realistic_scrolling(self):
        """Simulate realistic scrolling behavior."""
        try:
            # Get page height
            page_height = await self.page.evaluate("document.body.scrollHeight")
            viewport_height = (await self.page.viewport_size())['height']
            
            if page_height <= viewport_height:
                return
            
            # Simulate reading behavior with scrolling
            current_scroll = 0
            while current_scroll < page_height - viewport_height:
                # Scroll amount varies based on content
                scroll_amount = random.randint(100, 400)
                current_scroll += scroll_amount
                
                await self.page.mouse.wheel(0, scroll_amount)
                
                # Pause to "read" content
                read_time = random.uniform(2, 6)
                await asyncio.sleep(read_time)
                
                # Sometimes scroll back up slightly
                if random.random() < 0.3:
                    back_scroll = random.randint(20, 100)
                    await self.page.mouse.wheel(0, -back_scroll)
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                
                # Random longer pauses
                if random.random() < 0.1:
                    await asyncio.sleep(random.uniform(3, 8))
                    
        except Exception as e:
            logger.debug(f"Error in realistic scrolling: {e}")
    
    async def _simulate_page_interactions(self):
        """Simulate realistic page interactions."""
        try:
            # Find interactive elements
            elements = await self.page.query_selector_all('button, a, input, select, textarea')
            
            if not elements:
                return
            
            # Select random elements to interact with
            num_interactions = random.randint(2, 5)
            selected_elements = random.sample(elements, min(num_interactions, len(elements)))
            
            for element in selected_elements:
                try:
                    # Hover over element
                    await element.hover()
                    await asyncio.sleep(random.uniform(0.3, 1.0))
                    
                    # Sometimes click (rarely)
                    if random.random() < 0.05:
                        await element.click()
                        await asyncio.sleep(random.uniform(1.0, 3.0))
                        
                        # Handle potential navigation
                        if await self._detect_immediate_blocking():
                            await self.page.go_back()
                            await asyncio.sleep(random.uniform(2, 4))
                            
                except Exception as e:
                    logger.debug(f"Error interacting with element: {e}")
                    continue
                    
        except Exception as e:
            logger.debug(f"Error in page interactions: {e}")
    
    async def _simulate_reading_behavior(self):
        """Simulate realistic reading behavior."""
        try:
            # Find text content
            text_elements = await self.page.query_selector_all('p, h1, h2, h3, h4, h5, h6, li')
            
            if not text_elements:
                return
            
            # Simulate reading by moving through text elements
            for i, element in enumerate(text_elements[:random.randint(3, 8)]):
                try:
                    # Scroll element into view
                    await element.scroll_into_view_if_needed()
                    
                    # Hover over text (like reading)
                    await element.hover()
                    
                    # Simulate reading time based on text length
                    text = await element.text_content()
                    if text:
                        reading_time = min(5, len(text.split()) * 0.1)  # 0.1s per word, max 5s
                        await asyncio.sleep(reading_time)
                    
                    # Random pauses
                    if random.random() < 0.3:
                        await asyncio.sleep(random.uniform(0.5, 2.0))
                        
                except Exception as e:
                    logger.debug(f"Error in reading behavior simulation: {e}")
                    continue
                    
        except Exception as e:
            logger.debug(f"Error in reading behavior: {e}")
    
    async def _simulate_human_delays(self):
        """Simulate human-like delays and timing variations."""
        try:
            # Base delay with human-like variation
            base_delay = random.uniform(1, 3)
            
            # Add thinking time
            if random.random() < 0.4:
                thinking_time = random.uniform(2, 8)
                base_delay += thinking_time
            
            # Add distraction time
            if random.random() < 0.2:
                distraction_time = random.uniform(5, 15)
                base_delay += distraction_time
            
            await asyncio.sleep(base_delay)
            
        except Exception as e:
            logger.debug(f"Error in human delay simulation: {e}")
    
    async def _extract_content_robustly(self) -> str:
        """Extract page content using multiple robust strategies."""
        try:
            # Wait for content to stabilize
            await asyncio.sleep(random.uniform(2, 4))
            
            # Strategy 1: Wait for network idle
            try:
                await self.page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass  # Continue if timeout
            
            # Strategy 2: Wait for specific content indicators
            try:
                await self.page.wait_for_selector('body', timeout=5000)
            except:
                pass
            
            # Strategy 3: Get content with retry
            content = ""
            for attempt in range(3):
                try:
                    content = await self.page.content()
                    if content and len(content) > 1000:
                        break
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.warning(f"Content extraction attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(2)
            
            if not content or len(content) < 1000:
                raise Exception("Failed to extract sufficient content")
            
            return content
            
        except Exception as e:
            logger.error(f"Error in robust content extraction: {e}")
            raise
    
    async def _parse_reviews_enhanced(self, content: str, url: str, company_name: str, 
                                     parser: BaseParser) -> List[EnhancedReview]:
        """Parse reviews with enhanced capabilities."""
        try:
            # Use parser to extract reviews
            reviews = await parser.extract_reviews(content, url)
            
            # Enhance reviews with additional data
            enhanced_reviews = []
            for review in reviews:
                if hasattr(review, 'sentiment_score') and review.sentiment_score is None:
                    # Add sentiment analysis if not present
                    sentiment_score, sentiment_label = parser.analyze_sentiment(review.content)
                    review.sentiment_score = sentiment_score
                    review.sentiment_label = sentiment_label
                
                # Add extraction metadata
                review.extraction_method = f"advanced_chimera_{self.profile}"
                review.extraction_timestamp = datetime.now()
                
                enhanced_reviews.append(review)
            
            return enhanced_reviews
            
        except Exception as e:
            logger.error(f"Error in enhanced review parsing: {e}")
            return []
    
    async def _post_scraping_cleanup(self):
        """Perform post-scraping cleanup and rotation."""
        try:
            # Clear any sensitive data
            await self.context.clear_cookies()
            
            # Random delay before next operation
            await asyncio.sleep(random.uniform(3, 8))
            
            # Minor fingerprint rotation
            if random.random() < 0.2:
                await self._rotate_fingerprint_minor()
                
        except Exception as e:
            logger.warning(f"Error in post-scraping cleanup: {e}")
    
    async def _attempt_advanced_recovery(self, target_id: str, url: str, 
                                       company_name: str, parser: BaseParser) -> bool:
        """Attempt advanced recovery strategies."""
        try:
            logger.info(f"Attempting advanced recovery for {company_name}")
            
            # Strategy 1: Fingerprint rotation
            if self.anti_detection_state['fingerprint_rotation_count'] < self.retry_strategies['fingerprint_rotation']:
                await self._rotate_fingerprint_major()
                return True
            
            # Strategy 2: Browser restart
            if self.anti_detection_state['fingerprint_rotation_count'] < self.retry_strategies['browser_restart']:
                await self._restart_browser()
                return True
            
            # Strategy 3: Session renewal
            if self.anti_detection_state['fingerprint_rotation_count'] < self.retry_strategies['session_renewal']:
                await self._renew_session()
                return True
            
            logger.warning("All recovery strategies exhausted")
            return False
            
        except Exception as e:
            logger.error(f"Error in advanced recovery: {e}")
            return False
    
    async def _rotate_fingerprint_minor(self):
        """Perform minor fingerprint rotation."""
        try:
            # Rotate viewport size
            await self.page.set_viewport_size({
                'width': random.randint(1366, 1920),
                'height': random.randint(768, 1080)
            })
            
            # Rotate user agent slightly
            await self.context.set_extra_http_headers({
                'User-Agent': self._get_random_user_agent()
            })
            
            self.anti_detection_state['fingerprint_rotation_count'] += 1
            self.anti_detection_state['last_fingerprint_change'] = datetime.now()
            
            logger.info("Minor fingerprint rotation completed")
            
        except Exception as e:
            logger.warning(f"Error in minor fingerprint rotation: {e}")
    
    async def _rotate_fingerprint_major(self):
        """Perform major fingerprint rotation."""
        try:
            # Close current context
            if self.context:
                await self.context.close()
            
            # Create new context with different profile
            profiles = ['desktop_chrome', 'desktop_firefox', 'mac_chrome']
            new_profile = random.choice(profiles)
            
            self.context = await self.fingerprint_manager.create_stealth_browser_context(
                profile=new_profile
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Reinitialize components
            self.behavior_simulator = HumanBehaviorSimulator(self.context)
            self.behavior_simulator.set_page(self.page)
            self.cloudflare_bypass = CloudflareBypass(self.page)
            
            # Apply advanced stealth measures
            await self._apply_advanced_stealth_measures()
            await self._setup_advanced_monitoring()
            
            self.anti_detection_state['fingerprint_rotation_count'] += 1
            self.anti_detection_state['last_fingerprint_change'] = datetime.now()
            
            logger.info(f"Major fingerprint rotation completed with profile: {new_profile}")
            
        except Exception as e:
            logger.error(f"Error in major fingerprint rotation: {e}")
    
    async def _restart_browser(self):
        """Restart the entire browser instance."""
        try:
            # Close everything
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            
            # Reinitialize
            await self.initialize_browser(self.profile)
            
            logger.info("Browser restart completed")
            
        except Exception as e:
            logger.error(f"Error in browser restart: {e}")
    
    async def _renew_session(self):
        """Renew the entire scraping session."""
        try:
            # Close everything
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            
            # Create new session
            self.session_manager = ScrapingSession(f"Chimera_Advanced_{self.profile}_Renewed")
            
            # Reinitialize
            await self.initialize_browser(self.profile)
            
            logger.info("Session renewal completed")
            
        except Exception as e:
            logger.error(f"Error in session renewal: {e}")
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        return random.choice(user_agents)
    
    async def close(self):
        """Clean up resources."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            
            logger.info("Advanced scraper resources cleaned up")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_anti_detection_stats(self) -> Dict[str, Any]:
        """Get comprehensive anti-detection statistics."""
        return {
            'profile': self.profile,
            'fingerprint_rotations': self.anti_detection_state['fingerprint_rotation_count'],
            'last_fingerprint_change': self.anti_detection_state['last_fingerprint_change'],
            'blocking_indicators_seen': len(self.anti_detection_state['blocking_indicators_seen']),
            'successful_bypasses': self.anti_detection_state['successful_bypasses'],
            'failed_bypasses': self.anti_detection_state['failed_bypasses'],
            'bypass_success_rate': (
                self.anti_detection_state['successful_bypasses'] / 
                max(1, self.anti_detection_state['successful_bypasses'] + self.anti_detection_state['failed_bypasses'])
            )
        }
