"""
AURA-LITE Main Entry Point
Specialized Capterra scraper with Cloudflare bypass
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/aura_lite.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main entry point for AURA-LITE"""
    print("🎯 AURA-LITE - Specialized Capterra Scraper")
    print("=" * 60)
    print("Built on Chimera-Ultimate's proven CAPTCHA bypass techniques")
    print("Optimized for Cloudflare bypass and Capterra data extraction")
    print("=" * 60)
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        aura_lite = AuraLite()
        
        # Setup browser
        if not await aura_lite.setup_aura_browser():
            print("❌ Failed to setup browser")
            return
        
        print("✅ Browser setup completed")
        
        # Run comprehensive test
        print("\n🧪 Running comprehensive test suite...")
        test_results = await aura_lite.run_comprehensive_test()
        
        if test_results.get('overall_success'):
            print("✅ All tests passed! AURA-LITE is ready for production.")
            
            # Run actual scraping
            print("\n🚀 Starting targeted scraping...")
            scraping_results = await aura_lite.scrape_capterra_targets(max_competitors=2)
            
            # Print session summary
            aura_lite.session_manager.print_session_summary()
            
            # Save results
            report_file = aura_lite.session_manager.save_session_report()
            data_file = aura_lite.session_manager.save_scraped_data()
            csv_file = aura_lite.session_manager.export_to_csv()
            
            print(f"\n💾 Results saved:")
            if report_file:
                print(f"   📊 Session Report: {report_file}")
            if data_file:
                print(f"   📄 Raw Data: {data_file}")
            if csv_file:
                print(f"   📈 CSV Export: {csv_file}")
                
        else:
            print("❌ Some tests failed. Check logs for details.")
            print(f"Test Results: {test_results.get('test_summary', {})}")
    
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"❌ Execution error: {str(e)}")
    
    finally:
        if aura_lite:
            await aura_lite.close()
        print("\n🏁 AURA-LITE execution completed")

async def test_mode():
    """Test mode for MVP validation"""
    print("🧪 AURA-LITE Test Mode")
    print("=" * 40)
    
    aura_lite = None
    try:
        aura_lite = AuraLite()
        
        if not await aura_lite.setup_aura_browser():
            print("❌ Failed to setup browser")
            return
        
        print("✅ Browser setup completed")
        
        # Test single competitor
        print("\n🎯 Testing single competitor scraping...")
        result = await aura_lite.test_single_competitor()
        
        if 'error' not in result:
            print("✅ Single competitor test successful!")
            print(f"   Company: {result.get('company')}")
            print(f"   Overall Rating: {result.get('overall_rating')}")
            print(f"   Review Count: {result.get('review_count')}")
            print(f"   Reviews Scraped: {len(result.get('reviews', []))}")
            print(f"   Pricing: {result.get('pricing_info')}")
        else:
            print(f"❌ Single competitor test failed: {result.get('error')}")
        
        # Print system statistics
        stats = aura_lite.get_system_statistics()
        print(f"\n📊 System Statistics:")
        print(f"   Session: {stats['session']}")
        print(f"   Targets: {stats['targets']}")
        print(f"   Cloudflare: {stats['cloudflare']}")
    
    except Exception as e:
        logger.error(f"Error in test mode: {str(e)}")
        print(f"❌ Test error: {str(e)}")
    
    finally:
        if aura_lite:
            await aura_lite.close()

if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(test_mode())
    else:
        asyncio.run(main())
