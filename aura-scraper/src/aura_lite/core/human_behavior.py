"""
HumanBehaviorSimulator - Human behavior simulation
Adapted from Chimera-Ultimate's NaturalMovementPatterns
"""

import asyncio
import random
import logging
from typing import List, Dict, Any
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class HumanBehaviorSimulator:
    """Human behavior simulation adapted from Chimera-Ultimate's NaturalMovementPatterns"""
    
    def __init__(self, page: Page):
        self.page = page
        self.movement_patterns = self._load_movement_patterns()
        self.timing_profiles = self._load_timing_profiles()
        self.behavior_history = []
    
    def _load_movement_patterns(self) -> List[Dict[str, Any]]:
        """Load movement patterns for natural behavior"""
        return [
            {'type': 'mouse_movement', 'count': (4, 8), 'range': (50, 900), 'delay': (0.3, 0.7)},
            {'type': 'scrolling', 'patterns': [(150, 0.5), (200, 0.8), (300, 1.2), (100, 0.4), (250, 0.9)]},
            {'type': 'thinking_pause', 'probability': 0.3, 'duration': (1.0, 2.0)},
            {'type': 'reading_pause', 'probability': 0.2, 'duration': (3.0, 8.0)},
            {'type': 'element_interaction', 'probability': 0.5, 'delay': (0.5, 1.0)}
        ]
    
    def _load_timing_profiles(self) -> Dict[str, Any]:
        """Load timing profiles for natural behavior"""
        return {
            'base_delay': (1.0, 3.0),
            'action_delay': (0.2, 0.6),
            'scroll_back_probability': 0.4,
            'scroll_back_amount': 50
        }
    
    async def simulate_natural_browsing(self) -> bool:
        """Simulate realistic human browsing behavior"""
        try:
            logger.info("Starting natural browsing simulation")
            
            # Random mouse movements
            await self._random_mouse_movements()
            
            # Natural scrolling patterns
            await self._natural_scrolling()
            
            # Timing variations
            await self._timing_variations()
            
            # Random page interactions
            await self._random_page_interactions()
            
            # Record behavior
            self.behavior_history.append({
                'timestamp': asyncio.get_event_loop().time(),
                'actions_performed': ['mouse_movement', 'scrolling', 'timing_variations', 'page_interactions'],
                'success': True
            })
            
            logger.info("Natural browsing simulation completed successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Error in human behavior simulation: {str(e)}")
            self.behavior_history.append({
                'timestamp': asyncio.get_event_loop().time(),
                'error': str(e),
                'success': False
            })
            return False
    
    async def _random_mouse_movements(self):
        """Generate random mouse movements with acceleration"""
        pattern = self.movement_patterns[0]  # mouse_movement pattern
        count = random.randint(*pattern['count'])
        range_x, range_y = pattern['range']
        delay_range = pattern['delay']
        
        logger.debug(f"Performing {count} random mouse movements")
        
        for i in range(count):
            x = random.randint(50, range_x)
            y = random.randint(50, range_y)
            
            # Simulate human-like mouse movement
            await self.page.mouse.move(x, y)
            delay = random.uniform(*delay_range)
            await asyncio.sleep(delay)
            
            # Sometimes pause longer (like human thinking)
            thinking_pattern = self.movement_patterns[2]  # thinking_pause
            if random.random() < thinking_pattern['probability']:
                thinking_duration = random.uniform(*thinking_pattern['duration'])
                await asyncio.sleep(thinking_duration)
    
    async def _natural_scrolling(self):
        """Simulate natural scrolling patterns"""
        scroll_pattern = self.movement_patterns[1]  # scrolling pattern
        patterns = scroll_pattern['patterns']
        
        logger.debug(f"Performing natural scrolling with {len(patterns)} patterns")
        
        for scroll_amount, delay in patterns:
            await self.page.evaluate(f"window.scrollBy(0, {scroll_amount});")
            await asyncio.sleep(delay)
            
            # Sometimes scroll back up slightly
            if random.random() < self.timing_profiles['scroll_back_probability']:
                back_amount = self.timing_profiles['scroll_back_amount']
                await self.page.evaluate(f"window.scrollBy(0, -{back_amount});")
                await asyncio.sleep(random.uniform(0.3, 0.6))
    
    async def _timing_variations(self):
        """Apply natural timing variations"""
        # Random delays between actions
        delay_range = self.timing_profiles['base_delay']
        delay = random.uniform(*delay_range)
        await asyncio.sleep(delay)
        
        # Sometimes longer pauses (like reading)
        reading_pattern = self.movement_patterns[3]  # reading_pause
        if random.random() < reading_pattern['probability']:
            reading_duration = random.uniform(*reading_pattern['duration'])
            logger.debug(f"Simulating reading pause: {reading_duration:.1f}s")
            await asyncio.sleep(reading_duration)
    
    async def _random_page_interactions(self):
        """Random page interactions to appear more human"""
        interaction_pattern = self.movement_patterns[4]  # element_interaction
        
        if random.random() < interaction_pattern['probability']:
            try:
                # Move mouse to random elements
                elements = await self.page.query_selector_all('div, p, span, a, button')
                if elements:
                    # Limit to first 10 elements to avoid performance issues
                    random_element = random.choice(elements[:10])
                    await random_element.hover()
                    
                    delay = random.uniform(*interaction_pattern['delay'])
                    await asyncio.sleep(delay)
                    
                    logger.debug("Performed random element hover interaction")
            except Exception as e:
                logger.debug(f"Element interaction failed (expected): {str(e)}")
    
    async def simulate_reading_behavior(self, duration_range: tuple = (2.0, 5.0)):
        """Simulate reading behavior with natural pauses"""
        duration = random.uniform(*duration_range)
        logger.debug(f"Simulating reading behavior for {duration:.1f}s")
        
        # Simulate reading with occasional small movements
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < duration:
            # Small mouse movements while "reading"
            if random.random() < 0.3:
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                await self.page.mouse.move(x, y)
            
            await asyncio.sleep(random.uniform(0.5, 1.5))
    
    async def simulate_form_interaction(self):
        """Simulate natural form interaction behavior"""
        try:
            # Look for common form elements
            form_elements = await self.page.query_selector_all('input, textarea, select, button')
            
            if form_elements:
                # Randomly interact with some form elements
                for element in random.sample(form_elements[:5], min(3, len(form_elements))):
                    try:
                        await element.hover()
                        await asyncio.sleep(random.uniform(0.2, 0.5))
                        
                        # Simulate typing delay for input fields
                        tag_name = await element.evaluate('el => el.tagName.toLowerCase()')
                        if tag_name in ['input', 'textarea']:
                            await asyncio.sleep(random.uniform(0.5, 1.0))
                            
                    except Exception:
                        continue
                        
                logger.debug("Simulated form interaction behavior")
        except Exception as e:
            logger.debug(f"Form interaction simulation failed: {str(e)}")
    
    def get_behavior_statistics(self) -> Dict[str, Any]:
        """Get behavior simulation statistics"""
        if not self.behavior_history:
            return {
                'total_simulations': 0,
                'success_rate': 0.0,
                'average_actions': 0.0
            }
        
        successful_simulations = [b for b in self.behavior_history if b.get('success', False)]
        total_simulations = len(self.behavior_history)
        success_rate = len(successful_simulations) / total_simulations if total_simulations > 0 else 0.0
        
        # Calculate average actions per simulation
        total_actions = sum(len(b.get('actions_performed', [])) for b in successful_simulations)
        average_actions = total_actions / len(successful_simulations) if successful_simulations else 0.0
        
        return {
            'total_simulations': total_simulations,
            'success_rate': success_rate,
            'average_actions': average_actions,
            'recent_simulations': self.behavior_history[-5:] if self.behavior_history else []
        }
