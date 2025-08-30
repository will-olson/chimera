# capterra_cloudflare_scraper.py
import json
import random
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CapterraCloudflareScraper:
    def __init__(self):
        """Initialize with enhanced Cloudflare anti-detection measures"""
        chrome_options = webdriver.ChromeOptions()
        
        # Enhanced anti-detection for Cloudflare
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Cloudflare-specific anti-detection
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Speed up loading
        
        # Random user agent rotation
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
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
        
        # Set realistic window size
        self.driver.set_window_size(1920, 1080)
        
        self.wait = WebDriverWait(self.driver, 25)  # Increased timeout for Cloudflare
        self.actions = ActionChains(self.driver)
        
        # Initialize data storage
        self.scraped_data = {}
        self.session_stats = {
            'start_time': datetime.now(),
            'total_targets': 0,
            'successful_scrapes': 0,
            'failed_scrapes': 0,
            'errors': []
        }

    def load_targets(self, json_path='capterra_sentiment_targets.json'):
        """Load Capterra scraping targets"""
        try:
            with open(json_path, 'r') as file:
                targets = json.load(file)
                logger.info(f"Loaded {targets['metadata']['total_competitors']} competitors from {json_path}")
                return targets
        except Exception as e:
            logger.error(f"Error loading targets: {str(e)}")
            return {}

    def wait_for_cloudflare(self, max_wait=30):
        """Wait for Cloudflare to clear and page to load"""
        try:
            start_time = time.time()
            while time.time() - start_time < max_wait:
                page_source = self.driver.page_source.lower()
                
                # Check if Cloudflare is still active
                if 'checking your browser' in page_source or 'cloudflare' in page_source:
                    logger.info("Cloudflare check in progress, waiting...")
                    time.sleep(2)
                    continue
                
                # Check if page has loaded
                if len(page_source) > 1000 and 'capterra' in page_source:
                    logger.info("Page loaded successfully")
                    return True
                
                time.sleep(1)
            
            logger.warning("Cloudflare wait timeout")
            return False
            
        except Exception as e:
            logger.error(f"Error waiting for Cloudflare: {str(e)}")
            return False

    def human_like_behavior(self):
        """Simulate realistic human behavior"""
        try:
            # Random mouse movements (more realistic)
            for _ in range(random.randint(3, 6)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.2, 0.5))
            
            # Realistic scrolling patterns
            scroll_patterns = [
                (200, 0.8), (150, 0.6), (300, 1.2), (100, 0.4)
            ]
            
            for scroll_amount, delay in scroll_patterns:
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(delay)
            
            # Scroll back up partially
            self.driver.execute_script("window.scrollBy(0, -150);")
            time.sleep(random.uniform(0.3, 0.7))
            
        except Exception as e:
            logger.warning(f"Error in human behavior: {str(e)}")

    def check_for_blocking(self):
        """Check if access is blocked by Cloudflare or other measures"""
        try:
            blocking_indicators = [
                "checking your browser",
                "cloudflare",
                "access denied",
                "blocked",
                "unusual activity",
                "automated access",
                "bot detection"
            ]
            
            page_text = self.driver.page_source.lower()
            for indicator in blocking_indicators:
                if indicator in page_text:
                    logger.warning(f"Blocking detected: {indicator}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for blocking: {str(e)}")
            return False

    def extract_product_reviews(self, url, company_name):
        """Extract reviews using PRECISE selectors from screenshots"""
        try:
            logger.info(f"Scraping {company_name} from {url}")
            self.driver.get(url)
            
            # Wait for Cloudflare to clear
            if not self.wait_for_cloudflare():
                return {'error': 'Cloudflare timeout', 'company': company_name}
            
            # Check for blocking
            if self.check_for_blocking():
                return {'error': 'Access blocked', 'company': company_name}
            
            # Human-like behavior
            self.human_like_behavior()
            
            # PRECISE SELECTORS from screenshots for overall rating and review count
            # From screenshot: "Overall Rating: 4.6 (1848)"
            overall_rating = 'N/A'
            review_count = 'N/A'
            
            # Method 1: Look for rating pattern in text
            page_text = self.driver.page_source
            rating_match = re.search(r'Overall Rating:\s*(\d+\.\d+)\s*\((\d+)\)', page_text)
            if rating_match:
                overall_rating = rating_match.group(1)
                review_count = rating_match.group(2)
                logger.info(f"Found rating '{overall_rating}' with review count '{review_count}' using regex")
            
            # Method 2: Use precise selectors from screenshots
            if overall_rating == 'N/A':
                rating_selectors = [
                    'span[data-testid="star-rating-count"]',
                    '.star-rating-label',
                    '.sb.type-40.star-rating-label'
                ]
                
                for selector in rating_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for element in elements:
                                text = element.text.strip()
                                if text and re.match(r'\d+\.\d+', text):
                                    overall_rating = text
                                    logger.info(f"Found rating '{overall_rating}' with selector '{selector}'")
                                    break
                            if overall_rating != 'N/A':
                                break
                    except:
                        continue
            
            # Extract individual reviews using precise selectors
            reviews = self._extract_individual_reviews_precise()
            
            # Extract pricing information
            pricing_info = self._extract_pricing_precise()
            
            # Extract rating categories (Ease of Use, Customer Service, etc.)
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
            error_msg = f"Error scraping {company_name} from {url}: {str(e)}"
            logger.error(error_msg)
            self.session_stats['errors'].append(error_msg)
            return {'error': str(e), 'company': company_name}

    def _extract_individual_reviews_precise(self):
        """Extract individual reviews using precise selectors from screenshots"""
        reviews = []
        try:
            # PRECISE SELECTORS from screenshots
            # From screenshot: Reviews have structure with specific classes
            review_selectors = [
                # Primary selectors from screenshots
                'div[data-testid="review-summary-item"]',
                '.review-item',
                '.review-card',
                
                # Specific Capterra classes from screenshots
                '.sb.card.padding-medium',
                '.rounded-xl.border.border-neutral-20.bg-card',
                
                # Fallback selectors
                '.review',
                '.review-container'
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
                logger.warning("No review elements found with standard selectors")
                # Try to find review-like content by pattern
                all_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div, p, span')
                potential_reviews = []
                
                for element in all_elements:
                    text = element.text.strip()
                    if text and len(text) > 30:
                        # Look for review-like patterns from screenshots
                        if any(phrase in text.lower() for phrase in [
                            'what do you like best about',
                            'what do you dislike about',
                            'what problems are you solving',
                            'experience of working on',
                            'powerful tool that empowers',
                            'blended data feature',
                            'data connectors and reload'
                        ]):
                            potential_reviews.append(element)
                
                if potential_reviews:
                    logger.info(f"Found {len(potential_reviews)} potential review elements using pattern matching")
                    review_elements = potential_reviews[:25]  # Limit to 25
                else:
                    return reviews
            
            # Extract up to 25 reviews (reduced to avoid detection)
            max_reviews = 25
            for i, element in enumerate(review_elements[:max_reviews]):
                try:
                    review_data = self._extract_single_review_precise(element)
                    if review_data and review_data.get('text'):
                        reviews.append(review_data)
                        
                        # Human-like delay between reviews
                        time.sleep(random.uniform(0.3, 0.6))
                        
                except Exception as e:
                    logger.warning(f"Error extracting review {i}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(reviews)} individual reviews")
            
        except Exception as e:
            logger.error(f"Error extracting individual reviews: {str(e)}")
        
        return reviews

    def _extract_single_review_precise(self, element):
        """Extract data from a single review using precise selectors"""
        try:
            # Get text content
            text = element.text.strip()
            if not text or len(text) < 20:
                return None
            
            # Look for rating in the text (e.g., "5.0" from screenshots)
            rating_match = re.search(r'(\d+\.\d+)', text)
            rating = rating_match.group(1) if rating_match else 'N/A'
            
            # Look for date pattern (e.g., "August 9, 2025" from screenshots)
            date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', text)
            date = date_match.group(0) if date_match else 'N/A'
            
            # Extract reviewer name if present
            reviewer = 'Anonymous'
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line and len(line) < 50:
                    # Look for name patterns from screenshots
                    if not any(word in line.lower() for word in ['what', 'about', 'experience', 'powerful', 'tool', 'empowers']):
                        if not any(char.isdigit() for char in line):
                            if re.match(r'^[A-Z][a-z]+\s+[A-Z]\.?$', line):  # Pattern like "Erika G."
                                reviewer = line
                                break
            
            # Extract pros/cons if present
            pros = []
            cons = []
            
            if '+ Pros' in text:
                pros_section = text.split('+ Pros')[1].split('- Cons')[0] if '- Cons' in text else text.split('+ Pros')[1]
                pros = [line.strip() for line in pros_section.split('\n') if line.strip() and len(line.strip()) > 10]
            
            if '- Cons' in text:
                cons_section = text.split('- Cons')[1]
                cons = [line.strip() for line in cons_section.split('\n') if line.strip() and len(line.strip()) > 10]
            
            return {
                'text': text,
                'rating': rating,
                'date': date,
                'reviewer': reviewer,
                'pros': pros,
                'cons': cons
            }
            
        except Exception as e:
            logger.warning(f"Error extracting single review: {str(e)}")
            return None

    def _extract_pricing_precise(self):
        """Extract pricing using precise selectors from screenshots"""
        try:
            # From screenshot: "Starting from: $10/Per Month"
            pricing_selectors = [
                'text:contains("Starting from:")',
                '.pricing',
                '.price'
            ]
            
            for selector in pricing_selectors:
                try:
                    if selector.startswith('text:'):
                        # Text-based search
                        page_text = self.driver.page_source
                        pricing_match = re.search(r'Starting from:\s*\$?(\d+)/?Per Month', page_text)
                        if pricing_match:
                            return f"${pricing_match.group(1)}/Per Month"
                    else:
                        # CSS selector search
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for element in elements:
                                text = element.text.strip()
                                if text and '$' in text and 'Month' in text:
                                    return text
                except:
                    continue
            
            return 'N/A'
            
        except Exception as e:
            logger.warning(f"Error extracting pricing: {str(e)}")
            return 'N/A'

    def _extract_rating_categories_precise(self):
        """Extract rating categories using precise selectors from screenshots"""
        try:
            # From screenshot: "Ease of Use: 4.1", "Customer Service: 4.2", etc.
            rating_categories = {}
            
            # Look for rating category elements
            category_selectors = [
                'div[data-testid="review-summary-item"]',
                '.rating-category',
                '.feature-rating'
            ]
            
            for selector in category_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            # Look for patterns like "Ease of Use: 4.1"
                            category_match = re.search(r'([^:]+):\s*(\d+\.\d+)', text)
                            if category_match:
                                category_name = category_match.group(1).strip()
                                rating_value = category_match.group(2)
                                rating_categories[category_name] = rating_value
                except:
                    continue
            
            return rating_categories
            
        except Exception as e:
            logger.warning(f"Error extracting rating categories: {str(e)}")
            return {}

    def extract_alternatives_page(self, url, company_name):
        """Extract competitor alternatives from alternatives page"""
        try:
            logger.info(f"Scraping alternatives for {company_name} from {url}")
            self.driver.get(url)
            
            # Wait for Cloudflare
            if not self.wait_for_cloudflare():
                return {'error': 'Cloudflare timeout', 'company': company_name}
            
            if self.check_for_blocking():
                return {'error': 'Access blocked', 'company': company_name}
            
            self.human_like_behavior()
            
            # PRECISE SELECTORS from screenshots for alternatives
            # From screenshot: Product cards with ratings and pricing
            alternatives = []
            
            # Look for product cards
            card_selectors = [
                'div[data-testid="alternative-card"]',
                '.sb.card.padding-medium',
                '.product-card'
            ]
            
            product_cards = []
            for selector in card_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        product_cards = elements
                        logger.info(f"Found {len(elements)} product cards with selector '{selector}'")
                        break
                except:
                    continue
            
            if not product_cards:
                return alternatives
            
            # Extract data from each product card
            for i, card in enumerate(product_cards[:10]):  # Limit to 10
                try:
                    product_data = self._extract_product_card_data(card)
                    if product_data:
                        alternatives.append(product_data)
                        time.sleep(random.uniform(0.2, 0.4))
                except Exception as e:
                    logger.warning(f"Error extracting product card {i}: {str(e)}")
                    continue
            
            return alternatives
            
        except Exception as e:
            error_msg = f"Error scraping alternatives for {company_name}: {str(e)}"
            logger.error(error_msg)
            return []

    def _extract_product_card_data(self, card_element):
        """Extract data from a product card using precise selectors"""
        try:
            # Extract product name
            name_selectors = ['h3', 'h4', '.product-name', '.card-title']
            product_name = 'Unknown'
            
            for selector in name_selectors:
                try:
                    elements = card_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        product_name = elements[0].text.strip()
                        break
                except:
                    continue
            
            # Extract rating using precise selector from screenshots
            rating_selectors = [
                'span[data-testid="star-rating-count"]',
                '.star-rating-label',
                '.sb.type-40.star-rating-label'
            ]
            
            rating = 'N/A'
            for selector in rating_selectors:
                try:
                    elements = card_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            if text and re.match(r'\d+\.\d+', text):
                                rating = text
                                break
                        if rating != 'N/A':
                            break
                except:
                    continue
            
            # Extract review count
            review_count = 'N/A'
            if rating != 'N/A':
                # Look for pattern like "(1848)" next to rating
                card_text = card_element.text
                count_match = re.search(r'\((\d+)\)', card_text)
                if count_match:
                    review_count = count_match.group(1)
            
            # Extract pricing
            pricing = 'N/A'
            card_text = card_element.text
            pricing_match = re.search(r'Starting from:\s*\$?(\d+)/?Per Month', card_text)
            if pricing_match:
                pricing = f"${pricing_match.group(1)}/Per Month"
            
            return {
                'product_name': product_name,
                'rating': rating,
                'review_count': review_count,
                'pricing': pricing
            }
            
        except Exception as e:
            logger.warning(f"Error extracting product card data: {str(e)}")
            return None

    def batch_scrape_competitors(self, targets, max_competitors=3):
        """Batch scrape competitors with limited scope to avoid detection"""
        logger.info(f"Starting batch scrape of up to {max_competitors} competitors")
        
        # Limit scope to avoid detection
        limited_competitors = dict(list(targets['competitors'].items())[:max_competitors])
        self.session_stats['total_targets'] = len(limited_competitors)
        
        for competitor_id, competitor_data in limited_competitors.items():
            try:
                company_name = competitor_data['name']
                logger.info(f"Processing {company_name} ({competitor_id})")
                
                # HIGH PRIORITY: Extract product reviews
                if 'product_reviews' in competitor_data['targets']:
                    review_data = self.extract_product_reviews(
                        competitor_data['targets']['product_reviews'], 
                        company_name
                    )
                    
                    if 'error' not in review_data:
                        self.scraped_data[competitor_id] = review_data
                        self.session_stats['successful_scrapes'] += 1
                        logger.info(f"Successfully scraped reviews for {company_name}")
                        
                        # MEDIUM PRIORITY: Extract alternatives if reviews successful
                        if 'alternatives' in competitor_data['targets']:
                            alternatives = self.extract_alternatives_page(
                                competitor_data['targets']['alternatives'],
                                company_name
                            )
                            if alternatives:
                                self.scraped_data[competitor_id]['alternatives'] = alternatives
                                logger.info(f"Found {len(alternatives)} alternatives for {company_name}")
                    else:
                        self.session_stats['failed_scrapes'] += 1
                        logger.error(f"Failed to scrape reviews for {company_name}")
                        
                        # If we get blocked, stop scraping
                        if 'Access blocked' in str(review_data.get('error', '')):
                            logger.error("Access blocked detected. Stopping scraping to avoid further detection.")
                            break
                
                # Enhanced delay between competitors
                delay = random.uniform(15, 25)  # 15-25 seconds
                logger.info(f"Waiting {delay:.1f} seconds before next competitor...")
                time.sleep(delay)
                
            except Exception as e:
                error_msg = f"Error processing {competitor_id}: {str(e)}"
                logger.error(error_msg)
                self.session_stats['errors'].append(error_msg)
                self.session_stats['failed_scrapes'] += 1
                continue
        
        logger.info(f"Batch scrape completed. Success: {self.session_stats['successful_scrapes']}, Failed: {self.session_stats['failed_scrapes']}")
        return self.scraped_data

    def save_data_to_json(self, filename='capterra_sentiment_metrics.json'):
        """Save scraped data to JSON file"""
        try:
            output_data = {
                'metadata': {
                    'scraping_session': datetime.now().strftime('%Y-%m-%d_%H:%M'),
                    'platform': 'capterra',
                    'total_competitors': self.session_stats['total_targets'],
                    'successful_scrapes': self.session_stats['successful_scrapes'],
                    'failed_scrapes': self.session_stats['failed_scrapes'],
                    'scraping_duration_minutes': (datetime.now() - self.session_stats['start_time']).total_seconds() / 60,
                    'errors': self.session_stats['errors']
                },
                'competitors': self.scraped_data
            }
            
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            logger.info(f"Data saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data to JSON: {str(e)}")
            return False

    def save_data_to_csv(self, filename='capterra_sentiment_metrics.csv'):
        """Save scraped data to CSV file"""
        try:
            csv_data = []
            
            for competitor_id, data in self.scraped_data.items():
                if 'error' in data:
                    continue
                
                # Basic company info
                row = {
                    'company_id': competitor_id,
                    'company_name': data.get('company', ''),
                    'overall_rating': data.get('overall_rating', ''),
                    'review_count': data.get('review_count', ''),
                    'pricing_info': data.get('pricing_info', ''),
                    'total_reviews_scraped': len(data.get('reviews', [])),
                    'alternatives_found': len(data.get('alternatives', [])),
                    'scraped_at': data.get('scraped_at', ''),
                    'source_url': data.get('source_url', '')
                }
                
                # Add rating categories
                rating_categories = data.get('rating_categories', {})
                for category, rating in rating_categories.items():
                    row[f'{category.lower().replace(" ", "_")}_rating'] = rating
                
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False)
            
            logger.info(f"Data saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data to CSV: {str(e)}")
            return False

    def close(self):
        """Cleanup"""
        try:
            self.driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

