"""Cloudflare bypass and anti-detection module."""
import asyncio
import time
from typing import List, Dict, Any, Optional
from playwright.async_api import Page
from loguru import logger


class CloudflareBypass:
    """Advanced Cloudflare bypass with multiple detection methods."""
    
    def __init__(self, page: Page):
        self.page = page
        self.indicators = self._load_cloudflare_indicators()
        self.bypass_attempts = 0
        self.max_bypass_attempts = 3
        
    def _load_cloudflare_indicators(self) -> Dict[str, List[str]]:
        """Load Cloudflare detection indicators."""
        return {
            "primary": [
                "checking your browser",
                "cloudflare",
                "ray id",
                "please wait",
                "ddos protection",
                "security check",
                "verifying you are human"
            ],
            "secondary": [
                "access denied",
                "blocked",
                "unusual activity",
                "automated access",
                "bot detection",
                "captcha",
                "challenge page"
            ],
            "success": [
                "page loaded",
                "content visible",
                "main content",
                "product reviews",
                "company information"
            ]
        }
    
    async def wait_for_bypass(self, max_wait: int = 45, strategy: str = "comprehensive") -> bool:
        """Wait for Cloudflare to clear with multiple detection methods."""
        start_time = time.time()
        cloudflare_detected = False
        
        logger.info(f"Starting Cloudflare bypass with strategy: {strategy}")
        
        while time.time() - start_time < max_wait:
            try:
                # Check current page state
                page_source = await self.page.content()
                page_source_lower = page_source.lower()
                current_url = self.page.url.lower()
                
                # Detect Cloudflare presence
                if await self._detect_cloudflare(page_source_lower):
                    if not cloudflare_detected:
                        logger.info("Cloudflare protection detected, waiting for bypass...")
                        cloudflare_detected = True
                    
                    # Apply bypass strategy
                    if strategy == "comprehensive":
                        await self._apply_comprehensive_bypass()
                    elif strategy == "aggressive":
                        await self._apply_aggressive_bypass()
                    else:
                        await self._apply_basic_bypass()
                    
                    # Wait before next check
                    await asyncio.sleep(3)
                    continue
                
                # Check if page has loaded successfully
                if await self._validate_page_load(page_source_lower, current_url):
                    if cloudflare_detected:
                        logger.info("Cloudflare bypass successful - page loaded")
                    else:
                        logger.info("Page loaded successfully - no Cloudflare detected")
                    return True
                
                # Check for error pages
                if await self._detect_error_page(page_source_lower):
                    logger.warning("Error page detected during Cloudflare bypass")
                    return False
                
                # Progressive loading check
                if len(page_source) > 2000:
                    logger.debug("Page content growing, waiting for full load...")
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error during Cloudflare bypass: {e}")
                await asyncio.sleep(2)
                continue
        
        logger.warning(f"Cloudflare bypass timeout after {max_wait} seconds")
        return False
    
    async def _detect_cloudflare(self, page_source: str) -> bool:
        """Detect various Cloudflare protection states."""
        for indicator in self.indicators["primary"]:
            if indicator in page_source:
                return True
        return False
    
    async def _detect_error_page(self, page_source: str) -> bool:
        """Detect error or blocking pages."""
        for indicator in self.indicators["secondary"]:
            if indicator in page_source:
                return True
        return False
    
    async def _validate_page_load(self, page_source: str, current_url: str) -> bool:
        """Validate that page has loaded successfully."""
        # Check content length
        if len(page_source) < 2000:
            return False
        
        # Check for success indicators
        for indicator in self.indicators["success"]:
            if indicator in page_source:
                return True
        
        # Platform-specific validation
        if "g2.com" in current_url:
            return await self._validate_g2_page(page_source)
        elif "capterra.com" in current_url:
            return await self._validate_capterra_page(page_source)
        
        return False
    
    async def _validate_g2_page(self, page_source: str) -> bool:
        """Validate G2.com page load."""
        g2_indicators = [
            "product reviews",
            "g2 crowd",
            "rating",
            "reviews",
            "product information"
        ]
        
        for indicator in g2_indicators:
            if indicator in page_source.lower():
                return True
        return False
    
    async def _validate_capterra_page(self, page_source: str) -> bool:
        """Validate Capterra.com page load."""
        capterra_indicators = [
            "capterra",
            "software reviews",
            "product information",
            "rating",
            "reviews"
        ]
        
        for indicator in capterra_indicators:
            if indicator in page_source.lower():
                return True
        return False
    
    async def _apply_basic_bypass(self):
        """Apply basic Cloudflare bypass techniques."""
        try:
            # Wait for natural progression
            await asyncio.sleep(2)
            
            # Sometimes refresh the page
            if random.random() < 0.1:
                await self.page.reload()
                await asyncio.sleep(3)
                
        except Exception as e:
            logger.debug(f"Error in basic bypass: {e}")
    
    async def _apply_aggressive_bypass(self):
        """Apply aggressive Cloudflare bypass techniques."""
        try:
            # Multiple page interactions
            await self._simulate_human_interaction()
            
            # Sometimes clear cookies and retry
            if random.random() < 0.2:
                await self.page.context.clear_cookies()
                await self.page.reload()
                await asyncio.sleep(5)
                
        except Exception as e:
            logger.debug(f"Error in aggressive bypass: {e}")
    
    async def _apply_comprehensive_bypass(self):
        """Apply comprehensive Cloudflare bypass techniques."""
        try:
            # Human-like behavior simulation
            await self._simulate_human_interaction()
            
            # Wait for progressive loading
            await asyncio.sleep(random.uniform(2, 4))
            
            # Check for dynamic content loading
            await self._wait_for_dynamic_content()
            
            # Sometimes interact with page elements
            if random.random() < 0.3:
                await self._interact_with_page_elements()
                
        except Exception as e:
            logger.debug(f"Error in comprehensive bypass: {e}")
    
    async def _simulate_human_interaction(self):
        """Simulate human-like interactions to help bypass Cloudflare."""
        try:
            # Random mouse movements
            viewport = await self.page.viewport_size()
            if viewport:
                for _ in range(random.randint(2, 5)):
                    x = random.randint(100, viewport["width"] - 100)
                    y = random.randint(100, viewport["height"] - 100)
                    await self.page.mouse.move(x, y)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Random scrolling
            scroll_amount = random.randint(100, 300)
            await self.page.mouse.wheel(0, scroll_amount)
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
        except Exception as e:
            logger.debug(f"Error in human interaction simulation: {e}")
    
    async def _wait_for_dynamic_content(self):
        """Wait for dynamic content to load."""
        try:
            # Wait for network idle
            await self.page.wait_for_load_state("networkidle", timeout=10000)
        except:
            # Fallback: wait for a reasonable time
            await asyncio.sleep(3)
    
    async def _interact_with_page_elements(self):
        """Interact with page elements to appear more human-like."""
        try:
            # Find clickable elements
            elements = await self.page.query_selector_all('button, a, div[role="button"]')
            if elements and len(elements) > 0:
                # Select random element (limit to first 5)
                random_element = random.choice(elements[:5])
                
                # Hover over element
                await random_element.hover()
                await asyncio.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            logger.debug(f"Error in page element interaction: {e}")
    
    async def force_bypass(self) -> bool:
        """Force bypass Cloudflare with aggressive techniques."""
        logger.info("Attempting forced Cloudflare bypass...")
        
        try:
            # Clear all data
            await self.page.context.clear_cookies()
            await self.page.context.clear_permissions()
            
            # Reload with new session
            await self.page.reload()
            await asyncio.sleep(5)
            
            # Apply comprehensive bypass
            return await self.wait_for_bypass(max_wait=30, strategy="aggressive")
            
        except Exception as e:
            logger.error(f"Error in forced bypass: {e}")
            return False


# Import random for the bypass methods
import random
