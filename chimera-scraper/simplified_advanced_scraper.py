#!/usr/bin/env python3
"""
Simplified Advanced Scraper
Combines working CAPTCHA bypass with competitive intelligence extraction
Works with Python 3.8 and extracts AI summaries, competitive insights from G2.com
"""

import asyncio
import time
import json
import random
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import our working CAPTCHA bypass
from precision_puzzle_solver import PrecisionPuzzleSolver

# Import Playwright directly for browser control
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

class SimplifiedAdvancedScraper:
    """Simplified scraper combining CAPTCHA bypass with competitive intelligence extraction"""
    
    def __init__(self, headless=False):
        self.headless = headless
        self.captcha_solver = None
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        # Results tracking
        self.results = {
            'success': False,
            'captcha_bypassed': False,
            'data_extracted': False,
            'competitive_insights': [],
            'ai_summaries': [],
            'market_intelligence': {},
            'errors': [],
            'timing': {},
            'quality_metrics': {}
        }
    
    async def setup_browser_with_captcha_bypass(self):
        """Setup browser with our working CAPTCHA bypass"""
        try:
            print("🌐 Setting up browser with CAPTCHA bypass...")
            
            # Initialize Playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser with anti-detection measures
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-features=VizDisplayCompositor",
                    "--no-first-run",
                    "--disable-client-side-phishing-detection"
                ]
            )
            
            # Create context with stealth measures
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # Create page
            self.page = await self.context.new_page()
            
            # Add stealth scripts
            await self.page.add_init_script("""
                // Strategic stealth measures from analysis
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Prevent Playwright detection
                delete window._playwright_target_;
                delete window._playwright_global_listeners_check_;
            """)
            
            # Initialize our precision puzzle solver
            self.captcha_solver = PrecisionPuzzleSolver(self.page)
            
            print("✅ Browser setup with CAPTCHA bypass complete")
            return True
            
        except Exception as e:
            error_msg = f"Browser setup failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    async def navigate_and_bypass_captcha(self, url: str):
        """Navigate to URL and bypass any CAPTCHA challenges"""
        try:
            print(f"🌐 Navigating to: {url}")
            start_time = time.time()
            
            # Navigate to URL
            await self.page.goto(url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            # Check for CAPTCHA challenge
            captcha_detected = await self.detect_captcha_challenge()
            
            if captcha_detected:
                print("🛡️ CAPTCHA detected - applying precision solver...")
                
                # Use our working CAPTCHA bypass
                captcha_success = await self.captcha_solver.solve_puzzle()
                
                if captcha_success:
                    print("✅ CAPTCHA bypass successful!")
                    self.results['captcha_bypassed'] = True
                else:
                    print("❌ CAPTCHA bypass failed")
                    return False
                
                # Wait for page to load after CAPTCHA
                await asyncio.sleep(3)
            else:
                print("ℹ️ No CAPTCHA challenge detected")
            
            navigation_time = time.time() - start_time
            self.results['timing']['navigation'] = navigation_time
            
            print(f"✅ Navigation complete in {navigation_time:.2f}s")
            return True
            
        except Exception as e:
            error_msg = f"Navigation failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    async def detect_captcha_challenge(self) -> bool:
        """Detect if DataDome CAPTCHA challenge is present"""
        try:
            # Look for DataDome CAPTCHA elements
            captcha_selectors = [
                '[data-dd-captcha-container]',
                '.captcha__container',
                '#ddv1-captcha-container',
                '[class*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                try:
                    captcha_element = await self.page.query_selector(selector)
                    if captcha_element:
                        is_visible = await captcha_element.is_visible()
                        if is_visible:
                            print(f"✅ CAPTCHA challenge detected with selector: {selector}")
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ CAPTCHA detection error: {e}")
            return False
    
    async def extract_competitive_intelligence(self, url: str):
        """Extract competitive intelligence using direct DOM analysis"""
        try:
            print("🧠 Extracting competitive intelligence...")
            start_time = time.time()
            
            # Extract AI summaries (primary target)
            ai_summaries = await self._extract_ai_summaries()
            self.results['ai_summaries'] = ai_summaries
            
            # Extract competitive insights
            competitive_insights = await self._extract_competitive_insights()
            self.results['competitive_insights'] = competitive_insights
            
            # Extract market intelligence
            market_intelligence = await self._extract_market_intelligence()
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
    
    async def _extract_ai_summaries(self) -> List[Dict[str, Any]]:
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
                'h2',
                'h3',
                'div'
            ]
            
            for selector in ai_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    print(f"🔍 Found {len(elements)} elements with selector: {selector}")
                    
                    for i, element in enumerate(elements[:5]):  # Limit to first 5 elements
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    print(f"  Element {i+1}: {text.strip()[:100]}...")
                                    
                                    # Check if this looks like an AI summary
                                    if any(keyword in text.lower() for keyword in ['ai', 'generated', 'summary', 'powered by', 'user reviews']):
                                        ai_summaries.append({
                                            'summary_title': 'AI Generated Summary',
                                            'summary_text': text.strip(),
                                            'extraction_confidence': 90.0,
                                            'source': selector
                                        })
                                        print(f"✅ Found AI summary with selector: {selector}")
                                        print(f"   Text: {text.strip()[:100]}...")
                        except Exception as e:
                            print(f"  Element {i+1} error: {e}")
                            continue
                except Exception as e:
                    print(f"Selector {selector} error: {e}")
                    continue
            
            # Also look for summary text in the page content
            try:
                print("🔍 Extracting full page text...")
                # Get page content using the body selector
                page_text = await self.page.text_content('body')
                if page_text:
                    print(f"📄 Page text length: {len(page_text)} characters")
                    print(f"📄 Page text preview: {page_text[:500]}...")
                    
                    # Look for AI summary patterns in the text
                    ai_patterns = [
                        'AI Generated Summary',
                        'AI-generated summary',
                        'Powered by real user reviews',
                        'AI analysis'
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
    
    async def _extract_competitive_insights(self) -> List[Dict[str, Any]]:
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
                '.title', '.heading'
            ]
            
            for selector in product_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like product information
                                    if any(keyword in text.lower() for keyword in ['vs', 'compare', 'power bi', 'qlik', 'tableau', 'domo']):
                                        insights.append({
                                            'data_type': 'product_info',
                                            'content': text.strip(),
                                            'selector': selector,
                                            'extraction_confidence': 80.0
                                        })
                                        print(f"✅ Found product info: {text.strip()[:80]}...")
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
                '.rating', '.score', '.stars'
            ]
            
            for selector in rating_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like a rating
                                    if any(char in text for char in ['⭐', '★', '☆']) or any(word in text.lower() for word in ['rating', 'score', 'out of']):
                                        insights.append({
                                            'data_type': 'rating_score',
                                            'content': text.strip(),
                                            'selector': selector,
                                            'extraction_confidence': 85.0
                                        })
                                        print(f"✅ Found rating: {text.strip()}")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            # Extract review information
            review_selectors = [
                '[class*="review"]',
                '[data-testid*="review"]',
                '.review', '.reviews'
            ]
            
            for selector in review_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like review data
                                    if any(word in text.lower() for word in ['review', 'reviews', 'verified', 'helpful']):
                                        insights.append({
                                            'data_type': 'review_info',
                                            'content': text.strip(),
                                            'selector': selector,
                                            'extraction_confidence': 80.0
                                        })
                                        print(f"✅ Found review info: {text.strip()[:80]}...")
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            
            return insights
            
        except Exception as e:
            print(f"⚠️ Competitive insights extraction error: {e}")
            return insights
    
    async def _extract_market_intelligence(self) -> Dict[str, Any]:
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
                '[aria-label*="employees"]'
            ]
            
            market_segments = []
            for selector in segment_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like market segment data
                                    if any(word in text.lower() for word in ['small', 'mid', 'enterprise', 'employees', 'company']):
                                        market_segments.append({
                                            'text': text.strip(),
                                            'selector': selector,
                                            'confidence': 75.0
                                        })
                                        print(f"✅ Found market segment: {text.strip()}")
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
                '[class*="sector"]'
            ]
            
            industries = []
            for selector in industry_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like industry data
                                    if any(word in text.lower() for word in ['software', 'technology', 'healthcare', 'finance', 'marketing']):
                                        industries.append({
                                            'text': text.strip(),
                                            'selector': selector,
                                            'confidence': 75.0
                                        })
                                        print(f"✅ Found industry: {text.strip()}")
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
                '[data-testid*="pricing"]'
            ]
            
            pricing_info = []
            for selector in pricing_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        try:
                            is_visible = await element.is_visible()
                            if is_visible:
                                text = await element.text_content()
                                if text and text.strip():
                                    # Check if this looks like pricing data
                                    if any(char in text for char in ['$', '€', '£']) or any(word in text.lower() for word in ['price', 'pricing', 'cost', 'free', 'trial']):
                                        pricing_info.append({
                                            'text': text.strip(),
                                            'selector': selector,
                                            'confidence': 80.0
                                        })
                                        print(f"✅ Found pricing info: {text.strip()}")
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
    
    async def run_advanced_scraping_session(self, url: str):
        """Run complete advanced scraping session with CAPTCHA bypass"""
        print("🚀 Starting simplified advanced scraping session...")
        print("=" * 70)
        
        session_start = time.time()
        
        try:
            # Phase 1: Setup browser with CAPTCHA bypass
            if not await self.setup_browser_with_captcha_bypass():
                return False
            
            # Phase 2: Navigate and bypass CAPTCHA
            if not await self.navigate_and_bypass_captcha(url):
                return False
            
            # Phase 3: Extract competitive intelligence
            if not await self.extract_competitive_intelligence(url):
                print("⚠️ Competitive intelligence extraction had issues")
            
            # Phase 4: Session completion
            session_time = time.time() - session_start
            self.results['timing']['total_session'] = session_time
            self.results['success'] = True
            
            print("=" * 70)
            print(f"🎉 Advanced scraping session completed successfully in {session_time:.2f}s!")
            
            # Display results summary
            self._display_results_summary()
            
            return True
            
        except Exception as e:
            error_msg = f"Advanced scraping session failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
        
        finally:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
    
    def _display_results_summary(self):
        """Display comprehensive results summary"""
        print("\n📊 COMPREHENSIVE RESULTS SUMMARY:")
        print("=" * 50)
        
        print(f"✅ CAPTCHA Bypassed: {self.results['captcha_bypassed']}")
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
    
    def save_results(self, filename="simplified_advanced_results.json"):
        """Save comprehensive results to JSON file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            results_copy = self.results.copy()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_copy, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

async def main():
    """Test the simplified advanced scraper"""
    print("🧠 Simplified Advanced Scraper - Testing Phase")
    print("=" * 70)
    
    # Test configuration
    test_url = "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense"
    
    # Create scraper instance
    scraper = SimplifiedAdvancedScraper(headless=False)  # Set to True for production
    
    # Run advanced scraping session
    success = await scraper.run_advanced_scraping_session(test_url)
    
    # Save results
    if success:
        scraper.save_results()
        print("\n🎯 MVP VALIDATION: Advanced competitive intelligence achieved!")
    else:
        print("\n❌ MVP validation failed - review results for debugging")

if __name__ == "__main__":
    asyncio.run(main())