def main():
    """Test the Capterra Cloudflare scraper"""
    scraper = None
    try:
        scraper = CapterraCloudflareScraper()
        
        print("🚀 Capterra Cloudflare Scraper - Testing Phase")
        print("=" * 60)
        
        # Load targets
        targets = scraper.load_targets()
        if not targets:
            print("❌ Failed to load targets")
            return
        
        # Execute LIMITED batch scraping to test
        scraped_data = scraper.batch_scrape_competitors(targets, max_competitors=2)
        
        # Save data
        scraper.save_data_to_json()
        scraper.save_data_to_csv()
        
        # Print summary
        print(f"\n📊 Scraping Results:")
        print(f"   Total Competitors: {scraper.session_stats['total_targets']}")
        print(f"   Successful: {scraper.session_stats['successful_scrapes']}")
        print(f"   Failed: {scraper.session_stats['failed_scrapes']}")
        print(f"   Duration: {(datetime.now() - scraper.session_stats['start_time']).total_seconds() / 60:.1f} minutes")
        
        if scraper.session_stats['errors']:
            print(f"\n❌ Errors encountered: {len(scraper.session_stats['errors'])}")
            for error in scraper.session_stats['errors'][:3]:
                print(f"   - {error[:100]}...")
        
        print(f"\n💾 Data saved to:")
        print(f"   - capterra_sentiment_metrics.json")
        print(f"   - capterra_sentiment_metrics.csv")
        
        print(f"\n🛡️ Anti-Detection Features:")
        print(f"   - Cloudflare bypass measures")
        print(f"   - Human behavior simulation")
        print(f"   - Precise selectors from screenshots")
        print(f"   - Limited scope (2 competitors)")
        print(f"   - Enhanced delays and randomization")
        
    except Exception as e:
        print(f"❌ Execution error: {str(e)}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
