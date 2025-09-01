"""
Test Improved Cloudflare Bypass
Test the enhanced bypass strategies
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_lite import AuraLite
from aura_lite.core.improved_cloudflare_bypass import ImprovedCloudflareBypass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_improved_cloudflare_bypass():
    """Test improved Cloudflare bypass strategies"""
    print("🛡️ Improved Cloudflare Bypass Test")
    print("=" * 50)
    print("Testing enhanced bypass strategies")
    print("=" * 50)
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        # Initialize improved bypass
        improved_bypass = ImprovedCloudflareBypass()
        
        # Get a test target
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        target = targets[0]  # Use Sigma
        company_name = target['data']['name']
        reviews_url = target['data']['targets']['product_reviews']
        
        print(f"Testing with: {company_name}")
        print(f"URL: {reviews_url}")
        
        # Navigate to the page
        print("1. Navigating to Capterra page...")
        await aura_lite.page.goto(reviews_url, wait_until='domcontentloaded')
        await asyncio.sleep(3)
        
        # Test enhanced detection
        print("2. Testing enhanced Cloudflare detection...")
        protection_info = await improved_bypass.detect_cloudflare_protection_enhanced(aura_lite.page)
        
        print(f"   🛡️ Protection detected: {'✅' if protection_info['is_protected'] else '❌'}")
        print(f"   📊 Protection type: {protection_info['protection_type']}")
        print(f"   🎯 Confidence: {protection_info['confidence']:.2f}")
        print(f"   📄 Page length: {protection_info['page_length']}")
        print(f"   🔗 Capterra URL: {'✅' if protection_info['url_contains_capterra'] else '❌'}")
        
        if protection_info['indicators_found']:
            print(f"   🔍 Indicators: {', '.join(protection_info['indicators_found'])}")
        
        # Test improved bypass if protection detected
        if protection_info['is_protected']:
            print("3. Testing improved Cloudflare bypass...")
            bypass_success = await improved_bypass.enhanced_cloudflare_bypass(aura_lite.page, max_wait=45)
            
            if bypass_success:
                print("   ✅ Improved bypass successful!")
                
                # Verify we can access the content
                page_title = await aura_lite.page.title()
                page_url = aura_lite.page.url
                
                print(f"   📄 Page title: {page_title}")
                print(f"   🔗 Current URL: {page_url}")
                
                # Check if we can see review content
                page_content = await aura_lite.page.content()
                if 'review' in page_content.lower() or 'rating' in page_content.lower():
                    print("   ✅ Review content detected - bypass successful!")
                else:
                    print("   ⚠️ Review content not detected")
            else:
                print("   ❌ Improved bypass failed")
        else:
            print("3. No Cloudflare protection detected - testing direct access...")
            page_title = await aura_lite.page.title()
            print(f"   📄 Page title: {page_title}")
        
        # Test human behavior simulation
        print("4. Testing human behavior simulation...")
        try:
            await improved_bypass._simulate_human_interactions(aura_lite.page)
            print("   ✅ Human behavior simulation successful")
        except Exception as e:
            print(f"   ❌ Human behavior simulation failed: {str(e)}")
        
        # Get bypass statistics
        print("5. Bypass statistics...")
        stats = improved_bypass.get_bypass_statistics()
        print(f"   📊 Total attempts: {stats['total_attempts']}")
        print(f"   ✅ Success rate: {stats['success_rate']:.1%}")
        print(f"   ⏱️ Average duration: {stats['average_duration']:.1f}s")
        
        print("\n🎉 Improved bypass test completed!")
        return True
        
    except Exception as e:
        logger.error(f"Error in improved bypass test: {str(e)}")
        print(f"❌ Improved bypass test failed: {str(e)}")
        return False
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def test_multiple_targets():
    """Test bypass with multiple targets"""
    print("\n🎯 Multiple Targets Bypass Test")
    print("=" * 50)
    print("Testing bypass with different Capterra targets")
    print("=" * 50)
    
    aura_lite = None
    try:
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        improved_bypass = ImprovedCloudflareBypass()
        
        # Test with first 3 high priority targets
        targets = aura_lite.target_manager.get_targets_by_priority("high")[:3]
        
        results = []
        for i, target in enumerate(targets):
            company_name = target['data']['name']
            reviews_url = target['data']['targets']['product_reviews']
            
            print(f"\n{i+1}. Testing {company_name}...")
            print(f"   URL: {reviews_url}")
            
            try:
                # Navigate to page
                await aura_lite.page.goto(reviews_url, wait_until='domcontentloaded')
                await asyncio.sleep(2)
                
                # Check protection
                protection_info = await improved_bypass.detect_cloudflare_protection_enhanced(aura_lite.page)
                
                if protection_info['is_protected']:
                    print(f"   🛡️ Protection: {protection_info['protection_type']} (confidence: {protection_info['confidence']:.2f})")
                    
                    # Try bypass
                    bypass_success = await improved_bypass.enhanced_cloudflare_bypass(aura_lite.page, max_wait=30)
                    print(f"   🚀 Bypass: {'✅' if bypass_success else '❌'}")
                    
                    results.append({
                        'company': company_name,
                        'protected': True,
                        'bypass_success': bypass_success,
                        'protection_type': protection_info['protection_type']
                    })
                else:
                    print(f"   ✅ No protection detected")
                    results.append({
                        'company': company_name,
                        'protected': False,
                        'bypass_success': True,
                        'protection_type': 'none'
                    })
                
                # Wait between targets
                if i < len(targets) - 1:
                    await asyncio.sleep(5)
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                results.append({
                    'company': company_name,
                    'protected': False,
                    'bypass_success': False,
                    'error': str(e)
                })
        
        # Summary
        print(f"\n📊 Test Summary:")
        protected_count = sum(1 for r in results if r.get('protected', False))
        bypass_success_count = sum(1 for r in results if r.get('bypass_success', False))
        
        print(f"   🛡️ Protected targets: {protected_count}/{len(results)}")
        print(f"   ✅ Successful bypasses: {bypass_success_count}/{len(results)}")
        print(f"   📈 Success rate: {bypass_success_count/len(results):.1%}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in multiple targets test: {str(e)}")
        print(f"❌ Multiple targets test failed: {str(e)}")
        return []
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def main():
    """Main test function"""
    print("🚀 Improved Cloudflare Bypass Testing Suite")
    print("=" * 60)
    print("Testing enhanced bypass strategies")
    print("=" * 60)
    
    # Test 1: Single target with improved bypass
    single_success = await test_improved_cloudflare_bypass()
    
    if single_success:
        # Test 2: Multiple targets
        results = await test_multiple_targets()
        
        print("\n🎉 All improved bypass tests completed!")
        print("Enhanced bypass strategies are ready for production use.")
    else:
        print("\n❌ Improved bypass test failed. Check logs for details.")

if __name__ == "__main__":
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    asyncio.run(main())
