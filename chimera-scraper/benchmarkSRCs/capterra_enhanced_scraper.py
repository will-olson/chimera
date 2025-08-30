# capterra_scraper.py
import json
import random
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CapterraScraper:
    def __init__(self):
        """Initialize with Cloudflare anti-detection measures"""
        chrome_options = webdriver.ChromeOptions()
        
        # Anti-detection for Cloudflare
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        
        # Enhanced random user agent rotation
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Enhanced webdriver hiding
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        self.driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'})")
        self.driver.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8})")
        self.driver.execute_script("Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})")
        
        self.driver.set_window_size(1920, 1080)
        self.actions = ActionChains(self.driver)
        
        self.scraped_data = {}
        self.session_stats = {'successful': 0, 'failed': 0, 'errors': []}

    def load_targets(self, json_path='capterra_sentiment_targets.json'):
        """Load Capterra targets"""
        try:
            with open(json_path, 'r') as file:
                targets = json.load(file)
                logger.info(f"Loaded {targets['metadata']['total_competitors']} competitors")
                return targets
        except Exception as e:
            logger.error(f"Error loading targets: {str(e)}")
            return {}

    def wait_for_cloudflare(self, max_wait=45):
        """Enhanced wait for Cloudflare with multiple detection methods"""
        try:
            start_time = time.time()
            cloudflare_detected = False
            
            while time.time() - start_time < max_wait:
                page_source = self.driver.page_source.lower()
                current_url = self.driver.current_url.lower()
                
                # Check for various Cloudflare indicators
                cloudflare_indicators = [
                    'checking your browser',
                    'cloudflare',
                    'ray id',
                    'please wait',
                    'ddos protection',
                    'security check'
                ]
                
                for indicator in cloudflare_indicators:
                    if indicator in page_source:
                        if not cloudflare_detected:
                            logger.info(f"Cloudflare detected: {indicator}")
                            cloudflare_detected = True
                        time.sleep(3)  # Longer wait for Cloudflare
                        break
                else:
                    # No Cloudflare indicators found
                    if len(page_source) > 2000 and 'capterra' in page_source:
                        logger.info("Page loaded successfully - Cloudflare cleared")
                        return True
                    
                    # Check if we're still on a loading page
                    if len(page_source) < 1000:
                        time.sleep(2)
                        continue
                    
                    # Check for error pages
                    if any(error in page_source for error in ['error', 'blocked', 'access denied']):
                        logger.warning("Error page detected")
                        return False
                
                time.sleep(2)
            
            logger.warning("Cloudflare wait timeout")
            return False
            
        except Exception as e:
            logger.error(f"Error waiting for Cloudflare: {str(e)}")
            return False

    def enhanced_human_behavior(self):
        """Enhanced human behavior simulation"""
        try:
            # Realistic mouse movements with acceleration
            for _ in range(random.randint(4, 8)):
                x = random.randint(50, 900)
                y = random.randint(50, 700)
                
                # Simulate human-like mouse movement
                self.actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.3, 0.7))
                
                # Sometimes pause longer (like human thinking)
                if random.random() < 0.3:
                    time.sleep(random.uniform(1.0, 2.0))
            
            # Realistic scrolling patterns
            scroll_patterns = [
                (150, 0.5), (200, 0.8), (300, 1.2), (100, 0.4), (250, 0.9)
            ]
            
            for scroll_amount, delay in scroll_patterns:
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(delay)
                
                # Sometimes scroll back up slightly
                if random.random() < 0.4:
                    self.driver.execute_script("window.scrollBy(0, -50);")
                    time.sleep(random.uniform(0.3, 0.6))
            
            # Random page interactions
            if random.random() < 0.5:
                # Move mouse to random elements
                elements = self.driver.find_elements(By.CSS_SELECTOR, 'div, p, span')
                if elements:
                    random_element = random.choice(elements[:10])
                    try:
                        self.actions.move_to_element(random_element).perform()
                        time.sleep(random.uniform(0.5, 1.0))
                    except:
                        pass
            
        except Exception as e:
            logger.warning(f"Error in enhanced human behavior: {str(e)}")

    def extract_product_reviews(self, url, company_name):
        """Extract reviews using precise selectors from screenshots"""
        try:
            logger.info(f"Scraping {company_name} from {url}")
            self.driver.get(url)
            
            # Wait for Cloudflare
            if not self.wait_for_cloudflare():
                return {'error': 'Cloudflare timeout', 'company': company_name}
            
            # Enhanced human-like behavior
            self.enhanced_human_behavior()
            
            # PRECISE SELECTORS from screenshots
            # Look for "Overall Rating: 4.6 (1848)" pattern
            page_text = self.driver.page_source
            overall_rating = 'N/A'
            review_count = 'N/A'
            
            rating_match = re.search(r'Overall Rating:\s*(\d+\.\d+)\s*\((\d+)\)', page_text)
            if rating_match:
                overall_rating = rating_match.group(1)
                review_count = rating_match.group(2)
                logger.info(f"Found rating '{overall_rating}' with review count '{review_count}'")
            
            # Extract individual reviews
            reviews = self._extract_individual_reviews_precise()
            
            # Extract pricing
            pricing_info = self._extract_pricing_precise()
            
            # Extract rating categories
            rating_categories = self._extract_rating_categories_precise()
            
            result = {
                'company': company_name,
                'overall_rating': overall_rating,
                'review_count': review_count,
                'pricing_info': pricing_info,
                'rating_categories': rating_categories,
                'reviews': reviews,
                'scraped_at': datetime.now().isoformat(),
                'source_url': url
            }
            
            logger.info(f"Successfully scraped {len(reviews)} reviews for {company_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error scraping {company_name}: {str(e)}"
            logger.error(error_msg)
            self.session_stats['errors'].append(error_msg)
            return {'error': str(e), 'company': company_name}

    def _extract_individual_reviews_precise(self):
        """Extract reviews using precise selectors from screenshots"""
        reviews = []
        try:
            # PRECISE SELECTORS from screenshots
            review_selectors = [
                'div[data-testid="review-summary-item"]',
                '.sb.card.padding-medium',
                '.rounded-xl.border.border-neutral-20.bg-card'
            ]
            
            review_elements = []
            for selector in review_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        review_elements = elements
                        logger.info(f"Found {len(elements)} review elements with selector '{selector}'")
                        break
                except:
                    continue
            
            if not review_elements:
                # Pattern matching fallback
                all_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div, p, span')
                potential_reviews = []
                
                for element in all_elements:
                    text = element.text.strip()
                    if text and len(text) > 30:
                        if any(phrase in text.lower() for phrase in [
                            'what do you like best about',
                            'what do you dislike about',
                            'powerful tool that empowers',
                            'blended data feature'
                        ]):
                            potential_reviews.append(element)
                
                if potential_reviews:
                    review_elements = potential_reviews[:20]
            
            # Extract review data
            for i, element in enumerate(review_elements[:20]):
                try:
                    review_data = self._extract_single_review_precise(element)
                    if review_data and review_data.get('text'):
                        reviews.append(review_data)
                        time.sleep(random.uniform(0.2, 0.4))
                        
                except Exception as e:
                    logger.warning(f"Error extracting review {i}: {str(e)}")
                    continue
            
            return reviews
            
        except Exception as e:
            logger.error(f"Error extracting reviews: {str(e)}")
            return []

    def _extract_single_review_precise(self, element):
        """Extract single review data"""
        try:
            text = element.text.strip()
            if not text or len(text) < 20:
                return None
            
            # Extract rating
            rating_match = re.search(r'(\d+\.\d+)', text)
            rating = rating_match.group(1) if rating_match else 'N/A'
            
            # Extract date
            date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', text)
            date = date_match.group(0) if date_match else 'N/A'
            
            # Extract reviewer
            reviewer = 'Anonymous'
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) < 50:
                    if not any(word in line.lower() for word in ['what', 'about', 'powerful', 'tool']):
                        if not any(char.isdigit() for char in line):
                            if re.match(r'^[A-Z][a-z]+\s+[A-Z]\.?$', line):
                                reviewer = line
                                break
            
            return {
                'text': text,
                'rating': rating,
                'date': date,
                'reviewer': reviewer
            }
            
        except Exception as e:
            logger.warning(f"Error extracting single review: {str(e)}")
            return None

    def _extract_pricing_precise(self):
        """Extract pricing information"""
        try:
            page_text = self.driver.page_source
            pricing_match = re.search(r'Starting from:\s*\$?(\d+)/?Per Month', page_text)
            if pricing_match:
                return f"${pricing_match.group(1)}/Per Month"
            return 'N/A'
        except:
            return 'N/A'

    def _extract_rating_categories_precise(self):
        """Extract rating categories"""
        try:
            rating_categories = {}
            page_text = self.driver.page_source
            
            # Look for patterns like "Ease of Use: 4.1"
            category_pattern = r'([^:]+):\s*(\d+\.\d+)'
            matches = re.findall(category_pattern, page_text)
            
            for category, rating in matches:
                category_name = category.strip()
                if any(word in category_name.lower() for word in ['ease', 'customer', 'features', 'value']):
                    rating_categories[category_name] = rating
            
            return rating_categories
        except:
            return {}

    def test_single_competitor(self, targets_file='capterra_sentiment_targets.json'):
        """Test with single competitor"""
        try:
            with open(targets_file, 'r') as f:
                targets = json.load(f)
            
            # Test with Sigma
            test_comp = 'sigma'
            if test_comp in targets['competitors']:
                comp_data = targets['competitors'][test_comp]
                url = comp_data['targets']['product_reviews']
                
                result = self.extract_product_reviews(url, comp_data['name'])
                
                if 'error' not in result:
                    self.scraped_data[test_comp] = result
                    self.session_stats['successful'] += 1
                    
                    # Save test result
                    with open('test_sigma_enhanced.json', 'w') as f:
                        json.dump(result, f, indent=2)
                    
                    logger.info(f"Test completed successfully. Reviews: {len(result.get('reviews', []))}")
                    return result
                else:
                    self.session_stats['failed'] += 1
                    logger.error(f"Test failed: {result.get('error')}")
                    return result
            
        except Exception as e:
            logger.error(f"Test execution error: {str(e)}")
            return None

    def close(self):
        """Cleanup"""
        try:
            self.driver.quit()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

