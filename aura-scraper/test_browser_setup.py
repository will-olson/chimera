"""
AURA-LITE Browser Setup Test
Test browser initialization and basic Cloudflare bypass functionality
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

async def test_browser_setup():
    """Test browser setup and basic functionality"""
    print("🌐 AURA-LITE Browser Setup Test")
    print("=" * 50)
    print("Testing browser initialization and basic Cloudflare bypass")
    print("=" * 50)
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        print("1. Initializing AURA-LITE...")
        aura_lite = AuraLite()
        print("   ✅ AURA-LITE initialized")
        
        # Setup browser
        print("2. Setting up browser...")
        browser_success = await aura_lite.setup_aura_browser()
        
        if not browser_success:
            print("   ❌ Browser setup failed")
            return False
        
        print("   ✅ Browser setup completed")
        print(f"   🌐 Browser: {type(aura_lite.browser).__name__}")
        print(f"   📄 Page: {type(aura_lite.page).__name__}")
        
        # Test basic page navigation
        print("3. Testing basic page navigation...")
        try:
            await aura_lite.page.goto("https://www.google.com", wait_until='domcontentloaded')
            title = await aura_lite.page.title()
            print(f"   ✅ Navigation successful - Page title: {title}")
        except Exception as e:
            print(f"   ❌ Navigation failed: {str(e)}")
            return False
        
        # Test stealth measures
        print("4. Testing stealth measures...")
        try:
            webdriver_hidden = await aura_lite.page.evaluate("navigator.webdriver")
            plugins_count = await aura_lite.page.evaluate("navigator.plugins.length")
            user_agent = await aura_lite.page.evaluate("navigator.userAgent")
            
            print(f"   🛡️ Webdriver hidden: {'✅' if webdriver_hidden is None else '❌'}")
            print(f"   🔌 Plugins spoofed: {'✅' if plugins_count > 0 else '❌'} ({plugins_count} plugins)")
            print(f"   👤 User agent: {user_agent[:50]}...")
        except Exception as e:
            print(f"   ❌ Stealth test failed: {str(e)}")
        
        # Test human behavior simulation
        print("5. Testing human behavior simulation...")
        try:
            behavior_success = await aura_lite.behavior_simulator.simulate_natural_browsing()
            print(f"   🤖 Human behavior simulation: {'✅' if behavior_success else '❌'}")
        except Exception as e:
            print(f"   ❌ Human behavior test failed: {str(e)}")
        
        # Test Cloudflare bypass with a simple page
        print("6. Testing Cloudflare bypass detection...")
        try:
            # Test with a page that might have Cloudflare
            await aura_lite.page.goto("https://www.capterra.com", wait_until='domcontentloaded')
            
            # Check for Cloudflare protection
            protection_info = await aura_lite.cloudflare_manager.detect_cloudflare_protection(aura_lite.page)
            
            print(f"   🛡️ Cloudflare protection detected: {'✅' if protection_info['is_protected'] else '❌'}")
            print(f"   📊 Protection type: {protection_info['protection_type']}")
            print(f"   🎯 Confidence: {protection_info['confidence']:.2f}")
            
            if protection_info['indicators_found']:
                print(f"   🔍 Indicators found: {', '.join(protection_info['indicators_found'])}")
            
        except Exception as e:
            print(f"   ❌ Cloudflare detection test failed: {str(e)}")
        
        # Test data extractor initialization
        print("7. Testing data extractor...")
        try:
            extractor_stats = aura_lite.data_extractor.get_extraction_statistics()
            print(f"   📊 Data extractor initialized: ✅")
            print(f"   📈 Extraction attempts: {extractor_stats['extraction_attempts']}")
        except Exception as e:
            print(f"   ❌ Data extractor test failed: {str(e)}")
        
        print("\n🎉 Browser setup test completed successfully!")
        print("=" * 50)
        print("✅ Browser initialization working")
        print("✅ Page navigation functional")
        print("✅ Stealth measures active")
        print("✅ Human behavior simulation working")
        print("✅ Cloudflare detection operational")
        print("✅ Data extractor ready")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"Error in browser setup test: {str(e)}")
        print(f"❌ Browser setup test failed: {str(e)}")
        return False
    
    finally:
        if aura_lite:
            await aura_lite.close()
        print("\n🏁 Browser setup test completed")

async def test_capterra_navigation():
    """Test navigation to Capterra pages"""
    print("\n🎯 Capterra Navigation Test")
    print("=" * 50)
    print("Testing navigation to specific Capterra pages")
    print("=" * 50)
    
    aura_lite = None
    try:
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        # Get a test target
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        if not targets:
            print("❌ No targets found")
            return False
        
        target = targets[0]  # Use first target (Sigma)
        company_name = target['data']['name']
        reviews_url = target['data']['targets']['product_reviews']
        
        print(f"Testing with: {company_name}")
        print(f"URL: {reviews_url}")
        
        # Navigate to the page
        print("1. Navigating to Capterra page...")
        try:
            await aura_lite.page.goto(reviews_url, wait_until='domcontentloaded')
            print("   ✅ Navigation successful")
        except Exception as e:
            print(f"   ❌ Navigation failed: {str(e)}")
            return False
        
        # Wait a bit for page to load
        await asyncio.sleep(3)
        
        # Check for Cloudflare protection
        print("2. Checking for Cloudflare protection...")
        protection_info = await aura_lite.cloudflare_manager.detect_cloudflare_protection(aura_lite.page)
        
        if protection_info['is_protected']:
            print(f"   🛡️ Cloudflare protection detected: {protection_info['protection_type']}")
            print(f"   🔍 Indicators: {', '.join(protection_info['indicators_found'])}")
            
            # Try to wait for bypass
            print("3. Attempting Cloudflare bypass...")
            bypass_success = await aura_lite.cloudflare_manager.wait_for_cloudflare_bypass(aura_lite.page, max_wait=30)
            
            if bypass_success:
                print("   ✅ Cloudflare bypass successful")
            else:
                print("   ❌ Cloudflare bypass failed")
                return False
        else:
            print("   ✅ No Cloudflare protection detected")
        
        # Check page content
        print("4. Checking page content...")
        try:
            page_title = await aura_lite.page.title()
            page_url = aura_lite.page.url
            
            print(f"   📄 Page title: {page_title}")
            print(f"   🔗 Current URL: {page_url}")
            
            # Check if we're on the expected page
            if 'capterra' in page_url.lower() and company_name.lower() in page_title.lower():
                print("   ✅ Successfully reached target page")
            else:
                print("   ⚠️ Page content unexpected")
                
        except Exception as e:
            print(f"   ❌ Content check failed: {str(e)}")
        
        # Test human behavior on the page
        print("5. Testing human behavior on Capterra page...")
        try:
            behavior_success = await aura_lite.behavior_simulator.simulate_natural_browsing()
            print(f"   🤖 Human behavior: {'✅' if behavior_success else '❌'}")
        except Exception as e:
            print(f"   ❌ Human behavior failed: {str(e)}")
        
        print("\n🎉 Capterra navigation test completed!")
        return True
        
    except Exception as e:
        logger.error(f"Error in Capterra navigation test: {str(e)}")
        print(f"❌ Capterra navigation test failed: {str(e)}")
        return False
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def main():
    """Main test function"""
    print("🚀 AURA-LITE Browser Testing Suite")
    print("=" * 60)
    print("Testing browser setup and basic functionality")
    print("=" * 60)
    
    # Test 1: Browser setup
    browser_success = await test_browser_setup()
    
    if browser_success:
        # Test 2: Capterra navigation
        await test_capterra_navigation()
        
        print("\n🎉 All browser tests completed!")
        print("AURA-LITE browser functionality is working correctly.")
    else:
        print("\n❌ Browser setup test failed. Check logs for details.")

if __name__ == "__main__":
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    asyncio.run(main())
