#!/usr/bin/env python3
"""
Enhanced Competitive Intelligence Scraper
Builds on the working Selenium-based CAPTCHA bypass foundation
Extracts AI summaries, competitive insights, and market intelligence from G2.com
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

class EnhancedCompetitiveScraper:
    """Enhanced scraper that combines working CAPTCHA bypass with competitive intelligence extraction"""
    
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.puzzle_solver = None
        self.results = {
            'success': False,
            'puzzle_solved': False,
            'data_extracted': False,
            'competitive_insights': [],
            'ai_summaries': [],
            'market_intelligence': {},
            'errors': [],
            'timing': {},
            'quality_metrics': {}
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
                '[class*="captcha"]',
                'iframe[src*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    captcha_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in captcha_elements:
                        if element.is_displayed():
                            print(f"✅ CAPTCHA challenge detected with selector: {selector}")
                            return True
                except:
                    continue
            
            # Also check page source for CAPTCHA indicators
            page_source = self.driver.page_source
            if 'dd=' in page_source or 'captcha' in page_source.lower():
                print("✅ CAPTCHA challenge detected in page source")
                return True
            
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
            self.results['quality_metrics']['puzzle_solver_stats'] = solver_stats
            
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
    
    def extract_competitive_intelligence(self, url):
        """Extract competitive intelligence using advanced selectors"""
        try:
            print("🧠 Extracting competitive intelligence...")
            start_time = time.time()
            
            # Extract AI summaries (primary target)
            ai_summaries = self._extract_ai_summaries()
            self.results['ai_summaries'] = ai_summaries
            
            # Extract competitive insights
            competitive_insights = self._extract_competitive_insights()
            self.results['competitive_insights'] = competitive_insights
            
            # Extract market intelligence
            market_intelligence = self._extract_market_intelligence()
            self.results['market_intelligence'] = market_intelligence
            
            print(f"✅ Extracted {len(ai_summaries)} AI summaries")
            print(f"✅ Extracted {len(competitive_insights)} competitive insights")
            
            self.results['data_extracted'] = True
            
            extraction_time = time.time() - start_time
            self.results['timing']['data_extraction'] = extraction_time
            
            print(f"✅ Competitive intelligence extraction complete in {extraction_time:.2f}s")
            return True
            
        except Exception as e:
            error_msg = f"Competitive intelligence extraction failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    def _extract_ai_summaries(self):
        """Extract AI-generated summaries from the page"""
        ai_summaries = []
        
        try:
            print("🔍 Looking for AI-generated summaries...")
            
            # Look for AI summary sections using multiple strategies
            ai_selectors = [
                '[data-testid*="ai-summary"]',
                '[class*="ai-summary"]',
                '[class*="aiSummary"]',
                '[class*="summary"]',
                'h2', 'h3', 'h4',
                '[class*="ai"]',
                '[class*="generated"]'
            ]
            
            for selector in ai_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"🔍 Found {len(elements)} elements with selector: {selector}")
                    
                    for i, element in enumerate(elements[:5]):  # Limit to first 5 elements
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    print(f"  Element {i+1}: {text[:100]}...")
                                    
                                    # Check if this looks like an AI summary
                                    if any(keyword in text.lower() for keyword in ['ai', 'generated', 'summary', 'powered by', 'user reviews', 'analysis']):
                                        ai_summaries.append({
                                            'summary_title': 'AI Generated Summary',
                                            'summary_text': text,
                                            'extraction_confidence': 90.0,
                                            'source': selector
                                        })
                                        print(f"✅ Found AI summary with selector: {selector}")
                                        print(f"   Text: {text[:100]}...")
                        except Exception as e:
                            print(f"  Element {i+1} error: {e}")
                            continue
                except Exception as e:
                    print(f"Selector {selector} error: {e}")
                    continue
            
            # Also look for summary text in the page content
            try:
                print("🔍 Extracting full page text...")
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                if page_text:
                    print(f"📄 Page text length: {len(page_text)} characters")
                    print(f"📄 Page text preview: {page_text[:500]}...")
                    
                    # Look for AI summary patterns in the text
                    ai_patterns = [
                        'AI Generated Summary',
                        'AI-generated summary',
                        'Powered by real user reviews',
                        'AI analysis',
                        'AI-generated insights'
                    ]
                    
                    for pattern in ai_patterns:
                        if pattern.lower() in page_text.lower():
                            # Find the surrounding context
                            start_idx = page_text.lower().find(pattern.lower())
                            if start_idx >= 0:
                                # Extract surrounding text
                                context_start = max(0, start_idx - 200)
                                context_end = min(len(page_text), start_idx + 500)
                                context_text = page_text[context_start:context_end]
                                
                                ai_summaries.append({
                                    'summary_title': 'AI Summary Context',
                                    'summary_text': context_text.strip(),
                                    'extraction_confidence': 75.0,
                                    'source': 'text_pattern'
                                })
                                print(f"✅ Found AI summary context with pattern: {pattern}")
            except Exception as e:
                print(f"⚠️ Page text extraction error: {e}")
            
            return ai_summaries
            
        except Exception as e:
            print(f"⚠️ AI summary extraction error: {e}")
            return ai_summaries
    
    def _extract_competitive_insights(self):
        """Extract competitive insights from the page"""
        insights = []
        
        try:
            print("🔍 Looking for competitive insights...")
            
            # Extract product comparison data
            product_selectors = [
                'h1', 'h2', 'h3',
                '[class*="product"]',
                '[class*="company"]',
                '[data-testid*="title"]',
                '.title', '.heading',
                '[class*="comparison"]'
            ]
            
            for selector in product_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like product information
                                    if any(keyword in text.lower() for keyword in ['vs', 'compare', 'power bi', 'qlik', 'tableau', 'domo', 'business intelligence']):
                                        insights.append({
                                            'data_type': 'product_info',
                                            'content': text,
                                            'selector': selector,
                                            'extraction_confidence': 80.0
                                        })
                                        print(f"✅ Found product info: {text[:80]}...")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            # Extract ratings and scores
            rating_selectors = [
                '[class*="rating"]',
                '[class*="score"]',
                '[class*="star"]',
                '[data-testid*="rating"]',
                '.rating', '.score', '.stars',
                '[aria-label*="rating"]'
            ]
            
            for selector in rating_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like a rating
                                    if any(char in text for char in ['⭐', '★', '☆']) or any(word in text.lower() for word in ['rating', 'score', 'out of', 'stars']):
                                        insights.append({
                                            'data_type': 'rating_score',
                                            'content': text,
                                            'selector': selector,
                                            'extraction_confidence': 85.0
                                        })
                                        print(f"✅ Found rating: {text}")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            # Extract review information
            review_selectors = [
                '[class*="review"]',
                '[data-testid*="review"]',
                '.review', '.reviews',
                '[aria-label*="review"]'
            ]
            
            for selector in review_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like review data
                                    if any(word in text.lower() for word in ['review', 'reviews', 'verified', 'helpful', 'user']):
                                        insights.append({
                                            'data_type': 'review_info',
                                            'content': text,
                                            'selector': selector,
                                            'extraction_confidence': 80.0
                                        })
                                        print(f"✅ Found review info: {text[:80]}...")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            return insights
            
        except Exception as e:
            print(f"⚠️ Competitive insights extraction error: {e}")
            return insights
    
    def _extract_market_intelligence(self):
        """Extract market intelligence from the page"""
        market_intel = {}
        
        try:
            print("🔍 Looking for market intelligence...")
            
            # Extract market segment information
            segment_selectors = [
                '[class*="market"]',
                '[class*="segment"]',
                '[class*="company-size"]',
                '[aria-label*="company"]',
                '[aria-label*="employees"]',
                '[class*="demographic"]'
            ]
            
            market_segments = []
            for selector in segment_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like market segment data
                                    if any(word in text.lower() for word in ['small', 'mid', 'enterprise', 'employees', 'company', 'business']):
                                        market_segments.append({
                                            'text': text,
                                            'selector': selector,
                                            'confidence': 75.0
                                        })
                                        print(f"✅ Found market segment: {text}")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            if market_segments:
                market_intel['market_segments'] = market_segments
            
            # Extract industry information
            industry_selectors = [
                '[class*="industry"]',
                '[aria-label*="industry"]',
                '[class*="sector"]',
                '[class*="category"]'
            ]
            
            industries = []
            for selector in industry_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like industry data
                                    if any(word in text.lower() for word in ['software', 'technology', 'healthcare', 'finance', 'marketing', 'data']):
                                        industries.append({
                                            'text': text,
                                            'selector': selector,
                                            'confidence': 75.0
                                        })
                                        print(f"✅ Found industry: {text}")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            if industries:
                market_intel['industries'] = industries
            
            # Extract pricing information
            pricing_selectors = [
                '[class*="pricing"]',
                '[class*="price"]',
                '[class*="cost"]',
                '[data-testid*="pricing"]',
                '[class*="plan"]'
            ]
            
            pricing_info = []
            for selector in pricing_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        try:
                            if element.is_displayed():
                                text = element.text.strip()
                                if text:
                                    # Check if this looks like pricing data
                                    if any(char in text for char in ['$', '€', '£']) or any(word in text.lower() for word in ['price', 'pricing', 'cost', 'free', 'trial', 'plan']):
                                        pricing_info.append({
                                            'text': text,
                                            'selector': selector,
                                            'confidence': 80.0
                                        })
                                        print(f"✅ Found pricing info: {text}")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            if pricing_info:
                market_intel['pricing_info'] = pricing_info
            
            return market_intel
            
        except Exception as e:
            print(f"⚠️ Market intelligence extraction error: {e}")
            return market_intel
    
    def run_scraping_session(self, url):
        """Run complete enhanced scraping session with CAPTCHA bypass"""
        print("🚀 Starting enhanced competitive intelligence scraping session...")
        print("=" * 70)
        
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
            
            # Phase 3: Enhanced competitive intelligence extraction
            if not self.extract_competitive_intelligence(url):
                print("⚠️ Competitive intelligence extraction had issues")
            
            # Phase 4: Session completion
            session_time = time.time() - session_start
            self.results['timing']['total_session'] = session_time
            self.results['success'] = True
            
            print("=" * 70)
            print(f"🎉 Enhanced scraping session completed successfully in {session_time:.2f}s!")
            
            # Display results summary
            self._display_results_summary()
            
            return True
            
        except Exception as e:
            error_msg = f"Enhanced scraping session failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def _display_results_summary(self):
        """Display comprehensive results summary"""
        print("\n📊 COMPREHENSIVE RESULTS SUMMARY:")
        print("=" * 50)
        
        print(f"✅ CAPTCHA Bypassed: {self.results['puzzle_solved']}")
        print(f"✅ Data Extracted: {self.results['data_extracted']}")
        print(f"✅ AI Summaries: {len(self.results['ai_summaries'])}")
        print(f"✅ Competitive Insights: {len(self.results['competitive_insights'])}")
        print(f"✅ Market Intelligence: {len(self.results['market_intelligence'])}")
        
        if self.results['ai_summaries']:
            print(f"\n🧠 AI SUMMARY HIGHLIGHTS:")
            for i, summary in enumerate(self.results['ai_summaries'][:3], 1):
                title = summary.get('summary_title', 'Unknown')
                confidence = summary.get('extraction_confidence', 0)
                text_preview = summary.get('summary_text', '')[:100] + '...' if len(summary.get('summary_text', '')) > 100 else summary.get('summary_text', '')
                print(f"  {i}. {title} (Confidence: {confidence}%)")
                print(f"     Preview: {text_preview}")
        
        if self.results['competitive_insights']:
            print(f"\n📈 COMPETITIVE INSIGHTS:")
            for i, insight in enumerate(self.results['competitive_insights'][:3], 1):
                data_type = insight.get('data_type', 'Unknown')
                content_preview = insight.get('content', '')[:80] + '...' if len(insight.get('content', '')) > 80 else insight.get('content', '')
                confidence = insight.get('extraction_confidence', 0)
                print(f"  {i}. {data_type} (Confidence: {confidence}%)")
                print(f"     Content: {content_preview}")
        
        print(f"\n⏱️ TIMING BREAKDOWN:")
        for key, value in self.results['timing'].items():
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}s")
    
    def save_results(self, filename="enhanced_competitive_results.json"):
        """Save comprehensive results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

def main():
    """Test the enhanced competitive intelligence scraper"""
    print("🧠 Enhanced Competitive Intelligence Scraper - Testing Phase")
    print("=" * 70)
    
    # Test configuration
    test_url = "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense"
    
    # Create scraper instance
    scraper = EnhancedCompetitiveScraper(headless=False)  # Set to True for production
    
    # Run enhanced scraping session
    success = scraper.run_scraping_session(test_url)
    
    # Save results
    if success:
        scraper.save_results()
        print("\n🎯 MVP VALIDATION: Enhanced competitive intelligence achieved!")
    else:
        print("\n❌ MVP validation failed - review results for debugging")

if __name__ == "__main__":
    main()
