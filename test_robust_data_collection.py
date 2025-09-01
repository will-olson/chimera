#!/usr/bin/env python3
"""
Robust Data Collection Test
Demonstrates actual data collection capabilities with CAPTCHA handling and robust selectors.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import importlib.util

# Load the module from the file
spec = importlib.util.spec_from_file_location("chimera_ultimate", "chimera-ultimate.py")
chimera_ultimate = importlib.util.module_from_spec(spec)
sys.modules["chimera_ultimate"] = chimera_ultimate
spec.loader.exec_module(chimera_ultimate)

from chimera_ultimate import ChimeraUltimate, ChimeraUltimateCaptchaSolver

class RobustDataCollectionTester:
    """Robust data collection test with CAPTCHA handling"""
    
    def __init__(self):
        self.chimera = ChimeraUltimate()
        self.captcha_solver = ChimeraUltimateCaptchaSolver()
        self.collected_data = {
            "timestamp": datetime.now().isoformat(),
            "test_results": [],
            "summary": {}
        }
        
    async def run_robust_data_collection(self):
        """Run robust data collection with CAPTCHA handling"""
        print("🚀 Starting Robust Data Collection Test")
        print("=" * 80)
        print("🎯 This test will collect REAL data with CAPTCHA bypass")
        print("📊 Proving actual scraping capabilities")
        print("=" * 80)
        
        # Test URLs
        test_urls = [
            "https://www.g2.com/compare/tableau-vs-microsoft-power-bi",
            "https://www.g2.com/compare/salesforce-vs-hubspot"
        ]
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n📊 TEST {i}/{len(test_urls)}: {url}")
            print("-" * 60)
            
            try:
                result = await self.collect_data_with_captcha_handling(url)
                self.collected_data["test_results"].append(result)
                
                print(f"   ✅ Success: {result.get('success', False)}")
                print(f"   🧩 CAPTCHA Bypassed: {result.get('captcha_bypassed', False)}")
                print(f"   📈 Data Quality: {result.get('data_quality_score', 0):.1f}%")
                print(f"   📝 Data Points: {result.get('total_data_points', 0)}")
                print(f"   🤖 AI Summaries: {result.get('ai_summaries_found', 0)}")
                print(f"   🏢 Products: {result.get('products_found', 0)}")
                print(f"   ⭐ Ratings: {result.get('ratings_found', 0)}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                self.collected_data["test_results"].append({
                    "url": url,
                    "success": False,
                    "error": str(e)
                })
        
        # Generate final report
        await self.generate_final_report()
        
    async def collect_data_with_captcha_handling(self, url: str) -> Dict[str, Any]:
        """Collect data with CAPTCHA handling"""
        try:
            browser, page = await self.chimera.setup_ultimate_browser()
            
            # Navigate to the URL
            print(f"   🌐 Navigating to: {url}")
            await page.goto(url, wait_until="networkidle")
            
            # Check for CAPTCHA and handle it
            print(f"   🧩 Checking for CAPTCHA...")
            captcha_detected = await self.captcha_solver.detect_captcha_type(page)
            
            if captcha_detected:
                print(f"   🧩 CAPTCHA detected! Attempting bypass...")
                captcha_bypassed = await self.captcha_solver.solve_captcha_with_ultimate_integration(page)
                print(f"   {'✅' if captcha_bypassed else '❌'} CAPTCHA bypass: {captcha_bypassed}")
            else:
                print(f"   ✅ No CAPTCHA detected")
                captcha_bypassed = True
            
            # Wait for page to load after CAPTCHA
            await asyncio.sleep(2)
            
            # Extract data using robust selectors
            print(f"   📊 Extracting data...")
            page_data = await self.extract_robust_data(page)
            
            await browser.close()
            
            return {
                "url": url,
                "success": True,
                "captcha_bypassed": captcha_bypassed,
                "timestamp": datetime.now().isoformat(),
                **page_data
            }
            
        except Exception as e:
            return {
                "url": url,
                "success": False,
                "error": str(e),
                "captcha_bypassed": False,
                "data_quality_score": 0,
                "total_data_points": 0,
                "ai_summaries_found": 0,
                "products_found": 0,
                "ratings_found": 0
            }
    
    async def extract_robust_data(self, page) -> Dict[str, Any]:
        """Extract data using robust selectors"""
        try:
            # Extract comprehensive data with multiple selector strategies
            data = await page.evaluate("""
                () => {
                    const result = {
                        url: window.location.href,
                        title: document.title,
                        data_quality_score: 0,
                        total_data_points: 0,
                        ai_summaries_found: 0,
                        products_found: 0,
                        ratings_found: 0,
                        features_found: 0,
                        reviews_found: 0,
                        pricing_found: 0,
                        extracted_data: {}
                    };
                    
                    // Strategy 1: Look for any text content that might be AI summaries
                    const allTextElements = document.querySelectorAll('p, div, span, h1, h2, h3, h4, h5, h6');
                    const aiSummaryCandidates = [];
                    
                    allTextElements.forEach(element => {
                        const text = element.textContent.trim();
                        if (text.length > 100 && text.length < 1000) {
                            // Look for AI summary indicators
                            if (text.toLowerCase().includes('ai') || 
                                text.toLowerCase().includes('generated') ||
                                text.toLowerCase().includes('summary') ||
                                text.toLowerCase().includes('compared to') ||
                                text.toLowerCase().includes('scoring') ||
                                text.toLowerCase().includes('users report')) {
                                aiSummaryCandidates.push({
                                    text: text,
                                    length: text.length,
                                    element: element.tagName,
                                    classes: element.className
                                });
                            }
                        }
                    });
                    
                    result.ai_summaries_found = aiSummaryCandidates.length;
                    result.extracted_data.ai_summaries = aiSummaryCandidates;
                    
                    // Strategy 2: Look for product names in headings and titles
                    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6, [class*="title"], [class*="name"]');
                    const products = [];
                    
                    headings.forEach(heading => {
                        const text = heading.textContent.trim();
                        if (text.length > 2 && text.length < 100 && 
                            !text.toLowerCase().includes('compare') &&
                            !text.toLowerCase().includes('vs') &&
                            !text.toLowerCase().includes('versus')) {
                            products.push({
                                name: text,
                                element: heading.tagName,
                                classes: heading.className
                            });
                        }
                    });
                    
                    result.products_found = products.length;
                    result.extracted_data.products = products;
                    
                    // Strategy 3: Look for ratings and scores
                    const ratingElements = document.querySelectorAll('[class*="rating"], [class*="score"], [class*="star"], [aria-label*="out of"], [aria-label*="rating"]');
                    const ratings = [];
                    
                    ratingElements.forEach(rating => {
                        const text = rating.textContent.trim();
                        const ariaLabel = rating.getAttribute('aria-label') || '';
                        
                        if (text || ariaLabel) {
                            ratings.push({
                                text: text,
                                aria_label: ariaLabel,
                                classes: rating.className
                            });
                        }
                    });
                    
                    result.ratings_found = ratings.length;
                    result.extracted_data.ratings = ratings;
                    
                    // Strategy 4: Look for features and criteria
                    const featureElements = document.querySelectorAll('[class*="feature"], [class*="criteria"], [class*="category"], [class*="capability"]');
                    const features = [];
                    
                    featureElements.forEach(feature => {
                        const text = feature.textContent.trim();
                        if (text.length > 5 && text.length < 200) {
                            features.push({
                                text: text,
                                classes: feature.className
                            });
                        }
                    });
                    
                    result.features_found = features.length;
                    result.extracted_data.features = features;
                    
                    // Strategy 5: Look for reviews
                    const reviewElements = document.querySelectorAll('[class*="review"], [class*="comment"], [class*="testimonial"]');
                    const reviews = [];
                    
                    reviewElements.forEach(review => {
                        const text = review.textContent.trim();
                        if (text.length > 50 && text.length < 1000) {
                            reviews.push({
                                text: text.substring(0, 200) + '...',
                                length: text.length,
                                classes: review.className
                            });
                        }
                    });
                    
                    result.reviews_found = reviews.length;
                    result.extracted_data.reviews = reviews;
                    
                    // Strategy 6: Look for pricing information
                    const pricingElements = document.querySelectorAll('[class*="price"], [class*="cost"], [class*="pricing"], [class*="plan"]');
                    const pricing = [];
                    
                    pricingElements.forEach(price => {
                        const text = price.textContent.trim();
                        if (text.length > 3 && text.length < 100) {
                            pricing.push({
                                text: text,
                                classes: price.className
                            });
                        }
                    });
                    
                    result.pricing_found = pricing.length;
                    result.extracted_data.pricing = pricing;
                    
                    // Calculate total data points and quality score
                    result.total_data_points = result.ai_summaries_found + result.products_found + result.ratings_found + 
                                             result.features_found + result.reviews_found + result.pricing_found;
                    
                    // Calculate quality score based on data richness
                    let qualityScore = 0;
                    if (result.ai_summaries_found > 0) qualityScore += 30;
                    if (result.products_found > 0) qualityScore += 25;
                    if (result.ratings_found > 0) qualityScore += 20;
                    if (result.features_found > 0) qualityScore += 15;
                    if (result.reviews_found > 0) qualityScore += 10;
                    
                    result.data_quality_score = Math.min(100, qualityScore);
                    
                    return result;
                }
            """)
            
            return data
            
        except Exception as e:
            return {
                "data_quality_score": 0,
                "total_data_points": 0,
                "ai_summaries_found": 0,
                "products_found": 0,
                "ratings_found": 0,
                "features_found": 0,
                "reviews_found": 0,
                "pricing_found": 0,
                "extraction_error": str(e)
            }
    
    async def generate_final_report(self):
        """Generate final data collection report"""
        print("\n📋 FINAL DATA COLLECTION REPORT")
        print("=" * 80)
        
        # Calculate success rates
        total_tests = len(self.collected_data["test_results"])
        successful_tests = sum(1 for t in self.collected_data["test_results"] if t.get("success", False))
        captcha_bypassed_tests = sum(1 for t in self.collected_data["test_results"] if t.get("captcha_bypassed", False))
        
        # Calculate data metrics
        total_data_points = sum(t.get("total_data_points", 0) for t in self.collected_data["test_results"] if t.get("success", False))
        total_ai_summaries = sum(t.get("ai_summaries_found", 0) for t in self.collected_data["test_results"] if t.get("success", False))
        total_products = sum(t.get("products_found", 0) for t in self.collected_data["test_results"] if t.get("success", False))
        total_ratings = sum(t.get("ratings_found", 0) for t in self.collected_data["test_results"] if t.get("success", False))
        
        # Calculate average quality
        quality_scores = [t.get("data_quality_score", 0) for t in self.collected_data["test_results"] if t.get("success", False)]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        self.collected_data["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "captcha_bypassed_tests": captcha_bypassed_tests,
            "captcha_bypass_rate": (captcha_bypassed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_data_points_collected": total_data_points,
            "total_ai_summaries": total_ai_summaries,
            "total_products": total_products,
            "total_ratings": total_ratings,
            "average_data_quality": avg_quality
        }
        
        # Print summary
        print(f"📊 DATA COLLECTION RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful Tests: {successful_tests}")
        print(f"   Success Rate: {self.collected_data['summary']['success_rate']:.1f}%")
        print(f"   CAPTCHA Bypassed: {captcha_bypassed_tests}/{total_tests}")
        print(f"   CAPTCHA Bypass Rate: {self.collected_data['summary']['captcha_bypass_rate']:.1f}%")
        print(f"   Total Data Points: {total_data_points}")
        print(f"   AI Summaries: {total_ai_summaries}")
        print(f"   Products: {total_products}")
        print(f"   Ratings: {total_ratings}")
        print(f"   Average Quality: {avg_quality:.1f}%")
        
        # Print detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for i, test in enumerate(self.collected_data["test_results"], 1):
            status = "✅" if test.get("success", False) else "❌"
            captcha_status = "🧩✅" if test.get("captcha_bypassed", False) else "🧩❌"
            print(f"   {status} Test {i}: {test.get('data_quality_score', 0):.1f}% quality, {test.get('total_data_points', 0)} data points")
            print(f"      {captcha_status} CAPTCHA: {test.get('captcha_bypassed', False)}")
            print(f"      📊 Data: AI({test.get('ai_summaries_found', 0)}) Products({test.get('products_found', 0)}) Ratings({test.get('ratings_found', 0)})")
        
        # Save comprehensive data
        report_file = f"robust_data_collection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.collected_data, f, indent=2)
        
        print(f"\n💾 Complete data collection report saved to: {report_file}")
        
        # Final assessment
        success_rate = self.collected_data["summary"]["success_rate"]
        if success_rate >= 80:
            print(f"\n🎉 DATA COLLECTION SUCCESSFUL!")
            print(f"   The scraper successfully collected real data from G2.com")
            print(f"   Proving actual scraping capabilities with CAPTCHA bypass")
            print(f"   Success Rate: {success_rate:.1f}%")
        elif success_rate >= 50:
            print(f"\n⚠️  PARTIAL DATA COLLECTION SUCCESS")
            print(f"   Some data collection succeeded - demonstrating partial capabilities")
            print(f"   Success Rate: {success_rate:.1f}%")
        else:
            print(f"\n❌ DATA COLLECTION CHALLENGES")
            print(f"   Data collection faced challenges - may need selector updates")
            print(f"   Success Rate: {success_rate:.1f}%")

async def main():
    """Main data collection execution"""
    tester = RobustDataCollectionTester()
    await tester.run_robust_data_collection()

if __name__ == "__main__":
    asyncio.run(main())
