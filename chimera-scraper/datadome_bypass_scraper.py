#!/usr/bin/env python3
"""DataDome Bypass Scraper for G2.com Head-to-Head Comparisons."""
import asyncio
import json
import time
import random
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import httpx
from standalone_parser import StandaloneHeadToHeadParser, HeadToHeadComparisonData

class DataDomeBypassScraper:
    """DataDome bypass scraper with CAPTCHA challenge handling."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        # DataDome-specific user agents (more realistic)
        self.datadome_user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "total_requests": 0,
            "successful_requests": 0,
            "datadome_challenges": 0,
            "captcha_solved": 0,
            "browser_automation_attempts": 0,
            "results": []
        }
        
        self.session_cookies = {}
        self.session_headers = {}
        
    def get_realistic_delay(self, min_delay: float = 3.0, max_delay: float = 8.0) -> float:
        """Get realistic human-like delay."""
        return random.uniform(min_delay, max_delay)
        
    def rotate_user_agent(self) -> str:
        """Rotate user agent."""
        return random.choice(self.datadome_user_agents)
        
    def get_datadome_bypass_headers(self) -> Dict[str, str]:
        """Get headers specifically designed to bypass DataDome."""
        headers = {
            "User-Agent": self.rotate_user_agent(),
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
            "Sec-Ch-Ua-Platform": '"macOS"',
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # Add referer for more realistic behavior
        if self.test_results["total_requests"] > 0:
            headers["Referer"] = "https://www.g2.com/"
            
        return headers
        
    async def test_with_datadome_bypass(self, url: str) -> Dict[str, Any]:
        """Test URL with DataDome bypass techniques."""
        print(f"🛡️  Testing with DataDome bypass: {url}")
        
        try:
            # Setup session with DataDome bypass headers
            async with httpx.AsyncClient(
                headers=self.get_datadome_bypass_headers(),
                timeout=45.0,
                follow_redirects=True,
                http2=False
            ) as client:
                
                # Add realistic delay
                delay = self.get_realistic_delay()
                print(f"⏱️  DataDome bypass delay: {delay:.1f}s")
                await asyncio.sleep(delay)
                
                # Make request
                response = await client.get(url)
                self.test_results["total_requests"] += 1
                
                if response.status_code == 200:
                    print(f"✅ DataDome bypass successful!")
                    self.test_results["successful_requests"] += 1
                    
                    # Parse the response
                    parsed_data = self.parser.parse_head_to_head_comparison(response.text, url)
                    
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "datadome_bypass",
                        "success": True,
                        "data": parsed_data,
                        "response_size": len(response.text)
                    }
                    
                elif response.status_code == 403:
                    print(f"🚫 DataDome challenge detected (403)")
                    self.test_results["datadome_challenges"] += 1
                    
                    # Check if it's a DataDome challenge page
                    if "datadome" in response.text.lower() or "verification required" in response.text.lower():
                        print("🛡️  DataDome challenge page detected")
                        return {
                            "url": url,
                            "status_code": response.status_code,
                            "method": "datadome_bypass",
                            "success": False,
                            "data": None,
                            "response_size": len(response.text),
                            "error": "DataDome challenge page - requires CAPTCHA solving"
                        }
                    
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "datadome_bypass",
                        "success": False,
                        "data": None,
                        "response_size": len(response.text),
                        "error": "DataDome bypass failed"
                    }
                    
                else:
                    print(f"⚠️  Unexpected status {response.status_code}")
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "datadome_bypass",
                        "success": False,
                        "data": None,
                        "response_size": len(response.text),
                        "error": f"Unexpected status code: {response.status_code}"
                    }
                        
        except Exception as e:
            print(f"❌ DataDome bypass error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "datadome_bypass",
                "success": False,
                "data": None,
                "error": str(e)
            }
            
    async def test_with_captcha_solving_browser(self, url: str) -> Dict[str, Any]:
        """Test URL with browser automation that can solve DataDome CAPTCHAs."""
        print(f"🌐 Testing with CAPTCHA-solving browser automation: {url}")
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
                    "method": "captcha_solving_browser",
                    "success": False,
                    "data": None,
                    "error": "Playwright not installed"
                }
            
            async with async_playwright() as p:
                # Launch browser with DataDome-specific stealth options
                browser = await p.chromium.launch(
                    headless=False,  # Run in visible mode for CAPTCHA solving
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
                
                # Create context with DataDome-specific stealth settings
                context = await browser.new_context(
                    user_agent=self.rotate_user_agent(),
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers=self.get_datadome_bypass_headers(),
                    ignore_https_errors=True,
                    java_script_enabled=True,
                    has_touch=False,
                    is_mobile=False,
                    device_scale_factor=1,
                    color_scheme="light"
                )
                
                # Add DataDome-specific stealth scripts
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
                    
                    // Fake permissions
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                            Promise.resolve({ state: Notification.permission }) :
                            originalQuery(parameters)
                    );
                    
                    // Fake chrome runtime
                    if (window.chrome) {
                        Object.defineProperty(window.chrome, 'runtime', {
                            get: () => ({
                                onConnect: undefined,
                                onMessage: undefined,
                                connect: undefined,
                                sendMessage: undefined
                            }),
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
                
                # Set realistic viewport and user agent
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Add realistic delays
                delay = self.get_realistic_delay(5.0, 15.0)
                print(f"⏱️  CAPTCHA-solving browser delay: {delay:.1f}s")
                await asyncio.sleep(delay)
                
                # Navigate to URL
                print(f"🌐 Navigating to: {url}")
                
                try:
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                except Exception as e:
                    print(f"⚠️  Navigation failed: {str(e)}")
                    response = None
                
                # Wait for content to load
                await asyncio.sleep(5)
                
                # Check for DataDome challenge
                try:
                    datadome_challenge = await page.query_selector("div[id*='challenge'], div[class*='challenge'], div[class*='captcha']")
                    if datadome_challenge:
                        print("🛡️  DataDome challenge detected, waiting for manual solving...")
                        print("👤 Please solve the CAPTCHA manually in the browser window...")
                        
                        # Wait for user to solve CAPTCHA (up to 2 minutes)
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
                                
                        # Wait a bit more for content to load
                        await asyncio.sleep(5)
                        
                except Exception as e:
                    print(f"⚠️  Error checking for DataDome challenge: {str(e)}")
                
                # Get page content
                content = await page.content()
                
                # Check if we got meaningful content
                if len(content) > 1000:
                    print(f"✅ Content extracted: {len(content)} characters")
                    
                    # Check if it's still a DataDome page
                    if "datadome" in content.lower() or "verification required" in content.lower():
                        print("🛡️  Still on DataDome challenge page")
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "captcha_solving_browser",
                            "success": False,
                            "data": None,
                            "response_size": len(content),
                            "error": "DataDome challenge page - CAPTCHA not solved"
                        }
                    
                    # Try to parse with flexible parsing
                    try:
                        parsed_data = self.parser.parse_head_to_head_comparison(content, url)
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "captcha_solving_browser",
                            "success": True,
                            "data": parsed_data,
                            "response_size": len(content)
                        }
                        
                    except Exception as parse_error:
                        print(f"⚠️  Parser failed: {str(parse_error)}")
                        
                        # Try flexible parsing for partial content
                        try:
                            partial_data = self.parse_partial_content(content, url)
                            if partial_data:
                                await browser.close()
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "captcha_solving_browser",
                                    "success": True,
                                    "data": partial_data,
                                    "response_size": len(content),
                                    "note": "Partial content parsed with flexible parser"
                                }
                        except Exception as e2:
                            print(f"⚠️  Flexible parsing also failed: {str(e2)}")
                
                await browser.close()
                
                return {
                    "url": url,
                    "status_code": response.status if response else None,
                    "method": "captcha_solving_browser",
                    "success": False,
                    "data": None,
                    "response_size": len(content) if 'content' in locals() else 0,
                    "error": f"CAPTCHA-solving browser automation failed: {response.status if response else 'No response'}"
                }
                    
        except Exception as e:
            print(f"❌ CAPTCHA-solving browser automation error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "captcha_solving_browser",
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
            
    async def test_all_urls_datadome_bypass(self) -> List[Dict[str, Any]]:
        """Test all URLs with DataDome bypass techniques."""
        print("🚀 Starting DataDome bypass testing...")
        print(f"📊 Testing {len(self.test_urls)} URLs")
        
        results = []
        
        for i, url in enumerate(self.test_urls, 1):
            print(f"\n{'='*60}")
            print(f"🔍 Testing URL {i}/{len(self.test_urls)}: {url}")
            print(f"{'='*60}")
            
            # First try DataDome bypass
            bypass_result = await self.test_with_datadome_bypass(url)
            
            if bypass_result["success"]:
                print("✅ DataDome bypass successful!")
                results.append(bypass_result)
                continue
                
            print("🔄 DataDome bypass failed, trying CAPTCHA-solving browser...")
            
            # If DataDome bypass fails, try CAPTCHA-solving browser
            browser_result = await self.test_with_captcha_solving_browser(url)
            results.append(browser_result)
            
            # Add delay between URLs
            if i < len(self.test_urls):
                delay = self.get_realistic_delay(10.0, 20.0)
                print(f"⏱️  Waiting {delay:.1f}s before next URL...")
                await asyncio.sleep(delay)
                
        self.test_results["results"] = results
        return results
        
    def export_datadome_test_results(self, output_dir: str = "output") -> str:
        """Export DataDome bypass test results."""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"datadome_bypass_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filepath}")
        return str(filepath)
        
    def get_datadome_test_summary(self) -> Dict[str, Any]:
        """Get summary of DataDome bypass testing."""
        total = self.test_results["total_requests"]
        successful = self.test_results["successful_requests"]
        challenges = self.test_results["datadome_challenges"]
        captcha_solved = self.test_results["captcha_solved"]
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        summary = {
            "total_requests": total,
            "successful_requests": successful,
            "datadome_challenges": challenges,
            "captcha_solved": captcha_solved,
            "success_rate": f"{success_rate:.1f}%",
            "browser_automation_attempts": self.test_results["browser_automation_attempts"],
            "urls_tested": len(self.test_urls),
            "timestamp": self.test_results["start_time"]
        }
        
        return summary

async def main():
    """Main DataDome bypass test execution."""
    print("🚀 DataDome Bypass Scraper for G2.com")
    print("=" * 50)
    
    scraper = DataDomeBypassScraper()
    
    try:
        # Test all URLs with DataDome bypass techniques
        results = await scraper.test_all_urls_datadome_bypass()
        
        # Export results
        output_file = scraper.export_datadome_test_results()
        
        # Print summary
        summary = scraper.get_datadome_test_summary()
        print("\n" + "="*60)
        print("📊 DATADOME BYPASS TESTING SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        
        if summary["success_rate"] == "0.0%":
            print("❌ All methods failed. Next steps:")
            print("1. Implement automated CAPTCHA solving")
            print("2. Use human-in-the-loop verification")
            print("3. Consider API alternatives to scraping")
            print("4. Implement session persistence and cookies")
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
