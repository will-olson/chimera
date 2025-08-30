#!/usr/bin/env python3
"""Minimal test to isolate parser functionality."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_import():
    """Test basic import without complex type hints."""
    print("🧪 Testing basic import...")
    try:
        # Test basic imports
        from chimera.parsers.head_to_head_comparison import G2HeadToHeadComparisonParser
        print("   ✅ Basic import successful")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_parser_creation():
    """Test parser creation."""
    print("\n🧪 Testing parser creation...")
    try:
        from chimera.parsers.head_to_head_comparison import G2HeadToHeadComparisonParser
        parser = G2HeadToHeadComparisonParser()
        print("   ✅ Parser created successfully")
        print(f"   - Type: {type(parser).__name__}")
        return True
    except Exception as e:
        print(f"   ❌ Parser creation failed: {e}")
        return False

def test_data_models():
    """Test data model imports."""
    print("\n🧪 Testing data models...")
    try:
        from chimera.parsers.head_to_head_comparison import (
            HeadToHeadComparisonData, 
            ProductComparison, 
            AIGeneratedSummary, 
            SummaryPoint
        )
        print("   ✅ Data models imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ Data model import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Minimal Parser Test")
    print("=" * 50)
    
    tests = [
        ("Basic Import", test_basic_import),
        ("Parser Creation", test_parser_creation),
        ("Data Models", test_data_models)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"   ✅ {test_name}: PASS")
            else:
                print(f"   ❌ {test_name}: FAIL")
        except Exception as e:
            print(f"   💥 {test_name}: CRASH - {e}")
    
    print("\n" + "=" * 50)
    print("Minimal test completed.")
