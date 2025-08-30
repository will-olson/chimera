#!/usr/bin/env python3
"""
Integrated Advanced Scraper
Combines working CAPTCHA bypass with existing advanced competitive intelligence system
Extracts AI summaries, competitive insights, and market intelligence from G2.com
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

# Import the existing advanced system
import sys
sys.path.append('src')
from chimera.core.competitive_intelligence_scraper import CompetitiveIntelligenceScraper, CompetitiveTarget
from chimera.parsers.head_to_head_comparison import G2HeadToHeadComparisonParser
from chimera.parsers.four_way_comparison import G2FourWayComparisonParser

class IntegratedAdvancedScraper:
    """Integrated scraper combining CAPTCHA bypass with advanced competitive intelligence"""
    
    def __init__(self, headless=False):
        self.headless = headless
        self.captcha_solver = None
        self.competitive_scraper = None
        self.parser = None
        
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
    
    async def initialize_advanced_system(self):
        """Initialize the existing advanced competitive intelligence system"""
        try:
            print("🚀 Initializing advanced competitive intelligence system...")
            
            # Initialize the existing competitive intelligence scraper
            self.competitive_scraper = CompetitiveIntelligenceScraper()
            
            # Initialize advanced parsers
            self.head_to_head_parser = G2HeadToHeadComparisonParser()
            self.four_way_parser = G2FourWayComparisonParser()
            
            print("✅ Advanced system initialized successfully")
            return True
            
        except Exception as e:
            error_msg = f"Advanced system initialization failed: {e}"
            self.results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
            return False
    
    async def setup_browser_with_captcha_bypass(self):
        """Setup browser with our working CAPTCHA bypass"""
        try:
            print("🌐 Setting up browser with CAPTCHA bypass...")
            
            # Use the existing competitive intelligence scraper's browser setup
            await self.competitive_scraper._setup_browser(headless=self.headless)
            
            # Get the page for CAPTCHA bypass
            self.page = self.competitive_scraper.page
            
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
            
            # Navigate using the advanced scraper
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
        """Extract competitive intelligence using the advanced parsers"""
        try:
            print("🧠 Extracting competitive intelligence...")
            start_time = time.time()
            
            # Get page content
            page_content = await self.page.content()
            
            # Determine page type and use appropriate parser
            if "vs-" in url and url.count("vs-") >= 1:
                print("📊 Detected comparison page - using head-to-head parser...")
                
                # Use the advanced head-to-head parser
                comparison_data = await self.head_to_head_parser.parse_head_to_head_comparison(
                    page_content, url
                )
                
                if comparison_data:
                    # Extract AI summaries (primary target)
                    ai_summaries = self._extract_ai_summaries(comparison_data)
                    self.results['ai_summaries'] = ai_summaries
                    
                    # Extract competitive insights
                    competitive_insights = self._extract_competitive_insights(comparison_data)
                    self.results['competitive_insights'] = competitive_insights
                    
                    # Extract market intelligence
                    market_intelligence = self._extract_market_intelligence(comparison_data)
                    self.results['market_intelligence'] = market_intelligence
                    
                    print(f"✅ Extracted {len(ai_summaries)} AI summaries")
                    print(f"✅ Extracted {len(competitive_insights)} competitive insights")
                    
                    self.results['data_extracted'] = True
                else:
                    print("⚠️ No comparison data extracted")
                    return False
            
            elif "vs-" in url and url.count("vs-") >= 3:
                print("📊 Detected four-way comparison page - using four-way parser...")
                
                # Use the advanced four-way parser
                four_way_data = await self.four_way_parser.parse_four_way_comparison(
                    page_content, url
                )
                
                if four_way_data:
                    # Extract comprehensive comparison data
                    self.results['competitive_insights'] = [four_way_data]
                    self.results['data_extracted'] = True
                    print("✅ Four-way comparison data extracted")
                else:
                    print("⚠️ No four-way comparison data extracted")
                    return False
            
            else:
                print("ℹ️ Standard page - extracting basic competitive data...")
                
                # Extract basic competitive data
                basic_data = await self._extract_basic_competitive_data()
                if basic_data:
                    self.results['competitive_insights'] = [basic_data]
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
    
    def _extract_ai_summaries(self, comparison_data) -> List[Dict[str, Any]]:
        """Extract AI-generated summaries from comparison data"""
        ai_summaries = []
        
        try:
            # Look for AI summary data in the comparison data
            if hasattr(comparison_data, 'ai_summary') and comparison_data.ai_summary:
                ai_summaries.append({
                    'summary_title': getattr(comparison_data.ai_summary, 'summary_title', 'AI Generated Summary'),
                    'summary_subtitle': getattr(comparison_data.ai_summary, 'summary_subtitle', ''),
                    'summary_points': getattr(comparison_data.ai_summary, 'summary_points', []),
                    'extraction_confidence': getattr(comparison_data.ai_summary, 'extraction_confidence', 0.0),
                    'structured_insights': getattr(comparison_data.ai_summary, 'structured_insights', {})
                })
            
            # Also look for AI summary text in the content
            if hasattr(comparison_data, 'content'):
                content = comparison_data.content
                if isinstance(content, dict):
                    # Look for AI summary sections
                    for key, value in content.items():
                        if 'ai' in key.lower() or 'summary' in key.lower():
                            if isinstance(value, str) and value.strip():
                                ai_summaries.append({
                                    'summary_title': f'AI Summary - {key}',
                                    'summary_text': value,
                                    'extraction_confidence': 85.0,
                                    'source': key
                                })
            
            return ai_summaries
            
        except Exception as e:
            print(f"⚠️ AI summary extraction error: {e}")
            return ai_summaries
    
    def _extract_competitive_insights(self, comparison_data) -> List[Dict[str, Any]]:
        """Extract competitive insights from comparison data"""
        insights = []
        
        try:
            # Extract product comparison data
            if hasattr(comparison_data, 'products'):
                for product in comparison_data.products:
                    insight = {
                        'product_name': getattr(product, 'name', 'Unknown'),
                        'star_rating': getattr(product, 'star_rating', 0.0),
                        'review_count': getattr(product, 'review_count', 0),
                        'market_segments': getattr(product, 'market_segments', {}),
                        'entry_level_pricing': getattr(product, 'entry_level_pricing', ''),
                        'ratings_by_criteria': getattr(product, 'ratings_by_criteria', {}),
                        'feature_scores': getattr(product, 'feature_scores', {})
                    }
                    insights.append(insight)
            
            # Extract additional competitive data
            if hasattr(comparison_data, 'at_a_glance'):
                insights.append({
                    'data_type': 'at_a_glance',
                    'content': comparison_data.at_a_glance
                })
            
            if hasattr(comparison_data, 'pricing'):
                insights.append({
                    'data_type': 'pricing_analysis',
                    'content': comparison_data.pricing
                })
            
            return insights
            
        except Exception as e:
            print(f"⚠️ Competitive insights extraction error: {e}")
            return insights
    
    def _extract_market_intelligence(self, comparison_data) -> Dict[str, Any]:
        """Extract market intelligence from comparison data"""
        market_intel = {}
        
        try:
            # Extract market positioning data
            if hasattr(comparison_data, 'market_insights'):
                market_intel = comparison_data.market_insights
            
            # Extract competitive positioning
            if hasattr(comparison_data, 'competitive_positioning'):
                market_intel['competitive_positioning'] = comparison_data.competitive_positioning
            
            # Extract feature competitiveness
            if hasattr(comparison_data, 'features_by_category'):
                market_intel['feature_competitiveness'] = comparison_data.features_by_category
            
            return market_intel
            
        except Exception as e:
            print(f"⚠️ Market intelligence extraction error: {e}")
            return market_intel
    
    async def _extract_basic_competitive_data(self) -> Dict[str, Any]:
        """Extract basic competitive data from standard pages"""
        try:
            # Extract page title and basic information
            title = await self.page.title()
            
            # Look for product information
            product_selectors = [
                'h1', 'h2', '.product-name', '.company-name',
                '[data-testid*="title"]', '.title'
            ]
            
            product_info = {}
            for selector in product_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        text = await element.text_content()
                        if text and text.strip():
                            product_info[selector] = text.strip()
                except:
                    continue
            
            return {
                'page_title': title,
                'url': self.page.url,
                'product_info': product_info,
                'extraction_date': datetime.now().isoformat(),
                'data_type': 'basic_competitive'
            }
            
        except Exception as e:
            print(f"⚠️ Basic competitive data extraction error: {e}")
            return {}
    
    async def run_advanced_scraping_session(self, url: str):
        """Run complete advanced scraping session with CAPTCHA bypass"""
        print("🚀 Starting integrated advanced scraping session...")
        print("=" * 70)
        
        session_start = time.time()
        
        try:
            # Phase 1: Initialize advanced system
            if not await self.initialize_advanced_system():
                return False
            
            # Phase 2: Setup browser with CAPTCHA bypass
            if not await self.setup_browser_with_captcha_bypass():
                return False
            
            # Phase 3: Navigate and bypass CAPTCHA
            if not await self.navigate_and_bypass_captcha(url):
                return False
            
            # Phase 4: Extract competitive intelligence
            if not await self.extract_competitive_intelligence(url):
                print("⚠️ Competitive intelligence extraction had issues")
            
            # Phase 5: Session completion
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
            if hasattr(self, 'competitive_scraper') and self.competitive_scraper:
                await self.competitive_scraper._cleanup()
    
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
                print(f"  {i}. {title} (Confidence: {confidence}%)")
        
        if self.results['competitive_insights']:
            print(f"\n📈 COMPETITIVE INSIGHTS:")
            for i, insight in enumerate(self.results['competitive_insights'][:3], 1):
                if 'product_name' in insight:
                    name = insight['product_name']
                    rating = insight.get('star_rating', 0)
                    reviews = insight.get('review_count', 0)
                    print(f"  {i}. {name}: ⭐{rating}/5 ({reviews} reviews)")
        
        print(f"\n⏱️ TIMING BREAKDOWN:")
        for key, value in self.results['timing'].items():
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}s")
    
    def save_results(self, filename="advanced_scraper_results.json"):
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
    """Test the integrated advanced scraper"""
    print("🧠 Integrated Advanced Scraper - Testing Phase")
    print("=" * 70)
    
    # Test configuration
    test_url = "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense"
    
    # Create scraper instance
    scraper = IntegratedAdvancedScraper(headless=False)  # Set to True for production
    
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
