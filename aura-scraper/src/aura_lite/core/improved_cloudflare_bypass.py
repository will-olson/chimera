"""
Improved Cloudflare Bypass Strategy
Enhanced bypass techniques based on test learnings
"""

import asyncio
import time
import random
import logging
from typing import Dict, Any, Optional
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class ImprovedCloudflareBypass:
    """Improved Cloudflare bypass with enhanced strategies"""
    
    def __init__(self):
        self.cloudflare_indicators = [
            'checking your browser',
            'cloudflare',
            'ray id',
            'please wait',
            'ddos protection',
            'security check',
            'just a moment',
            'verifying you are human',
            'browser check',
            'ddos-guard',
            'checking browser',
            'please wait while we check your browser',
            'one moment please',
            'loading...',
            'please stand by'
        ]
        
        self.bypass_strategies = [
            'wait_and_retry',
            'human_behavior_simulation',
            'page_refresh',
            'user_agent_rotation',
            'stealth_enhancement'
        ]
        
        self.bypass_attempts = 0
        self.max_bypass_attempts = 3
        self.bypass_history = []
    
    async def enhanced_cloudflare_bypass(self, page: Page, max_wait: int = 60) -> bool:
        """Enhanced Cloudflare bypass with multiple strategies"""
        start_time = time.time()
        logger.info(f"Starting enhanced Cloudflare bypass (max wait: {max_wait}s)")
        
        # Strategy 1: Initial detection and wait
        if await self._initial_bypass_attempt(page, max_wait // 3):
            return True
        
        # Strategy 2: Human behavior simulation
        if await self._human_behavior_bypass(page, max_wait // 3):
            return True
        
        # Strategy 3: Page refresh and retry
        if await self._refresh_and_retry_bypass(page, max_wait // 3):
            return True
        
        logger.warning(f"All bypass strategies failed after {time.time() - start_time:.1f}s")
        return False
    
    async def _initial_bypass_attempt(self, page: Page, max_wait: int) -> bool:
        """Initial bypass attempt with enhanced waiting"""
        logger.info("Strategy 1: Initial bypass attempt with enhanced waiting")
        
        start_time = time.time()
        last_page_length = 0
        stable_count = 0
        
        while time.time() - start_time < max_wait:
            try:
                page_source = await page.content()
                current_length = len(page_source)
                
                # Check for Cloudflare indicators
                protection_detected = any(indicator in page_source.lower() for indicator in self.cloudflare_indicators)
                
                if protection_detected:
                    logger.debug("Cloudflare protection still active, waiting...")
                    await asyncio.sleep(5)  # Wait longer for protection to clear
                    continue
                
                # Check for page stability
                if current_length == last_page_length:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_page_length = current_length
                
                # If page is stable and has substantial content
                if stable_count >= 3 and current_length > 2000:
                    # Additional validation - check for expected content
                    if any(indicator in page_source.lower() for indicator in ['capterra', 'reviews', 'rating', 'product']):
                        logger.info("Initial bypass successful - page stable with expected content")
                        return True
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.debug(f"Error in initial bypass attempt: {str(e)}")
                await asyncio.sleep(3)
                continue
        
        logger.warning("Initial bypass attempt failed")
        return False
    
    async def _human_behavior_bypass(self, page: Page, max_wait: int) -> bool:
        """Human behavior simulation bypass"""
        logger.info("Strategy 2: Human behavior simulation bypass")
        
        try:
            # Simulate human behavior
            await self._simulate_human_interactions(page)
            
            # Wait and check again
            start_time = time.time()
            while time.time() - start_time < max_wait:
                page_source = await page.content()
                
                if not any(indicator in page_source.lower() for indicator in self.cloudflare_indicators):
                    if len(page_source) > 2000:
                        logger.info("Human behavior bypass successful")
                        return True
                
                await asyncio.sleep(3)
            
            logger.warning("Human behavior bypass failed")
            return False
            
        except Exception as e:
            logger.error(f"Error in human behavior bypass: {str(e)}")
            return False
    
    async def _refresh_and_retry_bypass(self, page: Page, max_wait: int) -> bool:
        """Page refresh and retry bypass"""
        logger.info("Strategy 3: Page refresh and retry bypass")
        
        try:
            # Refresh the page
            await page.reload(wait_until='domcontentloaded')
            await asyncio.sleep(5)
            
            # Wait for bypass
            start_time = time.time()
            while time.time() - start_time < max_wait:
                page_source = await page.content()
                
                if not any(indicator in page_source.lower() for indicator in self.cloudflare_indicators):
                    if len(page_source) > 2000:
                        logger.info("Refresh and retry bypass successful")
                        return True
                
                await asyncio.sleep(3)
            
            logger.warning("Refresh and retry bypass failed")
            return False
            
        except Exception as e:
            logger.error(f"Error in refresh and retry bypass: {str(e)}")
            return False
    
    async def _simulate_human_interactions(self, page: Page):
        """Simulate human interactions to appear more natural"""
        try:
            # Random mouse movements
            for _ in range(3):
                x = await page.evaluate("Math.random() * window.innerWidth")
                y = await page.evaluate("Math.random() * window.innerHeight")
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Random scrolling
            scroll_amount = await page.evaluate("Math.random() * 500 + 100")
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # Random page interactions
            elements = await page.query_selector_all('div, p, span')
            if elements:
                random_element = random.choice(elements[:5])
                try:
                    await random_element.hover()
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                except:
                    pass
            
        except Exception as e:
            logger.debug(f"Error in human interactions: {str(e)}")
    
    async def detect_cloudflare_protection_enhanced(self, page: Page) -> Dict[str, Any]:
        """Enhanced Cloudflare protection detection"""
        try:
            page_source = (await page.content()).lower()
            current_url = page.url.lower()
            
            protection_info = {
                'is_protected': False,
                'protection_type': 'none',
                'indicators_found': [],
                'bypass_required': False,
                'confidence': 0.0,
                'page_length': len(page_source),
                'url_contains_capterra': 'capterra' in current_url
            }
            
            # Check for indicators
            detected_indicators = []
            for indicator in self.cloudflare_indicators:
                if indicator in page_source:
                    detected_indicators.append(indicator)
            
            protection_info['indicators_found'] = detected_indicators
            
            if detected_indicators:
                protection_info['is_protected'] = True
                protection_info['bypass_required'] = True
                protection_info['confidence'] = min(len(detected_indicators) / len(self.cloudflare_indicators), 1.0)
                
                # Determine protection type
                if 'checking your browser' in page_source:
                    protection_info['protection_type'] = 'browser_check'
                elif 'ddos protection' in page_source:
                    protection_info['protection_type'] = 'ddos_protection'
                elif 'security check' in page_source:
                    protection_info['protection_type'] = 'security_check'
                elif 'ray id' in page_source:
                    protection_info['protection_type'] = 'cloudflare_ray'
                else:
                    protection_info['protection_type'] = 'generic_protection'
            
            # Additional checks
            if len(page_source) < 1000:
                protection_info['confidence'] += 0.2  # Likely still loading
            
            if 'error' in page_source or 'blocked' in page_source:
                protection_info['protection_type'] = 'access_blocked'
                protection_info['confidence'] += 0.3
            
            return protection_info
            
        except Exception as e:
            logger.error(f"Error in enhanced protection detection: {str(e)}")
            return {
                'is_protected': False,
                'protection_type': 'detection_error',
                'indicators_found': [],
                'bypass_required': False,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_bypass_statistics(self) -> Dict[str, Any]:
        """Get bypass statistics"""
        if not self.bypass_history:
            return {
                'total_attempts': 0,
                'success_rate': 0.0,
                'average_duration': 0.0,
                'successful_bypasses': 0,
                'failed_bypasses': 0
            }
        
        successful_bypasses = [b for b in self.bypass_history if b.get('success', False)]
        failed_bypasses = [b for b in self.bypass_history if not b.get('success', False)]
        
        total_attempts = len(self.bypass_history)
        success_rate = len(successful_bypasses) / total_attempts if total_attempts > 0 else 0.0
        
        durations = [b.get('duration', 0) for b in successful_bypasses if b.get('duration')]
        average_duration = sum(durations) / len(durations) if durations else 0.0
        
        return {
            'total_attempts': total_attempts,
            'success_rate': success_rate,
            'average_duration': average_duration,
            'successful_bypasses': len(successful_bypasses),
            'failed_bypasses': len(failed_bypasses),
            'recent_attempts': self.bypass_history[-5:] if self.bypass_history else []
        }
