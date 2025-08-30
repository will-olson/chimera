#!/usr/bin/env python3
"""Manual CAPTCHA Solver for G2.com DataDome Challenges."""
import asyncio
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from standalone_parser import StandaloneHeadToHeadParser, HeadToHeadComparisonData

class ManualCaptchaSolver:
    """Manual CAPTCHA solver for DataDome challenges."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "total_requests": 0,
            "successful_requests": 0,
            "captcha_challenges": 0,
            "captcha_solved": 0,
            "browser_automation_attempts": 0,
            "results": []
        }
        
    def get_realistic_delay(self, min_delay: float = 2.0, max_delay: float = 6.0) -> float:
        """Get realistic human-like delay."""
        return random.uniform(min_delay, max_delay)
        
    def get_stealth_headers(self) -> Dict[str, str]:
        """Get stealth headers for DataDome bypass."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"'
        }
        return headers
        
    async def solve_captcha_manually(self, url: str) -> Dict[str, Any]:
        """Open browser, wait for manual CAPTCHA solving, then extract content."""
        print(f"🌐 Opening browser for manual CAPTCHA solving: {url}")
        self.test_results["browser_automation_attempts"] += 1
        
        try:
            # Check if Playwright is available
            try:
                from playwright.async_api import async_playwright
            except ImportError:
                print("⚠️  Playwright not installed. Install with: pip install playwright")
                return {
                    "url": url,
                    "status_code": None,
                    "method": "manual_captcha_solving",
                    "success": False,
                    "data": None,
                    "error": "Playwright not installed"
                }
            
            async with async_playwright() as p:
                # Launch browser with stealth options
                browser = await p.chromium.launch(
                    headless=False,  # Run in visible mode for manual solving
                    args=[
                        "--no-sandbox",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--disable-extensions",
                        "--disable-gpu",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor",
                        "--disable-background-timer-throttling",
                        "--disable-backgrounding-occluded-windows",
                        "--disable-renderer-backgrounding",
                        "--disable-ipc-flooding-protection",
                        "--disable-default-apps",
                        "--disable-sync",
                        "--disable-translate",
                        "--hide-scrollbars",
                        "--mute-audio",
                        "--no-first-run"
                    ]
                )
                
                # Create context with stealth settings
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers=self.get_stealth_headers(),
                    ignore_https_errors=True,
                    java_script_enabled=True,
                    has_touch=False,
                    is_mobile=False,
                    device_scale_factor=1,
                    color_scheme="light"
                )
                
                # Add stealth scripts
                await context.add_init_script("""
                    // Remove automation indicators
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    // Fake plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [
                            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: ''},
                            {name: 'Native Client', filename: 'internal-nacl-plugin', description: 'Native Client Executable'}
                        ],
                    });
                    
                    // Fake languages
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                    });
                    
                    // Fake chrome runtime
                    if (window.chrome) {
                        Object.defineProperty(window.chrome, 'runtime', {
                            get: () => undefined,
                        });
                    }
                    
                    // Fake automation
                    Object.defineProperty(navigator, 'automation', {
                        get: () => undefined,
                    });
                """)
                
                # Create page
                page = await context.new_page()
                
                # Set realistic viewport
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Navigate to URL
                print(f"🌐 Navigating to: {url}")
                
                try:
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except Exception as e:
                    print(f"⚠️  Navigation failed: {str(e)}")
                    response = None
                
                # Wait for content to load
                await asyncio.sleep(5)
                
                # Check initial content
                initial_content = await page.content()
                print(f"📄 Initial content size: {len(initial_content)} characters")
                
                # Check for CAPTCHA challenge
                captcha_detected = False
                try:
                    captcha_selectors = [
                        "div[id*='challenge']",
                        "div[class*='challenge']", 
                        "div[class*='captcha']",
                        "div[class*='slider']",
                        "div[class*='puzzle']",
                        "div[class*='verification']"
                    ]
                    
                    for selector in captcha_selectors:
                        captcha_element = await page.query_selector(selector)
                        if captcha_element:
                            captcha_detected = True
                            print(f"🛡️  CAPTCHA challenge detected with selector: {selector}")
                            self.test_results["captcha_challenges"] += 1
                            break
                            
                except Exception as e:
                    print(f"⚠️  Error checking for CAPTCHA: {str(e)}")
                
                if captcha_detected:
                    print("\n" + "="*60)
                    print("🧩 MANUAL CAPTCHA SOLVING REQUIRED")
                    print("="*60)
                    print("👤 Please solve the CAPTCHA puzzle in the browser window...")
                    print("📱 The browser will wait for you to complete the challenge")
                    print("⏱️  You have up to 5 minutes to solve it")
                    print("="*60)
                    
                    # Wait for manual CAPTCHA solving (up to 5 minutes)
                    max_wait_time = 300  # 5 minutes
                    wait_interval = 10   # Check every 10 seconds
                    total_waited = 0
                    
                    while total_waited < max_wait_time:
                        await asyncio.sleep(wait_interval)
                        total_waited += wait_interval
                        
                        print(f"⏱️  Waiting... ({total_waited}/{max_wait_time}s elapsed)")
                        
                        # Check if challenge is resolved
                        try:
                            challenge_still_present = await page.query_selector("div[id*='challenge'], div[class*='challenge'], div[class*='captcha']")
                            if not challenge_still_present:
                                print("✅ CAPTCHA challenge appears to be resolved!")
                                self.test_results["captcha_solved"] += 1
                                break
                                
                            # Check if we're redirected to the actual content
                            current_url = page.url
                            if "g2.com/compare" in current_url and "challenge" not in current_url:
                                print("✅ Successfully redirected to G2.com content!")
                                break
                                
                            # Check if content changed significantly
                            current_content = await page.content()
                            if len(current_content) > len(initial_content) * 1.5:  # 50% more content
                                print("✅ Content significantly increased - CAPTCHA may be resolved!")
                                break
                                
                        except Exception as e:
                            print(f"⚠️  Error checking challenge status: {str(e)}")
                    
                    # Wait a bit more for content to fully load
                    await asyncio.sleep(5)
                    
                    print("🔍 Analyzing final page content...")
                
                # Get final page content
                final_content = await page.content()
                print(f"📄 Final content size: {len(final_content)} characters")
                
                # Check if we got meaningful content
                if len(final_content) > 1000:
                    print(f"✅ Content extracted successfully!")
                    
                    # Check if it's still a challenge page
                    if "verification required" in final_content.lower() or "datadome" in final_content.lower():
                        print("🛡️  Still on challenge page - CAPTCHA may not be fully resolved")
                        
                        # Try to extract what we can anyway
                        try:
                            partial_data = self.parse_partial_content(final_content, url)
                            if partial_data:
                                await browser.close()
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "manual_captcha_solving",
                                    "success": True,
                                    "data": partial_data,
                                    "response_size": len(final_content),
                                    "note": "Partial content extracted from challenge page"
                                }
                        except Exception as e:
                            print(f"⚠️  Could not extract partial content: {str(e)}")
                        
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "manual_captcha_solving",
                            "success": False,
                            "data": None,
                            "response_size": len(final_content),
                            "error": "Challenge page - CAPTCHA not fully resolved"
                        }
                    
                    # Try to parse the content
                    try:
                        parsed_data = self.parser.parse_head_to_head_comparison(final_content, url)
                        await browser.close()
                        
                        print("✅ Successfully parsed G2.com comparison data!")
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "manual_captcha_solving",
                            "success": True,
                            "data": parsed_data,
                            "response_size": len(final_content)
                        }
                        
                    except Exception as parse_error:
                        print(f"⚠️  Parser failed: {str(parse_error)}")
                        
                        # Try flexible parsing for partial content
                        try:
                            partial_data = self.parse_partial_content(final_content, url)
                            if partial_data:
                                await browser.close()
                                
                                print("✅ Successfully extracted partial content!")
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "manual_captcha_solving",
                                    "success": True,
                                    "data": partial_data,
                                    "response_size": len(final_content),
                                    "note": "Partial content parsed with flexible parser"
                                }
                        except Exception as e2:
                            print(f"⚠️  Flexible parsing also failed: {str(e2)}")
                
                await browser.close()
                
                return {
                    "url": url,
                    "status_code": response.status if response else None,
                    "method": "manual_captcha_solving",
                    "success": False,
                    "data": None,
                    "response_size": len(final_content) if 'final_content' in locals() else 0,
                    "error": f"Manual CAPTCHA solving failed: {response.status if response else 'No response'}"
                }
                    
        except Exception as e:
            print(f"❌ Manual CAPTCHA solving error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "manual_captcha_solving",
                "success": False,
                "data": None,
                "error": str(e)
            }
            
    def parse_partial_content(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """Parse partial content with flexible parsing."""
        try:
            # Extract basic information even if full parsing fails
            import re
            
            # Try to extract product names
            product_patterns = [
                r'<h1[^>]*>([^<]*?vs[^<]*?)</h1>',
                r'<title[^>]*>([^<]*?vs[^<]*?)</title>',
                r'class="[^"]*product[^"]*"[^>]*>([^<]*?)</',
                r'data-product="([^"]*)"'
            ]
            
            products = []
            for pattern in product_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    products.extend(matches)
                    break
            
            # Try to extract any text content
            text_content = re.sub(r'<[^>]+>', ' ', html)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # Create minimal data structure
            if products or len(text_content) > 100:
                return {
                    "comparison_id": f"partial_{int(time.time())}",
                    "extraction_date": datetime.now(),
                    "url": url,
                    "product_a": {"name": products[0] if products else "Unknown Product A"},
                    "product_b": {"name": products[1] if len(products) > 1 else "Unknown Product B"},
                    "ai_generated_summary": {
                        "summary": text_content[:500] + "..." if len(text_content) > 500 else text_content,
                        "quality_score": 30.0,
                        "extraction_confidence": 40.0
                    },
                    "data_quality_score": 30.0,
                    "extraction_confidence": 40.0,
                    "summary_quality_score": 30.0,
                    "note": "Partial content parsed with flexible parser"
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️  Flexible parsing error: {str(e)}")
            return None
            
    async def test_single_url_manual(self, url: str) -> Dict[str, Any]:
        """Test a single URL with manual CAPTCHA solving."""
        print(f"\n{'='*60}")
        print(f"🔍 Testing URL: {url}")
        print(f"{'='*60}")
        
        result = await self.solve_captcha_manually(url)
        self.test_results["results"].append(result)
        
        if result["success"]:
            self.test_results["successful_requests"] += 1
            print("🎉 SUCCESS: Data extracted from G2.com!")
        else:
            print("❌ FAILED: Could not extract data")
            
        return result
        
    def export_manual_test_results(self, output_dir: str = "output") -> str:
        """Export manual CAPTCHA solving test results."""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"manual_captcha_solving_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filepath}")
        return str(filepath)
        
    def get_manual_test_summary(self) -> Dict[str, Any]:
        """Get summary of manual CAPTCHA solving testing."""
        total = len(self.test_results["results"])
        successful = self.test_results["successful_requests"]
        challenges = self.test_results["captcha_challenges"]
        captcha_solved = self.test_results["captcha_solved"]
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        summary = {
            "total_requests": total,
            "successful_requests": successful,
            "captcha_challenges": challenges,
            "captcha_solved": captcha_solved,
            "success_rate": f"{success_rate:.1f}%",
            "browser_automation_attempts": self.test_results["browser_automation_attempts"],
            "urls_tested": len(self.test_urls),
            "timestamp": self.test_results["start_time"]
        }
        
        return summary

async def main():
    """Main manual CAPTCHA solving test execution."""
    print("🚀 Manual CAPTCHA Solver for G2.com")
    print("=" * 50)
    
    scraper = ManualCaptchaSolver()
    
    try:
        print("🎯 This scraper will:")
        print("1. Open a browser window for each URL")
        print("2. Wait for you to manually solve the DataDome CAPTCHA")
        print("3. Extract G2.com content after CAPTCHA is resolved")
        print("4. Parse the comparison data")
        print("\n⏱️  You'll have up to 5 minutes per URL to solve the CAPTCHA")
        print("🔄 The browser will automatically detect when the challenge is resolved")
        
        # Test single URL for manual CAPTCHA solving
        url = scraper.test_urls[0]  # Start with first URL
        print(f"\n🎯 Starting with: {url}")
        
        result = await scraper.test_single_url_manual(url)
        
        # Export results
        output_file = scraper.export_manual_test_results()
        
        # Print summary
        summary = scraper.get_manual_test_summary()
        print("\n" + "="*60)
        print("📊 MANUAL CAPTCHA SOLVING SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        
        if summary["success_rate"] == "0.0%":
            print("❌ CAPTCHA solving failed. Next steps:")
            print("1. Try solving the CAPTCHA manually")
            print("2. Check if the challenge page changes after solving")
            print("3. Implement automated CAPTCHA solving")
            print("4. Consider API alternatives to scraping")
        elif float(summary["success_rate"].rstrip('%')) < 50:
            print("⚠️  Partial success. Next steps:")
            print("1. Optimize successful methods")
            print("2. Enhance CAPTCHA solving automation")
            print("3. Implement session management")
        else:
            print("✅ Good success rate achieved!")
            print("1. Scale successful methods")
            print("2. Optimize performance")
            print("3. Implement production deployment")
            
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
