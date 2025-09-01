"""
AURA-LITE Data Extraction Test
Test actual data extraction using precise selectors from real page structure
"""

import asyncio
import logging
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from aura_lite import AuraLite

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class PreciseDataExtractor:
    """Precise data extractor based on actual page structure analysis"""
    
    def __init__(self, page):
        self.page = page
        self.extraction_results = {}
    
    async def extract_sigma_data(self) -> dict:
        """Extract data from Sigma page using precise selectors"""
        print("🔍 Extracting Sigma data using precise selectors...")
        
        try:
            # Wait for page to fully load
            await asyncio.sleep(3)
            
            # Extract company information
            company_info = await self._extract_company_info()
            
            # Extract overall rating and review count
            rating_info = await self._extract_rating_info()
            
            # Extract individual reviews
            reviews = await self._extract_individual_reviews()
            
            # Extract rating categories
            rating_categories = await self._extract_rating_categories()
            
            # Extract pricing information
            pricing_info = await self._extract_pricing_info()
            
            result = {
                'company_info': company_info,
                'rating_info': rating_info,
                'reviews': reviews,
                'rating_categories': rating_categories,
                'pricing_info': pricing_info,
                'extraction_timestamp': asyncio.get_event_loop().time(),
                'page_url': self.page.url,
                'page_title': await self.page.title()
            }
            
            self.extraction_results['sigma'] = result
            return result
            
        except Exception as e:
            logger.error(f"Error extracting Sigma data: {str(e)}")
            return {'error': str(e)}
    
    async def _extract_company_info(self) -> dict:
        """Extract company information"""
        print("   📊 Extracting company information...")
        
        try:
            # Company name - look for h1 or main heading
            company_name = await self.page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    if (h1) return h1.textContent.trim();
                    
                    // Fallback to any heading with company name
                    const headings = document.querySelectorAll('h1, h2, h3');
                    for (let heading of headings) {
                        if (heading.textContent.includes('Sigma')) {
                            return heading.textContent.trim();
                        }
                    }
                    return 'Unknown';
                }
            """)
            
            # Company description
            company_description = await self.page.evaluate("""
                () => {
                    // Look for description text
                    const descSelectors = [
                        'p[class*="description"]',
                        'div[class*="description"]',
                        'p:contains("Sigma")',
                        '.company-description'
                    ];
                    
                    for (let selector of descSelectors) {
                        const element = document.querySelector(selector);
                        if (element && element.textContent.length > 50) {
                            return element.textContent.trim();
                        }
                    }
                    return '';
                }
            """)
            
            return {
                'name': company_name,
                'description': company_description
            }
            
        except Exception as e:
            logger.error(f"Error extracting company info: {str(e)}")
            return {'name': 'Unknown', 'description': ''}
    
    async def _extract_rating_info(self) -> dict:
        """Extract overall rating and review count"""
        print("   ⭐ Extracting rating information...")
        
        try:
            # Extract overall rating and review count
            rating_data = await self.page.evaluate("""
                () => {
                    // Look for rating patterns like "4.3 out of 5 stars based on 83 reviews"
                    const text = document.body.textContent;
                    
                    // Pattern 1: "4.3 out of 5 stars based on 83 reviews"
                    const pattern1 = /(\\d+\\.\\d+)\\s+out\\s+of\\s+5\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i;
                    const match1 = text.match(pattern1);
                    if (match1) {
                        return {
                            overall_rating: match1[1],
                            review_count: match1[2],
                            method: 'pattern1'
                        };
                    }
                    
                    // Pattern 2: Look for rating elements
                    const ratingElements = document.querySelectorAll('[class*="rating"], [class*="star"]');
                    for (let element of ratingElements) {
                        const text = element.textContent;
                        const ratingMatch = text.match(/(\\d+\\.\\d+)/);
                        const countMatch = text.match(/(\\d+)\\s+reviews?/i);
                        if (ratingMatch && countMatch) {
                            return {
                                overall_rating: ratingMatch[1],
                                review_count: countMatch[1],
                                method: 'element_search'
                            };
                        }
                    }
                    
                    return { overall_rating: 'N/A', review_count: 'N/A', method: 'none' };
                }
            """)
            
            return rating_data
            
        except Exception as e:
            logger.error(f"Error extracting rating info: {str(e)}")
            return {'overall_rating': 'N/A', 'review_count': 'N/A', 'method': 'error'}
    
    async def _extract_individual_reviews(self) -> list:
        """Extract individual reviews using precise selectors"""
        print("   📝 Extracting individual reviews...")
        
        try:
            # Extract reviews using the structure we can see in the screenshot
            reviews = await self.page.evaluate("""
                () => {
                    const reviews = [];
                    
                    // Look for review containers - based on the screenshot structure
                    const reviewSelectors = [
                        'div[class*="review"]',
                        'div[class*="card"]',
                        'article',
                        '.review-item',
                        '[data-testid*="review"]'
                    ];
                    
                    let reviewElements = [];
                    for (let selector of reviewSelectors) {
                        const elements = document.querySelectorAll(selector);
                        if (elements.length > 0) {
                            reviewElements = Array.from(elements);
                            break;
                        }
                    }
                    
                    // If no specific review containers found, look for text patterns
                    if (reviewElements.length === 0) {
                        // Look for text that looks like reviews
                        const allElements = document.querySelectorAll('p, div, span');
                        for (let element of allElements) {
                            const text = element.textContent.trim();
                            if (text.length > 50 && text.length < 1000) {
                                // Check if it looks like a review
                                if (text.includes('ability') || text.includes('great') || 
                                    text.includes('excellent') || text.includes('recommend')) {
                                    reviewElements.push(element);
                                }
                            }
                        }
                    }
                    
                    // Extract data from each review element
                    for (let i = 0; i < Math.min(reviewElements.length, 10); i++) {
                        const element = reviewElements[i];
                        const text = element.textContent.trim();
                        
                        if (text.length > 20) {
                            // Extract reviewer name (look for patterns like "martha q" or "Shawn H")
                            const nameMatch = text.match(/^([A-Z][a-z]+\\s+[A-Z])\\.?/);
                            const reviewer = nameMatch ? nameMatch[1] : 'Anonymous';
                            
                            // Extract role/position
                            const roleMatch = text.match(/([A-Z][a-z]+\\s+[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*)/);
                            const role = roleMatch ? roleMatch[1] : '';
                            
                            // Extract review text (look for quoted content)
                            const reviewTextMatch = text.match(/"([^"]+)"/);
                            const reviewText = reviewTextMatch ? reviewTextMatch[1] : text;
                            
                            // Extract date
                            const dateMatch = text.match(/(\\d{1,2}\\/\\d{1,2}\\/\\d{4}|\\d{4}-\\d{2}-\\d{2})/);
                            const date = dateMatch ? dateMatch[1] : '';
                            
                            reviews.push({
                                reviewer: reviewer,
                                role: role,
                                text: reviewText,
                                date: date,
                                full_text: text,
                                element_index: i
                            });
                        }
                    }
                    
                    return reviews;
                }
            """)
            
            print(f"   ✅ Extracted {len(reviews)} reviews")
            return reviews
            
        except Exception as e:
            logger.error(f"Error extracting individual reviews: {str(e)}")
            return []
    
    async def _extract_rating_categories(self) -> dict:
        """Extract rating categories like 'Ease of use' and 'Customer Service'"""
        print("   📊 Extracting rating categories...")
        
        try:
            categories = await self.page.evaluate("""
                () => {
                    const categories = {};
                    
                    // Look for rating categories like "Ease of use: 3.9 stars"
                    const text = document.body.textContent;
                    
                    // Pattern for categories
                    const categoryPattern = /([A-Za-z\\s]+):\\s*(\\d+\\.\\d+)\\s*stars?/gi;
                    let match;
                    
                    while ((match = categoryPattern.exec(text)) !== null) {
                        const categoryName = match[1].trim();
                        const rating = match[2];
                        
                        // Filter out common false positives
                        if (categoryName.length > 3 && categoryName.length < 30) {
                            categories[categoryName] = rating;
                        }
                    }
                    
                    return categories;
                }
            """)
            
            print(f"   ✅ Extracted {len(categories)} rating categories")
            return categories
            
        except Exception as e:
            logger.error(f"Error extracting rating categories: {str(e)}")
            return {}
    
    async def _extract_pricing_info(self) -> dict:
        """Extract pricing information"""
        print("   💰 Extracting pricing information...")
        
        try:
            pricing = await self.page.evaluate("""
                () => {
                    const text = document.body.textContent;
                    
                    // Look for pricing patterns
                    const pricingPatterns = [
                        /Starting from:\\s*\\$?([\\d,]+)/i,
                        /From\\s*\\$?([\\d,]+)/i,
                        /\\$([\\d,]+)\\s*per\\s*month/i,
                        /\\$([\\d,]+)\\s*\\/month/i
                    ];
                    
                    for (let pattern of pricingPatterns) {
                        const match = text.match(pattern);
                        if (match) {
                            return {
                                price: match[1],
                                currency: '$',
                                period: 'month',
                                found: true
                            };
                        }
                    }
                    
                    return { found: false };
                }
            """)
            
            return pricing
            
        except Exception as e:
            logger.error(f"Error extracting pricing info: {str(e)}")
            return {'found': False}
    
    async def get_page_structure_analysis(self) -> dict:
        """Analyze page structure for better selector identification"""
        print("   🔍 Analyzing page structure...")
        
        try:
            structure = await self.page.evaluate("""
                () => {
                    const analysis = {
                        total_elements: document.querySelectorAll('*').length,
                        headings: [],
                        review_related_elements: [],
                        rating_related_elements: [],
                        common_classes: {}
                    };
                    
                    // Analyze headings
                    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                    headings.forEach((h, i) => {
                        analysis.headings.push({
                            tag: h.tagName,
                            text: h.textContent.trim().substring(0, 100),
                            classes: h.className
                        });
                    });
                    
                    // Look for review-related elements
                    const reviewKeywords = ['review', 'rating', 'star', 'comment', 'feedback'];
                    const allElements = document.querySelectorAll('*');
                    
                    allElements.forEach((el, i) => {
                        const text = el.textContent.toLowerCase();
                        const className = el.className.toLowerCase();
                        
                        if (reviewKeywords.some(keyword => 
                            text.includes(keyword) || className.includes(keyword))) {
                            analysis.review_related_elements.push({
                                tag: el.tagName,
                                classes: el.className,
                                text: el.textContent.trim().substring(0, 50)
                            });
                        }
                    });
                    
                    // Analyze common classes
                    const classCounts = {};
                    allElements.forEach(el => {
                        if (el.className) {
                            const classes = el.className.split(' ');
                            classes.forEach(cls => {
                                if (cls.length > 2) {
                                    classCounts[cls] = (classCounts[cls] || 0) + 1;
                                }
                            });
                        }
                    });
                    
                    // Get top 10 most common classes
                    analysis.common_classes = Object.entries(classCounts)
                        .sort(([,a], [,b]) => b - a)
                        .slice(0, 10)
                        .reduce((obj, [key, value]) => {
                            obj[key] = value;
                            return obj;
                        }, {});
                    
                    return analysis;
                }
            """)
            
            return structure
            
        except Exception as e:
            logger.error(f"Error analyzing page structure: {str(e)}")
            return {}

async def test_precise_data_extraction():
    """Test precise data extraction using real page structure"""
    print("🎯 Precise Data Extraction Test")
    print("=" * 50)
    print("Testing data extraction using actual page structure")
    print("=" * 50)
    
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
        
        # Navigate to the page
        print("1. Navigating to Capterra page...")
        await aura_lite.page.goto(reviews_url, wait_until='domcontentloaded')
        await asyncio.sleep(5)  # Wait for page to fully load
        
        # Check if we can access the page
        page_title = await aura_lite.page.title()
        print(f"   📄 Page title: {page_title}")
        
        if 'sigma' not in page_title.lower():
            print("   ⚠️ Page title doesn't contain 'sigma' - might be blocked")
        
        # Initialize precise extractor
        extractor = PreciseDataExtractor(aura_lite.page)
        
        # Analyze page structure first
        print("2. Analyzing page structure...")
        structure = await extractor.get_page_structure_analysis()
        print(f"   📊 Total elements: {structure.get('total_elements', 0)}")
        print(f"   📝 Headings found: {len(structure.get('headings', []))}")
        print(f"   🔍 Review-related elements: {len(structure.get('review_related_elements', []))}")
        
        # Show top classes
        common_classes = structure.get('common_classes', {})
        if common_classes:
            print("   🏷️ Top classes:")
            for cls, count in list(common_classes.items())[:5]:
                print(f"      {cls}: {count}")
        
        # Extract data
        print("3. Extracting data...")
        extracted_data = await extractor.extract_sigma_data()
        
        if 'error' not in extracted_data:
            print("   ✅ Data extraction successful!")
            
            # Display results
            print("\n📊 EXTRACTION RESULTS:")
            print("=" * 40)
            
            # Company info
            company_info = extracted_data.get('company_info', {})
            print(f"Company: {company_info.get('name', 'Unknown')}")
            
            # Rating info
            rating_info = extracted_data.get('rating_info', {})
            print(f"Overall Rating: {rating_info.get('overall_rating', 'N/A')}")
            print(f"Review Count: {rating_info.get('review_count', 'N/A')}")
            print(f"Extraction Method: {rating_info.get('method', 'unknown')}")
            
            # Reviews
            reviews = extracted_data.get('reviews', [])
            print(f"Reviews Extracted: {len(reviews)}")
            
            if reviews:
                print("\n📝 Sample Reviews:")
                for i, review in enumerate(reviews[:3]):
                    print(f"   {i+1}. {review.get('reviewer', 'Anonymous')} ({review.get('role', '')})")
                    print(f"      Text: {review.get('text', '')[:100]}...")
                    print(f"      Date: {review.get('date', 'N/A')}")
                    print()
            
            # Rating categories
            categories = extracted_data.get('rating_categories', {})
            if categories:
                print("📊 Rating Categories:")
                for category, rating in categories.items():
                    print(f"   {category}: {rating}")
            
            # Pricing
            pricing = extracted_data.get('pricing_info', {})
            if pricing.get('found'):
                print(f"💰 Pricing: ${pricing.get('price', 'N/A')}/{pricing.get('period', 'month')}")
            else:
                print("💰 Pricing: Not found")
            
            # Save results
            output_file = Path("output") / f"sigma_extraction_{int(asyncio.get_event_loop().time())}.json"
            with open(output_file, 'w') as f:
                json.dump(extracted_data, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")
            
            return extracted_data
        else:
            print(f"   ❌ Data extraction failed: {extracted_data.get('error')}")
            return None
        
    except Exception as e:
        logger.error(f"Error in precise data extraction test: {str(e)}")
        print(f"❌ Test failed: {str(e)}")
        return None
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def main():
    """Main test function"""
    print("🚀 AURA-LITE Precise Data Extraction Test")
    print("=" * 60)
    print("Testing data extraction using real page structure analysis")
    print("=" * 60)
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    # Run precise data extraction test
    results = await test_precise_data_extraction()
    
    if results:
        print("\n🎉 Precise data extraction test completed successfully!")
        print("Ready to implement improvements based on real page structure.")
    else:
        print("\n❌ Precise data extraction test failed.")
        print("Need to analyze page access and selector strategies.")

if __name__ == "__main__":
    asyncio.run(main())
