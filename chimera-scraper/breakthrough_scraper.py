#!/usr/bin/env python3
"""Breakthrough Scraper with Advanced Cloudflare Bypass and Anti-Detection."""
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

class BreakthroughScraper:
    """Breakthrough scraper with advanced Cloudflare bypass and anti-detection."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        # Premium proxy list (simulated - in production use real residential proxies)
        self.premium_proxies = [
            "http://residential1.proxy.com:8080",
            "http://residential2.proxy.com:8080",
            "http://residential3.proxy.com:8080"
        ]
        
        # Ultra-realistic user agents
        self.ultra_realistic_user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "total_requests": 0,
            "successful_requests": 0,
            "blocked_requests": 0,
            "cloudflare_bypass_attempts": 0,
            "browser_automation_attempts": 0,
            "results": []
        }
        
        self.current_proxy_index = 0
        self.session_cookies = {}
        self.session_headers = {}
        
    def get_next_proxy(self) -> Optional[str]:
        """Get next premium proxy."""
        if not self.premium_proxies:
            return None
            
        proxy = self.premium_proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.premium_proxies)
        return proxy
        
    def get_ultra_realistic_delay(self, min_delay: float = 5.0, max_delay: float = 15.0) -> float:
        """Get ultra-realistic human-like delay."""
        return random.uniform(min_delay, max_delay)
        
    def rotate_user_agent(self) -> str:
        """Rotate ultra-realistic user agent."""
        return random.choice(self.ultra_realistic_user_agents)
        
    def get_cloudflare_bypass_headers(self) -> Dict[str, str]:
        """Get headers specifically designed to bypass Cloudflare."""
        headers = {
            "User-Agent": self.rotate_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
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
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "X-Real-IP": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        }
        
        # Add referer for more realistic behavior
        if self.test_results["total_requests"] > 0:
            headers["Referer"] = "https://www.g2.com/"
            
        return headers
        
    async def test_with_cloudflare_bypass(self, url: str) -> Dict[str, Any]:
        """Test URL with advanced Cloudflare bypass techniques."""
        print(f"🛡️  Testing with Cloudflare bypass: {url}")
        self.test_results["cloudflare_bypass_attempts"] += 1
        
        try:
            # Setup session with Cloudflare bypass headers
            async with httpx.AsyncClient(
                headers=self.get_cloudflare_bypass_headers(),
                timeout=45.0,
                follow_redirects=True,
                http2=False
            ) as client:
                
                # Add ultra-realistic delay
                delay = self.get_ultra_realistic_delay()
                print(f"⏱️  Cloudflare bypass delay: {delay:.1f}s")
                await asyncio.sleep(delay)
                
                # Make request
                response = await client.get(url)
                self.test_results["total_requests"] += 1
                
                if response.status_code == 200:
                    print(f"✅ Cloudflare bypass successful!")
                    self.test_results["successful_requests"] += 1
                    
                    # Parse the response
                    parsed_data = self.parser.parse_head_to_head_comparison(response.text, url)
                    
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "cloudflare_bypass",
                        "success": True,
                        "data": parsed_data,
                        "response_size": len(response.text)
                    }
                    
                elif response.status_code == 403:
                    print(f"🚫 Cloudflare bypass failed (403)")
                    self.test_results["blocked_requests"] += 1
                    
                    # Check if we got partial content despite 403
                    if len(response.text) > 1000:
                        print("🔍 Detected partial content despite 403")
                        
                        # Check if it's Cloudflare protection page
                        if "cloudflare" in response.text.lower() or "captcha" in response.text.lower():
                            print("🛡️  Detected Cloudflare protection page")
                            return {
                                "url": url,
                                "status_code": response.status_code,
                                "method": "cloudflare_bypass",
                                "success": False,
                                "data": None,
                                "response_size": len(response.text),
                                "error": "Cloudflare protection page detected"
                            }
                        
                        # Try to parse partial content
                        try:
                            parsed_data = self.parser.parse_head_to_head_comparison(response.text, url)
                            return {
                                "url": url,
                                "status_code": response.status_code,
                                "method": "cloudflare_bypass",
                                "success": True,
                                "data": parsed_data,
                                "response_size": len(response.text),
                                "note": "Partial content extracted despite 403"
                            }
                        except Exception as e:
                            print(f"⚠️  Failed to parse partial content: {str(e)}")
                    
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "cloudflare_bypass",
                        "success": False,
                        "data": None,
                        "response_size": len(response.text),
                        "error": "Cloudflare bypass failed"
                    }
                    
                else:
                    print(f"⚠️  Unexpected status {response.status_code}")
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "method": "cloudflare_bypass",
                        "success": False,
                        "data": None,
                        "response_size": len(response.text),
                        "error": f"Unexpected status code: {response.status_code}"
                    }
                        
        except Exception as e:
            print(f"❌ Cloudflare bypass error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "cloudflare_bypass",
                "success": False,
                "data": None,
                "error": str(e)
            }
            
    async def test_with_advanced_browser_automation(self, url: str) -> Dict[str, Any]:
        """Test URL with advanced browser automation and Cloudflare bypass."""
        print(f"🌐 Testing with advanced browser automation: {url}")
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
                    "method": "advanced_browser_automation",
                    "success": False,
                    "data": None,
                    "error": "Playwright not installed"
                }
            
            async with async_playwright() as p:
                # Launch browser with ultra-stealth options
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
                        "--disable-sync-preferences",
                        "--disable-background-media-suspend",
                        "--disable-component-update",
                        "--disable-default-apps",
                        "--disable-hang-monitor",
                        "--disable-prompt-on-repost",
                        "--disable-sync",
                        "--disable-web-resources",
                        "--disable-client-side-phishing-detection",
                        "--disable-component-extensions-with-background-pages",
                        "--disable-domain-reliability",
                        "--disable-features=TranslateUI,BlinkGenPropertyTrees",
                        "--disable-ipc-flooding-protection",
                        "--no-default-browser-check",
                        "--no-first-run",
                        "--disable-default-apps",
                        "--disable-sync",
                        "--disable-translate",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor",
                        "--disable-background-timer-throttling",
                        "--disable-backgrounding-occluded-windows",
                        "--disable-renderer-backgrounding",
                        "--disable-ipc-flooding-protection"
                    ]
                )
                
                # Create context with ultra-stealth settings
                context = await browser.new_context(
                    user_agent=self.rotate_user_agent(),
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers=self.get_cloudflare_bypass_headers(),
                    ignore_https_errors=True,
                    java_script_enabled=True,
                    has_touch=False,
                    is_mobile=False,
                    device_scale_factor=1,
                    color_scheme="light",
                    permissions=["geolocation", "notifications", "camera", "microphone"]
                )
                
                # Add ultra-stealth scripts
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
                
                # Add ultra-realistic delays
                delay = self.get_ultra_realistic_delay(5.0, 20.0)
                print(f"⏱️  Advanced browser automation delay: {delay:.1f}s")
                await asyncio.sleep(delay)
                
                # Navigate to URL with enhanced options
                print(f"🌐 Navigating to: {url}")
                
                # Try to navigate with multiple strategies
                try:
                    # First attempt: direct navigation
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                except Exception as e:
                    print(f"⚠️  Direct navigation failed: {str(e)}")
                    try:
                        # Second attempt: with network idle
                        response = await page.goto(url, wait_until="networkidle", timeout=90000)
                    except Exception as e2:
                        print(f"⚠️  Network idle navigation failed: {str(e2)}")
                        # Third attempt: minimal wait
                        response = await page.goto(url, wait_until="load", timeout=90000)
                
                # Wait for content to load and potential Cloudflare challenge
                await asyncio.sleep(10)
                
                # Check for Cloudflare challenge
                try:
                    cloudflare_challenge = await page.query_selector("div[id*='challenge']")
                    if cloudflare_challenge:
                        print("🛡️  Cloudflare challenge detected, waiting for resolution...")
                        await asyncio.sleep(15)  # Wait for challenge to resolve
                except Exception as e:
                    print(f"⚠️  Error checking for Cloudflare challenge: {str(e)}")
                
                # Get page content
                content = await page.content()
                
                # Check if we got meaningful content
                if len(content) > 1000:
                    print(f"✅ Content extracted: {len(content)} characters")
                    
                    # Check if it's still a Cloudflare page
                    if "cloudflare" in content.lower() or "captcha" in content.lower():
                        print("🛡️  Still on Cloudflare protection page")
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "advanced_browser_automation",
                            "success": False,
                            "data": None,
                            "response_size": len(content),
                            "error": "Cloudflare protection page - challenge not resolved"
                        }
                    
                    # Try to parse with flexible parsing
                    try:
                        parsed_data = self.parser.parse_head_to_head_comparison(content, url)
                        await browser.close()
                        
                        return {
                            "url": url,
                            "status_code": response.status if response else None,
                            "method": "advanced_browser_automation",
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
                                    "method": "advanced_browser_automation",
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
                    "method": "advanced_browser_automation",
                    "success": False,
                    "data": None,
                    "response_size": len(content) if 'content' in locals() else 0,
                    "error": f"Advanced browser automation failed: {response.status if response else 'No response'}"
                }
                    
        except Exception as e:
            print(f"❌ Advanced browser automation error: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "method": "advanced_browser_automation",
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
            
    async def test_all_urls_breakthrough(self) -> List[Dict[str, Any]]:
        """Test all URLs with breakthrough anti-detection techniques."""
        print("🚀 Starting breakthrough anti-detection testing...")
        print(f"📊 Testing {len(self.test_urls)} URLs")
        
        results = []
        
        for i, url in enumerate(self.test_urls, 1):
            print(f"\n{'='*60}")
            print(f"🔍 Testing URL {i}/{len(self.test_urls)}: {url}")
            print(f"{'='*60}")
            
            # First try Cloudflare bypass
            bypass_result = await self.test_with_cloudflare_bypass(url)
            
            if bypass_result["success"]:
                print("✅ Cloudflare bypass successful!")
                results.append(bypass_result)
                continue
                
            print("🔄 Cloudflare bypass failed, trying advanced browser automation...")
            
            # If Cloudflare bypass fails, try advanced browser automation
            browser_result = await self.test_with_advanced_browser_automation(url)
            results.append(browser_result)
            
            # Add delay between URLs
            if i < len(self.test_urls):
                delay = self.get_ultra_realistic_delay(10.0, 25.0)
                print(f"⏱️  Waiting {delay:.1f}s before next URL...")
                await asyncio.sleep(delay)
                
        self.test_results["results"] = results
        return results
        
    def export_breakthrough_test_results(self, output_dir: str = "output") -> str:
        """Export breakthrough test results."""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"breakthrough_scraper_results_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filepath}")
        return str(filepath)
        
    def get_breakthrough_test_summary(self) -> Dict[str, Any]:
        """Get summary of breakthrough anti-detection testing."""
        total = self.test_results["total_requests"]
        successful = self.test_results["successful_requests"]
        blocked = self.test_results["blocked_requests"]
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        summary = {
            "total_requests": total,
            "successful_requests": successful,
            "blocked_requests": blocked,
            "success_rate": f"{success_rate:.1f}%",
            "cloudflare_bypass_attempts": self.test_results["cloudflare_bypass_attempts"],
            "browser_automation_attempts": self.test_results["browser_automation_attempts"],
            "urls_tested": len(self.test_urls),
            "timestamp": self.test_results["start_time"]
        }
        
        return summary

async def main():
    """Main breakthrough anti-detection test execution."""
    print("🚀 Breakthrough Anti-Detection Scraper")
    print("=" * 50)
    
    scraper = BreakthroughScraper()
    
    try:
        # Test all URLs with breakthrough techniques
        results = await scraper.test_all_urls_breakthrough()
        
        # Export results
        output_file = scraper.export_breakthrough_test_results()
        
        # Print summary
        summary = scraper.get_breakthrough_test_summary()
        print("\n" + "="*60)
        print("📊 BREAKTHROUGH ANTI-DETECTION TESTING SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
        print("\n" + "="*60)
        print("🎯 NEXT STEPS")
        print("="*60)
        
        if summary["success_rate"] == "0.0%":
            print("❌ All methods failed. Next steps:")
            print("1. Implement real residential proxies")
            print("2. Use cloud-based scraping services")
            print("3. Implement human-in-the-loop verification")
            print("4. Consider API alternatives to scraping")
        elif float(summary["success_rate"].rstrip('%')) < 50:
            print("⚠️  Partial success. Next steps:")
            print("1. Optimize successful methods")
            print("2. Implement additional proxy sources")
            print("3. Enhance Cloudflare bypass techniques")
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
