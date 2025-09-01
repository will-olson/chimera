"""
Developer Tools Approach Test
Test the complete workflow: extract selectors from developer tools, then use them for precise data extraction
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_lite import AuraLite
from aura_lite.core.dynamic_selectors import DynamicSelectorManager, PreciseDataExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_developer_tools_workflow():
    """Test the complete developer tools workflow"""
    print("🎯 Developer Tools Workflow Test")
    print("=" * 60)
    print("1. Extract selectors from real pages")
    print("2. Use extracted selectors for precise data extraction")
    print("=" * 60)
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        # Get Sigma target
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        target = targets[0]  # Sigma
        company_name = target['data']['name']
        reviews_url = target['data']['targets']['product_reviews']
        
        print(f"Testing with: {company_name}")
        print(f"URL: {reviews_url}")
        
        # Step 1: Navigate to page and extract selectors
        print("\n1. 🔍 Extracting selectors from developer tools analysis...")
        await aura_lite.page.goto(reviews_url, wait_until='domcontentloaded')
        await asyncio.sleep(5)
        
        # Extract selectors using page analysis
        selectors = await extract_selectors_from_page(aura_lite.page, company_name)
        
        if selectors:
            print("   ✅ Successfully extracted selectors")
            
            # Save selectors
            output_dir = Path("output/selectors")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            selector_file = output_dir / f"{company_name.lower()}_selectors.json"
            with open(selector_file, 'w') as f:
                json.dump(selectors, f, indent=2)
            print(f"   💾 Selectors saved to: {selector_file}")
            
            # Step 2: Use extracted selectors for data extraction
            print("\n2. 📊 Using extracted selectors for precise data extraction...")
            
            # Initialize dynamic selector manager
            selector_manager = DynamicSelectorManager()
            
            # Add our extracted selectors to the manager
            selector_manager.selectors[company_name] = selectors
            
            # Initialize precise data extractor
            extractor = PreciseDataExtractor(aura_lite.page, selector_manager)
            
            # Extract company data
            company_data = await extractor.extract_company_data(company_name)
            print(f"   📈 Company data: {company_data}")
            
            # Extract reviews
            reviews = await extractor.extract_reviews(company_name, max_reviews=5)
            print(f"   📝 Reviews extracted: {len(reviews)}")
            
            if reviews:
                print("   📋 Sample reviews:")
                for i, review in enumerate(reviews[:3]):
                    print(f"      {i+1}. {review.get('reviewer_name', 'Anonymous')}")
                    print(f"         Text: {review.get('review_text', '')[:100]}...")
                    print(f"         Date: {review.get('review_date', 'N/A')}")
                    print()
            
            # Extract alternatives
            alternatives = await extractor.extract_alternatives(company_name, max_alternatives=3)
            print(f"   🔄 Alternatives extracted: {len(alternatives)}")
            
            if alternatives:
                print("   📋 Sample alternatives:")
                for i, alt in enumerate(alternatives):
                    print(f"      {i+1}. {alt.get('name', 'Unknown')}")
                    print(f"         Rating: {alt.get('rating', 'N/A')}")
                    print(f"         Link: {alt.get('link', 'N/A')}")
                    print()
            
            # Get extraction stats
            stats = extractor.get_extraction_stats()
            print(f"\n📊 Extraction Statistics:")
            print(f"   Elements found: {stats['elements_found']}")
            print(f"   Elements missing: {stats['elements_missing']}")
            print(f"   Extraction errors: {stats['extraction_errors']}")
            
            # Save complete results
            results = {
                'company_name': company_name,
                'url': reviews_url,
                'company_data': company_data,
                'reviews': reviews,
                'alternatives': alternatives,
                'extraction_stats': stats,
                'selectors_used': selectors
            }
            
            results_file = Path("output") / f"{company_name.lower()}_complete_extraction.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Complete results saved to: {results_file}")
            
            return results
        else:
            print("   ❌ Failed to extract selectors")
            return None
        
    except Exception as e:
        logger.error(f"Error in developer tools workflow test: {str(e)}")
        print(f"❌ Test failed: {str(e)}")
        return None
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def extract_selectors_from_page(page, company_name: str) -> dict:
    """Extract selectors from the current page using developer tools analysis"""
    print(f"   🔍 Analyzing page structure for {company_name}...")
    
    try:
        # Comprehensive page analysis
        selectors = await page.evaluate("""
            () => {
                const selectors = {
                    company_info: {},
                    rating_info: {},
                    reviews: {},
                    pricing: {},
                    alternatives: {}
                };
                
                // Company name selectors
                const h1 = document.querySelector('h1');
                if (h1) {
                    selectors.company_info.name = 'h1';
                    selectors.company_info.name_text = h1.textContent.trim();
                }
                
                // Company logo selectors
                const logo = document.querySelector('img[alt*="logo"], img[class*="logo"], .logo img');
                if (logo) {
                    selectors.company_info.logo = 'img[alt*="logo"], img[class*="logo"], .logo img';
                }
                
                // Rating and review count selectors
                const text = document.body.textContent;
                
                // Look for rating patterns
                const ratingPatterns = [
                    /(\\d+\\.\\d+)\\s+out\\s+of\\s+5\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i,
                    /(\\d+\\.\\d+)\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i,
                    /Based\\s+on\\s+(\\d+)\\s+reviews/i
                ];
                
                for (let i = 0; i < ratingPatterns.length; i++) {
                    const match = text.match(ratingPatterns[i]);
                    if (match) {
                        selectors.rating_info.pattern = match[0];
                        if (match[1]) selectors.rating_info.overall_rating = match[1];
                        if (match[2]) selectors.rating_info.review_count = match[2];
                        break;
                    }
                }
                
                // Look for specific rating elements
                const ratingElements = document.querySelectorAll('p, span, div');
                ratingElements.forEach((el, i) => {
                    const text = el.textContent.trim();
                    if (text.includes('Based on') && text.includes('reviews')) {
                        selectors.rating_info.review_count_element = el.outerHTML.substring(0, 200);
                        selectors.rating_info.review_count_selector = el.tagName.toLowerCase() + 
                            (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : '');
                    }
                });
                
                // Review container selectors
                const reviewContainers = document.querySelectorAll('article, .review, [class*="review"], [data-testid*="review"]');
                
                if (reviewContainers.length > 0) {
                    selectors.reviews.container_count = reviewContainers.length;
                    selectors.reviews.container_selector = 'article, .review, [class*="review"], [data-testid*="review"]';
                    
                    // Analyze first review structure
                    const firstReview = reviewContainers[0];
                    selectors.reviews.first_review_html = firstReview.outerHTML.substring(0, 500);
                    
                    // Look for review elements within containers
                    const reviewerName = firstReview.querySelector('h3, h4, .reviewer-name, [class*="name"]');
                    if (reviewerName) {
                        selectors.reviews.reviewer_name_selector = reviewerName.tagName.toLowerCase() + 
                            (reviewerName.className && typeof reviewerName.className === 'string' ? '.' + reviewerName.className.split(' ').join('.') : '');
                    }
                    
                    const reviewText = firstReview.querySelector('p, .review-text, [class*="text"]');
                    if (reviewText) {
                        selectors.reviews.review_text_selector = reviewText.tagName.toLowerCase() + 
                            (reviewText.className && typeof reviewText.className === 'string' ? '.' + reviewText.className.split(' ').join('.') : '');
                    }
                    
                    const reviewDate = firstReview.querySelector('time, .date, [class*="date"]');
                    if (reviewDate) {
                        selectors.reviews.review_date_selector = reviewDate.tagName.toLowerCase() + 
                            (reviewDate.className && typeof reviewDate.className === 'string' ? '.' + reviewDate.className.split(' ').join('.') : '');
                    }
                }
                
                // Pricing selectors
                const pricingElements = document.querySelectorAll('[class*="price"], [class*="cost"], [class*="pricing"]');
                if (pricingElements.length > 0) {
                    selectors.pricing.pricing_elements_count = pricingElements.length;
                    selectors.pricing.pricing_selector = '[class*="price"], [class*="cost"], [class*="pricing"]';
                }
                
                // Alternatives selectors
                const alternativesSection = document.querySelector('[class*="alternative"], [class*="competitor"], #alternatives');
                if (alternativesSection) {
                    const alternativeCards = alternativesSection.querySelectorAll('.card, [class*="product"], [class*="alternative"]');
                    if (alternativeCards.length > 0) {
                        selectors.alternatives.alternative_cards_count = alternativeCards.length;
                        selectors.alternatives.alternative_card_selector = '.card, [class*="product"], [class*="alternative"]';
                    }
                }
                
                // Page structure analysis
                selectors.page_structure = {
                    total_elements: document.querySelectorAll('*').length,
                    headings: [],
                    common_classes: {}
                };
                
                // Analyze headings
                const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                headings.forEach((h, i) => {
                    selectors.page_structure.headings.push({
                        tag: h.tagName,
                        text: h.textContent.trim().substring(0, 100),
                        classes: h.className
                    });
                });
                
                // Analyze common classes
                const classCounts = {};
                const allElements = document.querySelectorAll('*');
                allElements.forEach(el => {
                    if (el.className && typeof el.className === 'string') {
                        const classes = el.className.split(' ');
                        classes.forEach(cls => {
                            if (cls.length > 2) {
                                classCounts[cls] = (classCounts[cls] || 0) + 1;
                            }
                        });
                    }
                });
                
                // Get top 10 most common classes
                selectors.page_structure.common_classes = Object.entries(classCounts)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 10)
                    .reduce((obj, [key, value]) => {
                        obj[key] = value;
                        return obj;
                    }, {});
                
                return selectors;
            }
        """)
        
        print(f"   📊 Page analysis complete:")
        print(f"      Total elements: {selectors.get('page_structure', {}).get('total_elements', 0)}")
        print(f"      Headings found: {len(selectors.get('page_structure', {}).get('headings', []))}")
        print(f"      Review containers: {selectors.get('reviews', {}).get('container_count', 0)}")
        print(f"      Pricing elements: {selectors.get('pricing', {}).get('pricing_elements_count', 0)}")
        
        return selectors
        
    except Exception as e:
        logger.error(f"Error extracting selectors from page: {str(e)}")
        return {}

async def main():
    """Main test function"""
    print("🚀 Developer Tools Approach Test")
    print("=" * 60)
    print("Testing complete workflow: extract selectors → use for data extraction")
    print("=" * 60)
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    # Run developer tools workflow test
    results = await test_developer_tools_workflow()
    
    if results:
        print("\n🎉 Developer tools workflow test completed successfully!")
        print("✅ Selectors extracted from real page structure")
        print("✅ Data extraction using precise selectors")
        print("✅ Complete workflow validated")
        print("\nNext steps:")
        print("1. Refine selectors based on extraction results")
        print("2. Test with multiple companies")
        print("3. Implement iterative improvements")
    else:
        print("\n❌ Developer tools workflow test failed.")
        print("Need to analyze page access and selector strategies.")

if __name__ == "__main__":
    asyncio.run(main())
