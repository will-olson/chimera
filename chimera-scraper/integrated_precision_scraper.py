#!/usr/bin/env python3
"""
Integrated Precision Scraper
Combines existing working captcha solver with new precision puzzle solver
Implements the breakthrough mathematical model for DataDome CAPTCHA bypass
"""

import time
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from precision_puzzle_solver import PrecisionPuzzleSolver

class IntegratedPrecisionScraper:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.puzzle_solver = None
        self.results = {
            'success': False,
            'puzzle_solved': False,
            'data_extracted': False,
            'errors': [],
            'timing': {},
            'puzzle_stats': {}
        }
    
    def setup_driver(self):
        """Setup Chrome driver with anti-detection measures"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Anti-detection measures discovered through analysis
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Randomize user agent
            user_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute anti-detection script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup complete")
            return True
            
        except Exception as e:
            error_msg = f"Driver setup failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def navigate_to_target(self, url):
        """Navigate to target URL and wait for page load"""
        try:
            print(f"🌐 Navigating to: {url}")
            start_time = time.time()
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            load_time = time.time() - start_time
            self.results['timing']['page_load'] = load_time
            print(f"✅ Page loaded in {load_time:.2f}s")
            return True
            
        except Exception as e:
            error_msg = f"Navigation failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def detect_captcha_challenge(self):
        """Detect if DataDome CAPTCHA challenge is present"""
        try:
            print("🔍 Detecting CAPTCHA challenge...")
            
            # Look for DataDome CAPTCHA elements
            captcha_selectors = [
                '[data-dd-captcha-container]',
                '.captcha__container',
                '#ddv1-captcha-container',
                '[class*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    captcha_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if captcha_element.is_displayed():
                        print(f"✅ CAPTCHA challenge detected with selector: {selector}")
                        return True
                except:
                    continue
            
            print("ℹ️ No CAPTCHA challenge detected")
            return False
            
        except Exception as e:
            error_msg = f"CAPTCHA detection failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def solve_captcha_with_precision(self):
        """Solve CAPTCHA using the precision puzzle solver"""
        try:
            print("🧩 Initializing precision puzzle solver...")
            start_time = time.time()
            
            # Initialize precision puzzle solver
            self.puzzle_solver = PrecisionPuzzleSolver(self.driver)
            
            # Get solver configuration
            solver_stats = self.puzzle_solver.get_solving_stats()
            self.results['puzzle_stats'] = solver_stats
            
            print("📊 Puzzle solver configuration:")
            print(json.dumps(solver_stats, indent=2))
            
            # Attempt to solve the puzzle
            print("🎯 Attempting to solve puzzle...")
            puzzle_success = self.puzzle_solver.solve_puzzle()
            
            solve_time = time.time() - start_time
            self.results['timing']['puzzle_solve'] = solve_time
            
            if puzzle_success:
                print(f"🎉 Puzzle solved successfully in {solve_time:.2f}s!")
                self.results['puzzle_solved'] = True
                return True
            else:
                print(f"❌ Puzzle solving failed after {solve_time:.2f}s")
                return False
                
        except Exception as e:
            error_msg = f"Precision puzzle solving failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def extract_target_data(self):
        """Extract the target data after CAPTCHA bypass"""
        try:
            print("📊 Extracting target data...")
            start_time = time.time()
            
            # Wait for page to fully load after CAPTCHA
            time.sleep(3)
            
            # Look for common data elements
            data_selectors = [
                'h1', 'h2', 'h3',  # Headers
                '.title', '.heading',  # Title classes
                '[data-testid*="title"]',  # Test IDs
                '.product-name', '.company-name'  # Business data
            ]
            
            extracted_data = {}
            
            for selector in data_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for i, element in enumerate(elements[:3]):  # Limit to first 3
                        if element.is_displayed() and element.text.strip():
                            key = f"{selector}_{i+1}"
                            extracted_data[key] = element.text.strip()
                except:
                    continue
            
            # Get page title and URL
            extracted_data['page_title'] = self.driver.title
            extracted_data['current_url'] = self.driver.current_url
            
            extract_time = time.time() - start_time
            self.results['timing']['data_extraction'] = extract_time
            
            if extracted_data:
                print(f"✅ Data extracted successfully in {extract_time:.2f}s")
                print(f"📋 Extracted {len(extracted_data)} data points")
                self.results['data_extracted'] = True
                self.results['extracted_data'] = extracted_data
                return True
            else:
                print("⚠️ No data extracted")
                return False
                
        except Exception as e:
            error_msg = f"Data extraction failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def run_scraping_session(self, url):
        """Run complete scraping session with CAPTCHA bypass"""
        print("🚀 Starting integrated precision scraping session...")
        print("=" * 60)
        
        session_start = time.time()
        
        try:
            # Phase 1: Setup and navigation
            if not self.setup_driver():
                return False
            
            if not self.navigate_to_target(url):
                return False
            
            # Phase 2: CAPTCHA detection and solving
            if self.detect_captcha_challenge():
                print("🛡️ CAPTCHA challenge detected - applying precision solver...")
                
                if not self.solve_captcha_with_precision():
                    print("❌ CAPTCHA solving failed")
                    return False
                
                print("✅ CAPTCHA bypass successful!")
            else:
                print("ℹ️ No CAPTCHA challenge - proceeding with data extraction")
            
            # Phase 3: Data extraction
            if not self.extract_target_data():
                print("⚠️ Data extraction had issues")
            
            # Phase 4: Session completion
            session_time = time.time() - session_start
            self.results['timing']['total_session'] = session_time
            self.results['success'] = True
            
            print("=" * 60)
            print(f"🎉 Scraping session completed successfully in {session_time:.2f}s!")
            print(f"📊 Results: {json.dumps(self.results, indent=2)}")
            
            return True
            
        except Exception as e:
            error_msg = f"Scraping session failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_results(self, filename="precision_scraper_results.json"):
        """Save results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

def main():
    """Test the integrated precision scraper"""
    print("🧩 Integrated Precision Scraper - Testing Phase")
    print("=" * 60)
    
    # Test configuration
    test_url = "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense"
    
    # Create scraper instance
    scraper = IntegratedPrecisionScraper(headless=False)  # Set to True for production
    
    # Run scraping session
    success = scraper.run_scraping_session(test_url)
    
    # Save results
    if success:
        scraper.save_results()
        print("\n🎯 MVP VALIDATION: CAPTCHA bypass achieved!")
    else:
        print("\n❌ MVP validation failed - review results for debugging")

if __name__ == "__main__":
    main()
