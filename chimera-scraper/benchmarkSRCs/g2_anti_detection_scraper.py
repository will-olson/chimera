# g2_anti_detection_scraper.py
import json
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class G2AntiDetectionScraper:
    def __init__(self):
        """Initialize with enhanced anti-detection measures"""
        chrome_options = webdriver.ChromeOptions()
        
        # Enhanced anti-detection
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Hide webdriver
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        
        self.driver.set_window_size(1920, 1080)
        self.actions = ActionChains(self.driver)
        
        self.scraped_data = {}
        self.session_stats = {'successful': 0, 'failed': 0, 'errors': []}

    def human_like_behavior(self):
        """Simulate human behavior"""
        try:
            # Random mouse movements
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.3))
            
            # Random scrolling
            scroll_amount = random.randint(100, 400)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.0))
            
        except Exception as e:
            logger.warning(f"Error in human behavior: {str(e)}")

    def check_for_blocking(self):
        """Check if access is blocked"""
        try:
            blocking_indicators = ["Access blocked", "We detected unusual activity", "Automated (bot) activity"]
            page_text = self.driver.page_source.lower()
            
            for indicator in blocking_indicators:
                if indicator.lower() in page_text:
                    logger.warning(f"Blocking detected: {indicator}")
                    return True
            return False
            
        except Exception as e:
            logger.error(f"Error checking for blocking: {str(e)}")
            return False

    def extract_reviews_with_precise_selectors(self, url, company_name):
        """Extract reviews using precise selectors from screenshots"""
        try:
            logger.info(f"Scraping {company_name} from {url}")
            self.driver.get(url)
            time.sleep(random.uniform(4, 6))
            
            if self.check_for_blocking():
                return {'error': 'Access blocked', 'company': company_name}
            
            self.human_like_behavior()
            
            # PRECISE SELECTORS from screenshots
            # Look for review questions like "What do you like best about..."
            review_elements = []
            
            # Method 1: Look for specific review question patterns
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div, p, span')
            for element in all_elements:
                text = element.text.strip()
                if text and len(text) > 30:
                    if any(phrase in text.lower() for phrase in [
                        'what do you like best about',
                        'what do you dislike about',
                        'what problems are you solving',
                        'experience of working on',
                        'several features in',
                        'associative model'
                    ]):
                        review_elements.append(element)
            
            if not review_elements:
                # Method 2: Look for review containers
                review_selectors = [
                    'div[itemprop="reviewBody"]',
                    '.review',
                    '.review-item',
                    '.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base'
                ]
                
                for selector in review_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            review_elements = elements[:20]  # Limit to 20
                            break
                    except:
                        continue
            
            # Extract review data
            reviews = []
            for i, element in enumerate(review_elements[:20]):  # Limit to 20
                try:
                    review_data = self._extract_single_review_precise(element)
                    if review_data and review_data.get('text'):
                        reviews.append(review_data)
                        time.sleep(random.uniform(0.2, 0.4))
                except Exception as e:
                    logger.warning(f"Error extracting review {i}: {str(e)}")
                    continue
            
            # Extract rating and review count using regex
            import re
            page_text = self.driver.page_source
            
            # Look for rating pattern like "4.4 out of 5"
            rating_match = re.search(r'(\d+\.\d+)\s*out\s*of\s*5', page_text)
            overall_rating = rating_match.group(1) if rating_match else 'N/A'
            
            # Look for review count pattern like "(919)"
            count_match = re.search(r'\((\d+)\)', page_text)
            review_count = count_match.group(1) if count_match else 'N/A'
            
            result = {
                'company': company_name,
                'overall_rating': overall_rating,
                'review_count': review_count,
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

    def _extract_single_review_precise(self, element):
        """Extract review data using precise selectors from screenshots"""
        try:
            # Get text content
            text = element.text.strip()
            if not text or len(text) < 20:
                return None
            
            # Look for rating in the text (e.g., "5/5 star rating")
            import re
            rating_match = re.search(r'(\d+/\d+)', text)
            rating = rating_match.group(1) if rating_match else 'N/A'
            
            # Look for date pattern (e.g., "8/11/2025")
            date_match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', text)
            date = date_match.group(0) if date_match else 'N/A'
            
            # Extract reviewer name if present
            reviewer = 'Anonymous'
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) < 50 and not any(word in line.lower() for word in ['what', 'about', 'experience', 'several', 'associative']):
                    if not any(char.isdigit() for char in line):
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

    def test_single_competitor(self, targets_file='g2_sentiment_targets.json'):
        """Test with single competitor to validate approach"""
        try:
            with open(targets_file, 'r') as f:
                targets = json.load(f)
            
            # Test with ThoughtSpot
            test_comp = 'thoughtspot'
            if test_comp in targets['competitors']:
                comp_data = targets['competitors'][test_comp]
                url = comp_data['targets']['product_reviews']
                
                result = self.extract_reviews_with_precise_selectors(url, comp_data['name'])
                
                if 'error' not in result:
                    self.scraped_data[test_comp] = result
                    self.session_stats['successful'] += 1
                    
                    # Save test result
                    with open('test_thoughtspot_reviews.json', 'w') as f:
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
    """Test the anti-detection scraper"""
    scraper = None
    try:
        scraper = G2AntiDetectionScraper()
        
        print("🧪 Testing G2 Anti-Detection Scraper...")
        result = scraper.test_single_competitor()
        
        if result and 'error' not in result:
            print(f"✅ Success! Scraped {len(result.get('reviews', []))} reviews")
            print(f"   Rating: {result.get('overall_rating')}")
            print(f"   Review Count: {result.get('review_count')}")
            print(f"   Data saved to: test_thoughtspot_reviews.json")
        else:
            print(f"❌ Failed: {result.get('error') if result else 'Unknown error'}")
        
    except Exception as e:
        print(f"❌ Execution error: {str(e)}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
