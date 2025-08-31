#!/usr/bin/env python3
"""
Detailed test to check available methods in ChimeraUltimateCaptchaSolver
"""

import sys
import importlib.util

# Load the chimera-ultimate module
spec = importlib.util.spec_from_file_location("chimera_ultimate", "chimera-ultimate.py")
chimera_ultimate = importlib.util.module_from_spec(spec)
sys.modules["chimera_ultimate"] = chimera_ultimate
spec.loader.exec_module(chimera_ultimate)

# Create a CAPTCHA solver instance
captcha_solver = chimera_ultimate.ChimeraUltimateCaptchaSolver()

print("Available methods in ChimeraUltimateCaptchaSolver:")
methods = [method for method in dir(captcha_solver) if not method.startswith('_')]
for method in methods:
    print(f"  - {method}")

print("\nChecking for specific methods:")
specific_methods = [
    'enhanced_puzzle_state',
    'math_engine', 
    'execute_proven_puzzle_movement_enhanced',
    'validate_captcha_success_comprehensive'
]

for method in specific_methods:
    if hasattr(captcha_solver, method):
        print(f"  ✅ {method}: FOUND")
        method_obj = getattr(captcha_solver, method)
        print(f"      Type: {type(method_obj)}")
        if callable(method_obj):
            print(f"      Callable: Yes")
            import inspect
            try:
                sig = inspect.signature(method_obj)
                print(f"      Signature: {sig}")
            except:
                print(f"      Signature: Could not inspect")
        else:
            print(f"      Callable: No")
    else:
        print(f"  ❌ {method}: NOT FOUND")

print("\nChecking for execute_proven_puzzle_movement_enhanced specifically:")
if hasattr(captcha_solver, 'execute_proven_puzzle_movement_enhanced'):
    method = getattr(captcha_solver, 'execute_proven_puzzle_movement_enhanced')
    print(f"  ✅ Method found: {type(method)}")
    print(f"  ✅ Method name: {method.__name__}")
    print(f"  ✅ Method qualname: {method.__qualname__}")
else:
    print("  ❌ Method not found")
