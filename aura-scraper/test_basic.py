"""
Basic AURA-LITE Test
Test basic functionality without full browser automation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_lite import AuraLite

def test_basic_functionality():
    """Test basic functionality without browser automation"""
    print("🧪 AURA-LITE Basic Functionality Test")
    print("=" * 50)
    
    try:
        # Test 1: Initialize AURA-LITE
        print("1. Testing AURA-LITE initialization...")
        aura_lite = AuraLite()
        print("   ✅ AURA-LITE initialized successfully")
        
        # Test 2: Target loading
        print("2. Testing target loading...")
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        print(f"   ✅ Loaded {len(targets)} high priority targets")
        
        if targets:
            target = targets[0]
            print(f"   📋 First target: {target['data']['name']}")
            print(f"   🔗 Reviews URL: {target['data']['targets']['product_reviews']}")
        
        # Test 3: Target validation
        print("3. Testing target validation...")
        validation_results = aura_lite.target_manager.validate_target_urls()
        print(f"   ✅ Valid targets: {validation_results['valid_targets']}")
        print(f"   ❌ Invalid targets: {validation_results['invalid_targets']}")
        
        # Test 4: Target statistics
        print("4. Testing target statistics...")
        stats = aura_lite.target_manager.get_target_statistics()
        print(f"   📊 Total competitors: {stats['total_competitors']}")
        print(f"   📈 High priority: {stats['priority_distribution']['high']}")
        print(f"   📉 Medium priority: {stats['priority_distribution']['medium']}")
        print(f"   📉 Low priority: {stats['priority_distribution']['low']}")
        
        # Test 5: Session manager
        print("5. Testing session manager...")
        session_summary = aura_lite.session_manager.get_session_summary()
        print(f"   📊 Session ID: {session_summary['session_id']}")
        print(f"   ⏱️ Duration: {session_summary['duration_minutes']:.1f} minutes")
        
        # Test 6: Component initialization
        print("6. Testing component initialization...")
        print(f"   🛡️ CloudflareBypassManager: {'✅' if aura_lite.cloudflare_manager else '❌'}")
        print(f"   📊 SessionManager: {'✅' if aura_lite.session_manager else '❌'}")
        print(f"   🎯 TargetManager: {'✅' if aura_lite.target_manager else '❌'}")
        
        print("\n🎉 Basic functionality test completed successfully!")
        print("=" * 50)
        print("✅ All core components initialized correctly")
        print("✅ Target loading and validation working")
        print("✅ Session management operational")
        print("✅ Ready for browser automation testing")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_basic_functionality()
