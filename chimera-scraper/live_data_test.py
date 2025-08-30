#!/usr/bin/env python3
"""Live Data Testing Script for Enhanced Head-to-Head Comparison Scraping."""

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


class LiveDataTester:
    """Live data tester for real G2.com head-to-head comparison pages."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.session = requests.Session()
        self.async_client = None
        
        # Real G2.com test URLs from benchmark targets
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        # Anti-detection user agents
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        
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
            "url_results": []
        }
        
        print("🚀 Live Data Tester Initialized")
        print(f"   - Parser: {type(self.parser).__name__}")
        print(f"   - Test URLs: {len(self.test_urls)}")
        print(f"   - User Agents: {len(self.user_agents)}")
        print(f"   - Start Time: {self.test_results['start_time'].strftime('%H:%M:%S')}")
    
    def setup_session(self):
        """Setup session with anti-detection headers."""
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        print("   ✅ Session configured with anti-detection headers")
    
    async def setup_async_client(self):
        """Setup async HTTP client."""
        self.async_client = httpx.AsyncClient(
            headers={'User-Agent': random.choice(self.user_agents)},
            timeout=30.0,
            follow_redirects=True
        )
        print("   ✅ Async HTTP client configured")
    
    def get_random_delay(self):
        """Get random delay between requests."""
        return random.uniform(2, 5)
    
    def rotate_user_agent(self):
        """Rotate to a different user agent."""
        new_agent = random.choice(self.user_agents)
        self.session.headers['User-Agent'] = new_agent
        if self.async_client:
            self.async_client.headers['User-Agent'] = new_agent
        return new_agent
    
    async def test_single_url_sync(self, url: str) -> dict:
        """Test a single URL using synchronous requests."""
        url_result = {
            "url": url,
            "method": "sync",
            "status_code": None,
            "html_length": 0,
            "parsing_success": False,
            "ai_summary_found": False,
            "processing_time": 0.0,
            "error": None,
            "parser_result": None
        }
        
        try:
            print(f"   🔄 Testing: {url}")
            
            # Add random delay
            delay = self.get_random_delay()
            print(f"      ⏱️  Waiting {delay:.1f}s...")
            time.sleep(delay)
            
            # Make request
            start_time = time.time()
            response = self.session.get(url, timeout=30)
            request_time = time.time() - start_time
            
            url_result["status_code"] = response.status_code
            url_result["html_length"] = len(response.text)
            
            print(f"      📡 Response: {response.status_code} ({len(response.text)} bytes) in {request_time:.2f}s")
            
            # Handle different response codes
            if response.status_code == 200:
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
            
            elif response.status_code == 429:  # Rate limited
                url_result["error"] = "Rate limited"
                self.test_results["rate_limited"] += 1
                print(f"      ⚠️  Rate limited - waiting 60s...")
                time.sleep(60)
                
            elif response.status_code == 403:  # Blocked
                url_result["error"] = "Access blocked"
                self.test_results["blocked_requests"] += 1
                print(f"      🚫 Access blocked - rotating user agent...")
                self.rotate_user_agent()
                
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
    
    async def test_single_url_async(self, url: str) -> dict:
        """Test a single URL using asynchronous requests."""
        url_result = {
            "url": url,
            "method": "async",
            "status_code": None,
            "html_length": 0,
            "parsing_success": False,
            "ai_summary_found": False,
            "processing_time": 0.0,
            "error": None,
            "parser_result": None
        }
        
        try:
            print(f"   🔄 Testing: {url}")
            
            # Add random delay
            delay = self.get_random_delay()
            print(f"      ⏱️  Waiting {delay:.1f}s...")
            await asyncio.sleep(delay)
            
            # Make request
            start_time = time.time()
            response = await self.async_client.get(url)
            request_time = time.time() - start_time
            
            url_result["status_code"] = response.status_code
            url_result["html_length"] = len(response.text)
            
            print(f"      📡 Response: {response.status_code} ({len(response.text)} bytes) in {request_time:.2f}s")
            
            # Handle different response codes
            if response.status_code == 200:
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
            
            elif response.status_code == 429:  # Rate limited
                url_result["error"] = "Rate limited"
                self.test_results["rate_limited"] += 1
                print(f"      ⚠️  Rate limited - waiting 60s...")
                await asyncio.sleep(60)
                
            elif response.status_code == 403:  # Blocked
                url_result["error"] = "Access blocked"
                self.test_results["blocked_requests"] += 1
                print(f"      🚫 Access blocked - rotating user agent...")
                self.rotate_user_agent()
                
            else:
                url_result["error"] = f"HTTP {response.status_code}"
                print(f"      ❌ HTTP error: {response.status_code}")
            
            # Update success/failure counts
            if url_result["parsing_success"]:
                self.test_results["successful_scrapes"] += 1
            else:
                self.test_results["failed_scrapes"] += 1
            
            self.test_results["total_processing_time"] += url_result["processing_time"]
            
        except httpx.TimeoutException:
            url_result["error"] = "Request timeout"
            print(f"      ⏰ Request timeout")
        except httpx.ConnectError:
            url_result["error"] = "Connection error"
            print(f"      🔌 Connection error")
        except Exception as e:
            url_result["error"] = f"Unexpected error: {str(e)}"
            print(f"      💥 Unexpected error: {e}")
        
        return url_result
    
    async def test_all_urls_sync(self):
        """Test all URLs using synchronous requests."""
        print("\n🧪 Testing All URLs (Synchronous)")
        print("=" * 60)
        
        for url in self.test_urls:
            url_result = await self.test_single_url_sync(url)
            self.test_results["url_results"].append(url_result)
            
            # Add delay between requests
            if url != self.test_urls[-1]:  # Not the last URL
                delay = random.uniform(3, 7)
                print(f"      ⏱️  Waiting {delay:.1f}s before next request...")
                time.sleep(delay)
    
    async def test_all_urls_async(self):
        """Test all URLs using asynchronous requests."""
        print("\n🧪 Testing All URLs (Asynchronous)")
        print("=" * 60)
        
        # Create tasks for all URLs
        tasks = [self.test_single_url_async(url) for url in self.test_urls]
        
        # Execute all tasks concurrently
        url_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(url_results):
            if isinstance(result, Exception):
                # Handle exceptions
                url_result = {
                    "url": self.test_urls[i],
                    "method": "async",
                    "status_code": None,
                    "html_length": 0,
                    "parsing_success": False,
                    "ai_summary_found": False,
                    "processing_time": 0.0,
                    "error": f"Task failed: {str(result)}",
                    "parser_result": None
                }
                self.test_results["failed_scrapes"] += 1
            else:
                url_result = result
            
            self.test_results["url_results"].append(url_result)
    
    def export_live_test_results(self, output_dir: str = "output"):
        """Export live test results to JSON for analysis."""
        try:
            # Create output directory
            Path(output_dir).mkdir(exist_ok=True)
            
            # Prepare export data
            export_data = {
                "test_timestamp": datetime.now().isoformat(),
                "test_summary": self.get_test_summary(),
                "url_results": self.test_results["url_results"],
                "parser_capabilities": self.parser.get_extraction_statistics()
            }
            
            # Export to JSON
            output_file = Path(output_dir) / f"live_data_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Live test results exported to: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Failed to export results: {e}")
            return None
    
    def get_test_summary(self) -> dict:
        """Get comprehensive test summary."""
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
            "start_time": self.test_results["start_time"].isoformat(),
            "end_time": datetime.now().isoformat()
        }


async def main():
    """Main test execution."""
    print("🚀 LIVE DATA TESTING - Enhanced Head-to-Head Comparison Scraping")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize tester
    tester = LiveDataTester()
    
    # Setup session and client
    tester.setup_session()
    await tester.setup_async_client()
    
    # Test 1: Synchronous testing
    print("\n📋 Test 1: Synchronous HTTP Requests")
    await tester.test_all_urls_sync()
    
    # Test 2: Asynchronous testing (if sync was successful)
    if tester.test_results["successful_scrapes"] > 0:
        print("\n📋 Test 2: Asynchronous HTTP Requests")
        await tester.test_all_urls_async()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 LIVE DATA TEST SUMMARY")
    print("=" * 80)
    
    summary = tester.get_test_summary()
    
    print(f"📈 Overall Performance:")
    print(f"   - Scraping Success Rate: {summary['scraping_success_rate']}")
    print(f"   - Parsing Success Rate: {summary['parsing_success_rate']}")
    print(f"   - AI Summary Extractions: {summary['ai_summary_extractions']}")
    print(f"   - Blocked Requests: {summary['blocked_requests']}")
    print(f"   - Rate Limited: {summary['rate_limited']}")
    print(f"   - Average Processing Time: {summary['average_processing_time']}")
    print(f"   - Total Elapsed Time: {summary['elapsed_time_seconds']:.1f}s")
    
    # URL-specific results
    print(f"\n🌐 URL Results:")
    for i, result in enumerate(tester.test_results["url_results"]):
        status = "✅ SUCCESS" if result["parsing_success"] else "❌ FAILED"
        method = result["method"].upper()
        print(f"   {i+1}. {status} ({method}) - {result['url']}")
        if result["error"]:
            print(f"      Error: {result['error']}")
        elif result["parser_result"]:
            print(f"      Products: {result['parser_result']['products'][0]} vs {result['parser_result']['products'][1]}")
            print(f"      AI Summary Quality: {result['parser_result']['ai_summary_quality']:.1f}/100")
    
    # Success criteria evaluation
    scraping_success = float(summary['scraping_success_rate'].rstrip('%'))
    parsing_success = float(summary['parsing_success_rate'].rstrip('%'))
    
    if scraping_success >= 80 and parsing_success >= 70:
        print(f"\n🎉 LIVE DATA TESTING SUCCESSFUL!")
        print(f"   - Scraping: {summary['scraping_success_rate']} ✅ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ✅ (Target: 70%+)")
        print(f"   Next: Implement advanced anti-detection and production features")
        
        # Export results
        tester.export_live_test_results()
        
    elif scraping_success >= 50 and parsing_success >= 50:
        print(f"\n⚠️  PARTIAL LIVE DATA SUCCESS")
        print(f"   - Scraping: {summary['scraping_success_rate']} ⚠️ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ⚠️ (Target: 70%+)")
        print(f"   Next: Improve anti-detection and retry mechanisms")
        
        # Export results
        tester.export_live_test_results()
        
    else:
        print(f"\n💥 LIVE DATA TESTING FAILED")
        print(f"   - Scraping: {summary['scraping_success_rate']} ❌ (Target: 80%+)")
        print(f"   - Parsing: {summary['parsing_success_rate']} ❌ (Target: 70%+)")
        print(f"   Next: Investigate blocking mechanisms and improve stealth")
    
    # Cleanup
    if tester.async_client:
        await tester.async_client.aclose()
    
    return scraping_success >= 80 and parsing_success >= 70


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Live testing interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        exit(1)
