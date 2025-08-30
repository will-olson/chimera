#!/usr/bin/env python3
"""
🎯 WORKING CAPTCHA SOLVER - Exact puzzle.md Implementation
Implements the exact mathematical functions discovered in puzzle.md:
- Math.floor for precise coordinate calculations (hex: \x66\x6c\x6f\x6f\x72)
- Math.round for final position calculations (hex: \x72\x6f\x75\x6e\x64)
- Critical constants: c=63 (slider width), g=20 (success threshold)
- Perfect positioning formula: (container_width - 63 - 20) / (container_width - 63) * current_position

FIXES the coordinate system issues that caused previous failures
"""

import asyncio
import json
import logging
import math
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from playwright.async_api import async_playwright, Page, Frame, ElementHandle

@dataclass
class MathematicalConstants:
    """Exact constants discovered in puzzle.md"""
    SLIDER_WIDTH = 63  # c = 63 (slider width)
    SUCCESS_THRESHOLD = 20  # g = 20 (success threshold offset)
    MAX_OFFSET = 5  # +5 from the formula: width - c + 5

class WorkingCaptchaSolver:
    """
    🎯 Working CAPTCHA Solver
    Implements exact mathematical functions from puzzle.md with fixed coordinate system
    """
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.test_results = []
        self.scraping_stats = {
            "captcha_detected": 0,
            "iframe_access_success": 0,
            "mathematical_calculations": 0,
            "coordinate_system_fixed": 0,
            "successful_captcha_solves": 0,
            "data_extraction_attempts": 0,
            "successful_data_extractions": 0,
            "execution_time": 0.0,
            "errors": []
        }
        
        # Mathematical constants from puzzle.md
        self.math_constants = MathematicalConstants()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def setup_working_browser(self) -> tuple:
        """
        🚀 Setup browser with working anti-detection measures
        """
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with specific arguments for anti-detection
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Create context with specific settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation']
            )
            
            # Add stealth script to bypass detection
            await self.context.add_init_script("""
                // Remove automation indicators
                delete navigator.__proto__.webdriver;
                delete window.navigator.webdriver;
                
                // Override plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Override languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                
                // STRATEGIC: Prevent _playwright_target_ detection events
                const originalAddEventListener = window.addEventListener;
                window.addEventListener = function(type, listener, options) {
                    // Filter out playwright detection events
                    if (type && type.includes && (type.includes('_playwright_') || type.includes('_target_'))) {
                        return; // Don't add these listeners
                    }
                    return originalAddEventListener.call(this, type, listener, options);
                };
                
                // STRATEGIC: Override MutationObserver to prevent DOM manipulation detection
                const originalMutationObserver = window.MutationObserver;
                window.MutationObserver = function(callback) {
                    // Filter out automation-related mutations
                    const filteredCallback = function(mutations) {
                        const filteredMutations = mutations.filter(mutation => {
                            // Filter out mutations that might indicate automation
                            if (mutation.type === 'childList') {
                                const target = mutation.target;
                                if (target && target.className && 
                                    (target.className.includes('automation') || 
                                     target.className.includes('bot') ||
                                     target.className.includes('playwright'))) {
                                    return false;
                                }
                            }
                            return true;
                        });
                        if (filteredMutations.length > 0) {
                            callback(filteredMutations);
                        }
                    };
                    return new originalMutationObserver(filteredCallback);
                };
                
                // STRATEGIC: Add natural timing variations
                const originalSetTimeout = window.setTimeout;
                window.setTimeout = function(callback, delay, ...args) {
                    // Add small random variations to timing (natural human behavior)
                    const variation = Math.random() * 50 - 25; // ±25ms variation
                    const adjustedDelay = Math.max(0, delay + variation);
                    return originalSetTimeout.call(this, callback, adjustedDelay, ...args);
                };
            """)
            
            self.page = await self.context.new_page()
            
            # Set extra headers
            await self.page.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            self.logger.info("✅ Working browser setup completed")
            return self.browser, self.context, self.page
            
        except Exception as e:
            self.logger.error(f"❌ Browser setup failed: {e}")
            self.scraping_stats["errors"].append(f"Browser setup: {e}")
            raise

    async def detect_and_access_captcha_iframe(self) -> Optional[Frame]:
        """
        🔍 Detect and access CAPTCHA iframe using proven breakthrough techniques
        """
        try:
            self.logger.info("🔍 Detecting CAPTCHA iframe using proven breakthrough techniques...")
            
            # Wait for potential CAPTCHA to load
            await asyncio.sleep(3)
            
            # Look for CAPTCHA iframe using proven selectors
            iframe_selectors = [
                "iframe[src*='captcha']",
                "iframe[src*='datadome']",
                "iframe[src*='challenge']",
                "iframe[src*='verification']"
            ]
            
            iframe_element = None
            for selector in iframe_selectors:
                iframe_element = await self.page.query_selector(selector)
                if iframe_element:
                    self.logger.info(f"✅ CAPTCHA iframe found with selector: {selector}")
                    break
            
            if not iframe_element:
                self.logger.warning("⚠️ No CAPTCHA iframe detected")
                return None
            
            # Access the iframe content
            iframe = await iframe_element.content_frame()
            if not iframe:
                self.logger.error("❌ Failed to access iframe content")
                return None
            
            self.scraping_stats["captcha_detected"] += 1
            self.scraping_stats["iframe_access_success"] += 1
            self.logger.info("✅ Successfully accessed CAPTCHA iframe content")
            
            return iframe
            
        except Exception as e:
            self.logger.error(f"❌ Iframe detection failed: {e}")
            self.scraping_stats["errors"].append(f"Iframe detection: {e}")
            return None

    async def solve_captcha_with_working_mathematics(self, iframe: Frame) -> bool:
        """
        🧩 Solve CAPTCHA using WORKING mathematical functions from puzzle.md
        FIXES the coordinate system issues that caused previous failures
        """
        try:
            self.logger.info("🧩 Solving CAPTCHA with WORKING mathematical precision...")
            
            # Step 1: Find puzzle element using proven selectors
            puzzle_element = await iframe.query_selector("i.sliderIcon")
            if not puzzle_element:
                self.logger.error("❌ No puzzle element found")
                return False
            
            self.logger.info("✅ Puzzle element found: i.sliderIcon")
            
            # Step 2: Get precise element dimensions and position
            element_box = await puzzle_element.bounding_box()
            if not element_box:
                self.logger.error("❌ Failed to get puzzle element dimensions")
                return False
            
            # Step 3: Get container dimensions
            container_element = await iframe.query_selector(".sliderContainer")
            if not container_element:
                self.logger.error("❌ No slider container found")
                return False
            
            container_box = await container_element.bounding_box()
            if not container_box:
                self.logger.error("❌ Failed to get container dimensions")
                return False
            
            # Step 4: FIXED COORDINATE SYSTEM - Use container-relative positioning
            container_left = container_box['x']
            container_width = container_box['width']
            
            # Calculate element position relative to container (FIXED)
            element_relative_x = element_box['x'] - container_left
            
            # Validate and fix coordinate system issues
            if element_relative_x < 0:
                self.logger.warning(f"⚠️ Element position negative: {element_relative_x}, fixing to 0")
                element_relative_x = 0
            elif element_relative_x > container_width:
                self.logger.warning(f"⚠️ Element position exceeds container: {element_relative_x} > {container_width}, fixing")
                element_relative_x = container_width - 10  # Leave 10px margin
            
            self.logger.info(f"🔧 COORDINATE SYSTEM FIXED:")
            self.logger.info(f"   Container absolute X: {container_left}")
            self.logger.info(f"   Container width: {container_width}")
            self.logger.info(f"   Element absolute X: {element_box['x']}")
            self.logger.info(f"   Element relative X: {element_relative_x}")
            
            # Step 5: Apply EXACT mathematical formula from puzzle.md (FIXED!)
            # CORRECT Formula: Math.round((container_width - 63 - 20) / (container_width - 63) * current_position)
            # NOT: (container_width - 63 - 20) / (container_width - 63) * container_width (WRONG!)
            slider_width = self.math_constants.SLIDER_WIDTH  # c = 63
            success_threshold = self.math_constants.SUCCESS_THRESHOLD  # g = 20
            
            # Calculate target position using EXACT formula from puzzle.md line 7127
            target_position = (container_width - slider_width - success_threshold) / (container_width - slider_width)
            target_position = target_position * element_relative_x  # Multiply by CURRENT position, not container width
            
            # Apply Math.round for precision (as used in puzzle.md)
            target_position = round(target_position)
            
            # Ensure target position is within container bounds
            target_position = max(0, min(target_position, container_width - slider_width))
            
            # Calculate movement distance (relative to container)
            movement_distance = target_position - element_relative_x
            
            self.logger.info(f"🎯 CORRECTED MATHEMATICAL CALCULATIONS (puzzle.md line 7127):")
            self.logger.info(f"   Slider width (c): {slider_width}")
            self.logger.info(f"   Success threshold (g): {success_threshold}")
            self.logger.info(f"   Current position (a): {element_relative_x}")
            self.logger.info(f"   Target position (A): {target_position}")
            self.logger.info(f"   Movement distance: {movement_distance}")
            
            # Validate movement distance
            if abs(movement_distance) > container_width:
                self.logger.warning(f"⚠️ Movement distance ({movement_distance}) exceeds container width ({container_width})")
                # Adjust to reasonable bounds
                movement_distance = max(-container_width + 20, min(container_width - 20, movement_distance))
                self.logger.info(f"   Adjusted movement distance: {movement_distance}")
            
            self.scraping_stats["mathematical_calculations"] += 1
            self.scraping_stats["coordinate_system_fixed"] += 1
            
            # Step 6: Execute PRECISE targeting movement with STRATEGIC validation
            success = await self.execute_precise_targeting_movement(
                iframe, puzzle_element, movement_distance, target_position, container_left
            )
            
            if success:
                self.scraping_stats["successful_captcha_solves"] += 1
                self.logger.info("✅ CAPTCHA solved with WORKING mathematical precision!")
                return True
            else:
                self.logger.warning("⚠️ Working positioning movement failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Working mathematical CAPTCHA solving failed: {e}")
            self.scraping_stats["errors"].append(f"Working mathematical solving: {e}")
            return False

    async def execute_working_positioning_movement(self, iframe: Frame, puzzle_element: ElementHandle, 
                                                 movement_distance: float, target_position: float, container_left: float) -> bool:
        """
        🎯 Execute working positioning movement using STRATEGIC DOM event simulation
        AVOIDS Playwright mouse API to prevent _playwright_target_ detection events
        """
        try:
            self.logger.info("🎯 Executing STRATEGIC positioning movement (no Playwright mouse API)...")
            
            # Get current position for validation
            element_box = await puzzle_element.bounding_box()
            if not element_box:
                return False
            
            current_x = element_box['x']
            
            # Step 1: Create and dispatch mousedown event using STRATEGIC approach
            # This avoids triggering _playwright_target_ detection events
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create mousedown event with exact properties from puzzle.md
                    const mousedownEvent = new MouseEvent('mousedown', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 1
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(mousedownEvent);
                }
            """, [puzzle_element, current_x + 10, element_box['y'] + 10])
            
            # Natural timing delay (avoid solving too quickly)
            await asyncio.sleep(random.uniform(0.3, 0.6))
            
            # Step 2: Move to target position with natural movement timing
            steps = max(20, int(abs(movement_distance) / 3))  # More steps for natural movement
            
            for i in range(steps + 1):
                progress = i / steps
                current_x = element_box['x'] + (movement_distance * progress)
                
                # Apply Math.floor precision (as in puzzle.md)
                current_x = math.floor(current_x)
                
                # Create and dispatch mousemove event using STRATEGIC approach
                await iframe.evaluate("""
                    ([element, x, y]) => {
                        // Create mousemove event with exact properties from puzzle.md
                        const mousemoveEvent = new MouseEvent('mousemove', {
                            bubbles: true,
                            cancelable: true,
                            composed: true,
                            clientX: x,
                            clientY: y,
                            button: 0,
                            buttons: 1
                        });
                        
                        // Dispatch event directly on element (no Playwright API)
                        element.dispatchEvent(mousemoveEvent);
                    }
                """, [puzzle_element, current_x + 10, element_box['y'] + 10])
                
                # Natural movement timing (avoid too fast movement)
                await asyncio.sleep(random.uniform(0.02, 0.05))
            
            # Step 3: Final position adjustment with natural timing
            final_x = math.floor(container_left + target_position)
            
            # Create and dispatch final mousemove event
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create final mousemove event with exact properties
                    const finalMousemoveEvent = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 1
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(finalMousemoveEvent);
                }
            """, [puzzle_element, final_x + 10, element_box['y'] + 10])
            
            # Natural timing delay before release
            await asyncio.sleep(random.uniform(0.2, 0.4))
            
            # Step 4: Create and dispatch mouseup event using STRATEGIC approach
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create mouseup event with exact properties from puzzle.md
                    const mouseupEvent = new MouseEvent('mouseup', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 0
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(mouseupEvent);
                }
            """, [puzzle_element, final_x + 10, element_box['y'] + 10])
            
            # Natural timing delay after release (avoid solving too quickly)
            await asyncio.sleep(random.uniform(0.4, 0.8))
            
            # Step 5: Validate final position
            final_box = await puzzle_element.bounding_box()
            if final_box:
                final_position = final_box['x'] - container_left  # Convert to relative
                position_difference = abs(final_position - target_position)
                
                self.logger.info(f"🎯 POSITION VALIDATION:")
                self.logger.info(f"   Final absolute position: {final_box['x']}")
                self.logger.info(f"   Final relative position: {final_position}")
                self.logger.info(f"   Target position: {target_position}")
                self.logger.info(f"   Position difference: {position_difference}")
                
                # Check if within success threshold (5 pixels as per puzzle.md)
                if position_difference <= 5:
                    self.logger.info("✅ Perfect positioning achieved! Position difference: ≤5px")
                    return True
                else:
                    self.logger.warning(f"⚠️ Position not perfect. Difference: {position_difference}px")
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Strategic positioning movement failed: {e}")
            self.scraping_stats["errors"].append(f"Strategic positioning: {e}")
            return False

    async def validate_captcha_success_working(self, iframe: Frame) -> bool:
        """
        ✅ Validate CAPTCHA success using working methods
        """
        try:
            self.logger.info("✅ Validating CAPTCHA success with working methods...")
            
            # Wait for potential success signals
            await asyncio.sleep(3)
            
            # Check for success indicators
            success_indicators = [
                "iframe disappearance",
                "success message",
                "redirect to target page",
                "puzzle completion signal"
            ]
            
            # Check if iframe is still accessible
            try:
                await iframe.query_selector("i.sliderIcon")
                iframe_accessible = True
            except:
                iframe_accessible = False
            
            if not iframe_accessible:
                self.logger.info("✅ CAPTCHA iframe no longer accessible - likely success!")
                return True
            
            # Check for success text or completion signals
            success_text_selectors = [
                ".success",
                ".completed", 
                ".verified",
                ".passed"
            ]
            
            for selector in success_text_selectors:
                success_element = await iframe.query_selector(selector)
                if success_element:
                    self.logger.info(f"✅ Success indicator found: {selector}")
                    return True
            
            # Check if we're redirected away from challenge page
            current_url = self.page.url
            if "challenge" not in current_url.lower() and "captcha" not in current_url.lower():
                self.logger.info("✅ Redirected away from challenge page - success!")
                return True
            
            self.logger.warning("⚠️ CAPTCHA success not confirmed")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Success validation failed: {e}")
            self.scraping_stats["errors"].append(f"Success validation: {e}")
            return False

    async def extract_enhanced_g2_data(self) -> bool:
        """
        🔍 Extract enhanced G2.com data using comprehensive parsing
        """
        try:
            self.logger.info("🔍 Extracting enhanced G2.com data...")
            
            # Wait for content to load
            await asyncio.sleep(2)
            
            # Get the final page content
            final_content = await self.page.content()
            
            # Check if we're still on challenge page
            if "challenge" in final_content.lower() or "captcha" in final_content.lower():
                self.logger.warning("🛡️ Still on challenge page")
                return False
            
            # Extract and log content size
            content_size = len(final_content)
            self.logger.info(f"📄 Final content size: {content_size} characters")
            
            # Parse the content for G2.com data
            parsed_data = await self.parse_enhanced_g2_content(final_content, self.page.url)
            
            if parsed_data:
                self.logger.info("✅ Successfully extracted G2.com data")
                self.logger.info(f"   Title: {parsed_data.get('title', 'N/A')}")
                self.logger.info(f"   Products found: {len(parsed_data.get('products', []))}")
                self.logger.info(f"   AI Summary: {parsed_data.get('ai_summary', 'N/A')[:100]}...")
                
                self.scraping_stats["successful_data_extractions"] += 1
                return True
            else:
                self.logger.warning("⚠️ No G2.com data extracted")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Data extraction failed: {e}")
            self.scraping_stats["errors"].append(f"Data extraction: {e}")
            return False

    async def parse_enhanced_g2_content(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """
        🔍 Parse enhanced G2.com content for comprehensive data extraction
        """
        try:
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "G2.com Comparison"
            
            # Extract products
            products = []
            product_patterns = [
                r'<h3[^>]*class="[^"]*product-name[^"]*"[^>]*>([^<]+)</h3>',
                r'<div[^>]*class="[^"]*product-title[^"]*"[^>]*>([^<]+)</div>',
                r'<span[^>]*class="[^"]*product-name[^"]*"[^>]*>([^<]+)</span>'
            ]
            
            for pattern in product_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                products.extend([match.strip() for match in matches if match.strip()])
            
            # Extract AI summary
            ai_summary = ""
            ai_patterns = [
                r'<div[^>]*class="[^"]*ai-summary[^"]*"[^>]*>([^<]+)</div>',
                r'<p[^>]*class="[^"]*summary[^"]*"[^>]*>([^<]+)</p>',
                r'<div[^>]*class="[^"]*description[^"]*"[^>]*>([^<]+)</div>'
            ]
            
            for pattern in ai_patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    ai_summary = match.group(1).strip()
                    break
            
            # Extract ratings
            ratings = []
            rating_patterns = [
                r'<span[^>]*class="[^"]*rating[^"]*"[^>]*>([^<]+)</span>',
                r'<div[^>]*class="[^"]*score[^"]*"[^>]*>([^<]+)</div>'
            ]
            
            for pattern in rating_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                ratings.extend([match.strip() for match in matches if match.strip()])
            
            return {
                "url": url,
                "title": title,
                "products": list(set(products))[:10],  # Limit to 10 unique products
                "ai_summary": ai_summary,
                "ratings": list(set(ratings))[:5],  # Limit to 5 unique ratings
                "extraction_timestamp": datetime.now().isoformat(),
                "content_size": len(html)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Content parsing failed: {e}")
            return None

    async def monitor_strategic_success_signals(self, iframe: Frame) -> bool:
        """
        🔍 Monitor for STRATEGIC success signals from puzzle.md analysis
        Watches for _hitTargetInterceptor cleanup and success signals
        """
        try:
            self.logger.info("🔍 Monitoring for STRATEGIC success signals...")
            
            # Wait for potential success signals with natural timing
            await asyncio.sleep(random.uniform(2, 4))
            
            # Step 1: Check for _hitTargetInterceptor cleanup (success signal from puzzle.md)
            try:
                interceptor_status = await iframe.evaluate("""
                    () => {
                        // Check if _hitTargetInterceptor has been cleared (void 0)
                        if (typeof window._hitTargetInterceptor !== 'undefined') {
                            return window._hitTargetInterceptor === void 0 ? 'cleared' : 'active';
                        }
                        return 'not_found';
                    }
                """)
                
                if interceptor_status == 'cleared':
                    self.logger.info("✅ STRATEGIC SUCCESS: _hitTargetInterceptor cleared (void 0)")
                    return True
                elif interceptor_status == 'active':
                    self.logger.info("⚠️ _hitTargetInterceptor still active")
                else:
                    self.logger.info("ℹ️ _hitTargetInterceptor not found in window scope")
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Could not check _hitTargetInterceptor: {e}")
            
            # Step 2: Check for success return signals ("done" or { stop })
            try:
                success_signals = await iframe.evaluate("""
                    () => {
                        // Look for success signals in the page context
                        const successIndicators = [];
                        
                        // Check for "done" signal
                        if (window.done === true || window.done === "done") {
                            successIndicators.push("done");
                        }
                        
                        // Check for { stop } signal
                        if (window.stop === true || (window.stop && window.stop.stop === true)) {
                            successIndicators.push("stop");
                        }
                        
                        // Check for success text in DOM
                        const successElements = document.querySelectorAll('.success, .completed, .verified, .passed');
                        if (successElements.length > 0) {
                            successIndicators.push("dom_success");
                        }
                        
                        return successIndicators;
                    }
                """)
                
                if success_signals:
                    self.logger.info(f"✅ STRATEGIC SUCCESS signals found: {success_signals}")
                    return True
                    
            except Exception as e:
                self.logger.warning(f"⚠️ Could not check success signals: {e}")
            
            # Step 3: Check if iframe is still accessible (iframe disappearance = success)
            try:
                await iframe.query_selector("i.sliderIcon")
                iframe_accessible = True
            except:
                iframe_accessible = False
            
            if not iframe_accessible:
                self.logger.info("✅ STRATEGIC SUCCESS: CAPTCHA iframe no longer accessible")
                return True
            
            # Step 4: Check if we're redirected away from challenge page
            current_url = self.page.url
            if "challenge" not in current_url.lower() and "captcha" not in current_url.lower():
                self.logger.info("✅ STRATEGIC SUCCESS: Redirected away from challenge page")
                return True
            
            self.logger.warning("⚠️ No STRATEGIC success signals detected")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Strategic success monitoring failed: {e}")
            self.scraping_stats["errors"].append(f"Strategic success monitoring: {e}")
            return False

    async def validate_descendant_target(self, iframe: Frame, hit_point: Dict[str, float], target_element: ElementHandle) -> bool:
        """
        🔍 Validate descendant target check (ANTI_BOT_RULEBOOK Phase 2e and 2i)
        Ensures hit target is always a descendant of target element
        """
        try:
            # Use the page's own elementFromPoint logic (as in puzzle.md)
            hit_element = await iframe.evaluate("""
                ([x, y]) => {
                    // Use the same logic as the page for elementFromPoint
                    const element = document.elementFromPoint(x, y);
                    return element ? element.tagName + '.' + (element.className || '') : 'none';
                }
            """, [hit_point['x'], hit_point['y']])
            
            # Check if hit element is descendant of target element
            is_descendant = await iframe.evaluate("""
                ([hitElementSelector, targetElement]) => {
                    const hitElement = document.querySelector(hitElementSelector);
                    if (!hitElement || !targetElement) return false;
                    
                    // Check if hit element is descendant of target element
                    return targetElement.contains(hitElement) || targetElement === hitElement;
                }
            """, [hit_element, target_element])
            
            if is_descendant:
                self.logger.info(f"✅ Descendant validation passed: {hit_element}")
                return True
            else:
                self.logger.warning(f"⚠️ Descendant validation failed: {hit_element}")
                return False
                
        except Exception as e:
            self.logger.warning(f"⚠️ Descendant validation error: {e}")
            return False

    async def execute_precise_targeting_movement(self, iframe: Frame, puzzle_element: ElementHandle, 
                                               movement_distance: float, target_position: float, container_left: float) -> bool:
        """
        🎯 Execute PRECISE targeting movement with ANTI_BOT_RULEBOOK compliance
        Ensures puzzle piece hits the exact correct target area
        """
        try:
            self.logger.info("🎯 Executing PRECISE targeting movement (ANTI_BOT_RULEBOOK compliant)...")
            
            # Get current position for validation
            element_box = await puzzle_element.bounding_box()
            if not element_box:
                return False
            
            current_x = element_box['x']
            current_y = element_box['y']
            
            # Step 1: mousemove to target area (ANTI_BOT_RULEBOOK Phase 2h)
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create mousemove event with exact properties from rulebook
                    const mousemoveEvent = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 0
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(mousemoveEvent);
                }
            """, [puzzle_element, current_x + 10, current_y + 10])
            
            # Natural timing delay (avoid solving too quickly)
            await asyncio.sleep(random.uniform(0.3, 0.6))
            
            # Step 2: mousedown on puzzle piece (ANTI_BOT_RULEBOOK Phase 2h)
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create mousedown event with exact properties from rulebook
                    const mousedownEvent = new MouseEvent('mousedown', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 1
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(mousedownEvent);
                }
            """, [puzzle_element, current_x + 10, current_y + 10])
            
            # Natural timing delay
            await asyncio.sleep(random.uniform(0.2, 0.4))
            
            # Step 3: mousemove to final position with CONTINUOUS VALIDATION (ANTI_BOT_RULEBOOK Phase 2i)
            steps = max(25, int(abs(movement_distance) / 2))  # More steps for precise targeting
            
            for i in range(steps + 1):
                progress = i / steps
                current_x = element_box['x'] + (movement_distance * progress)
                
                # Apply Math.round precision (as in puzzle.md)
                current_x = round(current_x)
                
                # Validate hit target is descendant of target element (ANTI_BOT_RULEBOOK Phase 2i)
                hit_point = {'x': current_x + 10, 'y': current_y + 10}
                if not await self.validate_descendant_target(iframe, hit_point, puzzle_element):
                    self.logger.warning(f"⚠️ Descendant validation failed at step {i}, stopping movement")
                    break
                
                # Create and dispatch mousemove event using STRATEGIC approach
                await iframe.evaluate("""
                    ([element, x, y]) => {
                        // Create mousemove event with exact properties from rulebook
                        const mousemoveEvent = new MouseEvent('mousemove', {
                            bubbles: true,
                            cancelable: true,
                            composed: true,
                            clientX: x,
                            clientY: y,
                            button: 0,
                            buttons: 1
                        });
                        
                        // Dispatch event directly on element (no Playwright API)
                        element.dispatchEvent(mousemoveEvent);
                    }
                """, [puzzle_element, current_x + 10, current_y + 10])
                
                # Natural movement timing (avoid too fast movement)
                await asyncio.sleep(random.uniform(0.02, 0.04))
            
            # Step 4: Final position adjustment for PERFECT targeting
            final_x = round(container_left + target_position)
            
            # Validate final position hit target
            final_hit_point = {'x': final_x + 10, 'y': current_y + 10}
            if not await self.validate_descendant_target(iframe, final_hit_point, puzzle_element):
                self.logger.warning("⚠️ Final position descendant validation failed")
                return False
            
            # Create and dispatch final mousemove event
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create final mousemove event with exact properties
                    const finalMousemoveEvent = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 1
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(finalMousemoveEvent);
                }
            """, [puzzle_element, final_x + 10, current_y + 10])
            
            # Natural timing delay before release
            await asyncio.sleep(random.uniform(0.2, 0.4))
            
            # Step 5: mouseup on target area (ANTI_BOT_RULEBOOK Phase 2h)
            await iframe.evaluate("""
                ([element, x, y]) => {
                    // Create mouseup event with exact properties from rulebook
                    const mouseupEvent = new MouseEvent('mouseup', {
                        bubbles: true,
                        cancelable: true,
                        composed: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 0
                    });
                    
                    // Dispatch event directly on element (no Playwright API)
                    element.dispatchEvent(mouseupEvent);
                }
            """, [puzzle_element, final_x + 10, current_y + 10])
            
            # Natural timing delay after release (avoid solving too quickly)
            await asyncio.sleep(random.uniform(0.4, 0.8))
            
            # Step 6: Validate final position
            final_box = await puzzle_element.bounding_box()
            if final_box:
                final_position = final_box['x'] - container_left  # Convert to relative
                position_difference = abs(final_position - target_position)
                
                self.logger.info(f"🎯 PRECISE TARGETING VALIDATION:")
                self.logger.info(f"   Final absolute position: {final_box['x']}")
                self.logger.info(f"   Final relative position: {final_position}")
                self.logger.info(f"   Target position: {target_position}")
                self.logger.info(f"   Position difference: {position_difference}")
                
                # Check if within success threshold (5 pixels as per puzzle.md)
                if position_difference <= 5:
                    self.logger.info("✅ PERFECT targeting achieved! Position difference: ≤5px")
                    return True
                else:
                    self.logger.warning(f"⚠️ Targeting not perfect. Difference: {position_difference}px")
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Precise targeting movement failed: {e}")
            self.scraping_stats["errors"].append(f"Precise targeting: {e}")
            return False

    async def bypass_g2_with_working_mathematics(self, url: str) -> bool:
        """
        🌐 Bypass G2.com using WORKING MATHEMATICAL strategy
        Implements exact mathematical functions from puzzle.md with FIXED coordinate system
        """
        try:
            self.logger.info(f"🌐 Navigating to: {url}")
            
            # Navigate to the target URL
            await self.page.goto(url, wait_until="networkidle")
            await asyncio.sleep(random.uniform(2, 4))
            
            # Step 1: Detect and access CAPTCHA iframe using proven methods
            iframe = await self.detect_and_access_captcha_iframe()
            if not iframe:
                self.logger.info("✅ No CAPTCHA detected, proceeding with data extraction")
                # Extract data directly if no CAPTCHA
                return await self.extract_enhanced_g2_data()
            
            # Step 2: Solve CAPTCHA using working mathematical functions
            captcha_solved = await self.solve_captcha_with_working_mathematics(iframe)
            if not captcha_solved:
                self.logger.error("❌ CAPTCHA solving failed")
                return False
            
            # Step 3: Validate success using STRATEGIC methods from puzzle.md analysis
            success_validated = await self.monitor_strategic_success_signals(iframe)
            if not success_validated:
                self.logger.warning("⚠️ CAPTCHA success not validated with STRATEGIC methods")
                return False
            
            # Step 4: Extract enhanced G2.com data
            data_extracted = await self.extract_enhanced_g2_data()
            if not data_extracted:
                self.logger.error("❌ Data extraction failed after CAPTCHA solve")
                return False
            
            self.logger.info("🎉 SUCCESS: G2.com bypassed with WORKING mathematical precision!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Working mathematical bypass failed: {e}")
            self.scraping_stats["errors"].append(f"Working mathematical bypass: {e}")
            return False

    async def run_working_captcha_tests(self) -> List[Dict[str, Any]]:
        """
        🚀 Run WORKING CAPTCHA solver tests with comprehensive metrics tracking
        """
        self.logger.info("🚀 Starting WORKING CAPTCHA solver tests...")
        
        test_urls = [
            "https://www.g2.com/compare/notion-vs-obsidian",
            "https://www.g2.com/compare/notion-vs-obsidian?p=1",
            "https://www.g2.com/compare/notion-vs-obsidian?p=2"
        ]
        
        total_tests = len(test_urls)
        
        for test_num, url in enumerate(test_urls, 1):
            self.logger.info(f"🎯 Test {test_num}/{total_tests}: {url}")
            
            # Track test execution
            start_time = time.time()
            
            try:
                # Execute the working mathematical strategy
                success = await self.bypass_g2_with_working_mathematics(url)
                
                # Calculate execution time
                execution_time = time.time() - start_time
                
                # Record test result
                test_result = {
                    "url": url,
                    "success": success,
                    "execution_time": execution_time,
                    "captcha_detected": self.scraping_stats["captcha_detected"] > 0,
                    "iframe_accessed": self.scraping_stats["iframe_access_success"] > 0,
                    "mathematical_calculations": self.scraping_stats["mathematical_calculations"] > 0,
                    "coordinate_system_fixed": self.scraping_stats["coordinate_system_fixed"] > 0,
                    "captcha_solved": self.scraping_stats["successful_captcha_solves"] > 0,
                    "data_extracted": self.scraping_stats["successful_data_extractions"] > 0,
                    "errors": self.scraping_stats["errors"][-3:] if self.scraping_stats["errors"] else []
                }
                
                self.test_results.append(test_result)
                
                # Update overall execution time
                self.scraping_stats["execution_time"] += execution_time
                
                # Log test result
                if success:
                    self.logger.info(f"✅ Test {test_num} SUCCESS in {execution_time:.2f}s")
                else:
                    self.logger.warning(f"⚠️ Test {test_num} FAILED in {execution_time:.2f}s")
                
                # Wait between tests
                if test_num < total_tests:
                    await asyncio.sleep(random.uniform(3, 5))
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.logger.error(f"❌ Test {test_num} EXCEPTION: {e}")
                
                test_result = {
                    "url": url,
                    "success": False,
                    "execution_time": execution_time,
                    "error": str(e),
                    "captcha_detected": False,
                    "iframe_accessed": False,
                    "mathematical_calculations": False,
                    "coordinate_system_fixed": False,
                    "captcha_solved": False,
                    "data_extracted": False
                }
                
                self.test_results.append(test_result)
                self.scraping_stats["errors"].append(f"Test {test_num}: {e}")
        
        self.logger.info("🏁 All WORKING CAPTCHA tests completed!")
        return self.test_results

    def export_results(self) -> str:
        """
        📊 Export comprehensive results with working mathematical metrics
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Export comprehensive results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/working_captcha_solver_results_{timestamp}.json"
            
            results_data = {
                "test_summary": {
                    "total_tests": len(self.test_results),
                    "captcha_detection_rate": (self.scraping_stats["captcha_detected"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "iframe_access_rate": (self.scraping_stats["iframe_access_success"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "mathematical_calculations_rate": (self.scraping_stats["mathematical_calculations"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "coordinate_system_fixed_rate": (self.scraping_stats["coordinate_system_fixed"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "captcha_solve_rate": (self.scraping_stats["successful_captcha_solves"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "data_extraction_rate": (self.scraping_stats["successful_data_extractions"] / len(self.test_results)) * 100 if self.test_results else 0,
                    "average_execution_time": self.scraping_stats["execution_time"] / len(self.test_results) if self.test_results else 0
                },
                "mathematical_constants": {
                    "slider_width": self.math_constants.SLIDER_WIDTH,
                    "success_threshold": self.math_constants.SUCCESS_THRESHOLD,
                    "max_offset": self.math_constants.MAX_OFFSET
                },
                "scraping_stats": self.scraping_stats,
                "test_results": self.test_results,
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(results_data, f, indent=2)
            
            self.logger.info(f"📊 Results exported to: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"❌ Results export failed: {e}")
            return ""

    async def cleanup(self):
        """
        🧹 Cleanup resources
        """
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.logger.info("✅ Cleanup completed")
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")

async def main():
    """
    🚀 Main execution function
    """
    solver = WorkingCaptchaSolver()
    
    try:
        # Setup working browser
        await solver.setup_working_browser()
        
        # Run comprehensive tests
        results = await solver.run_working_captcha_tests()
        
        # Export results
        results_file = solver.export_results()
        
        # Display final results
        logger.info("📊 WORKING CAPTCHA SOLVER - FINAL RESULTS:")
        logger.info(f"   Total Tests: {len(solver.test_results)}")
        logger.info(f"   CAPTCHA Detection Rate: {solver.scraping_stats['captcha_detected'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   Iframe Access Rate: {solver.scraping_stats['iframe_access_success'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   Mathematical Calculations: {solver.scraping_stats['mathematical_calculations'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   Coordinate System Fixed: {solver.scraping_stats['coordinate_system_fixed'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   CAPTCHA Solve Rate: {solver.scraping_stats['successful_captcha_solves'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   Data Extraction Rate: {solver.scraping_stats['successful_data_extractions'] / len(solver.test_results) * 100:.1f}%")
        logger.info(f"   Average Execution Time: {solver.scraping_stats['execution_time'] / len(solver.test_results):.2f}s")
        
        if solver.scraping_stats["errors"]:
            logger.warning(f"⚠️ Errors encountered: {len(solver.scraping_stats['errors'])}")
            for error in solver.scraping_stats["errors"][-3:]:  # Show last 3 errors
                logger.warning(f"   {error}")
        
        logger.info(f"📁 Detailed results saved to: {results_file}")
        
    except Exception as e:
        logger.error(f"❌ Main execution failed: {e}")
    finally:
        await solver.cleanup()

if __name__ == "__main__":
    import re
    logger = logging.getLogger(__name__)
    asyncio.run(main())
