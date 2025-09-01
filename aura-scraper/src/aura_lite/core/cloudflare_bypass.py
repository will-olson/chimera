"""
CloudflareBypassManager - Specialized Cloudflare bypass manager
Adapted from Chimera-Ultimate's frame persistence logic
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class CloudflareBypassManager:
    """Specialized Cloudflare bypass manager adapted from Chimera-Ultimate's frame persistence"""
    
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
            'please wait while we check your browser'
        ]
        self.bypass_attempts = 0
        self.max_bypass_attempts = 5
        self.bypass_success_rate = 0.0
        self.bypass_history = []
    
    async def wait_for_cloudflare_bypass(self, page: Page, max_wait: int = 45) -> bool:
        """Wait for Cloudflare to clear with multiple detection methods"""
        start_time = time.time()
        cloudflare_detected = False
        bypass_start = time.time()
        
        logger.info(f"Starting Cloudflare bypass detection (max wait: {max_wait}s)")
        
        while time.time() - start_time < max_wait:
            try:
                page_source = (await page.content()).lower()
                current_url = page.url.lower()
                
                # Check for various Cloudflare indicators
                for indicator in self.cloudflare_indicators:
                    if indicator in page_source:
                        if not cloudflare_detected:
                            logger.info(f"Cloudflare detected: {indicator}")
                            cloudflare_detected = True
                        await asyncio.sleep(3)  # Longer wait for Cloudflare
                        break
                else:
                    # No Cloudflare indicators found
                    if len(page_source) > 2000 and ('capterra' in page_source or 'content' in page_source):
                        bypass_duration = time.time() - bypass_start
                        logger.info(f"Page loaded successfully - Cloudflare cleared (took {bypass_duration:.1f}s)")
                        
                        # Record successful bypass
                        self.bypass_history.append({
                            'success': True,
                            'duration': bypass_duration,
                            'indicators_found': self._get_detected_indicators(page_source),
                            'timestamp': time.time()
                        })
                        
                        self.bypass_attempts += 1
                        return True
                    
                    # Check if we're still on a loading page
                    if len(page_source) < 1000:
                        await asyncio.sleep(2)
                        continue
                    
                    # Check for error pages
                    if any(error in page_source for error in ['error', 'blocked', 'access denied', 'forbidden']):
                        logger.warning("Error page detected")
                        self.bypass_history.append({
                            'success': False,
                            'error': 'error_page_detected',
                            'timestamp': time.time()
                        })
                        return False
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Error during Cloudflare bypass: {str(e)}")
                await asyncio.sleep(2)
                continue
        
        # Timeout
        bypass_duration = time.time() - bypass_start
        logger.warning(f"Cloudflare wait timeout after {bypass_duration:.1f}s")
        self.bypass_history.append({
            'success': False,
            'error': 'timeout',
            'duration': bypass_duration,
            'timestamp': time.time()
        })
        return False
    
    async def detect_cloudflare_protection(self, page: Page) -> Dict[str, Any]:
        """Detect various Cloudflare protection states"""
        try:
            page_source = (await page.content()).lower()
            current_url = page.url.lower()
            
            protection_info = {
                'is_protected': False,
                'protection_type': 'none',
                'indicators_found': [],
                'bypass_required': False,
                'confidence': 0.0
            }
            
            detected_indicators = self._get_detected_indicators(page_source)
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
            
            return protection_info
            
        except Exception as e:
            logger.error(f"Error detecting Cloudflare protection: {str(e)}")
            return {
                'is_protected': False,
                'protection_type': 'detection_error',
                'indicators_found': [],
                'bypass_required': False,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _get_detected_indicators(self, page_source: str) -> list:
        """Get list of detected Cloudflare indicators"""
        detected = []
        for indicator in self.cloudflare_indicators:
            if indicator in page_source:
                detected.append(indicator)
        return detected
    
    def get_bypass_statistics(self) -> Dict[str, Any]:
        """Get bypass statistics and success rate"""
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
        
        # Calculate average duration for successful bypasses
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
    
    async def enhanced_cloudflare_wait(self, page: Page, max_wait: int = 60) -> bool:
        """Enhanced Cloudflare bypass with progressive validation"""
        start_time = time.time()
        last_page_length = 0
        stable_count = 0
        
        logger.info(f"Starting enhanced Cloudflare bypass (max wait: {max_wait}s)")
        
        while time.time() - start_time < max_wait:
            try:
                page_source = await page.content()
                current_length = len(page_source)
                
                # Check for Cloudflare indicators
                protection_info = await self.detect_cloudflare_protection(page)
                
                if protection_info['is_protected']:
                    logger.info(f"Cloudflare protection detected: {protection_info['protection_type']}")
                    await asyncio.sleep(5)  # Wait longer for protection to clear
                    continue
                
                # Check for page stability (content not changing)
                if current_length == last_page_length:
                    stable_count += 1
                else:
                    stable_count = 0
                    last_page_length = current_length
                
                # If page is stable and has substantial content
                if stable_count >= 3 and current_length > 2000:
                    # Additional validation - check for expected content
                    if any(indicator in page_source.lower() for indicator in ['capterra', 'reviews', 'rating', 'product']):
                        bypass_duration = time.time() - start_time
                        logger.info(f"Enhanced bypass successful - page stable with expected content (took {bypass_duration:.1f}s)")
                        return True
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Error in enhanced bypass: {str(e)}")
                await asyncio.sleep(3)
                continue
        
        logger.warning(f"Enhanced Cloudflare bypass timeout after {max_wait}s")
        return False
