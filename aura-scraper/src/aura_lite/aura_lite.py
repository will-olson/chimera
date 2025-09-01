"""
AuraLite - Main AURA-LITE class
Adapted from ChimeraUltimate for targeted Capterra scraping
"""

import asyncio
import random
import logging
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from .core.cloudflare_bypass import CloudflareBypassManager
from .core.human_behavior import HumanBehaviorSimulator
from .managers.target_manager import CapterraTargetManager
from .managers.session_manager import SessionManager
from .extractors.data_extractor import CapterraDataExtractor

logger = logging.getLogger(__name__)

class AuraLite:
    """Main AURA-LITE class adapted from ChimeraUltimate"""
    
    def __init__(self, targets_file: str = 'capterra_sentiment_targets.json'):
        self.targets_file = targets_file
        self.target_manager = CapterraTargetManager(targets_file)
        self.session_manager = SessionManager()
        self.browser = None
        self.context = None
        self.page = None
        
        # Initialize components
        self.cloudflare_manager = CloudflareBypassManager()
        self.behavior_simulator = None
        self.data_extractor = None
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
    
    async def setup_aura_browser(self) -> bool:
        """Setup browser with Cloudflare-optimized options"""
        try:
            logger.info("Setting up AURA-LITE browser...")
            
            # Launch browser with stealth options
            self.browser = await async_playwright().start()
            browser = await self.browser.chromium.launch(
                headless=False,  # Set to True for production
                args=[
                    '--start-maximized',
                    '--disable-notifications',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--allow-running-insecure-content',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            )
            
            # Create context with stealth settings
            self.context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={'width': 1920, 'height': 1080},
                ignore_https_errors=True
            )
            
            # Create page
            self.page = await self.context.new_page()
            
            # Initialize components
            self.behavior_simulator = HumanBehaviorSimulator(self.page)
            self.data_extractor = CapterraDataExtractor(self.page)
            
            # Apply stealth measures
            await self._apply_stealth_measures()
            
            logger.info("AURA-LITE browser setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up AURA-LITE browser: {str(e)}")
            return False
    
    async def _apply_stealth_measures(self):
        """Apply stealth measures to avoid detection"""
        try:
            # Hide webdriver properties
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'});
                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
                Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            """)
            
            logger.debug("Stealth measures applied successfully")
            
        except Exception as e:
            logger.warning(f"Error applying stealth measures: {str(e)}")
    
    async def scrape_capterra_targets(self, max_competitors: int = 3) -> Dict[str, Any]:
        """Scrape Capterra targets with Cloudflare bypass"""
        try:
            logger.info(f"Starting AURA-LITE scraping of up to {max_competitors} competitors")
            
            # Get targets by priority
            targets = self.target_manager.get_targets_by_priority("high")
            limited_targets = targets[:max_competitors]
            
            self.session_manager.stats['total_targets'] = len(limited_targets)
            
            for i, target in enumerate(limited_targets):
                competitor_id = target['id']
                competitor_data = target['data']
                company_name = competitor_data['name']
                
                logger.info(f"Processing {company_name} ({competitor_id}) - {i+1}/{len(limited_targets)}")
                
                # Extract product reviews
                if 'product_reviews' in competitor_data['targets']:
                    review_data = await self.data_extractor.extract_product_reviews(
                        competitor_data['targets']['product_reviews'], 
                        company_name
                    )
                    
                    if 'error' not in review_data:
                        self.session_manager.add_scraped_data(competitor_id, review_data)
                        self.session_manager.update_stats(success=True)
                        logger.info(f"Successfully scraped reviews for {company_name}")
                        
                        # Extract alternatives if reviews successful
                        if 'alternatives' in competitor_data['targets']:
                            alternatives = await self._extract_alternatives(
                                competitor_data['targets']['alternatives'],
                                company_name
                            )
                            if alternatives:
                                self.session_manager.scraped_data[competitor_id]['alternatives'] = alternatives
                                logger.info(f"Found {len(alternatives)} alternatives for {company_name}")
                    else:
                        self.session_manager.update_stats(success=False, error=review_data.get('error'))
                        logger.error(f"Failed to scrape reviews for {company_name}")
                        
                        # If we get blocked, stop scraping
                        if 'Access blocked' in str(review_data.get('error', '')):
                            logger.error("Access blocked detected. Stopping scraping to avoid further detection.")
                            break
                
                # Enhanced delay between competitors
                if i < len(limited_targets) - 1:  # Don't delay after last competitor
                    delay = random.uniform(15, 25)  # 15-25 seconds
                    logger.info(f"Waiting {delay:.1f} seconds before next competitor...")
                    await asyncio.sleep(delay)
            
            logger.info(f"AURA-LITE scraping completed. Success: {self.session_manager.stats['successful_scrapes']}, Failed: {self.session_manager.stats['failed_scrapes']}")
            return self.session_manager.generate_session_report()
            
        except Exception as e:
            logger.error(f"Error in AURA-LITE scraping: {str(e)}")
            return {'error': str(e)}
    
    async def _extract_alternatives(self, url: str, company_name: str) -> List[Dict[str, Any]]:
        """Extract competitor alternatives"""
        try:
            logger.info(f"Scraping alternatives for {company_name} from {url}")
            await self.page.goto(url, wait_until='domcontentloaded')
            
            # Wait for Cloudflare
            if not await self.cloudflare_manager.wait_for_cloudflare_bypass(self.page):
                logger.warning("Cloudflare bypass failed for alternatives page")
                return []
            
            # Human-like behavior
            await self.behavior_simulator.simulate_natural_browsing()
            
            # Extract alternatives using data extractor
            alternatives = await self.data_extractor.extract_alternatives(url, company_name)
            return alternatives
            
        except Exception as e:
            logger.error(f"Error extracting alternatives for {company_name}: {str(e)}")
            return []
    
    async def test_single_competitor(self, competitor_id: str = None) -> Dict[str, Any]:
        """Test with single competitor for MVP validation"""
        try:
            if not competitor_id:
                # Get first high priority competitor
                targets = self.target_manager.get_targets_by_priority("high")
                if not targets:
                    return {'error': 'No high priority targets found'}
                competitor_id = targets[0]['id']
            
            target = self.target_manager.get_target_by_id(competitor_id)
            if not target:
                return {'error': f'Target not found: {competitor_id}'}
            
            competitor_data = target['data']
            company_name = competitor_data['name']
            
            logger.info(f"Testing single competitor: {company_name}")
            
            # Extract product reviews
            if 'product_reviews' in competitor_data['targets']:
                review_data = await self.data_extractor.extract_product_reviews(
                    competitor_data['targets']['product_reviews'], 
                    company_name
                )
                
                if 'error' not in review_data:
                    self.session_manager.add_scraped_data(competitor_id, review_data)
                    self.session_manager.update_stats(success=True)
                    
                    # Save test result
                    test_filename = f"test_{competitor_id}_{self.session_manager.session_id}.json"
                    test_filepath = self.session_manager.output_dir / test_filename
                    
                    with open(test_filepath, 'w') as f:
                        import json
                        json.dump(review_data, f, indent=2)
                    
                    logger.info(f"Test completed successfully. Data saved to {test_filepath}")
                    return review_data
                else:
                    self.session_manager.update_stats(success=False, error=review_data.get('error'))
                    logger.error(f"Test failed: {review_data.get('error')}")
                    return review_data
            
            return {'error': 'No product reviews target found'}
            
        except Exception as e:
            logger.error(f"Test execution error: {str(e)}")
            return {'error': str(e)}
    
    async def test_cloudflare_bypass(self) -> Dict[str, Any]:
        """Test Cloudflare bypass capabilities"""
        try:
            logger.info("Testing Cloudflare bypass capabilities...")
            
            # Test with known Cloudflare-protected pages
            test_urls = [
                "https://www.capterra.com/p/188405/Sigma/reviews/",
                "https://www.capterra.com/p/176586/Power-BI/reviews/"
            ]
            
            results = []
            for url in test_urls:
                logger.info(f"Testing Cloudflare bypass for: {url}")
                await self.page.goto(url, wait_until='domcontentloaded')
                
                bypass_success = await self.cloudflare_manager.wait_for_cloudflare_bypass(self.page)
                protection_info = await self.cloudflare_manager.detect_cloudflare_protection(self.page)
                
                results.append({
                    'url': url,
                    'bypass_success': bypass_success,
                    'protection_info': protection_info
                })
                
                if bypass_success:
                    logger.info(f"✅ Cloudflare bypass successful for {url}")
                else:
                    logger.warning(f"❌ Cloudflare bypass failed for {url}")
            
            # Get bypass statistics
            bypass_stats = self.cloudflare_manager.get_bypass_statistics()
            
            return {
                'test_results': results,
                'bypass_statistics': bypass_stats,
                'overall_success': all(r['bypass_success'] for r in results)
            }
            
        except Exception as e:
            logger.error(f"Error testing Cloudflare bypass: {str(e)}")
            return {'error': str(e)}
    
    async def test_anti_detection(self) -> Dict[str, Any]:
        """Test anti-detection measures"""
        try:
            logger.info("Testing anti-detection measures...")
            
            # Test human behavior simulation
            behavior_success = await self.behavior_simulator.simulate_natural_browsing()
            
            # Test stealth measures
            webdriver_hidden = await self.page.evaluate("navigator.webdriver")
            plugins_spoofed = await self.page.evaluate("navigator.plugins.length")
            
            # Get behavior statistics
            behavior_stats = self.behavior_simulator.get_behavior_statistics()
            
            return {
                'behavior_simulation_success': behavior_success,
                'webdriver_hidden': webdriver_hidden is None,
                'plugins_spoofed': plugins_spoofed > 0,
                'behavior_statistics': behavior_stats,
                'overall_success': behavior_success and webdriver_hidden is None
            }
            
        except Exception as e:
            logger.error(f"Error testing anti-detection: {str(e)}")
            return {'error': str(e)}
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        try:
            logger.info("Running comprehensive AURA-LITE test suite...")
            
            test_results = {}
            
            # Test 1: Cloudflare bypass
            logger.info("Test 1: Cloudflare bypass")
            test_results['cloudflare_bypass'] = await self.test_cloudflare_bypass()
            
            # Test 2: Anti-detection
            logger.info("Test 2: Anti-detection measures")
            test_results['anti_detection'] = await self.test_anti_detection()
            
            # Test 3: Single competitor scraping
            logger.info("Test 3: Single competitor scraping")
            test_results['single_competitor'] = await self.test_single_competitor()
            
            # Generate overall test summary
            overall_success = (
                test_results['cloudflare_bypass'].get('overall_success', False) and
                test_results['anti_detection'].get('overall_success', False) and
                'error' not in test_results['single_competitor']
            )
            
            test_results['overall_success'] = overall_success
            test_results['test_summary'] = {
                'cloudflare_bypass_success': test_results['cloudflare_bypass'].get('overall_success', False),
                'anti_detection_success': test_results['anti_detection'].get('overall_success', False),
                'data_extraction_success': 'error' not in test_results['single_competitor'],
                'overall_success': overall_success
            }
            
            # Save test results
            test_filename = f"comprehensive_test_{self.session_manager.session_id}.json"
            test_filepath = self.session_manager.output_dir / test_filename
            
            with open(test_filepath, 'w') as f:
                import json
                json.dump(test_results, f, indent=2)
            
            logger.info(f"Comprehensive test completed. Results saved to {test_filepath}")
            return test_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive test: {str(e)}")
            return {'error': str(e)}
    
    async def close(self):
        """Cleanup resources"""
        try:
            if self.browser:
                await self.browser.stop()
            logger.info("AURA-LITE browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing AURA-LITE browser: {str(e)}")
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        return {
            'session': self.session_manager.get_session_summary(),
            'targets': self.target_manager.get_target_statistics(),
            'cloudflare': self.cloudflare_manager.get_bypass_statistics(),
            'behavior': self.behavior_simulator.get_behavior_statistics() if self.behavior_simulator else {},
            'extraction': self.data_extractor.get_extraction_statistics() if self.data_extractor else {}
        }
