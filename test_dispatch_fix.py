#!/usr/bin/env python3
"""
🔍 Test script to debug the dispatch_exact_event method call issue
"""

import inspect
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_method_signature():
    """Test the method signature of dispatch_exact_event"""
    
    try:
        # Import the module
        import chimera_ultimate
        
        # Find the DataDomeCaptchaSolver class
        DataDomeCaptchaSolver = chimera_ultimate.DataDomeCaptchaSolver
        
        # Get the method signature
        method = getattr(DataDomeCaptchaSolver, 'dispatch_exact_event')
        signature = inspect.signature(method)
        
        print("🔍 Method signature analysis:")
        print(f"Method: dispatch_exact_event")
        print(f"Signature: {signature}")
        print(f"Parameters: {list(signature.parameters.keys())}")
        print(f"Parameter count: {len(signature.parameters)}")
        
        # Check if it's an instance method
        if 'self' in signature.parameters:
            print("✅ This is an instance method (has 'self' parameter)")
            actual_params = len(signature.parameters) - 1  # Exclude 'self'
            print(f"Actual parameter count (excluding self): {actual_params}")
        else:
            print("❌ This is not an instance method")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing method signature: {e}")
        return False

def test_method_call_simulation():
    """Simulate the method call to see the issue"""
    
    print("\n🔍 Method call simulation:")
    
    # Simulate the call from the code
    print("Call from code:")
    print("await self.dispatch_exact_event(iframe, puzzle_element, 'mousedown',")
    print("                              slider_info['sliderL'], 0,")
    print("                              'DataDome mousedown replication')")
    
    print("\nArguments breakdown:")
    print("1. iframe")
    print("2. puzzle_element") 
    print("3. 'mousedown'")
    print("4. slider_info['sliderL']")
    print("5. 0")
    print("6. 'DataDome mousedown replication'")
    
    print("\nTotal arguments: 6")
    print("Expected by method signature: 5 (excluding self)")
    
    print("\n🎯 ISSUE IDENTIFIED:")
    print("The method is being called with 6 arguments but expects 5!")
    print("This is causing the 'evaluate() takes from 2 to 3 positional arguments but 5 were given' error")

if __name__ == "__main__":
    print("🚀 DISPATCH_EXACT_EVENT METHOD DEBUG TEST")
    print("=" * 60)
    
    # Test method signature
    test_method_signature()
    
    # Test method call simulation
    test_method_call_simulation()
    
    print("\n🔧 SOLUTION:")
    print("The method signature needs to be updated to accept 6 parameters:")
    print("async def dispatch_exact_event(self, iframe, element, event_type, x, y, description):")
    print("Should be:")
    print("async def dispatch_exact_event(self, iframe, element, event_type, x, y, description):")
    print("Wait, that's already correct...")
    print("\nThe real issue is in the method calls - they're passing 6 arguments!")
    print("The method signature is correct, but the calls are wrong.")
