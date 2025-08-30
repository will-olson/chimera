"""Human behavior simulation for anti-detection."""
import asyncio
import random
from typing import Optional
from playwright.async_api import Page, BrowserContext
from loguru import logger


class HumanBehaviorSimulator:
    """Simulates realistic human browsing behavior to avoid detection."""
    
    def __init__(self, context: BrowserContext):
        self.context = context
        self.page: Optional[Page] = None
        
    async def set_page(self, page: Page):
        """Set the current page for behavior simulation."""
        self.page = page
        
    async def simulate_human_behavior(self, intensity: str = "medium"):
        """Simulate realistic human browsing behavior."""
        if not self.page:
            logger.warning("No page set for behavior simulation")
            return
            
        try:
            # Random mouse movements
            await self._random_mouse_movements(intensity)
            
            # Natural scrolling patterns
            await self._natural_scrolling(intensity)
            
            # Timing variations
            await self._timing_variations(intensity)
            
            # Random page interactions
            await self._random_page_interactions(intensity)
            
            logger.debug("Human behavior simulation completed")
            
        except Exception as e:
            logger.warning(f"Error in human behavior simulation: {e}")
    
    async def _random_mouse_movements(self, intensity: str):
        """Generate random mouse movements."""
        if not self.page:
            return
            
        # Determine number of movements based on intensity
        movement_counts = {"low": (2, 4), "medium": (4, 8), "high": (6, 12)}
        min_movements, max_movements = movement_counts.get(intensity, (4, 8))
        
        movements = random.randint(min_movements, max_movements)
        
        for _ in range(movements):
            try:
                # Get viewport size
                viewport = await self.page.viewport_size()
                if not viewport:
                    continue
                    
                # Generate random coordinates
                x = random.randint(100, viewport["width"] - 100)
                y = random.randint(100, viewport["height"] - 100)
                
                # Move mouse with realistic timing
                await self.page.mouse.move(x, y)
                
                # Random delay between movements
                delay = random.uniform(0.1, 0.5)
                await asyncio.sleep(delay)
                
                # Sometimes pause longer (like human thinking)
                if random.random() < 0.3:
                    think_delay = random.uniform(0.5, 2.0)
                    await asyncio.sleep(think_delay)
                    
            except Exception as e:
                logger.debug(f"Error in mouse movement: {e}")
                continue
    
    async def _natural_scrolling(self, intensity: str):
        """Simulate natural scrolling patterns."""
        if not self.page:
            return
            
        # Determine scroll patterns based on intensity
        scroll_patterns = {
            "low": [(100, 0.3), (150, 0.5)],
            "medium": [(150, 0.5), (200, 0.8), (300, 1.2), (100, 0.4)],
            "high": [(150, 0.5), (200, 0.8), (300, 1.2), (100, 0.4), (250, 0.9), (180, 0.6)]
        }
        
        patterns = scroll_patterns.get(intensity, scroll_patterns["medium"])
        
        for scroll_amount, delay in patterns:
            try:
                # Scroll down
                await self.page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(delay)
                
                # Sometimes scroll back up slightly (like human reading)
                if random.random() < 0.4:
                    back_scroll = random.randint(20, 80)
                    await self.page.mouse.wheel(0, -back_scroll)
                    await asyncio.sleep(random.uniform(0.2, 0.5))
                    
            except Exception as e:
                logger.debug(f"Error in scrolling: {e}")
                continue
    
    async def _timing_variations(self, intensity: str):
        """Add realistic timing variations."""
        # Base delays based on intensity
        base_delays = {"low": 0.5, "medium": 1.0, "high": 1.5}
        base_delay = base_delays.get(intensity, 1.0)
        
        # Add random variation
        variation = random.uniform(0.5, 1.5)
        total_delay = base_delay * variation
        
        await asyncio.sleep(total_delay)
    
    async def _random_page_interactions(self, intensity: str):
        """Perform random page interactions."""
        if not self.page:
            return
            
        # Determine interaction probability based on intensity
        interaction_prob = {"low": 0.2, "medium": 0.5, "high": 0.8}
        prob = interaction_prob.get(intensity, 0.5)
        
        if random.random() < prob:
            try:
                # Find random elements to interact with
                elements = await self.page.query_selector_all('div, p, span, button, a')
                if elements and len(elements) > 0:
                    # Select random element (limit to first 10 to avoid overwhelming)
                    random_element = random.choice(elements[:10])
                    
                    # Move mouse to element
                    await random_element.hover()
                    await asyncio.sleep(random.uniform(0.3, 1.0))
                    
                    # Sometimes click (rarely)
                    if random.random() < 0.1:
                        await random_element.click()
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                        
            except Exception as e:
                logger.debug(f"Error in page interaction: {e}")
    
    async def simulate_reading_behavior(self, scroll_speed: str = "medium"):
        """Simulate realistic reading behavior with scrolling."""
        if not self.page:
            return
            
        # Reading behavior patterns
        reading_patterns = {
            "slow": [(50, 2.0), (100, 3.0), (75, 2.5)],
            "medium": [(100, 1.5), (150, 2.0), (120, 1.8)],
            "fast": [(150, 1.0), (200, 1.5), (180, 1.2)]
        }
        
        patterns = reading_patterns.get(scroll_speed, reading_patterns["medium"])
        
        for scroll_amount, delay in patterns:
            try:
                # Scroll down slowly (like reading)
                await self.page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(delay)
                
                # Sometimes pause to "read" content
                if random.random() < 0.6:
                    read_pause = random.uniform(1.0, 3.0)
                    await asyncio.sleep(read_pause)
                    
            except Exception as e:
                logger.debug(f"Error in reading behavior: {e}")
                continue
    
    async def simulate_form_interaction(self):
        """Simulate realistic form interaction behavior."""
        if not self.page:
            return
            
        try:
            # Find form elements
            inputs = await self.page.query_selector_all('input, textarea, select')
            
            if inputs:
                for input_element in inputs[:3]:  # Limit to 3 inputs
                    try:
                        # Focus on input
                        await input_element.focus()
                        await asyncio.sleep(random.uniform(0.3, 0.8))
                        
                        # Sometimes type (rarely)
                        if random.random() < 0.1:
                            await input_element.type("test", delay=random.uniform(100, 200))
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            
                    except Exception as e:
                        logger.debug(f"Error interacting with input: {e}")
                        continue
                        
        except Exception as e:
            logger.debug(f"Error in form interaction: {e}")


class BehaviorProfile:
    """Predefined behavior profiles for different scenarios."""
    
    @staticmethod
    def get_profile(profile_name: str) -> dict:
        """Get behavior profile configuration."""
        profiles = {
            "stealth": {
                "mouse_movements": "high",
                "scrolling": "medium",
                "timing": "medium",
                "interactions": "low",
                "reading": "slow"
            },
            "aggressive": {
                "mouse_movements": "low",
                "scrolling": "fast",
                "timing": "low",
                "interactions": "low",
                "reading": "fast"
            },
            "natural": {
                "mouse_movements": "medium",
                "scrolling": "medium",
                "timing": "medium",
                "interactions": "medium",
                "reading": "medium"
            }
        }
        
        return profiles.get(profile_name, profiles["natural"])
