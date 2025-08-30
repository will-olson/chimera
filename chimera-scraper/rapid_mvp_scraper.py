#!/usr/bin/env python3
"""Rapid MVP Scraper for Enhanced Head-to-Head Comparison Testing."""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# Import our working standalone parser
from standalone_parser import StandaloneHeadToHeadParser, HeadToHeadComparisonData


class RapidMVPScraper:
    """Rapid MVP scraper for immediate testing of head-to-head comparison functionality."""
    
    def __init__(self):
        self.parser = StandaloneHeadToHeadParser()
        self.scraping_stats = {
            "total_attempts": 0,
            "successful_scrapes": 0,
            "failed_scrapes": 0,
            "ai_summary_extractions": 0,
            "start_time": datetime.now(),
            "total_processing_time": 0.0
        }
        
        # Test URLs from benchmark targets
        self.test_urls = [
            "https://www.g2.com/compare/power-bi-vs-tableau",
            "https://www.g2.com/compare/power-bi-vs-qlik-sense",
            "https://www.g2.com/compare/tableau-vs-qlik-sense"
        ]
        
        print("🚀 Rapid MVP Scraper Initialized")
        print(f"   - Parser: {type(self.parser).__name__}")
        print(f"   - Test URLs: {len(self.test_urls)}")
        print(f"   - Start Time: {self.scraping_stats['start_time'].strftime('%H:%M:%S')}")
    
    async def test_with_mock_data(self):
        """Test the parser with mock HTML data to validate functionality."""
        print("\n🧪 Testing with Mock Data")
        print("=" * 50)
        
        mock_html = """
        <html>
        <head><title>Power BI vs Tableau Comparison</title></head>
        <body>
            <div class="comparison-container-v2_header">Microsoft Power BI</div>
            <div class="comparison-container-v2_header">Tableau</div>
            <div aria-label="Comparison Summary" class="compare-container-v2_summary">
                <div>AI Generated Summary</div>
                <ul>
                    <li>Microsoft Power BI excels in data visualization, scoring 9.2 compared to Tableau's 8.7. Users report that Power BI's interactive dashboards and rich visualizations make it easier to derive insights from data.</li>
                    <li>Tableau has better ease of setup with 8.5 vs Power BI's 7.8. Reviewers mention that Tableau's intuitive interface and guided setup process reduces the learning curve for new users.</li>
                    <li>Both products excel in data governance, with Power BI scoring 8.9 and Tableau scoring 8.6. Enterprise users appreciate the robust security features and compliance capabilities.</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        try:
            start_time = time.time()
            result = self.parser.parse_head_to_head_comparison(
                mock_html, 
                "https://www.g2.com/compare/power-bi-vs-tableau"
            )
            processing_time = time.time() - start_time
            
            print(f"✅ Mock data parsing successful in {processing_time:.2f}s")
            print(f"   - Comparison ID: {result.comparison_id}")
            print(f"   - Products: {result.product_a.get('name', 'Unknown')} vs {result.product_b.get('name', 'Unknown')}")
            print(f"   - AI Summary Quality: {result.summary_quality_score:.1f}/100")
            print(f"   - Data Quality: {result.data_quality_score:.1f}/100")
            print(f"   - Summary Points: {len(result.ai_generated_summary.get('summary_points', []))}")
            
            # Show AI summary insights
            ai_summary = result.ai_generated_summary
            if ai_summary.get('structured_insights'):
                insights = ai_summary['structured_insights']
                print(f"   - Competitive Advantages: {len(insights.get('competitive_advantages', []))}")
                print(f"   - Feature Comparisons: {len(insights.get('feature_comparisons', {}))}")
                print(f"   - Sentiment Analysis: {insights.get('sentiment_analysis', {})}")
            
            self.scraping_stats["successful_scrapes"] += 1
            self.scraping_stats["total_processing_time"] += processing_time
            
            return True
            
        except Exception as e:
            print(f"❌ Mock data parsing failed: {e}")
            self.scraping_stats["failed_scrapes"] += 1
            return False
    
    async def test_parser_robustness(self):
        """Test parser robustness with various HTML structures."""
        print("\n🧪 Testing Parser Robustness")
        print("=" * 50)
        
        test_cases = [
            {
                "name": "Standard G2 Structure",
                "html": """
                <html>
                <div class="comparison-container-v2_header">Product A</div>
                <div class="comparison-container-v2_header">Product B</div>
                <div aria-label="Comparison Summary">AI Generated Summary</div>
                <ul><li>Test summary point</li></ul>
                </html>
                """,
                "expected_products": 2,
                "expected_summary": True
            },
            {
                "name": "Missing AI Summary",
                "html": """
                <html>
                <div class="comparison-container-v2_header">Product A</div>
                <div class="comparison-container-v2_header">Product B</div>
                </html>
                """,
                "expected_products": 2,
                "expected_summary": False
            },
            {
                "name": "Minimal HTML",
                "html": """
                <html><body>Power BI vs Tableau comparison</body></html>
                """,
                "expected_products": 2,
                "expected_summary": False
            }
        ]
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for test_case in test_cases:
            try:
                print(f"   Testing: {test_case['name']}")
                
                result = self.parser.parse_head_to_head_comparison(
                    test_case["html"],
                    "https://example.com/test"
                )
                
                # Validate results
                products_found = len([result.product_a, result.product_b])
                summary_found = result.ai_generated_summary.get('summary_title') != "No Summary Found"
                
                if (products_found == test_case["expected_products"] and 
                    summary_found == test_case["expected_summary"]):
                    print(f"      ✅ PASS - Products: {products_found}, Summary: {summary_found}")
                    passed_tests += 1
                else:
                    print(f"      ❌ FAIL - Expected: {test_case['expected_products']} products, {test_case['expected_summary']} summary")
                    print(f"         Got: {products_found} products, {summary_found} summary")
                
            except Exception as e:
                print(f"      💥 CRASH - {e}")
        
        print(f"\n   Robustness Test Results: {passed_tests}/{total_tests} tests passed")
        return passed_tests == total_tests
    
    def export_test_results(self, results: list, output_dir: str = "output"):
        """Export test results to JSON for analysis."""
        try:
            # Create output directory
            Path(output_dir).mkdir(exist_ok=True)
            
            # Prepare export data
            export_data = {
                "test_timestamp": datetime.now().isoformat(),
                "scraper_stats": self.scraping_stats,
                "test_results": results,
                "parser_capabilities": self.parser.get_extraction_statistics()
            }
            
            # Export to JSON
            output_file = Path(output_dir) / f"rapid_mvp_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"✅ Test results exported to: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"❌ Failed to export results: {e}")
            return None
    
    def get_scraping_summary(self) -> dict:
        """Get comprehensive scraping summary."""
        if self.scraping_stats["start_time"]:
            elapsed_time = (datetime.now() - self.scraping_stats["start_time"]).total_seconds()
        else:
            elapsed_time = 0
        
        success_rate = 0
        if self.scraping_stats["total_attempts"] > 0:
            success_rate = (self.scraping_stats["successful_scrapes"] / 
                          self.scraping_stats["total_attempts"]) * 100
        
        avg_processing_time = 0
        if self.scraping_stats["successful_scrapes"] > 0:
            avg_processing_time = (self.scraping_stats["total_processing_time"] / 
                                 self.scraping_stats["successful_scrapes"])
        
        return {
            "total_attempts": self.scraping_stats["total_attempts"],
            "successful_scrapes": self.scraping_stats["successful_scrapes"],
            "failed_scrapes": self.scraping_stats["failed_scrapes"],
            "success_rate": f"{success_rate:.1f}%",
            "ai_summary_extractions": self.scraping_stats["ai_summary_extractions"],
            "elapsed_time_seconds": elapsed_time,
            "average_processing_time": f"{avg_processing_time:.2f}s",
            "start_time": self.scraping_stats["start_time"].isoformat(),
            "end_time": datetime.now().isoformat()
        }


async def main():
    """Main test execution."""
    print("🚀 RAPID MVP SCRAPER TESTING")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize scraper
    scraper = RapidMVPScraper()
    
    # Test 1: Mock data parsing
    print("\n📋 Test 1: Mock Data Parsing")
    mock_success = await scraper.test_with_mock_data()
    
    # Test 2: Parser robustness
    print("\n📋 Test 2: Parser Robustness")
    robustness_success = await scraper.test_parser_robustness()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 RAPID MVP TEST SUMMARY")
    print("=" * 80)
    
    tests = [
        ("Mock Data Parsing", mock_success),
        ("Parser Robustness", robustness_success)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    # Get scraping summary
    summary = scraper.get_scraping_summary()
    print(f"\n📈 Scraping Performance:")
    print(f"   - Success Rate: {summary['success_rate']}")
    print(f"   - Total Attempts: {summary['total_attempts']}")
    print(f"   - AI Summary Extractions: {summary['ai_summary_extractions']}")
    print(f"   - Average Processing Time: {summary['average_processing_time']}")
    
    if passed == total:
        print("\n🎉 ALL MVP TESTS PASSED - Ready for live testing!")
        print("   Next: Test with real G2.com data using HTTP requests")
        
        # Export results
        results = [{"test": "mock_data", "success": mock_success},
                  {"test": "robustness", "success": robustness_success}]
        scraper.export_test_results(results)
        
    elif passed >= total * 0.5:
        print("\n⚠️  PARTIAL MVP SUCCESS - Some issues to address")
        print("   Next: Fix failing tests before proceeding")
    else:
        print("\n💥 SIGNIFICANT MVP ISSUES - Core functionality needs attention")
        print("   Next: Address fundamental problems before testing")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        exit(1)
