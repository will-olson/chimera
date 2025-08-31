#!/usr/bin/env python3
"""
Simple test to check available methods in ChimeraUltimateTestingHarness
"""

import sys
import importlib.util

# Load the chimera-ultimate module
spec = importlib.util.spec_from_file_location("chimera_ultimate", "chimera-ultimate.py")
chimera_ultimate = importlib.util.module_from_spec(spec)
sys.modules["chimera_ultimate"] = chimera_ultimate
spec.loader.exec_module(chimera_ultimate)

# Load the testing harness
spec = importlib.util.spec_from_file_location("testing_harness", "chimera_ultimate_testing_harness.py")
testing_harness = importlib.util.module_from_spec(spec)
sys.modules["testing_harness"] = testing_harness
spec.loader.exec_module(testing_harness)

# Check available methods
harness = testing_harness.ChimeraUltimateTestingHarness()

print("Available methods in ChimeraUltimateTestingHarness:")
methods = [method for method in dir(harness) if not method.startswith('_')]
for method in methods:
    print(f"  - {method}")

print("\nChecking for rapid_improvement_drive:")
if hasattr(harness, 'rapid_improvement_drive'):
    print("  ✅ rapid_improvement_drive method found")
else:
    print("  ❌ rapid_improvement_drive method NOT found")

print("\nChecking for cleanup:")
if hasattr(harness, 'cleanup'):
    print("  ✅ cleanup method found")
else:
    print("  ❌ cleanup method NOT found")
