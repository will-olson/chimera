#!/usr/bin/env python3
"""Enhanced Anti-Detection Scraper for G2.com Head-to-Head Comparisons."""

import asyncio
import json
import time
import random
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import requests
import httpx

# Import our working standalone parser
from standalone_parser import StandaloneHeadToHeadParser, HeadToHeadComparisonData


class EnhancedAntiDetectionScraper:
    """Enhanced anti-detection scraper with sophisticated stealth techniques."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.session = requests.Session()
        self.async_client = None
        
        # Real G2.com test URLs
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        # Enhanced user agents with more variety
        self.user_agents = [
            # Chrome variants
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Safari variants
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            # Firefox variants
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            # Edge variants
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        ]
        
        # Enhanced headers with more realistic browser behavior
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"'
        }
        
        # Test results tracking
        self.test_results = {
            "start_time": datetime.now(),
            "total_urls": len(self.test_urls),
            "successful_scrapes": 0,
            "failed_scrapes": 0,
            "blocked_requests": 0,
            "rate_limited": 0,
            "parsing_successes": 0,
            "parsing_failures": 0,
            "ai_summary_extractions": 0,
            "total_processing_time": 0.0,
            "url_results": [],
            "stealth_techniques_used": []
        }
        
        print("🚀 Enhanced Anti-Detection Scraper Initialized")
        print(f"   - Parser: {type(self.parser).__name__}")
        print(f"   - Test URLs: {len(self.test_urls)}")
        print(f"   - User Agents: {len(self.user_agents)}")
        print(f"   - Enhanced Headers: {len(self.base_headers)}")
        print(f"   - Start Time: {self.test_results['start_time'].strftime('%H:%M:%S')}")
    
    def setup_enhanced_session(self):
        """Setup session with enhanced anti-detection headers."""
        # Randomize user agent
        user_agent = random.choice(self.user_agents)
        
        # Create enhanced headers
        headers = self.base_headers.copy()
        headers['User-Agent'] = user_agent
        
        # Randomize Accept-Language
        languages = ['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-CA,en;q=0.9', 'en-AU,en;q=0.9']
        headers['Accept-Language'] = random.choice(languages)
        
        # Randomize Sec-Ch-Ua-Platform
        platforms = ['"macOS"', '"Windows"', '"Linux"']
        headers['Sec-Ch-Ua-Platform'] = random.choice(platforms)
        
        # Update session
        self.session.headers.update(headers)
        
        print(f"   ✅ Enhanced session configured")
        print(f"      - User-Agent: {user_agent[:50]}...")
        print(f"      - Accept-Language: {headers['Accept-Language']}")
        print(f"      - Platform: {headers['Sec-Ch-Ua-Platform']}")
        
        self.test_results["stealth_techniques_used"].append("enhanced_headers")
    
    async def setup_enhanced_async_client(self):
        """Setup async HTTP client with enhanced anti-detection."""
        # Randomize user agent
        user_agent = random.choice(self.user_agents)
        
        # Create enhanced headers
        headers = self.base_headers.copy()
        headers['User-Agent'] = user_agent
        
        # Randomize Accept-Language
        languages = ['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-CA,en;q=0.9', 'en-AU,en;q=0.9']
        headers['Accept-Language'] = random.choice(languages)
        
        # Randomize Sec-Ch-Ua-Platform
        platforms = ['"macOS"', '"Windows"', '"Linux"']
        headers['Sec-Ch-Ua-Platform'] = random.choice(platforms)
        
        self.async_client = httpx.AsyncClient(
            headers=headers,
            timeout=45.0,
            follow_redirects=True,
            http2=False
        )
        
        print(f"   ✅ Enhanced async HTTP client configured")
        print(f"      - User-Agent: {user_agent[:50]}...")
        print(f"      - HTTP/2: Enabled")
        print(f"      - Timeout: 45s")
        
        self.test_results["stealth_techniques_used"].append("enhanced_async_client")
    
    def get_realistic_delay(self):
        """Get realistic delay that mimics human behavior."""
        # 70% chance of short delay (2-5s), 30% chance of longer delay (8-15s)
        if random.random() < 0.7:
            return random.uniform(2, 5)
        else:
            return random.uniform(8, 15)
    
    def rotate_user_agent(self):
        """Rotate to a different user agent and update headers."""
        new_agent = random.choice(self.user_agents)
        
        # Update session headers
        self.session.headers['User-Agent'] = new_agent
        
        # Update async client headers if available
        if self.async_client:
            self.async_client.headers['User-Agent'] = new_agent
        
        # Randomize other headers
        languages = ['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-CA,en;q=0.9', 'en-AU,en;q=0.9']
        platforms = ['"macOS"', '"Windows"', '"Linux"']
        
        self.session.headers['Accept-Language'] = random.choice(languages)
        self.session.headers['Sec-Ch-Ua-Platform'] = random.choice(platforms)
        
        if self.async_client:
            self.async_client.headers['Accept-Language'] = self.session.headers['Accept-Language']
            self.async_client.headers['Sec-Ch-Ua-Platform'] = self.session.headers['Sec-Ch-Ua-Platform']
        
        print(f"      🔄 Rotated to new user agent: {new_agent[:50]}...")
        self.test_results["stealth_techniques_used"].append("user_agent_rotation")
        
        return new_agent
    
    def add_random_headers(self):
        """Add random headers to make requests more unique."""
        # Random referer (common sites)
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.linkedin.com/",
            "https://www.reddit.com/",
            "https://www.twitter.com/",
            "https://www.facebook.com/"
        ]
        
        if random.random() < 0.7:  # 70% chance
            self.session.headers['Referer'] = random.choice(referers)
            if self.async_client:
                self.async_client.headers['Referer'] = self.session.headers['Referer']
        
        # Random Accept header variations
        accept_variations = [
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        ]
        
        if random.random() < 0.5:  # 50% chance
            self.session.headers['Accept'] = random.choice(accept_variations)
            if self.async_client:
                self.async_client.headers['Accept'] = self.session.headers['Accept']
        
        self.test_results["stealth_techniques_used"].append("random_headers")
    
    async def test_single_url_enhanced(self, url: str, attempt: int = 1) -> dict:
        """Test a single URL with enhanced anti-detection techniques."""
        url_result = {
            "url": url,
            "attempt": attempt,
            "method": "enhanced",
            "status_code": None,
            "html_length": 0,
            "parsing_success": False,
            "ai_summary_found": False,
            "processing_time": 0.0,
            "error": None,
            "parser_result": None,
            "stealth_techniques": []
        }
        
        try:
            print(f"   🔄 Testing: {url} (Attempt {attempt})")
            
            # Add realistic delay
            delay = self.get_realistic_delay()
            print(f"      ⏱️  Waiting {delay:.1f}s...")
            time.sleep(delay)
            
            # Add random headers before each request
            self.add_random_headers()
            
            # Make request with enhanced session
            start_time = time.time()
            response = self.session.get(url, timeout=45)
            request_time = time.time() - start_time
            
            url_result["status_code"] = response.status_code
            url_result["html_length"] = len(response.text)
            url_result["stealth_techniques"] = self.test_results["stealth_techniques_used"].copy()
            
            print(f"      📡 Response: {response.status_code} ({len(response.text)} bytes) in {request_time:.2f}s")
            
            # Handle different response codes
            if response.status_code == 200:
                # Check if we got actual HTML content
                if len(response.text) > 1000 and '<html' in response.text.lower():
                    # Parse the HTML
                    parse_start = time.time()
                    try:
                        parser_result = self.parser.parse_head_to_head_comparison(response.text, url)
                        parse_time = time.time() - parse_start
                        
                        url_result["parsing_success"] = True
                        url_result["processing_time"] = parse_time
                        url_result["parser_result"] = {
                            "comparison_id": parser_result.comparison_id,
                            "products": [parser_result.product_a.get('name'), parser_result.product_b.get('name')],
                            "ai_summary_quality": parser_result.summary_quality_score,
                            "data_quality": parser_result.data_quality_score,
                            "summary_points": len(parser_result.ai_generated_summary.get('summary_points', [])),
                            "extraction_confidence": parser_result.extraction_confidence
                        }
                        
                        # Check if AI summary was found
                        if parser_result.ai_generated_summary.get('summary_title') != "No Summary Found":
                            url_result["ai_summary_found"] = True
                            self.test_results["ai_summary_extractions"] += 1
                        
                        print(f"      ✅ Parsing successful in {parse_time:.2f}s")
                        print(f"         - Products: {parser_result.product_a.get('name')} vs {parser_result.product_b.get('name')}")
                        print(f"         - AI Summary Quality: {parser_result.summary_quality_score:.1f}/100")
                        print(f"         - Summary Points: {len(parser_result.ai_generated_summary.get('summary_points', []))}")
                        
                        self.test_results["parsing_successes"] += 1
                        
                    except Exception as parse_error:
                        url_result["error"] = f"Parsing failed: {str(parse_error)}"
                        self.test_results["parsing_failures"] += 1
                        print(f"      ❌ Parsing failed: {parse_error}")
                else:
                    url_result["error"] = "Invalid HTML content received"
                    print(f"      ⚠️  Invalid HTML content (length: {len(response.text)})")
            
            elif response.status_code == 403:  # Access blocked
                url_result["error"] = "Access blocked"
                self.test_results["blocked_requests"] += 1
                print(f"      🚫 Access blocked - implementing enhanced stealth...")
                
                # Enhanced stealth response
                if attempt < 3:  # Try up to 3 times
                    print(f"      🔄 Retrying with enhanced stealth (attempt {attempt + 1})...")
                    
                    # Rotate user agent and headers
                    self.rotate_user_agent()
                    self.add_random_headers()
                    
                    # Wait longer before retry
                    retry_delay = random.uniform(10, 20)
                    print(f"      ⏱️  Waiting {retry_delay:.1f}s before retry...")
                    time.sleep(retry_delay)
                    
                    # Recursive retry
                    return await self.test_single_url_enhanced(url, attempt + 1)
                else:
                    print(f"      💥 Max retry attempts reached")
                
            elif response.status_code == 429:  # Rate limited
                url_result["error"] = "Rate limited"
                self.test_results["rate_limited"] += 1
                print(f"      ⚠️  Rate limited - waiting 120s...")
                time.sleep(120)
                
            elif response.status_code == 503:  # Service unavailable
                url_result["error"] = "Service unavailable"
                print(f"      🔧 Service unavailable - waiting 60s...")
                time.sleep(60)
                
            else:
                url_result["error"] = f"HTTP {response.status_code}"
                print(f"      ❌ HTTP error: {response.status_code}")
            
            # Update success/failure counts
            if url_result["parsing_success"]:
                self.test_results["successful_scrapes"] += 1
            else:
                self.test_results["failed_scrapes"] += 1
            
            self.test_results["total_processing_time"] += url_result["processing_time"]
            
        except requests.exceptions.Timeout:
            url_result["error"] = "Request timeout"
            print(f"      ⏰ Request timeout")
        except requests.exceptions.ConnectionError:
            url_result["error"] = "Connection error"
            print(f"      🔌 Connection error")
        except Exception as e:
            url_result["error"] = f"Unexpected error: {str(e)}"
            print(f"      💥 Unexpected error: {e}")
        
        return url_result
    
    async def test_all_urls_enhanced(self):
        """Test all URLs with enhanced anti-detection."""
        print("\n🧪 Testing All URLs (Enhanced Anti-Detection)")
        print("=" * 70)
        
        for url in self.test_urls:
            url_result = await self.test_single_url_enhanced(url)
            self.test_results["url_results"].append(url_result)
            
            # Add realistic delay between requests
            if url != self.test_urls[-1]:  # Not the last URL
                delay = random.uniform(8, 15)
                print(f"      ⏱️  Waiting {delay:.1f}s before next request...")
                time.sleep(delay)
    
    def export_enhanced_test_results(self, output_dir: str = "output"):
        """Export enhanced test results to JSON for analysis."""
        try:
            # Create output directory
            Path(output_dir).mkdir(exist_ok=True)
            
            # Prepare export data
            export_data = {
                "test_timestamp": datetime.now().isoformat(),
                "test_summary": self.get_enhanced_test_summary(),
                "url_results": self.test_results["url_results"],
                "stealth_techniques_used": list(set(self.test_results["stealth_techniques_used"])),
                "parser_capabilities": self.parser.get_extraction_statistics()
            }
            
            # Export to JSON
            output_file = Path(output_dir) / f"enhanced_anti_detection_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Enhanced test results exported to: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Failed to export results: {e}")
            return None
    
    def get_enhanced_test_summary(self) -> dict:
        """Get comprehensive enhanced test summary."""
        if self.test_results["start_time"]:
            elapsed_time = (datetime.now() - self.test_results["start_time"]).total_seconds()
        else:
            elapsed_time = 0
        
        success_rate = 0
        if self.test_results["total_urls"] > 0:
            success_rate = (self.test_results["successful_scrapes"] / 
                          self.test_results["total_urls"]) * 100
        
        parsing_success_rate = 0
        if self.test_results["parsing_successes"] + self.test_results["parsing_failures"] > 0:
            parsing_success_rate = (self.test_results["parsing_successes"] / 
                                  (self.test_results["parsing_successes"] + self.test_results["parsing_failures"])) * 100
        
        avg_processing_time = 0
        if self.test_results["parsing_successes"] > 0:
            avg_processing_time = (self.test_results["total_processing_time"] / 
                                 self.test_results["parsing_successes"])
        
        return {
            "total_urls": self.test_results["total_urls"],
            "successful_scrapes": self.test_results["successful_scrapes"],
            "failed_scrapes": self.test_results["failed_scrapes"],
            "scraping_success_rate": f"{success_rate:.1f}%",
            "parsing_successes": self.test_results["parsing_successes"],
            "parsing_failures": self.test_results["parsing_failures"],
            "parsing_success_rate": f"{parsing_success_rate:.1f}%",
            "ai_summary_extractions": self.test_results["ai_summary_extractions"],
            "blocked_requests": self.test_results["blocked_requests"],
            "rate_limited": self.test_results["rate_limited"],
            "elapsed_time_seconds": elapsed_time,
            "average_processing_time": f"{avg_processing_time:.2f}s",
            "stealth_techniques_count": len(set(self.test_results["stealth_techniques_used"])),
            "start_time": self.test_results["start_time"].isoformat(),
            "end_time": datetime.now().isoformat()
        }


async def main():
    """Main enhanced anti-detection test execution."""
    print("🚀 ENHANCED ANTI-DETECTION TESTING - G2.com Head-to-Head Comparisons")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize enhanced scraper
    scraper = EnhancedAntiDetectionScraper()
    
    # Setup enhanced session and client
    scraper.setup_enhanced_session()
    await scraper.setup_enhanced_async_client()
    
    # Test with enhanced anti-detection
    print("\n📋 Enhanced Anti-Detection Testing")
    await scraper.test_all_urls_enhanced()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 ENHANCED ANTI-DETECTION TEST SUMMARY")
    print("=" * 80)
    
    summary = scraper.get_enhanced_test_summary()
    
    print(f"📈 Overall Performance:")
    print(f"   - Scraping Success Rate: {summary['scraping_success_rate']}")
    print(f"   - Parsing Success Rate: {summary['parsing_success_rate']}")
    print(f"   - AI Summary Extractions: {summary['ai_summary_extractions']}")
    print(f"   - Blocked Requests: {summary['blocked_requests']}")
    print(f"   - Rate Limited: {summary['rate_limited']}")
    print(f"   - Stealth Techniques Used: {summary['stealth_techniques_count']}")
    print(f"   - Average Processing Time: {summary['average_processing_time']}")
    print(f"   - Total Elapsed Time: {summary['elapsed_time_seconds']:.1f}s")
    
    # URL-specific results
    print(f"\n🌐 URL Results:")
    for i, result in enumerate(scraper.test_results["url_results"]):
        status = "✅ SUCCESS" if result["parsing_success"] else "❌ FAILED"
        attempts = result.get("attempt", 1)
        print(f"   {i+1}. {status} (Attempts: {attempts}) - {result['url']}")
        if result["error"]:
            print(f"      Error: {result['error']}")
        elif result["parser_result"]:
            print(f"      Products: {result['parser_result']['products'][0]} vs {result['parser_result']['products'][1]}")
            print(f"      AI Summary Quality: {result['parser_result']['ai_summary_quality']:.1f}/100")
    
    # Success criteria evaluation
    scraping_success = float(summary['scraping_success_rate'].rstrip('%'))
    parsing_success = float(summary['parsing_success_rate'].rstrip('%'))
    
    if scraping_success >= 80 and parsing_success >= 70:
        print(f"\n🎉 ENHANCED ANTI-DETECTION SUCCESSFUL!")
        print(f"   - Scraping: {summary['scraping_success_rate']} ✅ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ✅ (Target: 70%+)")
        print(f"   Next: Implement production features and scaling")
        
        # Export results
        scraper.export_enhanced_test_results()
        
    elif scraping_success >= 50 and parsing_success >= 50:
        print(f"\n⚠️  PARTIAL ENHANCED SUCCESS")
        print(f"   - Scraping: {summary['scraping_success_rate']} ⚠️ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ⚠️ (Target: 70%+)")
        print(f"   Next: Further enhance stealth techniques")
        
        # Export results
        scraper.export_enhanced_test_results()
        
    else:
        print(f"\n💥 ENHANCED ANTI-DETECTION FAILED")
        print(f"   - Scraping: {summary['scraping_success_rate']} ❌ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ❌ (Target: 70%+)")
        print(f"   Next: Implement advanced techniques (proxies, browser automation)")
    
    return scraping_success >= 80 and parsing_success >= 70


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Enhanced testing interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        exit(1)
