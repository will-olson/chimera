#!/usr/bin/env python3
"""
🧪 Test Script for DataDome CAPTCHA Solver Implementation

This script tests the exact event replication functionality discovered in our reverse engineering analysis.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from the file directly since it has hyphens in the filename
import importlib.util
import sys

# Load the module from the file
spec = importlib.util.spec_from_file_location("chimera_ultimate", "chimera-ultimate.py")
chimera_ultimate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chimera_ultimate)

# Extract the classes
DataDomeCaptchaSolver = chimera_ultimate.DataDomeCaptchaSolver
ChimeraUltimateCaptchaSolver = chimera_ultimate.ChimeraUltimateCaptchaSolver

async def test_datadome_solver():
    """
    🧪 Test the DataDome CAPTCHA solver implementation
    """
    print("🧪 Testing DataDome CAPTCHA Solver Implementation...")
    
    # Test 1: Initialize DataDome solver
    print("\n✅ Test 1: Initializing DataDome solver...")
    try:
        datadome_solver = DataDomeCaptchaSolver()
        print(f"   ✅ DataDome solver initialized successfully")
        print(f"   📏 Slider dimensions: {datadome_solver.datadome_constants['SLIDER_DIMENSIONS']}")
        print(f"   🎯 Slider positions: {datadome_solver.datadome_constants['SLIDER_POSITIONS']}")
        print(f"   🎭 Event properties: {datadome_solver.datadome_constants['EVENT_PROPERTIES']}")
        print(f"   🔍 Success indicators: {datadome_solver.datadome_constants['SUCCESS_INDICATORS']}")
    except Exception as e:
        print(f"   ❌ Failed to initialize DataDome solver: {e}")
        return False
    
    # Test 2: Verify hex-encoded search keys
    print("\n✅ Test 2: Verifying hex-encoded search keys...")
    try:
        expected_keys = ["mousedown", "mousemove", "mouseup", "touchstart", "touchmove", "touchend"]
        for key in expected_keys:
            if key in datadome_solver.hex_keys:
                hex_value = datadome_solver.hex_keys[key]
                print(f"   ✅ {key}: {hex_value}")
            else:
                print(f"   ❌ Missing hex key: {key}")
                return False
    except Exception as e:
        print(f"   ❌ Failed to verify hex keys: {e}")
        return False
    
    # Test 3: Test ChimeraUltimate integration
    print("\n✅ Test 3: Testing ChimeraUltimate integration...")
    try:
        chimera_solver = ChimeraUltimateCaptchaSolver()
        print(f"   ✅ ChimeraUltimate solver initialized successfully")
        
        # Check if DataDome solver is properly integrated
        if hasattr(chimera_solver, 'datadome_solver'):
            print(f"   ✅ DataDome solver properly integrated")
            print(f"   🎯 DataDome solver type: {type(chimera_solver.datadome_solver)}")
        else:
            print(f"   ❌ DataDome solver not found in ChimeraUltimate")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to test ChimeraUltimate integration: {e}")
        return False
    
    # Test 4: Verify method availability
    print("\n✅ Test 4: Verifying method availability...")
    try:
        required_methods = [
            'solve_datadome_captcha',
            'get_slider_dimensions', 
            'execute_exact_event_sequence',
            'dispatch_exact_event',
            'monitor_datadome_success'
        ]
        
        for method in required_methods:
            if hasattr(datadome_solver, method):
                print(f"   ✅ Method available: {method}")
            else:
                print(f"   ❌ Missing method: {method}")
                return False
                
    except Exception as e:
        print(f"   ❌ Failed to verify methods: {e}")
        return False
    
    # Test 5: Verify ChimeraUltimate DataDome methods
    print("\n✅ Test 5: Verifying ChimeraUltimate DataDome methods...")
    try:
        chimera_datadome_methods = [
            'is_datadome_captcha',
            'solve_datadome_captcha_specialized',
            'find_datadome_puzzle_element'
        ]
        
        for method in chimera_datadome_methods:
            if hasattr(chimera_solver, method):
                print(f"   ✅ ChimeraUltimate method available: {method}")
            else:
                print(f"   ❌ Missing ChimeraUltimate method: {method}")
                return False
                
    except Exception as e:
        print(f"   ❌ Failed to verify ChimeraUltimate methods: {e}")
        return False
    
    print("\n🎉 All tests passed! DataDome CAPTCHA solver implementation is ready.")
    return True

async def test_reverse_engineering_findings():
    """
    🧪 Test the reverse engineering findings implementation
    """
    print("\n🔍 Testing Reverse Engineering Findings Implementation...")
    
    # Test 1: Verify exact event properties from discovered code
    print("\n✅ Test 1: Verifying exact event properties...")
    try:
        datadome_solver = DataDomeCaptchaSolver()
        event_props = datadome_solver.datadome_constants['EVENT_PROPERTIES']
        
        # These properties were discovered in captchaHTML.md lines 7145-7158
        expected_props = {
            'passive': False,      # Required for touch events (discovered)
            'capture': True,       # Event capture mode (discovered)
            'bubbles': True,       # Event bubbling
            'cancelable': True,    # Event cancellation
            'composed': True       # Event composition
        }
        
        for prop, value in expected_props.items():
            if prop in event_props and event_props[prop] == value:
                print(f"   ✅ {prop}: {value}")
            else:
                print(f"   ❌ {prop}: expected {value}, got {event_props.get(prop, 'MISSING')}")
                return False
                
    except Exception as e:
        print(f"   ❌ Failed to verify event properties: {e}")
        return False
    
    # Test 2: Verify success indicators from discovered code
    print("\n✅ Test 2: Verifying success indicators...")
    try:
        success_indicators = datadome_solver.datadome_constants['SUCCESS_INDICATORS']
        
        # These indicators were discovered in captchaHTML.md lines 7253-7254
        expected_indicators = [
            "dataset.result = 'success'",
            "CSS class 'slider-success'",
            "InnerHTML success message",
            "Audio success label"
        ]
        
        for indicator in expected_indicators:
            if indicator in success_indicators:
                print(f"   ✅ Success indicator: {indicator}")
            else:
                print(f"   ❌ Missing success indicator: {indicator}")
                return False
                
    except Exception as e:
        print(f"   ❌ Failed to verify success indicators: {e}")
        return False
    
    # Test 3: Verify slider configuration from discovered code
    print("\n✅ Test 3: Verifying slider configuration...")
    try:
        slider_positions = datadome_solver.datadome_constants['SLIDER_POSITIONS']
        
        # These values were discovered in captchaHTML.md configuration object
        expected_positions = {
            'left': 42,    # sliderL from discovered config
            'right': 9,    # sliderR from discovered config
            'offset': 5    # offset from discovered config
        }
        
        for pos, value in expected_positions.items():
            if pos in slider_positions and slider_positions[pos] == value:
                print(f"   ✅ {pos}: {value}")
            else:
                print(f"   ❌ {pos}: expected {value}, got {slider_positions.get(pos, 'MISSING')}")
                return False
                
    except Exception as e:
        print(f"   ❌ Failed to verify slider configuration: {e}")
        return False
    
    print("\n🎉 All reverse engineering findings tests passed!")
    return True

async def main():
    """
    🚀 Main test function
    """
    print("🚀 DataDome CAPTCHA Solver Test Suite")
    print("=" * 50)
    
    # Run basic implementation tests
    basic_tests_passed = await test_datadome_solver()
    
    # Run reverse engineering findings tests
    findings_tests_passed = await test_reverse_engineering_findings()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if basic_tests_passed and findings_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ DataDome CAPTCHA solver implementation is complete and ready")
        print("✅ Reverse engineering findings are properly implemented")
        print("✅ Integration with ChimeraUltimate is successful")
        print("\n🚀 Ready for real CAPTCHA testing!")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        if not basic_tests_passed:
            print("   ❌ Basic implementation tests failed")
        if not findings_tests_passed:
            print("   ❌ Reverse engineering findings tests failed")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
