
# 🎯 DEBUG CODE TO TEST IFRAME OBJECT

async def debug_iframe_object_type(iframe):
    """Debug the iframe object to understand its type and methods"""
    
    try:
        print(f"🔍 IFRAME OBJECT DEBUG:")
        print(f"Type: {type(iframe)}")
        print(f"Class: {iframe.__class__.__name__}")
        print(f"Module: {iframe.__class__.__module__}")
        
        # Check if it's a Playwright Frame
        if hasattr(iframe, 'evaluate'):
            print("✅ Has evaluate method")
            evaluate_method = getattr(iframe, 'evaluate')
            print(f"Evaluate method type: {type(evaluate_method)}")
            
            # Check method signature
            if hasattr(evaluate_method, '__call__'):
                print("✅ Evaluate method is callable")
                
                # Try to get signature info
                try:
                    sig = inspect.signature(evaluate_method)
                    print(f"Evaluate method signature: {sig}")
                    print(f"Parameters: {list(sig.parameters.keys())}")
                    print(f"Parameter count: {len(sig.parameters)}")
                except Exception as e:
                    print(f"⚠️ Could not get signature: {e}")
            else:
                print("❌ Evaluate method is not callable")
        else:
            print("❌ No evaluate method found")
            
        # Check for alternative methods
        alternative_methods = ['evaluate_handle', 'query_selector', 'query_selector_all']
        for method in alternative_methods:
            if hasattr(iframe, method):
                print(f"✅ Has {method} method")
            else:
                print(f"❌ No {method} method")
                
        return True
        
    except Exception as e:
        print(f"❌ Error debugging iframe object: {e}")
        return False

async def test_alternative_event_dispatching(iframe):
    """Test alternative event dispatching methods"""
    
    try:
        print(f"🔍 TESTING ALTERNATIVE EVENT DISPATCHING:")
        
        # Method 1: Use query_selector + dispatch_event
        print("🎯 Method 1: query_selector + dispatch_event")
        try:
            element = await iframe.query_selector("#ddv1-captcha-container")
            if element:
                print("✅ Element found via query_selector")
                # Try to dispatch event directly
                print("✅ query_selector method works")
            else:
                print("❌ Element not found via query_selector")
        except Exception as e:
            print(f"❌ query_selector failed: {e}")
        
        # Method 2: Use evaluate_handle
        print("🎯 Method 2: evaluate_handle")
        try:
            if hasattr(iframe, 'evaluate_handle'):
                print("✅ evaluate_handle method available")
            else:
                print("❌ evaluate_handle method not available")
        except Exception as e:
            print(f"❌ evaluate_handle check failed: {e}")
            
        # Method 3: Use page.evaluate instead
        print("🎯 Method 3: page.evaluate (if available)")
        try:
            if hasattr(iframe, 'page'):
                page = iframe.page
                print("✅ Page object available")
                if hasattr(page, 'evaluate'):
                    print("✅ page.evaluate method available")
                else:
                    print("❌ page.evaluate method not available")
            else:
                print("❌ Page object not available")
        except Exception as e:
            print(f"❌ page.evaluate check failed: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing alternative methods: {e}")
        return False
