# g2_sentiment_scraper_v3.py
import os
import json
import random
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class G2SentimentScraperV3:
    def __init__(self):
        """Initialize the G2 sentiment scraper with enhanced anti-detection measures"""
        # Enhanced Chrome options with advanced anti-detection
        chrome_options = webdriver.ChromeOptions()
        
        # Basic anti-detection
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Enhanced anti-detection measures
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Random user agent
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
        
        # Set window size to common resolution
        self.driver.set_window_size(1920, 1080)
        
        self.wait = WebDriverWait(self.driver, 20)
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

    def load_targets(self, json_path='g2_sentiment_targets.json'):
        """Load G2 scraping targets from JSON file"""
        try:
            with open(json_path, 'r') as file:
                targets = json.load(file)
                logger.info(f"Loaded {targets['metadata']['total_competitors']} competitors from {json_path}")
                return targets
        except Exception as e:
            logger.error(f"Error loading targets: {str(e)}")
            return {}

    def human_like_behavior(self):
        """Simulate human-like behavior to avoid detection"""
        try:
            # Random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.1, 0.3))
            
            # Random scrolling
            scroll_amount = random.randint(100, 500)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Random scroll back
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount//2});")
            time.sleep(random.uniform(0.3, 0.8))
            
        except Exception as e:
            logger.warning(f"Error in human-like behavior: {str(e)}")

    def check_for_blocking(self):
        """Check if the page is blocking access"""
        try:
            # Check for blocking indicators
            blocking_indicators = [
                "Access blocked",
                "We detected unusual activity",
                "Automated (bot) activity",
                "Please verify you are human",
                "Security check"
            ]
            
            page_text = self.driver.page_source.lower()
            for indicator in blocking_indicators:
                if indicator.lower() in page_text:
                    logger.warning(f"Blocking detected: {indicator}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for blocking: {str(e)}")
            return False

    def extract_product_reviews(self, url, company_name):
        """Extract sentiment data from G2 product review pages using PRECISE selectors from screenshots"""
        try:
            logger.info(f"Scraping product reviews for {company_name} from {url}")
            self.driver.get(url)
            
            # Enhanced page loading wait
            time.sleep(random.uniform(4, 7))
            
            # Check for blocking
            if self.check_for_blocking():
                logger.error(f"Access blocked for {company_name}")
                return {'error': 'Access blocked by G2', 'company': company_name}
            
            # Human-like behavior
            self.human_like_behavior()
            
            # PRECISE SELECTORS from screenshots for overall rating
            overall_rating = 'N/A'
            rating_selectors = [
                # From screenshot: Look for star ratings like "★★★★☆(919) 4.4 out of 5"
                'span:contains("out of 5")',
                '.rating',
                '.stars',
                '[data-testid="rating"]',
                '.product-header__rating'
            ]
            
            # Try to find rating in page text first (more reliable)
            page_text = self.driver.page_source
            import re
            rating_match = re.search(r'(\d+\.\d+)\s*out\s*of\s*5', page_text)
            if rating_match:
                overall_rating = rating_match.group(1)
                logger.info(f"Found rating '{overall_rating}' using regex")
            
            # PRECISE SELECTORS from screenshots for review count
            review_count = 'N/A'
            # Look for patterns like "(919)" in the rating text
            count_match = re.search(r'\((\d+)\)', page_text)
            if count_match:
                review_count = count_match.group(1)
                logger.info(f"Found review count '{review_count}' using regex")
            
            # Extract market segments
            market_segments = self._extract_market_segments()
            
            # Extract pricing information
            pricing_info = self._extract_pricing_info()
            
            # PRECISE SELECTORS from screenshots for individual reviews
            reviews = self._extract_individual_reviews_v3()
            
            result = {
                'company': company_name,
                'overall_rating': overall_rating,
                'review_count': review_count,
                'market_segments': market_segments,
                'pricing_info': pricing_info,
                'reviews': reviews,
                'scraped_at': datetime.now().isoformat(),
                'source_url': url
            }
            
            logger.info(f"Successfully scraped {len(reviews)} reviews for {company_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error scraping product reviews for {company_name} from {url}: {str(e)}"
            logger.error(error_msg)
            self.session_stats['errors'].append(error_msg)
            return {'error': str(e), 'company': company_name}

    def _extract_individual_reviews_v3(self):
        """PRECISE: Extract individual review text using selectors from screenshots"""
        reviews = []
        try:
            # PRECISE SELECTORS from screenshots
            # From screenshot: Reviews have structure like "What do you like best about Qlik Sense?"
            # followed by review text in <p> tags with classes like "elv-tracking-normal elv-text-default elv-font-figtree elv-text-base elv-leading-base"
            
            review_selectors = [
                # Primary selectors from screenshots
                'div[itemprop="reviewBody"]',
                'div[itemprop="review"]',
                '.review',
                '.review-item',
                
                # Specific G2 classes from screenshots
                '.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base',
                'p.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base',
                
                # Fallback selectors
                '[data-testid="review"]',
                '.review-content',
                '.review-body'
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
                # Try to find review questions and answers from screenshots
                question_selectors = [
                    'div:contains("What do you like best about")',
                    'div:contains("What do you dislike about")',
                    'div:contains("What problems are you solving")'
                ]
                
                # Look for text patterns that indicate reviews
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
                            'several features in',
                            'associative model',
                            'data visualization',
                            'dashboard management'
                        ]):
                            potential_reviews.append(element)
                
                if potential_reviews:
                    logger.info(f"Found {len(potential_reviews)} potential review elements using pattern matching")
                    review_elements = potential_reviews[:30]  # Limit to 30
                else:
                    return reviews
            
            # Extract up to 30 reviews (reduced to avoid detection)
            max_reviews = 30
            for i, review_element in enumerate(review_elements[:max_reviews]):
                try:
                    review_data = self._extract_single_review_v3(review_element)
                    if review_data and review_data.get('text'):
                        reviews.append(review_data)
                        
                        # Human-like delay between reviews
                        time.sleep(random.uniform(0.2, 0.5))
                        
                except Exception as e:
                    logger.warning(f"Error extracting review {i}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(reviews)} individual reviews")
            
        except Exception as e:
            logger.error(f"Error extracting individual reviews: {str(e)}")
        
        return reviews

    def _extract_single_review_v3(self, review_element):
        """PRECISE: Extract data from a single review element using selectors from screenshots"""
        try:
            # PRECISE TEXT EXTRACTION from screenshots
            # From screenshot: Review text is in <p> tags with specific classes
            text_selectors = [
                # Primary selectors from screenshots
                'p.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base',
                '.elv-tracking-normal.elv-text-default.elv-font-figtree.elv-text-base.elv-leading-base',
                
                # Fallback selectors
                '.review-text',
                '.review-content',
                '.review-body',
                '[data-testid="review-text"]',
                'p',
                'span'
            ]
            
            review_text = ''
            for selector in text_selectors:
                try:
                    elements = review_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 20:  # Only meaningful text
                                review_text = text
                                break
                        if review_text:
                            break
                except:
                    continue
            
            # If no specific text found, try the element itself
            if not review_text:
                review_text = review_element.text.strip()
            
            # PRECISE RATING EXTRACTION from screenshots
            # From screenshot: Ratings appear as "5/5 star rating"
            rating_selectors = [
                '.rating',
                '.stars',
                '.score',
                '[data-testid="rating"]',
                '.review__rating',
                '.review-item__rating'
            ]
            
            rating = 'N/A'
            for selector in rating_selectors:
                try:
                    elements = review_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            # Look for patterns like "5/5" from screenshots
                            if text and '/' in text and any(char.isdigit() for char in text):
                                rating = text
                                break
                        if rating != 'N/A':
                            break
                except:
                    continue
            
            # PRECISE DATE EXTRACTION from screenshots
            # From screenshot: Dates appear as "8/11/2025"
            date_selectors = [
                '.review-date',
                '.date',
                '.timestamp',
                '[data-testid="date"]',
                '.review__date',
                '.review-item__date'
            ]
            
            date = 'N/A'
            for selector in date_selectors:
                try:
                    elements = review_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            # Look for date patterns from screenshots
                            if text and re.match(r'\d{1,2}/\d{1,2}/\d{4}', text):
                                date = text
                                break
                        if date != 'N/A':
                            break
                except:
                    continue
            
            # PRECISE REVIEWER EXTRACTION from screenshots
            # From screenshot: Reviewer names like "shailendra s." appear
            reviewer_selectors = [
                '.reviewer-name',
                '.author',
                '.user-name',
                '[data-testid="reviewer"]',
                '.review__author',
                '.review-item__author'
            ]
            
            reviewer = 'Anonymous'
            for selector in reviewer_selectors:
                try:
                    elements = review_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            if text and len(text) > 2 and text != 'Anonymous':
                                reviewer = text
                                break
                        if reviewer != 'Anonymous':
                            break
                except:
                    continue
            
            # Only return if we have meaningful text
            if review_text and len(review_text) > 20:
                return {
                    'text': review_text,
                    'rating': rating,
                    'date': date,
                    'reviewer': reviewer
                }
            else:
                return None
            
        except Exception as e:
            logger.warning(f"Error extracting single review: {str(e)}")
            return None

    def extract_head_to_head_comparison(self, url, company_name):
        """PRECISE: Extract AI-generated summary using selectors from screenshots"""
        try:
            logger.info(f"Scraping head-to-head comparison for {company_name} from {url}")
            self.driver.get(url)
            time.sleep(random.uniform(4, 7))
            
            # Check for blocking
            if self.check_for_blocking():
                logger.error(f"Access blocked for comparison: {company_name}")
                return {'error': 'Access blocked by G2', 'company': company_name}
            
            # Human-like behavior
            self.human_like_behavior()
            
            # PRECISE SELECTORS from screenshots for AI-generated summary
            # From screenshot: AI Generated Summary is in a div with tabindex="0"
            summary_selectors = [
                # Primary selector from screenshot
                'div[tabindex="0"]:contains("AI Generated Summary")',
                'div.compare-container-v2__summary div[tabindex="0"]',
                
                # Fallback selectors
                '.ai-summary',
                '.comparison-summary',
                '[data-testid="ai-summary"]'
            ]
            
            ai_summary = 'N/A'
            for selector in summary_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            text = element.text.strip()
                            if text and 'AI Generated Summary' in text:
                                # Get the actual summary content from the next element
                                try:
                                    summary_content = element.find_element(By.XPATH, 'following-sibling::div[1]')
                                    ai_summary = summary_content.text.strip()
                                    logger.info(f"Found AI summary with selector '{selector}'")
                                    break
                                except:
                                    ai_summary = text
                                    break
                        if ai_summary != 'N/A':
                            break
                except:
                    continue
            
            # Extract individual product ratings
            product_ratings = self._extract_comparison_ratings()
            
            # Extract pros/cons for each product
            pros_cons = self._extract_pros_cons()
            
            return {
                'company': company_name,
                'ai_generated_summary': ai_summary,
                'product_ratings': product_ratings,
                'pros_cons': pros_cons,
                'comparison_url': url,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error scraping head-to-head comparison for {company_name} from {url}: {str(e)}"
            logger.error(error_msg)
            self.session_stats['errors'].append(error_msg)
            return {'error': str(e), 'company': company_name}

    def _extract_market_segments(self):
        """Extract market segment information"""
        try:
            segment_selectors = [
                '.market-segment',
                '.segment',
                '.company-size',
                '[data-testid="market-segment"]',
                '.product-header__segment'
            ]
            return self._try_multiple_selectors(segment_selectors, 'N/A')
        except:
            return 'N/A'

    def _extract_pricing_info(self):
        """Extract pricing information"""
        try:
            pricing_selectors = [
                '.pricing',
                '.price',
                '.cost',
                '[data-testid="pricing"]',
                '.product-header__pricing'
            ]
            return self._try_multiple_selectors(pricing_selectors, 'N/A')
        except:
            return 'N/A'

    def _extract_comparison_ratings(self):
        """Extract ratings from comparison pages"""
        try:
            rating_elements = self.driver.find_elements(By.CSS_SELECTOR, '.rating, .score, [data-testid="rating"]')
            ratings = {}
            for element in rating_elements:
                try:
                    # Try to identify which product the rating belongs to
                    product_name = element.get_attribute('data-product') or 'unknown'
                    rating_value = element.text.strip()
                    ratings[product_name] = rating_value
                except:
                    continue
            return ratings
        except:
            return {}

    def _extract_pros_cons(self):
        """Extract pros and cons from comparison pages"""
        try:
            pros_cons = {}
            # Look for pros/cons sections
            pros_elements = self.driver.find_elements(By.CSS_SELECTOR, '.pros, .advantages, [data-testid="pros"]')
            cons_elements = self.driver.find_elements(By.CSS_SELECTOR, '.cons, .disadvantages, [data-testid="cons"]')
            
            for element in pros_elements:
                try:
                    product_name = element.get_attribute('data-product') or 'unknown'
                    if product_name not in pros_cons:
                        pros_cons[product_name] = {'pros': [], 'cons': []}
                    pros_cons[product_name]['pros'].append(element.text.strip())
                except:
                    continue
            
            for element in cons_elements:
                try:
                    product_name = element.get_attribute('data-product') or 'unknown'
                    if product_name not in pros_cons:
                        pros_cons[product_name] = {'pros': [], 'cons': []}
                    pros_cons[product_name]['cons'].append(element.text.strip())
                except:
                    continue
            
            return pros_cons
        except:
            return {}

    def _try_multiple_selectors(self, selectors, default_value='N/A'):
        """Try multiple CSS selectors to find an element"""
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        text = element.text.strip()
                        if text:
                            return text
            except:
                continue
        return default_value

    def batch_scrape_competitors(self, targets, focus_on_reviews=True, max_competitors=5):
        """Batch scrape competitors with enhanced anti-detection and limited scope"""
        logger.info(f"Starting batch scrape of up to {max_competitors} competitors")
        
        # Limit to first N competitors to avoid detection
        limited_competitors = dict(list(targets['competitors'].items())[:max_competitors])
        self.session_stats['total_targets'] = len(limited_competitors)
        
        for competitor_id, competitor_data in limited_competitors.items():
            try:
                company_name = competitor_data['name']
                logger.info(f"Processing {company_name} ({competitor_id})")
                
                # HIGH PRIORITY: Extract product reviews
                if focus_on_reviews and 'product_reviews' in competitor_data['targets']:
                    review_data = self.extract_product_reviews(
                        competitor_data['targets']['product_reviews'], 
                        company_name
                    )
                    
                    if 'error' not in review_data:
                        self.scraped_data[competitor_id] = review_data
                        self.session_stats['successful_scrapes'] += 1
                        logger.info(f"Successfully scraped reviews for {company_name}")
                    else:
                        self.session_stats['failed_scrapes'] += 1
                        logger.error(f"Failed to scrape reviews for {company_name}")
                        
                        # If we get blocked, stop scraping
                        if 'Access blocked' in str(review_data.get('error', '')):
                            logger.error("Access blocked detected. Stopping scraping to avoid further detection.")
                            break
                
                # Enhanced delay between competitors
                delay = random.uniform(10, 20)  # 10-20 seconds
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

    def save_data_to_json(self, filename='g2_sentiment_metrics_v3.json'):
        """Save scraped data to JSON file"""
        try:
            output_data = {
                'metadata': {
                    'scraping_session': datetime.now().strftime('%Y-%m-%d_%H:%M'),
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

    def save_data_to_csv(self, filename='g2_sentiment_metrics_v3.csv'):
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
                    'market_segments': data.get('market_segments', ''),
                    'pricing_info': data.get('pricing_info', ''),
                    'total_reviews_scraped': len(data.get('reviews', [])),
                    'scraped_at': data.get('scraped_at', ''),
                    'source_url': data.get('source_url', '')
                }
                
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False)
            
            logger.info(f"Data saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data to CSV: {str(e)}")
            return False

    def close(self):
        """Close the browser and cleanup"""
        try:
            self.driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

def main():
    """Main execution function with limited scope to avoid detection"""
    scraper = None
    try:
        # Initialize scraper
        scraper = G2SentimentScraperV3()
        
        # Load targets
        targets = scraper.load_targets()
        if not targets:
            logger.error("Failed to load targets")
            return
        
        # Execute LIMITED batch scraping to avoid detection
        # Start with just 3 competitors to test
        scraped_data = scraper.batch_scrape_competitors(targets, focus_on_reviews=True, max_competitors=3)
        
        # Save data to both formats
        scraper.save_data_to_json()
        scraper.save_data_to_csv()
        
        # Print summary
        print(f"\n{'='*60}")
        print("🎯 G2 SENTIMENT SCRAPING V3 COMPLETED (LIMITED SCOPE)")
        print(f"{'='*60}")
        print(f"Total Competitors: {scraper.session_stats['total_targets']}")
        print(f"Successful Scrapes: {scraper.session_stats['successful_scrapes']}")
        print(f"Failed Scrapes: {scraper.session_stats['failed_scrapes']}")
        print(f"Duration: {(datetime.now() - scraper.session_stats['start_time']).total_seconds() / 60:.1f} minutes")
        print(f"Data saved to: g2_sentiment_metrics_v3.json and g2_sentiment_metrics_v3.csv")
        
        if scraper.session_stats['errors']:
            print(f"\nErrors encountered: {len(scraper.session_stats['errors'])}")
            for error in scraper.session_stats['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
        
        print(f"\n💡 ANTI-DETECTION MEASURES IMPLEMENTED:")
        print(f"   - Enhanced Chrome options")
        print(f"   - Human-like behavior simulation")
        print(f"   - Random delays and user agents")
        print(f"   - Limited scope (3 competitors)")
        print(f"   - Blocking detection and prevention")
        
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
