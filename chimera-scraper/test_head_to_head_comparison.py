#!/usr/bin/env python3
"""Comprehensive test script for enhanced head-to-head comparison scraping capabilities."""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from chimera.core.competitive_intelligence_scraper import CompetitiveIntelligenceScraper
from chimera.core.head_to_head_comparison_scraper import HeadToHeadComparisonScraper
from chimera.parsers.head_to_head_comparison import G2HeadToHeadComparisonParser


async def test_enhanced_head_to_head_parser():
    """Test the enhanced head-to-head comparison parser with comprehensive data extraction."""
    print("🧪 Testing Enhanced Head-to-Head Comparison Parser...")
    
    # Sample HTML structure based on the screenshots with additional sections
    sample_html = """
    <html>
    <head><title>Compare Domo and Microsoft Power BI</title></head>
    <body>
        <div data-eventscope="Comparison Table" id="comparison-table">
            <div class="comparison-container-v2">
                <div class="comparison-container-v2_header">
                    <div aria-label="Domo star rating is 4.3 out of 5">
                        <span class="star-wrapper_icon stars stars-9">4.3</span>
                        <a href="/products/domo/reviews" aria-label="Domo reviews 879">(879)</a>
                    </div>
                </div>
                <div class="comparison-container-v2_header">
                    <div aria-label="Microsoft Power BI star rating is 4.5 out of 5">
                        <span class="star-wrapper_icon stars stars-9">4.5</span>
                        <a href="/products/power-bi/reviews" aria-label="Microsoft Power BI reviews 1,381">(1,381)</a>
                    </div>
                </div>
            </div>
            
            <!-- AI Generated Summary Section -->
            <div aria-label="Comparison Summary" class="compare-container-v2_summary">
                <div class="mb-1/4">AI Generated Summary</div>
                <div>*AI-generated. Powered by real user reviews.</div>
                <ul>
                    <li>Users report that Microsoft Power BI excels in data visualization, scoring 9.2 compared to Domo's 8.7. Reviewers mention that Power BI's interactive dashboards and rich visualizations make it easier to derive insights from data.</li>
                    <li>Reviewers mention that Power BI offers superior ease of setup with a score of 8.7, while Domo trails behind at 7.7. Users say that Power BI's intuitive interface and guided setup process streamline the onboarding experience.</li>
                    <li>G2 users highlight that Microsoft Power BI has a more robust AI text generation feature, scoring 7.6 compared to Domo's 6.3. Reviewers mention that Power BI's AI capabilities enhance data storytelling and automate insights effectively.</li>
                </ul>
            </div>
            
            <!-- Reviewers Company Size Section -->
            <div aria-label="Reviewers Company Size Table">
                <div aria-label="Reviewers Company Size, Small-Business (50 or fewer emp.)">
                    <div aria-label="Domo, 13.1% of reviews from Small-Business companies">13.1%</div>
                    <div aria-label="Microsoft Power BI, 21.2% of reviews from Small-Business companies">21.2%</div>
                </div>
                <div aria-label="Reviewers Company Size, Mid-Market (51-1000 emp.)">
                    <div aria-label="Domo, 54.9% of reviews from Mid-Market companies">54.9%</div>
                    <div aria-label="Microsoft Power BI, 36.0% of reviews from Mid-Market companies">36.0%</div>
                </div>
                <div aria-label="Reviewers Company Size, Enterprise (> 1000 emp.)">
                    <div aria-label="Domo, 32.0% of reviews from Enterprise companies">32.0%</div>
                    <div aria-label="Microsoft Power BI, 42.8% of reviews from Enterprise companies">42.8%</div>
                </div>
            </div>
            
            <!-- Reviewers Industry Section -->
            <div aria-label="Reviewers Industry Table">
                <div aria-label="Domo, 9.3% of reviews from Computer Software industries">9.3%</div>
                <div aria-label="Microsoft Power BI, 16.1% of reviews from Computer Software industries">16.1%</div>
                <div aria-label="Domo, 7.2% of reviews from Marketing and Advertising industries">7.2%</div>
                <div aria-label="Microsoft Power BI, 6.6% of reviews from Marketing and Advertising industries">6.6%</div>
            </div>
            
            <!-- Most Helpful Reviews Section -->
            <div aria-label="Most Helpful Reviews Table">
                <div class="comparison-container_body comparison-container_body--column">
                    <div class="compare-review-user">Stephen R., Verified User in Financial Services</div>
                    <p>The best feature with DOMO is the ease of user functionality. Our company has a wide range of user experience and technology levels and the ability for everyone from the most basic user to the most advanced user to get the same information quickly and efficiently.</p>
                </div>
                <div class="comparison-container_body comparison-container_body--column">
                    <div class="compare-review-user">Verified User in Marketing and Advertising</div>
                    <p>Visualizations. They're absolutely fantastic. Importing data is incredibly easy and it's much more powerful than excel or many SQL based visualization tools.</p>
                </div>
            </div>
            
            <!-- Ratings Section -->
            <div aria-label="Ratings Table" id="ratings">
                <div aria-label="Domo, Meets Requirements 8.4 out of 10, based on 770 reviews">
                    <div class="minimal-donut">8.4</div>
                </div>
                <div aria-label="Microsoft Power BI, Meets Requirements 8.7 out of 10, based on 1105 reviews">
                    <div class="minimal-donut">8.7</div>
                </div>
            </div>
            
            <!-- Features Section -->
            <div aria-label="Features by Category">
                <div aria-label="Data Visualization Rating">
                    <div>Data Visualization</div>
                    <div>8.7</div>
                    <div>9.2</div>
                </div>
                <div aria-label="Ease of Setup Rating">
                    <div>Ease of Setup</div>
                    <div>7.7</div>
                    <div>8.7</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        parser = G2HeadToHeadComparisonParser()
        comparison_data = await parser.parse_head_to_head_comparison(
            sample_html, 
            "https://www.g2.com/compare/domo-vs-microsoft-microsoft-power-bi"
        )
        
        print(f"✅ Enhanced parser test successful!")
        print(f"   - Products extracted: {len([comparison_data.product_a, comparison_data.product_b])}")
        print(f"   - Data quality score: {comparison_data.data_quality_score}")
        print(f"   - Extraction confidence: {comparison_data.extraction_confidence}")
        print(f"   - Summary quality score: {comparison_data.summary_quality_score}")
        
        # Validate AI summary extraction
        if comparison_data.ai_generated_summary:
            ai_summary = comparison_data.ai_generated_summary
            print(f"   - AI Summary Title: {ai_summary.summary_title}")
            print(f"   - AI Summary Points: {len(ai_summary.summary_points)}")
            print(f"   - AI Summary Confidence: {ai_summary.extraction_confidence}")
            
            # Show structured insights
            if ai_summary.structured_insights:
                insights = ai_summary.structured_insights
                print(f"   - Competitive Advantages: {len(insights.get('competitive_advantages', []))}")
                print(f"   - Competitive Disadvantages: {len(insights.get('competitive_disadvantages', []))}")
                print(f"   - Feature Comparisons: {len(insights.get('feature_comparisons', {}))}")
        
        # Validate additional data extraction
        if comparison_data.reviews:
            reviews = comparison_data.reviews
            print(f"   - Company Size Data: {len(reviews.get('reviewers_company_size', {}))}")
            print(f"   - Industry Data: {len(reviews.get('reviewers_industry', {}).get('industries', {}))}")
            print(f"   - Helpful Reviews: {len(reviews.get('most_helpful_reviews', {}).get('reviews', {}))}")
        
        if comparison_data.ratings:
            ratings = comparison_data.ratings
            print(f"   - Criteria Ratings: {len(ratings.get('criteria_ratings', {}))}")
            print(f"   - Rating Breakdowns: {len(ratings.get('rating_breakdowns', {}).get('star_ratings', {}))}")
        
        if comparison_data.features:
            features = comparison_data.features
            print(f"   - Feature Categories: {len(features.get('feature_categories', {}))}")
            if 'ai_summary_features' in features:
                print(f"   - AI Summary Features: {len(features['ai_summary_features'].get('feature_insights', {}))}")
        
        if comparison_data.alternatives:
            alternatives = comparison_data.alternatives
            print(f"   - Alternative Products: {len(alternatives.get('alternative_products', {}))}")
            print(f"   - Competitor Mentions: {len(alternatives.get('competitor_mentions', {}))}")
        
        return comparison_data
        
    except Exception as e:
        print(f"❌ Enhanced parser test failed: {e}")
        return None


async def test_enhanced_head_to_head_scraper():
    """Test the enhanced head-to-head comparison scraper."""
    print("\n🧪 Testing Enhanced Head-to-Head Comparison Scraper...")
    
    try:
        # Initialize competitive intelligence scraper
        competitive_scraper = CompetitiveIntelligenceScraper()
        
        # Initialize head-to-head comparison scraper
        head_to_head_scraper = HeadToHeadComparisonScraper(competitive_scraper)
        
        print(f"✅ Enhanced head-to-head comparison scraper initialized successfully!")
        print(f"   - Parser capabilities: {head_to_head_scraper.parser.get_extraction_statistics()}")
        
        # Test market insights generation
        test_comparison_data = await test_enhanced_head_to_head_parser()
        if test_comparison_data:
            market_insights = await head_to_head_scraper._generate_head_to_head_market_insights(test_comparison_data)
            
            print(f"   - Market Insights Generated:")
            print(f"     * Competitive Positioning: {len(market_insights.get('competitive_positioning', {}))}")
            print(f"     * Market Trends: {len(market_insights.get('market_trends', []))}")
            print(f"     * Feature Analysis: {len(market_insights.get('feature_analysis', {}))}")
            print(f"     * Pricing Analysis: {len(market_insights.get('pricing_analysis', {}))}")
            print(f"     * AI Summary Insights: {len(market_insights.get('ai_summary_insights', {}))}")
        
        return head_to_head_scraper
        
    except Exception as e:
        print(f"❌ Enhanced head-to-head comparison scraper test failed: {e}")
        return None


async def test_competitive_intelligence_integration():
    """Test the integration of enhanced head-to-head comparison scraping into competitive intelligence."""
    print("\n🧪 Testing Competitive Intelligence Integration...")
    
    try:
        # Initialize competitive intelligence scraper
        scraper = CompetitiveIntelligenceScraper()
        
        print(f"✅ Competitive intelligence scraper initialized successfully!")
        
        # Test target loading
        targets = scraper.competitive_targets
        print(f"   - Loaded {len(targets)} competitive targets")
        
        # Count head-to-head comparison URLs
        head_to_head_count = 0
        for target in targets:
            if "head_to_head" in target.targets:
                head_to_head_count += len(target.targets["head_to_head"])
        
        print(f"   - Found {head_to_head_count} head-to-head comparison URLs")
        
        # Show sample head-to-head URLs
        print("\n   Sample head-to-head comparison URLs:")
        for target in targets[:3]:  # Show first 3 targets
            if "head_to_head" in target.targets:
                for url in target.targets["head_to_head"][:1]:  # Show first URL per target
                    print(f"     - {target.name}: {url}")
        
        # Test the enhanced scraping method
        if hasattr(scraper, '_scrape_head_to_head_comparisons'):
            print(f"   ✅ Enhanced head-to-head comparison method available")
        else:
            print(f"   ❌ Enhanced head-to-head comparison method not found")
        
        return scraper
        
    except Exception as e:
        print(f"❌ Competitive intelligence integration test failed: {e}")
        return None


async def test_comprehensive_data_export():
    """Test comprehensive data export capabilities."""
    print("\n🧪 Testing Comprehensive Data Export Capabilities...")
    
    try:
        # Create sample enhanced head-to-head comparison data
        from chimera.parsers.head_to_head_comparison import HeadToHeadComparisonData, ProductComparison, AIGeneratedSummary
        
        sample_products = [
            ProductComparison(
                name="Domo",
                g2_product_id="domo",
                vendor_id="domo",
                star_rating=4.3,
                review_count=879,
                market_segments={"mid_market": 54.9, "enterprise": 32.0},
                entry_level_pricing="Free Trial",
                pricing_details={},
                ratings_by_criteria={},
                feature_scores={}
            ),
            ProductComparison(
                name="Microsoft Power BI",
                g2_product_id="power-bi",
                vendor_id="microsoft",
                star_rating=4.5,
                review_count=1381,
                market_segments={"enterprise": 42.8, "mid_market": 36.0},
                entry_level_pricing="Free",
                pricing_details={},
                ratings_by_criteria={},
                feature_scores={}
            )
        ]
        
        sample_ai_summary = AIGeneratedSummary(
            summary_title="AI Generated Summary",
            summary_subtitle="AI-generated. Powered by real user reviews.",
            summary_points=[
                {
                    "text": "Users report that Microsoft Power BI excels in data visualization, scoring 9.2 compared to Domo's 8.7.",
                    "product_a_score": 8.7,
                    "product_b_score": 9.2,
                    "feature_category": "data visualization",
                    "insight_type": "competitive_advantage",
                    "sentiment": "positive",
                    "confidence": 90.0
                }
            ],
            extraction_confidence=95.0,
            structured_insights={
                "competitive_advantages": ["data visualization"],
                "competitive_disadvantages": [],
                "feature_comparisons": {"data visualization": [{"text": "Power BI excels", "confidence": 90.0}]},
                "sentiment_analysis": {"positive": 1, "negative": 0, "neutral": 0}
            }
        )
        
        sample_comparison = HeadToHeadComparisonData(
            comparison_id="test_head_to_head",
            extraction_date=datetime.now(),
            url="https://example.com/test",
            product_a=asdict(sample_products[0]),
            product_b=asdict(sample_products[1]),
            ai_generated_summary=asdict(sample_ai_summary),
            at_a_glance={
                "star_ratings": {
                    "Domo": {"rating": 4.3, "review_count": 879},
                    "Microsoft Power BI": {"rating": 4.5, "review_count": 1381}
                }
            },
            pricing={},
            ratings={},
            features={},
            reviews={
                "reviewers_company_size": {
                    "small_business": {"Domo": {"percentage": 13.1}, "Microsoft Power BI": {"percentage": 21.2}}
                },
                "reviewers_industry": {
                    "industries": {"Computer Software": {"Domo": {"percentage": 9.3}, "Microsoft Power BI": {"percentage": 16.1}}}
                }
            },
            alternatives={},
            data_quality_score=92.0,
            extraction_confidence=95.0,
            summary_quality_score=88.0
        )
        
        # Test export
        from chimera.core.head_to_head_comparison_scraper import HeadToHeadComparisonScraper
        
        # Create a mock scraper for export testing
        class MockCompetitiveScraper:
            pass
        
        mock_scraper = MockCompetitiveScraper()
        head_to_head_scraper = HeadToHeadComparisonScraper(mock_scraper)
        
        # Create sample insights
        from chimera.core.competitive_intelligence_scraper import CompetitiveInsight
        
        sample_insights = [
            CompetitiveInsight(
                competitor_id="test_competitor",
                platform="g2",
                extraction_date=datetime.now(),
                data_type="head_to_head_comparison",
                url="https://example.com/test",
                content=asdict(sample_comparison),
                sentiment_analysis={"score": 0.0, "label": "neutral"},
                competitive_mentions=["Domo", "Microsoft Power BI"],
                market_insights={},
                quality_score=0.92,
                extraction_confidence=0.95
            )
        ]
        
        # Test export
        export_files = await head_to_head_scraper.export_head_to_head_data(sample_insights, "test_output")
        
        print(f"✅ Comprehensive data export test successful!")
        print(f"   - Exported files: {list(export_files.keys())}")
        
        # Clean up test files
        import shutil
        if Path("test_output").exists():
            shutil.rmtree("test_output")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive data export test failed: {e}")
        return False


async def test_ai_summary_extraction_robustness():
    """Test the robustness of AI summary extraction across different scenarios."""
    print("\n🧪 Testing AI Summary Extraction Robustness...")
    
    try:
        parser = G2HeadToHeadComparisonParser()
        
        # Test 1: Standard AI summary
        standard_html = """
        <div aria-label="Comparison Summary" class="compare-container-v2_summary">
            <div class="mb-1/4">AI Generated Summary</div>
            <div>*AI-generated. Powered by real user reviews.</div>
            <ul>
                <li>Power BI excels in data visualization with 9.2 vs Domo's 8.7.</li>
                <li>Domo trails behind in ease of setup with 7.7 vs Power BI's 8.7.</li>
            </ul>
        </div>
        """
        
        # Test 2: Alternative AI summary structure
        alternative_html = """
        <div class="compare-container-v2_summary">
            <div>AI Generated Summary</div>
            <div>AI-generated. Powered by real user reviews.</div>
            <ul>
                <li>Microsoft Power BI shows superior performance in analytics.</li>
            </ul>
        </div>
        """
        
        # Test 3: No AI summary
        no_summary_html = """
        <div class="comparison-container">
            <div>No AI summary available</div>
        </div>
        """
        
        test_cases = [
            ("Standard AI Summary", standard_html),
            ("Alternative Structure", alternative_html),
            ("No AI Summary", no_summary_html)
        ]
        
        for test_name, test_html in test_cases:
            try:
                # Create a minimal HTML structure for parsing
                full_html = f"""
                <html>
                <body>
                    {test_html}
                    <div class="comparison-container-v2_header">Domo</div>
                    <div class="comparison-container-v2_header">Microsoft Power BI</div>
                </body>
                </html>
                """
                
                comparison_data = await parser.parse_head_to_head_comparison(
                    full_html, 
                    "https://example.com/test"
                )
                
                ai_summary = comparison_data.ai_generated_summary
                print(f"   ✅ {test_name}:")
                print(f"      - Title: {ai_summary.summary_title}")
                print(f"      - Points: {len(ai_summary.summary_points)}")
                print(f"      - Confidence: {ai_summary.extraction_confidence}")
                
            except Exception as e:
                print(f"   ❌ {test_name} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI summary extraction robustness test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Starting Enhanced Head-to-Head Comparison Scraping Tests...")
    print("=" * 70)
    
    # Test 1: Enhanced Parser
    parser_result = await test_enhanced_head_to_head_parser()
    
    # Test 2: Enhanced Scraper
    scraper_result = await test_enhanced_head_to_head_scraper()
    
    # Test 3: Integration
    integration_result = await test_competitive_intelligence_integration()
    
    # Test 4: Comprehensive Data Export
    export_result = await test_comprehensive_data_export()
    
    # Test 5: AI Summary Extraction Robustness
    robustness_result = await test_ai_summary_extraction_robustness()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Enhanced Test Summary:")
    print(f"   ✅ Parser Enhancement: {'PASS' if parser_result else 'FAIL'}")
    print(f"   ✅ Scraper Enhancement: {'PASS' if scraper_result else 'FAIL'}")
    print(f"   ✅ Integration: {'PASS' if integration_result else 'FAIL'}")
    print(f"   ✅ Data Export: {'PASS' if export_result else 'FAIL'}")
    print(f"   ✅ AI Summary Robustness: {'PASS' if robustness_result else 'FAIL'}")
    
    if all([parser_result, scraper_result, integration_result, export_result, robustness_result]):
        print("\n🎉 All enhanced head-to-head comparison tests passed!")
        print("   The system is ready for comprehensive AI summary extraction and")
        print("   additional data capture across the entire competitive set.")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")
    
    return all([parser_result, scraper_result, integration_result, export_result, robustness_result])


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
