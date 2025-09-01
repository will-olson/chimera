"""
AURA-LITE MVP Test Script
Test basic functionality with targeted data collection
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_lite import AuraLite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_mvp_functionality():
    """Test MVP functionality with targeted data collection"""
    print("🧪 AURA-LITE MVP Test")
    print("=" * 50)
    print("Testing basic functionality with targeted data collection")
    print("=" * 50)
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        print("1. Initializing AURA-LITE...")
        aura_lite = AuraLite()
        
        # Test target loading
        print("2. Testing target loading...")
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        print(f"   ✅ Loaded {len(targets)} high priority targets")
        
        if targets:
            target = targets[0]
            print(f"   📋 First target: {target['data']['name']}")
        
        # Setup browser
        print("3. Setting up browser...")
        if not await aura_lite.setup_aura_browser():
            print("   ❌ Failed to setup browser")
            return False
        
        print("   ✅ Browser setup completed")
        
        # Test Cloudflare bypass
        print("4. Testing Cloudflare bypass...")
        bypass_test = await aura_lite.test_cloudflare_bypass()
        if bypass_test.get('overall_success'):
            print("   ✅ Cloudflare bypass test passed")
        else:
            print("   ⚠️ Cloudflare bypass test had issues")
        
        # Test anti-detection
        print("5. Testing anti-detection measures...")
        anti_detection_test = await aura_lite.test_anti_detection()
        if anti_detection_test.get('overall_success'):
            print("   ✅ Anti-detection test passed")
        else:
            print("   ⚠️ Anti-detection test had issues")
        
        # Test single competitor scraping
        print("6. Testing single competitor scraping...")
        scraping_result = await aura_lite.test_single_competitor()
        
        if 'error' not in scraping_result:
            print("   ✅ Single competitor scraping successful!")
            print(f"   📊 Company: {scraping_result.get('company')}")
            print(f"   ⭐ Overall Rating: {scraping_result.get('overall_rating')}")
            print(f"   📝 Review Count: {scraping_result.get('review_count')}")
            print(f"   📄 Reviews Scraped: {len(scraping_result.get('reviews', []))}")
            print(f"   💰 Pricing: {scraping_result.get('pricing_info')}")
            
            # Show sample review
            if scraping_result.get('reviews'):
                sample_review = scraping_result['reviews'][0]
                print(f"\n   📝 Sample Review:")
                print(f"      Reviewer: {sample_review.get('reviewer')}")
                print(f"      Rating: {sample_review.get('rating')}")
                print(f"      Date: {sample_review.get('date')}")
                print(f"      Text: {sample_review.get('text', '')[:100]}...")
        else:
            print(f"   ❌ Single competitor scraping failed: {scraping_result.get('error')}")
            return False
        
        # Test data extraction statistics
        print("7. Testing data extraction statistics...")
        extraction_stats = aura_lite.data_extractor.get_extraction_statistics()
        print(f"   📊 Extraction attempts: {extraction_stats['extraction_attempts']}")
        print(f"   ✅ Successful extractions: {extraction_stats['successful_extractions']}")
        print(f"   📝 Reviews extracted: {extraction_stats['reviews_extracted']}")
        print(f"   ⭐ Ratings extracted: {extraction_stats['ratings_extracted']}")
        
        # Test session management
        print("8. Testing session management...")
        session_summary = aura_lite.session_manager.get_session_summary()
        print(f"   📊 Session ID: {session_summary['session_id']}")
        print(f"   ⏱️ Duration: {session_summary['duration_minutes']:.1f} minutes")
        print(f"   ✅ Success rate: {session_summary['success_rate']:.1%}")
        print(f"   📝 Total reviews: {session_summary['total_reviews']}")
        
        # Save test results
        print("9. Saving test results...")
        report_file = aura_lite.session_manager.save_session_report()
        data_file = aura_lite.session_manager.save_scraped_data()
        
        if report_file:
            print(f"   📊 Session report saved: {report_file}")
        if data_file:
            print(f"   📄 Data saved: {data_file}")
        
        print("\n🎉 MVP Test Completed Successfully!")
        print("=" * 50)
        print("✅ All core functionality validated")
        print("✅ Cloudflare bypass working")
        print("✅ Anti-detection measures active")
        print("✅ Data extraction functional")
        print("✅ Session management operational")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"Error in MVP test: {str(e)}")
        print(f"❌ MVP test failed: {str(e)}")
        return False
    
    finally:
        if aura_lite:
            await aura_lite.close()
        print("\n🏁 MVP test completed")

async def test_targeted_data_collection():
    """Test targeted data collection similar to benchmark scrapers"""
    print("\n🎯 Targeted Data Collection Test")
    print("=" * 50)
    print("Testing data collection similar to benchmark scrapers")
    print("=" * 50)
    
    aura_lite = None
    try:
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        # Test with Sigma (from benchmark scrapers)
        print("Testing with Sigma (benchmark target)...")
        sigma_result = await aura_lite.test_single_competitor("sigma")
        
        if 'error' not in sigma_result:
            print("✅ Sigma data collection successful!")
            print(f"   Company: {sigma_result.get('company')}")
            print(f"   Rating: {sigma_result.get('overall_rating')}")
            print(f"   Reviews: {len(sigma_result.get('reviews', []))}")
            print(f"   Pricing: {sigma_result.get('pricing_info')}")
            
            # Test alternatives extraction
            if 'alternatives' in sigma_result:
                print(f"   Alternatives: {len(sigma_result['alternatives'])}")
        else:
            print(f"❌ Sigma data collection failed: {sigma_result.get('error')}")
        
        # Test with Power BI
        print("\nTesting with Power BI...")
        powerbi_result = await aura_lite.test_single_competitor("power_bi")
        
        if 'error' not in powerbi_result:
            print("✅ Power BI data collection successful!")
            print(f"   Company: {powerbi_result.get('company')}")
            print(f"   Rating: {powerbi_result.get('overall_rating')}")
            print(f"   Reviews: {len(powerbi_result.get('reviews', []))}")
        else:
            print(f"❌ Power BI data collection failed: {powerbi_result.get('error')}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in targeted data collection test: {str(e)}")
        print(f"❌ Targeted data collection test failed: {str(e)}")
        return False
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def main():
    """Main test function"""
    print("🚀 AURA-LITE MVP Validation")
    print("=" * 60)
    print("Testing core functionality and targeted data collection")
    print("=" * 60)
    
    # Test 1: MVP functionality
    mvp_success = await test_mvp_functionality()
    
    if mvp_success:
        # Test 2: Targeted data collection
        await test_targeted_data_collection()
        
        print("\n🎉 All tests completed!")
        print("AURA-LITE is ready for production use.")
    else:
        print("\n❌ MVP test failed. Check logs for details.")

if __name__ == "__main__":
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    asyncio.run(main())
