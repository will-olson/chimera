#!/usr/bin/env python3
"""Simple test for Python 3.8 compatible parser."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_parser_import():
    """Test basic parser import."""
    print("🧪 Testing parser import...")
    try:
        from chimera.parsers.head_to_head_comparison_simple import G2HeadToHeadComparisonParser
        print("   ✅ Parser imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_parser_creation():
    """Test parser creation."""
    print("\n🧪 Testing parser creation...")
    try:
        from chimera.parsers.head_to_head_comparison_simple import G2HeadToHeadComparisonParser
        parser = G2HeadToHeadComparisonParser()
        print("   ✅ Parser created successfully")
        print(f"   - Type: {type(parser).__name__}")
        print(f"   - Known sections: {len(parser.known_sections)}")
        print(f"   - Feature categories: {len(parser.feature_categories)}")
        return True
    except Exception as e:
        print(f"   ❌ Parser creation failed: {e}")
        return False

def test_data_models():
    """Test data model imports."""
    print("\n🧪 Testing data models...")
    try:
        from chimera.parsers.head_to_head_comparison_simple import (
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

def test_basic_parsing():
    """Test basic HTML parsing."""
    print("\n🧪 Testing basic HTML parsing...")
    try:
        from chimera.parsers.head_to_head_comparison_simple import G2HeadToHeadComparisonParser
        
        # Minimal test HTML
        test_html = """
        <html>
        <body>
            <div class="comparison-container-v2_header">Microsoft Power BI</div>
            <div class="comparison-container-v2_header">Tableau</div>
            <div aria-label="Comparison Summary" class="compare-container-v2_summary">
                <div>AI Generated Summary</div>
                <ul>
                    <li>Microsoft Power BI excels in data visualization, scoring 9.2 compared to Tableau's 8.7.</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        parser = G2HeadToHeadComparisonParser()
        
        # Test basic parsing
        import asyncio
        result = asyncio.run(parser.parse_head_to_head_comparison(
            test_html, 
            "https://example.com/test"
        ))
        
        print("   ✅ Basic parsing completed successfully")
        print(f"   - Result type: {type(result).__name__}")
        print(f"   - Products extracted: {len([result.product_a, result.product_b])}")
        print(f"   - AI summary quality: {result.summary_quality_score:.1f}")
        return True
        
    except Exception as e:
        print(f"   ❌ Basic parsing failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Parser Test - Python 3.8 Compatible")
    print("=" * 60)
    
    tests = [
        ("Parser Import", test_parser_import),
        ("Parser Creation", test_parser_creation),
        ("Data Models", test_data_models),
        ("Basic Parsing", test_basic_parsing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"   ✅ {test_name}: PASS")
                passed += 1
            else:
                print(f"   ❌ {test_name}: FAIL")
        except Exception as e:
            print(f"   💥 {test_name}: CRASH - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Parser is working correctly!")
        print("   Next: Test with real G2.com data")
    elif passed >= total * 0.75:
        print("\n⚠️  MOST TESTS PASSED - Minor issues to address")
        print("   Next: Fix remaining issues before live testing")
    else:
        print("\n💥 SIGNIFICANT ISSUES - Core functionality needs attention")
        print("   Next: Address fundamental problems")
    
    sys.exit(0 if passed == total else 1)
