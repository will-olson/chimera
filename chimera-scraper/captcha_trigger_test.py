#!/usr/bin/env python3
"""
CAPTCHA Trigger Test
Tests the precision puzzle solver with URLs likely to trigger DataDome CAPTCHA
"""

import time
import json
from integrated_precision_scraper import IntegratedPrecisionScraper

def test_captcha_triggers():
    """Test various URLs that might trigger CAPTCHA challenges"""
    
    # URLs that commonly trigger DataDome CAPTCHA
    test_urls = [
        "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense",
        "https://www.g2.com/compare/tableau-vs-microsoft-power-bi",
        "https://www.g2.com/compare/salesforce-vs-hubspot",
        "https://www.g2.com/compare/zoom-vs-microsoft-teams",
        "https://www.g2.com/compare/slack-vs-microsoft-teams",
        "https://www.g2.com/compare/notion-vs-confluence",
        "https://www.g2.com/compare/figma-vs-sketch",
        "https://www.g2.com/compare/trello-vs-asana"
    ]
    
    results = []
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'='*60}")
        print(f"🧪 TEST {i}/{len(test_urls)}: {url}")
        print(f"{'='*60}")
        
        try:
            # Create scraper instance
            scraper = IntegratedPrecisionScraper(headless=False)
            
            # Run scraping session
            success = scraper.run_scraping_session(url)
            
            # Record results
            test_result = {
                'test_number': i,
                'url': url,
                'success': success,
                'captcha_detected': scraper.results.get('puzzle_solved', False),
                'data_extracted': scraper.results.get('data_extracted', False),
                'errors': scraper.results.get('errors', []),
                'timing': scraper.results.get('timing', {}),
                'puzzle_stats': scraper.results.get('puzzle_stats', {})
            }
            
            results.append(test_result)
            
            # Save individual test results
            filename = f"test_{i}_results.json"
            scraper.save_results(filename)
            
            # Brief pause between tests
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Test {i} failed with error: {e}")
            results.append({
                'test_number': i,
                'url': url,
                'success': False,
                'error': str(e)
            })
    
    # Save comprehensive results
    with open('comprehensive_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 COMPREHENSIVE TEST RESULTS")
    print(f"{'='*60}")
    
    successful_tests = sum(1 for r in results if r.get('success', False))
    captcha_detected = sum(1 for r in results if r.get('captcha_detected', False))
    
    print(f"Total Tests: {len(test_urls)}")
    print(f"Successful: {successful_tests}")
    print(f"CAPTCHA Detected: {captcha_detected}")
    print(f"Success Rate: {(successful_tests/len(test_urls)*100):.1f}%")
    
    if captcha_detected > 0:
        print(f"\n🎯 CAPTCHA CHALLENGES ENCOUNTERED: {captcha_detected}")
        print("This means our precision solver will be tested!")
    else:
        print(f"\nℹ️ No CAPTCHA challenges encountered")
        print("DataDome may not be active on these URLs currently")
    
    return results

def test_with_rapid_requests():
    """Test with rapid requests to trigger rate limiting and CAPTCHA"""
    print("\n🚀 Testing with rapid requests to trigger CAPTCHA...")
    
    url = "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense"
    
    for i in range(5):
        print(f"\n🔥 Rapid Request {i+1}/5")
        
        try:
            scraper = IntegratedPrecisionScraper(headless=True)  # Headless for speed
            success = scraper.run_scraping_session(url)
            
            if success:
                print(f"✅ Request {i+1} successful")
            else:
                print(f"❌ Request {i+1} failed")
            
            # Very short pause to trigger rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Rapid request {i+1} error: {e}")
    
    print("\n🎯 Rapid request testing complete")

if __name__ == "__main__":
    print("🧪 CAPTCHA Trigger Test Suite")
    print("Testing precision puzzle solver with various scenarios")
    
    # Test 1: Multiple URLs
    results = test_captcha_triggers()
    
    # Test 2: Rapid requests to trigger rate limiting
    test_with_rapid_requests()
    
    print("\n🎉 All tests completed!")
    print("Check comprehensive_test_results.json for detailed results")
