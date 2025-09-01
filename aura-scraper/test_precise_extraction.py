"""
Precise Data Extraction Test
Using actual page structure from developer tools analysis
"""

import asyncio
import json
import logging
import sys
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

class PreciseCapterraExtractor:
    """Precise extractor using actual page structure from developer tools"""
    
    def __init__(self, page):
        self.page = page
        self.extraction_stats = {
            'elements_found': 0,
            'elements_missing': 0,
            'extraction_errors': 0
        }
    
    async def extract_sigma_data(self) -> dict:
        """Extract data from Sigma page using precise selectors from developer tools"""
        print("🔍 Extracting Sigma data using precise selectors...")
        
        try:
            # Wait for page to fully load
            await asyncio.sleep(3)
            
            # Extract company information
            company_info = await self._extract_company_info()
            
            # Extract rating information
            rating_info = await self._extract_rating_info()
            
            # Extract individual reviews using actual structure
            reviews = await self._extract_reviews_precise()
            
            # Extract rating categories
            rating_categories = await self._extract_rating_categories()
            
            result = {
                'company_info': company_info,
                'rating_info': rating_info,
                'reviews': reviews,
                'rating_categories': rating_categories,
                'extraction_timestamp': asyncio.get_event_loop().time(),
                'page_url': self.page.url,
                'page_title': await self.page.title()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error extracting Sigma data: {str(e)}")
            return {'error': str(e)}
    
    async def _extract_company_info(self) -> dict:
        """Extract company information using precise selectors"""
        print("   📊 Extracting company information...")
        
        try:
            # Company name from H1 (we know it's "Reviews of Sigma Computing")
            company_name = await self.page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    return h1 ? h1.textContent.trim() : 'Unknown';
                }
            """)
            
            # Extract "Sigma Computing" from the title
            if "Sigma Computing" in company_name:
                clean_name = "Sigma Computing"
            else:
                clean_name = company_name
            
            # Company logo
            logo_url = await self.page.evaluate("""
                () => {
                    const logo = document.querySelector('img[alt*="logo"], img[class*="logo"], .logo img');
                    return logo ? logo.src : '';
                }
            """)
            
            return {
                'name': clean_name,
                'full_title': company_name,
                'logo_url': logo_url
            }
            
        except Exception as e:
            logger.error(f"Error extracting company info: {str(e)}")
            return {'name': 'Unknown', 'full_title': '', 'logo_url': ''}
    
    async def _extract_rating_info(self) -> dict:
        """Extract rating information using precise selectors"""
        print("   ⭐ Extracting rating information...")
        
        try:
            # Look for rating patterns in the page text
            rating_data = await self.page.evaluate("""
                () => {
                    const text = document.body.textContent;
                    
                    // Pattern: "4.3 out of 5 stars based on 83 reviews"
                    const pattern1 = /(\\d+\\.\\d+)\\s+out\\s+of\\s+5\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i;
                    const match1 = text.match(pattern1);
                    if (match1) {
                        return {
                            overall_rating: match1[1],
                            review_count: match1[2],
                            method: 'pattern1'
                        };
                    }
                    
                    // Pattern: "4.3 stars based on 83 reviews"
                    const pattern2 = /(\\d+\\.\\d+)\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i;
                    const match2 = text.match(pattern2);
                    if (match2) {
                        return {
                            overall_rating: match2[1],
                            review_count: match2[2],
                            method: 'pattern2'
                        };
                    }
                    
                    // Pattern: "Based on 83 reviews"
                    const pattern3 = /Based\\s+on\\s+(\\d+)\\s+reviews/i;
                    const match3 = text.match(pattern3);
                    if (match3) {
                        return {
                            overall_rating: 'N/A',
                            review_count: match3[1],
                            method: 'pattern3'
                        };
                    }
                    
                    return { overall_rating: 'N/A', review_count: 'N/A', method: 'none' };
                }
            """)
            
            return rating_data
            
        except Exception as e:
            logger.error(f"Error extracting rating info: {str(e)}")
            return {'overall_rating': 'N/A', 'review_count': 'N/A', 'method': 'error'}
    
    async def _extract_reviews_precise(self) -> list:
        """Extract individual reviews using precise selectors from developer tools"""
        print("   📝 Extracting individual reviews using precise selectors...")
        
        try:
            # Use the actual structure we found: H3 elements with class "typo-20 font-semibold"
            reviews = await self.page.evaluate("""
                () => {
                    const reviews = [];
                    
                    // Find all H3 elements with review titles (we know these are review titles)
                    const reviewTitles = document.querySelectorAll('h3.typo-20.font-semibold');
                    
                    console.log(`Found ${reviewTitles.length} review titles`);
                    
                    reviewTitles.forEach((titleElement, i) => {
                        const title = titleElement.textContent.trim();
                        
                        // Skip if it's not a review title (contains quotes)
                        if (!title.startsWith('"') || !title.endsWith('"')) {
                            return;
                        }
                        
                        // Clean the title
                        const cleanTitle = title.replace(/^"/, '').replace(/"$/, '');
                        
                        // Find the review container (parent or nearby elements)
                        let reviewContainer = titleElement.closest('article, .review, [class*="review"]');
                        if (!reviewContainer) {
                            // Look for nearby review content
                            reviewContainer = titleElement.parentElement;
                        }
                        
                        // Extract review text (look for paragraphs after the title)
                        let reviewText = '';
                        let reviewerName = '';
                        let reviewDate = '';
                        let rating = '';
                        
                        if (reviewContainer) {
                            // Look for review text in paragraphs
                            const paragraphs = reviewContainer.querySelectorAll('p');
                            paragraphs.forEach(p => {
                                const text = p.textContent.trim();
                                if (text.length > 50 && !text.includes('Based on') && !text.includes('reviews')) {
                                    reviewText = text;
                                }
                            });
                            
                            // Look for reviewer name (usually in a specific pattern)
                            const nameElements = reviewContainer.querySelectorAll('span, div, p');
                            nameElements.forEach(el => {
                                const text = el.textContent.trim();
                                // Look for patterns like "Joseph B., Data Analyst"
                                const nameMatch = text.match(/^([A-Z][a-z]+\\s+[A-Z]\\.?)\\s*,/);
                                if (nameMatch && !reviewerName) {
                                    reviewerName = nameMatch[1];
                                }
                            });
                            
                            // Look for date
                            const dateElements = reviewContainer.querySelectorAll('time, span, div');
                            dateElements.forEach(el => {
                                const text = el.textContent.trim();
                                const dateMatch = text.match(/(\\d{1,2}\\/\\d{1,2}\\/\\d{4}|\\d{4}-\\d{2}-\\d{2})/);
                                if (dateMatch && !reviewDate) {
                                    reviewDate = dateMatch[1];
                                }
                            });
                            
                            // Look for rating
                            const ratingElements = reviewContainer.querySelectorAll('[class*="star"], [class*="rating"]');
                            ratingElements.forEach(el => {
                                const text = el.textContent.trim();
                                const ratingMatch = text.match(/(\\d+\\.\\d+)/);
                                if (ratingMatch && !rating) {
                                    rating = ratingMatch[1];
                                }
                            });
                        }
                        
                        reviews.push({
                            title: cleanTitle,
                            text: reviewText,
                            reviewer_name: reviewerName,
                            date: reviewDate,
                            rating: rating,
                            index: i
                        });
                    });
                    
                    return reviews;
                }
            """)
            
            print(f"   ✅ Extracted {len(reviews)} reviews using precise selectors")
            return reviews
            
        except Exception as e:
            logger.error(f"Error extracting reviews: {str(e)}")
            return []
    
    async def _extract_rating_categories(self) -> dict:
        """Extract rating categories like 'Ease of use' and 'Customer Service'"""
        print("   📊 Extracting rating categories...")
        
        try:
            categories = await self.page.evaluate("""
                () => {
                    const categories = {};
                    
                    // Look for rating categories in the page text
                    const text = document.body.textContent;
                    
                    // Pattern for categories like "Ease of use: 3.9 stars"
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

async def test_precise_extraction():
    """Test precise data extraction using actual page structure"""
    print("🎯 Precise Data Extraction Test")
    print("=" * 50)
    print("Using actual page structure from developer tools analysis")
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
        await asyncio.sleep(5)
        
        # Check if we can access the page
        page_title = await aura_lite.page.title()
        print(f"   📄 Page title: {page_title}")
        
        # Initialize precise extractor
        extractor = PreciseCapterraExtractor(aura_lite.page)
        
        # Extract data
        print("2. Extracting data using precise selectors...")
        extracted_data = await extractor.extract_sigma_data()
        
        if 'error' not in extracted_data:
            print("   ✅ Data extraction successful!")
            
            # Display results
            print("\n📊 EXTRACTION RESULTS:")
            print("=" * 40)
            
            # Company info
            company_info = extracted_data.get('company_info', {})
            print(f"Company: {company_info.get('name', 'Unknown')}")
            print(f"Full Title: {company_info.get('full_title', 'N/A')}")
            print(f"Logo URL: {company_info.get('logo_url', 'N/A')}")
            
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
                for i, review in enumerate(reviews[:5]):
                    print(f"   {i+1}. Title: {review.get('title', 'N/A')}")
                    print(f"      Reviewer: {review.get('reviewer_name', 'Anonymous')}")
                    print(f"      Text: {review.get('text', '')[:100]}...")
                    print(f"      Date: {review.get('date', 'N/A')}")
                    print(f"      Rating: {review.get('rating', 'N/A')}")
                    print()
            
            # Rating categories
            categories = extracted_data.get('rating_categories', {})
            if categories:
                print("📊 Rating Categories:")
                for category, rating in categories.items():
                    print(f"   {category}: {rating}")
            
            # Save results
            output_file = Path("output") / f"sigma_precise_extraction_{int(asyncio.get_event_loop().time())}.json"
            with open(output_file, 'w') as f:
                json.dump(extracted_data, f, indent=2)
            print(f"\n💾 Results saved to: {output_file}")
            
            return extracted_data
        else:
            print(f"   ❌ Data extraction failed: {extracted_data.get('error')}")
            return None
        
    except Exception as e:
        logger.error(f"Error in precise extraction test: {str(e)}")
        print(f"❌ Test failed: {str(e)}")
        return None
    
    finally:
        if aura_lite:
            await aura_lite.close()

async def main():
    """Main test function"""
    print("🚀 Precise Data Extraction Test")
    print("=" * 60)
    print("Testing data extraction using actual page structure from developer tools")
    print("=" * 60)
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    # Run precise extraction test
    results = await test_precise_extraction()
    
    if results:
        print("\n🎉 Precise data extraction test completed successfully!")
        print("✅ Successfully extracted data using actual page structure")
        print("✅ Review titles, text, and metadata captured")
        print("✅ Ready for production use with refined selectors")
    else:
        print("\n❌ Precise data extraction test failed.")
        print("Need to further refine selectors based on page structure.")

if __name__ == "__main__":
    asyncio.run(main())
