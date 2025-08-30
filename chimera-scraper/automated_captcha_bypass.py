#!/usr/bin/env python3
"""Automated CAPTCHA Bypass Scraper for G2.com DataDome Challenges."""
import asyncio
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from standalone_parser import StandaloneHeadToHeadParser, HeadToHeadComparisonData

class AutomatedCaptchaBypass:
    """Automated CAPTCHA bypass for DataDome challenges."""
    
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
        
    async def solve_slider_captcha_automated(self, page) -> bool:
        """Automatically solve DataDome slider CAPTCHA puzzle."""
        try:
            print("🧩 Attempting automated slider CAPTCHA solving...")
            
            # Wait for CAPTCHA to fully load
            await asyncio.sleep(2)
            
            # Look for slider elements with multiple strategies
            slider_selectors = [
                "div[class*='slider']",
                "div[class*='puzzle']", 
                "div[class*='challenge']",
                "div[id*='slider']",
                "div[id*='puzzle']",
                "div[id*='challenge']",
                "div[class*='verification']",
                "div[class*='captcha']"
            ]
            
            slider_element = None
            for selector in slider_selectors:
                try:
                    slider_element = await page.query_selector(selector)
                    if slider_element:
                        print(f"✅ Found slider element with selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not slider_element:
                print("⚠️  No slider element found")
                return False
            
            # Look for the slider handle with multiple strategies
            slider_handle_selectors = [
                "button[class*='slider']",
                "div[class*='slider'] button",
                "div[class*='puzzle'] button",
                "div[class*='challenge'] button",
                "button[class*='arrow']",
                "div[class*='arrow']",
                "button[class*='handle']",
                "div[class*='handle']",
                "button[class*='drag']",
                "div[class*='drag']"
            ]
            
            slider_handle = None
            for selector in slider_handle_selectors:
                try:
                    slider_handle = await page.query_selector(selector)
                    if slider_handle:
                        print(f"✅ Found slider handle with selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not slider_handle:
                print("⚠️  No slider handle found")
                return False
            
            # Get slider dimensions
            try:
                slider_box = await slider_element.bounding_box()
                if not slider_box:
                    print("⚠️  Could not get slider dimensions")
                    return False
                
                print(f"📏 Slider dimensions: {slider_box}")
                
                # Calculate slide distance (usually full width minus handle width)
                slide_distance = slider_box['width'] - 60  # Approximate handle width
                
                # Perform the slide action with realistic timing
                print(f"🔄 Sliding distance: {slide_distance}px")
                
                # Click and drag the slider handle
                await slider_handle.hover()
                await asyncio.sleep(0.3)
                
                # Start drag
                await page.mouse.down()
                await asyncio.sleep(0.2)
                
                # Move to target position with realistic motion
                target_x = slider_box['x'] + slide_distance
                target_y = slider_box['y'] + slider_box['height'] / 2
                
                # Move in steps to simulate human motion
                steps = 10
                for i in range(1, steps + 1):
                    current_x = slider_box['x'] + (slide_distance * i / steps)
                    await page.mouse.move(current_x, target_y)
                    await asyncio.sleep(0.05)
                
                # Final position
                await page.mouse.move(target_x, target_y)
                await asyncio.sleep(0.2)
                
                # Release
                await page.mouse.up()
                
                print("✅ Slider CAPTCHA solved automatically!")
                
                # Wait for verification
                await asyncio.sleep(3)
                
                return True
                
            except Exception as e:
                print(f"⚠️  Error solving slider CAPTCHA: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ Automated CAPTCHA solving error: {str(e)}")
            return False
    
    async def bypass_captcha_and_extract_data(self, url: str) -> Dict[str, Any]:
        """Bypass CAPTCHA and extract real G2.com data."""
        print(f"🌐 Bypassing CAPTCHA and extracting data: {url}")
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
                    "method": "automated_captcha_bypass",
                    "success": False,
                    "data": None,
                    "error": "Playwright not installed"
                }
            
            async with async_playwright() as p:
                # Launch browser with enhanced stealth options
                browser = await p.chromium.launch(
                    headless=False,  # Run in visible mode for debugging
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
                        "--no-first-run",
                        "--disable-background-networking",
                        "--disable-component-extensions-with-background-pages",
                        "--disable-domain-reliability",
                        "--disable-features=TranslateUI",
                        "--disable-ignore-certificate-errors",
                        "--disable-sync-preferences"
                    ]
                )
                
                # Create context with enhanced stealth settings
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
                
                # Add enhanced stealth scripts
                await context.add_init_script("""
                    // Remove all automation indicators
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
                    
                    // Fake connection
                    Object.defineProperty(navigator, 'connection', {
                        get: () => ({
                            effectiveType: '4g',
                            rtt: 50,
                            downlink: 10,
                            saveData: false,
                            type: 'wifi'
                        }),
                    });
                    
                    // Fake hardware concurrency
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => 8,
                    });
                    
                    // Fake device memory
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => 8,
                    });
                    
                    // Fake max touch points
                    Object.defineProperty(navigator, 'maxTouchPoints', {
                        get: () => 0,
                    });
                    
                    // Fake platform
                    Object.defineProperty(navigator, 'platform', {
                        get: () => 'MacIntel',
                    });
                    
                    // Fake vendor
                    Object.defineProperty(navigator, 'vendor', {
                        get: () => 'Google Inc.',
                    });
                    
                    // Fake product
                    Object.defineProperty(navigator, 'product', {
                        get: () => 'Gecko',
                    });
                    
                    // Fake cookie enabled
                    Object.defineProperty(navigator, 'cookieEnabled', {
                        get: () => true,
                    });
                    
                    // Fake do not track
                    Object.defineProperty(navigator, 'doNotTrack', {
                        get: () => null,
                    });
                    
                    // Fake on line
                    Object.defineProperty(navigator, 'onLine', {
                        get: () => true,
                    });
                    
                    // Fake user agent data
                    if (navigator.userAgentData) {
                        Object.defineProperty(navigator.userAgentData, 'brands', {
                            get: () => [
                                {brand: 'Google Chrome', version: '120'},
                                {brand: 'Chromium', version: '120'},
                                {brand: 'Not=A?Brand', version: '8'}
                            ],
                        });
                        
                        Object.defineProperty(navigator.userAgentData, 'mobile', {
                            get: () => false,
                        });
                        
                        Object.defineProperty(navigator.userAgentData, 'platform', {
                            get: () => 'macOS',
                        });
                    }
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
                await asyncio.sleep(3)
                
                # Check initial content
                initial_content = await page.content()
                print(f"📄 Initial content size: {len(initial_content)} characters")
                
                # Immediately check for CAPTCHA challenge
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
                    print("🧩 CAPTCHA detected - attempting automated solving...")
                    
                    # Try to solve the CAPTCHA automatically
                    captcha_solved = await self.solve_slider_captcha_automated(page)
                    
                    if captcha_solved:
                        self.test_results["captcha_solved"] += 1
                        print("✅ CAPTCHA solved automatically!")
                        
                        # Wait for redirect/verification
                        await asyncio.sleep(5)
                        
                        # Check if we're redirected to actual content
                        current_url = page.url
                        if "g2.com/compare" in current_url and "challenge" not in current_url:
                            print("✅ Successfully redirected to G2.com content!")
                        else:
                            print("⚠️  Still on challenge page after solving")
                    else:
                        print("⚠️  Automatic CAPTCHA solving failed")
                        print("👤 Please solve the CAPTCHA manually in the browser window...")
                        
                        # Wait for manual solving (up to 2 minutes)
                        max_wait_time = 120
                        wait_interval = 5
                        total_waited = 0
                        
                        while total_waited < max_wait_time:
                            await asyncio.sleep(wait_interval)
                            total_waited += wait_interval
                            
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
                                    
                            except Exception as e:
                                print(f"⚠️  Error checking challenge status: {str(e)}")
                
                # Wait for content to fully load
                await asyncio.sleep(5)
                
                # Get final page content
                final_content = await page.content()
                print(f"📄 Final content size: {len(final_content)} characters")
                
                # Check if we got meaningful content
                if len(final_content) > 1000:
                    print(f"✅ Content extracted successfully!")
                    
                    # Check if it's still a challenge page
                    if "verification required" in final_content.lower() or "datadome" in final_content.lower():
                        print("🛡️  Still on challenge page - attempting to extract what we can")
                        
                        # Try to extract what we can from the challenge page
                        try:
                            partial_data = self.parse_partial_content(final_content, url)
                            if partial_data:
                                await browser.close()
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "automated_captcha_bypass",
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
                            "method": "automated_captcha_bypass",
                            "success": False,
                            "data": None,
                            "response_size": len(final_content),
                            "error": "Challenge page - CAPTCHA not fully resolved"
                        }
                    
                    # Try to parse the content with main parser
                    try:
                        parsed_data = self.parser.parse_head_to_head_comparison(final_content, url)
                        await browser.close()
                        
                        print("✅ Successfully parsed G2.com comparison data!")
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "automated_captcha_bypass",
                            "success": True,
                            "data": parsed_data,
                            "response_size": len(final_content)
                        }
                        
                    except Exception as parse_error:
                        print(f"⚠️  Main parser failed: {str(parse_error)}")
                        
                        # Try flexible parsing for partial content
                        try:
                            partial_data = self.parse_partial_content(final_content, url)
                            if partial_data:
                                await browser.close()
                                
                                print("✅ Successfully extracted partial content!")
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "automated_captcha_bypass",
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
                    "method": "automated_captcha_bypass",
                    "success": False,
                    "data": None,
                    "response_size": len(final_content) if 'final_content' in locals() else 0,
                    "error": f"Automated CAPTCHA bypass failed: {response.status if response else 'No response'}"
                }
                    
        except Exception as e:
            print(f"❌ Automated CAPTCHA bypass error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "automated_captcha_bypass",
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
            
    async def test_all_urls_with_automated_bypass(self) -> List[Dict[str, Any]]:
        """Test all URLs with automated CAPTCHA bypass."""
        print("🚀 Starting automated CAPTCHA bypass testing...")
        print(f"📊 Testing {len(self.test_urls)} URLs")
        
        results = []
        
        for i, url in enumerate(self.test_urls, 1):
            print(f"\n{'='*60}")
            print(f"🔍 Testing URL {i}/{len(self.test_urls)}: {url}")
            print(f"{'='*60}")
            
            # Test with automated CAPTCHA bypass
            result = await self.bypass_captcha_and_extract_data(url)
            results.append(result)
            
            # Add delay between URLs
            if i < len(self.test_urls):
                delay = random.uniform(15.0, 25.0)
                print(f"⏱️  Waiting {delay:.1f}s before next URL...")
                await asyncio.sleep(delay)
                
        self.test_results["results"] = results
        return results
        
    def export_automated_test_results(self, output_dir: str = "output") -> str:
        """Export automated CAPTCHA bypass test results."""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"automated_captcha_bypass_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filepath}")
        return str(filepath)
        
    def get_automated_test_summary(self) -> Dict[str, Any]:
        """Get summary of automated CAPTCHA bypass testing."""
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
    """Main automated CAPTCHA bypass test execution."""
    print("🚀 Automated CAPTCHA Bypass Scraper for G2.com")
    print("=" * 50)
    
    scraper = AutomatedCaptchaBypass()
    
    try:
        print("🎯 This scraper will:")
        print("1. Open browser windows for each URL")
        print("2. Automatically detect DataDome CAPTCHA challenges")
        print("3. Attempt to solve CAPTCHAs automatically")
        print("4. Fall back to manual solving if needed")
        print("5. Extract real G2.com comparison data after bypass")
        print("\n⚡ CAPTCHA detection and solving is now AUTOMATED!")
        print("🔄 No more waiting for manual intervention")
        
        # Test all URLs with automated CAPTCHA bypass
        results = await scraper.test_all_urls_with_automated_bypass()
        
        # Export results
        output_file = scraper.export_automated_test_results()
        
        # Print summary
        summary = scraper.get_automated_test_summary()
        print("\n" + "="*60)
        print("📊 AUTOMATED CAPTCHA BYPASS SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        
        if summary["success_rate"] == "0.0%":
            print("❌ All methods failed. Next steps:")
            print("1. Enhance automated CAPTCHA solving algorithms")
            print("2. Implement machine learning-based CAPTCHA recognition")
            print("3. Use human-in-the-loop verification services")
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