def main():
    """Test the Capterra scraper"""
    scraper = None
    try:
        scraper = CapterraScraper()
        
        print("🚀 Enhanced Capterra Cloudflare Scraper - Testing Phase")
        print("=" * 60)
        print("🛡️  Enhanced Anti-Detection Features:")
        print("   - Advanced Cloudflare bypass")
        print("   - Sophisticated human behavior")
        print("   - Multiple extraction methods")
        print("   - Precise selectors from screenshots")
        print("=" * 60)
        result = scraper.test_single_competitor()
        
        if result and 'error' not in result:
            print(f"\n✅ Enhanced Scraper Success!")
            print(f"   Company: {result.get('company')}")
            print(f"   Overall Rating: {result.get('overall_rating')}")
            print(f"   Review Count: {result.get('review_count')}")
            print(f"   Reviews Scraped: {len(result.get('reviews', []))}")
            print(f"   Pricing: {result.get('pricing_info')}")
            print(f"   Rating Categories: {len(result.get('rating_categories', {}))}")
            print(f"\n💾 Data saved to: test_sigma_enhanced.json")
            
            # Show sample review
            if result.get('reviews'):
                sample_review = result['reviews'][0]
                print(f"\n📝 Sample Review:")
                print(f"   Reviewer: {sample_review.get('reviewer')}")
                print(f"   Rating: {sample_review.get('rating')}")
                print(f"   Date: {sample_review.get('date')}")
                print(f"   Text: {sample_review.get('text', '')[:100]}...")
        else:
            print(f"\n❌ Enhanced Scraper Failed: {result.get('error') if result else 'Unknown error'}")
        
    except Exception as e:
        print(f"❌ Execution error: {str(e)}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
