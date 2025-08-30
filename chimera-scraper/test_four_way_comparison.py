#!/usr/bin/env python3
"""Test script for four-way comparison scraping capabilities."""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chimera.core.competitive_intelligence_scraper import CompetitiveIntelligenceScraper
from chimera.core.four_way_comparison_scraper import FourWayComparisonScraper
from chimera.parsers.four_way_comparison import G2FourWayComparisonParser


async def test_four_way_parser():
    """Test the four-way comparison parser with sample HTML."""
    print("🧪 Testing Four-Way Comparison Parser...")
    
    # Sample HTML structure based on the screenshots
    sample_html = """
    <html>
    <head><title>Microsoft Power BI vs Qlik Sense vs Tableau vs Domo</title></head>
    <body>
        <div data-eventscope="Comparison Table" id="comparison-table">
            <div class="comparison-container-v2">
                <div class="comparison-container-v2_header">
                    <div aria-label="Microsoft Power BI star rating is 4.4 out of 5">
                        <span class="star-wrapper_icon stars stars-9">4.4</span>
                        <a href="/products/power-bi/reviews" aria-label="Microsoft Power BI reviews 1,391">(1,391)</a>
                    </div>
                </div>
                <div class="comparison-container-v2_header">
                    <div aria-label="Qlik Sense star rating is 4.3 out of 5">
                        <span class="star-wrapper_icon stars stars-8">4.3</span>
                        <a href="/products/qlik-sense/reviews" aria-label="Qlik Sense reviews 1,234">(1,234)</a>
                    </div>
                </div>
                <div class="comparison-container-v2_header">
                    <div aria-label="Tableau star rating is 4.4 out of 5">
                        <span class="star-wrapper_icon stars stars-9">4.4</span>
                        <a href="/products/tableau/reviews" aria-label="Tableau reviews 2,818">(2,818)</a>
                    </div>
                </div>
                <div class="comparison-container-v2_header">
                    <div aria-label="Domo star rating is 4.2 out of 5">
                        <span class="star-wrapper_icon stars stars-8">4.2</span>
                        <a href="/products/domo/reviews" aria-label="Domo reviews 987">(987)</a>
                    </div>
                </div>
            </div>
            
            <div class="comparison-container-v2_block" aria-label="Ratings Table" id="ratings">
                <div aria-label="Microsoft Power BI, Meets Requirements 8.9 out of 10, based on 1105 reviews">
                    <div class="minimal-donut" style="background: conic-gradient(#4CAF50 0deg 320deg, #E0E0E0 320deg 360deg);">
                        <div class="center-center fw-semibold text-normal-medium">8.9</div>
                    </div>
                </div>
                <div aria-label="Qlik Sense, Meets Requirements 8.5 out of 10, based on 987 reviews">
                    <div class="minimal-donut" style="background: conic-gradient(#4CAF50 0deg 306deg, #E0E0E0 306deg 360deg);">
                        <div class="center-center fw-semibold text-normal-medium">8.5</div>
                    </div>
                </div>
                <div aria-label="Tableau, Meets Requirements 8.7 out of 10, based on 2247 reviews">
                    <div class="minimal-donut" style="background: conic-gradient(#4CAF50 0deg 313deg, #E0E0E0 313deg 360deg);">
                        <div class="center-center fw-semibold text-normal-medium">8.7</div>
                    </div>
                </div>
                <div aria-label="Domo, Meets Requirements 8.4 out of 10, based on 770 reviews">
                    <div class="minimal-donut" style="background: conic-gradient(#4CAF50 0deg 302deg, #E0E0E0 302deg 360deg);">
                        <div class="center-center fw-semibold text-normal-medium">8.4</div>
                    </div>
                </div>
            </div>
            
            <div class="comparison-container-v2_block" aria-label="Features by Category">
                <div aria-label="Business Intelligence Rating">
                    <div>Business Intelligence</div>
                    <div>8.7</div>
                    <div>8.3</div>
                    <div>8.5</div>
                    <div>8.0</div>
                </div>
                <div aria-label="Analytics Platforms Rating">
                    <div>Analytics Platforms</div>
                    <div>8.3</div>
                    <div>8.5</div>
                    <div>8.0</div>
                    <div>7.6</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        parser = G2FourWayComparisonParser()
        comparison_data = await parser.parse_four_way_comparison(
            sample_html, 
            "https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense-vs-tableau-vs-domo"
        )
        
        print(f"✅ Parser test successful!")
        print(f"   - Products extracted: {len(comparison_data.products)}")
        print(f"   - Data quality score: {comparison_data.data_quality_score}")
        print(f"   - Extraction confidence: {comparison_data.extraction_confidence}")
        
        # Print product details
        for product in comparison_data.products:
            print(f"   - {product['name']}: {product['star_rating']} stars, {product['review_count']} reviews")
        
        return comparison_data
        
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
        return None


async def test_four_way_scraper():
    """Test the four-way comparison scraper."""
    print("\n🧪 Testing Four-Way Comparison Scraper...")
    
    try:
        # Initialize competitive intelligence scraper
        competitive_scraper = CompetitiveIntelligenceScraper()
        
        # Initialize four-way comparison scraper
        four_way_scraper = FourWayComparisonScraper(competitive_scraper)
        
        print(f"✅ Four-way comparison scraper initialized successfully!")
        print(f"   - Parser capabilities: {four_way_scraper.parser.get_extraction_statistics()}")
        
        return four_way_scraper
        
    except Exception as e:
        print(f"❌ Four-way comparison scraper test failed: {e}")
        return None


async def test_competitive_intelligence_integration():
    """Test the integration of four-way comparison scraping into competitive intelligence."""
    print("\n🧪 Testing Competitive Intelligence Integration...")
    
    try:
        # Initialize competitive intelligence scraper
        scraper = CompetitiveIntelligenceScraper()
        
        print(f"✅ Competitive intelligence scraper initialized successfully!")
        
        # Test target loading
        targets = scraper.competitive_targets
        print(f"   - Loaded {len(targets)} competitive targets")
        
        # Count four-way comparison URLs
        four_way_count = 0
        for target in targets:
            if "four_way" in target.targets:
                four_way_count += len(target.targets["four_way"])
        
        print(f"   - Found {four_way_count} four-way comparison URLs")
        
        # Show sample four-way URLs
        print("\n   Sample four-way comparison URLs:")
        for target in targets[:3]:  # Show first 3 targets
            if "four_way" in target.targets:
                for url in target.targets["four_way"][:1]:  # Show first URL per target
                    print(f"     - {target.name}: {url}")
        
        return scraper
        
    except Exception as e:
        print(f"❌ Competitive intelligence integration test failed: {e}")
        return None


async def test_data_export():
    """Test data export capabilities."""
    print("\n🧪 Testing Data Export Capabilities...")
    
    try:
        # Create sample four-way comparison data
        from chimera.parsers.four_way_comparison import FourWayComparisonData, ProductComparison
        
        sample_products = [
            ProductComparison(
                name="Microsoft Power BI",
                g2_product_id="power-bi",
                vendor_id="microsoft",
                star_rating=4.4,
                review_count=1391,
                market_segments={"enterprise": 42.8},
                entry_level_pricing="Free",
                pricing_details={},
                ratings_by_criteria={},
                feature_scores={}
            ),
            ProductComparison(
                name="Tableau",
                g2_product_id="tableau",
                vendor_id="salesforce",
                star_rating=4.4,
                review_count=2818,
                market_segments={"enterprise": 45.2},
                entry_level_pricing="$70.00",
                pricing_details={},
                ratings_by_criteria={},
                feature_scores={}
            )
        ]
        
        sample_comparison = FourWayComparisonData(
            comparison_id="test_comparison",
            extraction_date=datetime.now(),
            url="https://example.com/test",
            products=[asdict(p) for p in sample_products],
            at_a_glance={
                "star_ratings": {
                    "Microsoft Power BI": {"rating": 4.4, "review_count": 1391},
                    "Tableau": {"rating": 4.4, "review_count": 2818}
                }
            },
            pricing={},
            ratings={},
            features_by_category={},
            total_products=2,
            comparison_categories=["At a Glance", "Ratings"],
            data_quality_score=85.0,
            extraction_confidence=90.0
        )
        
        # Test export
        from chimera.core.four_way_comparison_scraper import FourWayComparisonScraper
        
        # Create a mock scraper for export testing
        class MockCompetitiveScraper:
            pass
        
        mock_scraper = MockCompetitiveScraper()
        four_way_scraper = FourWayComparisonScraper(mock_scraper)
        
        # Create sample insights
        from chimera.core.competitive_intelligence_scraper import CompetitiveInsight
        
        sample_insights = [
            CompetitiveInsight(
                competitor_id="test_competitor",
                platform="g2",
                extraction_date=datetime.now(),
                data_type="four_way_comparison",
                url="https://example.com/test",
                content=asdict(sample_comparison),
                sentiment_analysis={"score": 0.0, "label": "neutral"},
                competitive_mentions=["Microsoft Power BI", "Tableau"],
                market_insights={},
                quality_score=0.85,
                extraction_confidence=0.90
            )
        ]
        
        # Test export
        export_files = await four_way_scraper.export_four_way_data(sample_insights, "test_output")
        
        print(f"✅ Data export test successful!")
        print(f"   - Exported files: {list(export_files.keys())}")
        
        # Clean up test files
        import shutil
        if Path("test_output").exists():
            shutil.rmtree("test_output")
        
        return True
        
    except Exception as e:
        print(f"❌ Data export test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Starting Four-Way Comparison Scraping Tests...")
    print("=" * 60)
    
    # Test 1: Parser
    parser_result = await test_four_way_parser()
    
    # Test 2: Scraper
    scraper_result = await test_four_way_scraper()
    
    # Test 3: Integration
    integration_result = await test_competitive_intelligence_integration()
    
    # Test 4: Data Export
    export_result = await test_data_export()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   - Parser Test: {'✅ PASSED' if parser_result else '❌ FAILED'}")
    print(f"   - Scraper Test: {'✅ PASSED' if scraper_result else '❌ FAILED'}")
    print(f"   - Integration Test: {'✅ PASSED' if integration_result else '❌ FAILED'}")
    print(f"   - Export Test: {'✅ PASSED' if export_result else '❌ FAILED'}")
    
    if all([parser_result, scraper_result, integration_result, export_result]):
        print("\n🎉 All tests passed! Four-way comparison scraping is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n🔍 Next Steps:")
    print("   1. Run the competitive intelligence scraper to test real four-way comparisons")
    print("   2. Monitor the scraping process for any issues")
    print("   3. Review the exported data for quality and completeness")
    print("   4. Adjust selectors and parsing logic if needed")


if __name__ == "__main__":
    # Import datetime for the export test
    from datetime import datetime
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
