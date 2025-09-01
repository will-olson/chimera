#!/usr/bin/env python3
"""
🔍 Debug script to test iframe.evaluate method
"""

async def test_evaluate_method():
    """Test the iframe.evaluate method to understand the issue"""
    
    print("🔍 Testing iframe.evaluate method...")
    
    # Simulate the exact call that's failing
    print("\n🎯 Simulating the failing call:")
    print("await iframe.evaluate(f'''")
    print("    (elementSelector, eventType, propsJson) => {{")
    print("        // ... JavaScript code ...")
    print("    }}")
    print("''', '#ddv1-captcha-container', 'mousedown', '{\"clientX\": 42, \"clientY\": 0}')")
    
    print("\n📊 Arguments breakdown:")
    print("1. JavaScript code (f-string)")
    print("2. '#ddv1-captcha-container' (elementSelector)")
    print("3. 'mousedown' (eventType)")
    print("4. '{\"clientX\": 42, \"clientY\": 0}' (propsJson)")
    
    print("\n🎯 Total arguments: 4")
    print("Expected by iframe.evaluate: 2-3")
    
    print("\n🔧 POSSIBLE ISSUES:")
    print("1. The f-string is being expanded into multiple arguments")
    print("2. The iframe object is not a Playwright Frame")
    print("3. There's a method signature mismatch")
    
    print("\n💡 SOLUTION APPROACH:")
    print("Use a regular string instead of f-string to avoid expansion")
    print("Or use iframe.evaluate_handle() for complex operations")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_evaluate_method())
