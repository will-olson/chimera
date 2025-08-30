#!/usr/bin/env python3
"""Robust Anti-Detection Scraper with Working Proxy Rotation and Flexible Parsing."""
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

class RobustAntiDetectionScraper:
    """Robust anti-detection scraper with working proxy rotation and flexible parsing."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        # Working proxy list (using public proxies that are more reliable)
        self.working_proxies = [
            "http://185.199.229.156:7492",
            "http://185.199.228.220:7492", 
            "http://185.199.231.45:7492",
            "http://188.74.210.207:6286",
            "http://188.74.183.10:8279",
            "http://188.74.210.21:6100",
            "http://45.155.68.129:8133",
            "http://154.85.100.162:5836"
        ]
        
        # Enhanced user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "total_requests": 0,
            "successful_requests": 0,
            "blocked_requests": 0,
            "proxy_rotations": 0,
            "browser_automation_attempts": 0,
            "partial_content_extractions": 0,
            "results": []
        }
        
        self.current_proxy_index = 0
        self.session_cookies = {}
        self.session_headers = {}
        
    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy from rotation."""
        if not self.working_proxies:
            return None
            
        proxy = self.working_proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.working_proxies)
        self.test_results["proxy_rotations"] += 1
        return proxy
        
    def get_realistic_delay(self, min_delay: float = 2.0, max_delay: float = 8.0) -> float:
        """Get realistic human-like delay."""
        return random.uniform(min_delay, max_delay)
        
    def rotate_user_agent(self) -> str:
        """Rotate user agent."""
        return random.choice(self.user_agents)
        
    def get_enhanced_headers(self) -> Dict[str, str]:
        """Get enhanced browser headers."""
        headers = {
            "User-Agent": self.rotate_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
        # Add referer for more realistic behavior
        if self.test_results["total_requests"] > 0:
            headers["Referer"] = "https://www.g2.com/"
            
        return headers
        
    async def test_with_proxy_rotation(self, url: str) -> Dict[str, Any]:
        """Test URL with working proxy rotation."""
        print(f"🔍 Testing with proxy rotation: {url}")
        
        for attempt in range(3):  # Try 3 different proxies
            proxy = self.get_next_proxy()
            if not proxy:
                print("⚠️  No more proxies available")
                break
                
            print(f"🔄 Attempt {attempt + 1} with proxy: {proxy}")
            
            try:
                # Setup enhanced session with correct httpx proxy syntax
                async with httpx.AsyncClient(
                    proxies=proxy,  # Use the correct httpx syntax
                    headers=self.get_enhanced_headers(),
                    timeout=30.0,
                    follow_redirects=True,
                    http2=False
                ) as client:
                    
                    # Add realistic delay
                    delay = self.get_realistic_delay()
                    print(f"⏱️  Waiting {delay:.1f}s before request...")
                    await asyncio.sleep(delay)
                    
                    # Make request
                    response = await client.get(url)
                    self.test_results["total_requests"] += 1
                    
                    if response.status_code == 200:
                        print(f"✅ Success with proxy {proxy}")
                        self.test_results["successful_requests"] += 1
                        
                        # Parse the response
                        parsed_data = self.parser.parse_head_to_head_comparison(response.text, url)
                        
                        return {
                            "url": url,
                            "status_code": response.status_code,
                            "proxy_used": proxy,
                            "attempt": attempt + 1,
                            "success": True,
                            "data": parsed_data,
                            "response_size": len(response.text)
                        }
                        
                    elif response.status_code == 403:
                        print(f"🚫 Blocked with proxy {proxy} (403)")
                        self.test_results["blocked_requests"] += 1
                        
                        # Check if we got partial content despite 403
                        if len(response.text) > 1000:  # Significant content
                            print("🔍 Detected partial content despite 403")
                            try:
                                parsed_data = self.parser.parse_head_to_head_comparison(response.text, url)
                                self.test_results["partial_content_extractions"] += 1
                                
                                return {
                                    "url": url,
                                    "status_code": response.status_code,
                                    "proxy_used": proxy,
                                    "attempt": attempt + 1,
                                    "success": True,
                                    "data": parsed_data,
                                    "response_size": len(response.text),
                                    "note": "Partial content extracted despite 403"
                                }
                            except Exception as e:
                                print(f"⚠️  Failed to parse partial content: {str(e)}")
                        
                        continue
                        
                    else:
                        print(f"⚠️  Unexpected status {response.status_code} with proxy {proxy}")
                        continue
                        
            except Exception as e:
                print(f"❌ Error with proxy {proxy}: {str(e)}")
                continue
                
        # All proxy attempts failed
        return {
            "url": url,
            "status_code": None,
            "proxy_used": None,
            "attempt": 3,
            "success": False,
            "data": None,
            "response_size": 0,
            "error": "All proxy attempts failed"
        }
        
    async def test_with_browser_automation(self, url: str) -> Dict[str, Any]:
        """Test URL with enhanced browser automation."""
        print(f"🌐 Testing with browser automation: {url}")
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
                    "method": "browser_automation",
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
                    user_agent=self.rotate_user_agent(),
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers=self.get_enhanced_headers(),
                    ignore_https_errors=True,
                    java_script_enabled=True,
                    has_touch=False,
                    is_mobile=False,
                    device_scale_factor=1,
                    color_scheme="light"
                )
                
                # Add enhanced stealth scripts
                await context.add_init_script("""
                    // Remove webdriver property
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    // Fake plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
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
                            saveData: false
                        }),
                    });
                """)
                
                # Create page
                page = await context.new_page()
                
                # Set realistic viewport and user agent
                await page.set_viewport_size({"width": 1920, "height": 1080})
                
                # Add realistic delays
                delay = self.get_realistic_delay(3.0, 10.0)
                print(f"⏱️  Browser automation delay: {delay:.1f}s")
                await asyncio.sleep(delay)
                
                # Navigate to URL with enhanced options
                print(f"🌐 Navigating to: {url}")
                
                # Try to navigate with multiple strategies
                try:
                    # First attempt: direct navigation
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                except Exception as e:
                    print(f"⚠️  Direct navigation failed: {str(e)}")
                    try:
                        # Second attempt: with network idle
                        response = await page.goto(url, wait_until="networkidle", timeout=60000)
                    except Exception as e2:
                        print(f"⚠️  Network idle navigation failed: {str(e2)}")
                        # Third attempt: minimal wait
                        response = await page.goto(url, wait_until="load", timeout=60000)
                
                # Wait for content to load
                await asyncio.sleep(5)
                
                # Get page content
                content = await page.content()
                
                # Check if we got meaningful content
                if len(content) > 1000:
                    print(f"✅ Content extracted: {len(content)} characters")
                    
                    # Try to parse with flexible parsing
                    try:
                        parsed_data = self.parser.parse_head_to_head_comparison(content, url)
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "browser_automation",
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
                                self.test_results["partial_content_extractions"] += 1
                                await browser.close()
                                
                                return {
                                    "url": url,
                                    "status_code": response.status if response else None,
                                    "method": "browser_automation",
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
                    "method": "browser_automation",
                    "success": False,
                    "data": None,
                    "response_size": len(content) if 'content' in locals() else 0,
                    "error": f"Browser automation failed: {response.status if response else 'No response'}"
                }
                    
        except Exception as e:
            print(f"❌ Browser automation error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "browser_automation",
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
            
    async def test_all_urls_robust(self) -> List[Dict[str, Any]]:
        """Test all URLs with robust anti-detection techniques."""
        print("🚀 Starting robust anti-detection testing...")
        print(f"📊 Testing {len(self.test_urls)} URLs")
        
        results = []
        
        for i, url in enumerate(self.test_urls, 1):
            print(f"\n{'='*60}")
            print(f"🔍 Testing URL {i}/{len(self.test_urls)}: {url}")
            print(f"{'='*60}")
            
            # First try proxy rotation
            proxy_result = await self.test_with_proxy_rotation(url)
            
            if proxy_result["success"]:
                print("✅ Proxy rotation successful!")
                results.append(proxy_result)
                continue
                
            print("🔄 Proxy rotation failed, trying browser automation...")
            
            # If proxy rotation fails, try browser automation
            browser_result = await self.test_with_browser_automation(url)
            results.append(browser_result)
            
            # Add delay between URLs
            if i < len(self.test_urls):
                delay = self.get_realistic_delay(5.0, 15.0)
                print(f"⏱️  Waiting {delay:.1f}s before next URL...")
                await asyncio.sleep(delay)
                
        self.test_results["results"] = results
        return results
        
    def export_robust_test_results(self, output_dir: str = "output") -> str:
        """Export robust test results."""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"robust_anti_detection_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filepath}")
        return str(filepath)
        
    def get_robust_test_summary(self) -> Dict[str, Any]:
        """Get summary of robust anti-detection testing."""
        total = self.test_results["total_requests"]
        successful = self.test_results["successful_requests"]
        blocked = self.test_results["blocked_requests"]
        partial = self.test_results["partial_content_extractions"]
        
        success_rate = ((successful + partial) / total * 100) if total > 0 else 0
        
        summary = {
            "total_requests": total,
            "successful_requests": successful,
            "blocked_requests": blocked,
            "partial_content_extractions": partial,
            "overall_success_rate": f"{success_rate:.1f}%",
            "proxy_rotations": self.test_results["proxy_rotations"],
            "browser_automation_attempts": self.test_results["browser_automation_attempts"],
            "urls_tested": len(self.test_urls),
            "timestamp": self.test_results["start_time"]
        }
        
        return summary

async def main():
    """Main robust anti-detection test execution."""
    print("🚀 Robust Anti-Detection Scraper")
    print("=" * 50)
    
    scraper = RobustAntiDetectionScraper()
    
    try:
        # Test all URLs with robust techniques
        results = await scraper.test_all_urls_robust()
        
        # Export results
        output_file = scraper.export_robust_test_results()
        
        # Print summary
        summary = scraper.get_robust_test_summary()
        print("\n" + "="*60)
        print("📊 ROBUST ANTI-DETECTION TESTING SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        
        if summary["overall_success_rate"] == "0.0%":
            print("❌ All methods failed. Next steps:")
            print("1. Implement paid proxy services")
            print("2. Use residential proxies")
            print("3. Implement more sophisticated browser automation")
            print("4. Consider cloud-based scraping services")
        elif float(summary["overall_success_rate"].rstrip('%')) < 50:
            print("⚠️  Partial success. Next steps:")
            print("1. Optimize successful methods")
            print("2. Implement additional proxy sources")
            print("3. Enhance browser automation")
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
