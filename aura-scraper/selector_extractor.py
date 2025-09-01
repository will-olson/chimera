"""
Developer Tools Selector Extractor
Extract precise selectors from Capterra pages using developer tools analysis
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from playwright.async_api import Page

logger = logging.getLogger(__name__)

class CapterraSelectorExtractor:
    """Extract precise selectors from Capterra pages using developer tools analysis"""
    
    def __init__(self, page: Page):
        self.page = page
        self.extracted_selectors = {}
        self.page_structure = {}
    
    async def extract_all_selectors(self, url: str) -> Dict[str, Any]:
        """Extract all relevant selectors from a Capterra page"""
        print(f"🔍 Extracting selectors from: {url}")
        
        try:
            # Navigate to the page
            await self.page.goto(url, wait_until='domcontentloaded')
            await asyncio.sleep(3)
            
            # Extract different types of selectors
            selectors = {
                'company_info': await self._extract_company_selectors(),
                'rating_info': await self._extract_rating_selectors(),
                'reviews': await self._extract_review_selectors(),
                'pricing': await self._extract_pricing_selectors(),
                'alternatives': await self._extract_alternatives_selectors(),
                'page_structure': await self._analyze_page_structure()
            }
            
            # Save extracted selectors
            self.extracted_selectors = selectors
            await self._save_selectors(selectors, url)
            
            return selectors
            
        except Exception as e:
            logger.error(f"Error extracting selectors: {str(e)}")
            return {}
    
    async def _extract_company_selectors(self) -> Dict[str, str]:
        """Extract selectors for company information"""
        print("   📊 Extracting company selectors...")
        
        selectors = await self.page.evaluate("""
            () => {
                const companySelectors = {};
                
                // Company name - look for h1 or main heading
                const h1 = document.querySelector('h1');
                if (h1) {
                    companySelectors['name'] = 'h1';
                    companySelectors['name_text'] = h1.textContent.trim();
                }
                
                // Company logo
                const logo = document.querySelector('img[alt*="logo"], img[class*="logo"], .logo img');
                if (logo) {
                    companySelectors['logo'] = 'img[alt*="logo"], img[class*="logo"], .logo img';
                }
                
                // Company description
                const descSelectors = [
                    'p[class*="description"]',
                    'div[class*="description"]',
                    '.company-description',
                    'p:contains("description")'
                ];
                
                for (let selector of descSelectors) {
                    const element = document.querySelector(selector);
                    if (element && element.textContent.length > 50) {
                        companySelectors['description'] = selector;
                        companySelectors['description_text'] = element.textContent.trim();
                        break;
                    }
                }
                
                return companySelectors;
            }
        """)
        
        return selectors
    
    async def _extract_rating_selectors(self) -> Dict[str, str]:
        """Extract selectors for rating information"""
        print("   ⭐ Extracting rating selectors...")
        
        selectors = await self.page.evaluate("""
            () => {
                const ratingSelectors = {};
                
                // Look for rating elements with specific patterns
                const ratingPatterns = [
                    // Pattern: "4.6 out of 5 stars based on 279 reviews"
                    /(\\d+\\.\\d+)\\s+out\\s+of\\s+5\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i,
                    // Pattern: "4.6 stars based on 279 reviews"
                    /(\\d+\\.\\d+)\\s+stars\\s+based\\s+on\\s+(\\d+)\\s+reviews/i,
                    // Pattern: "Based on 279 reviews"
                    /Based\\s+on\\s+(\\d+)\\s+reviews/i
                ];
                
                const text = document.body.textContent;
                
                for (let i = 0; i < ratingPatterns.length; i++) {
                    const match = text.match(ratingPatterns[i]);
                    if (match) {
                        ratingSelectors[`pattern_${i}`] = match[0];
                        if (match[1]) ratingSelectors['overall_rating'] = match[1];
                        if (match[2]) ratingSelectors['review_count'] = match[2];
                        break;
                    }
                }
                
                // Look for star rating elements
                const starElements = document.querySelectorAll('[class*="star"], [class*="rating"]');
                starElements.forEach((el, i) => {
                    if (el.textContent.includes('star') || el.textContent.includes('rating')) {
                        ratingSelectors[`star_element_${i}`] = el.outerHTML.substring(0, 200);
                    }
                });
                
                // Look for specific rating text elements
                const ratingTextElements = document.querySelectorAll('p, span, div');
                ratingTextElements.forEach((el, i) => {
                    const text = el.textContent.trim();
                    if (text.includes('Based on') && text.includes('reviews')) {
                        ratingSelectors['review_count_element'] = el.outerHTML.substring(0, 200);
                        ratingSelectors['review_count_selector'] = el.tagName.toLowerCase() + 
                            (el.className ? '.' + el.className.split(' ').join('.') : '');
                    }
                });
                
                return ratingSelectors;
            }
        """)
        
        return selectors
    
    async def _extract_review_selectors(self) -> Dict[str, Any]:
        """Extract selectors for individual reviews"""
        print("   📝 Extracting review selectors...")
        
        selectors = await self.page.evaluate("""
            () => {
                const reviewSelectors = {};
                
                // Look for review containers
                const reviewContainers = document.querySelectorAll('article, .review, [class*="review"], [data-testid*="review"]');
                
                if (reviewContainers.length > 0) {
                    reviewSelectors['container_count'] = reviewContainers.length;
                    reviewSelectors['container_selector'] = 'article, .review, [class*="review"], [data-testid*="review"]';
                    
                    // Analyze first review structure
                    const firstReview = reviewContainers[0];
                    reviewSelectors['first_review_html'] = firstReview.outerHTML.substring(0, 500);
                    
                    // Look for review elements within containers
                    const reviewerName = firstReview.querySelector('h3, h4, .reviewer-name, [class*="name"]');
                    if (reviewerName) {
                        reviewSelectors['reviewer_name_selector'] = reviewerName.tagName.toLowerCase() + 
                            (reviewerName.className ? '.' + reviewerName.className.split(' ').join('.') : '');
                    }
                    
                    const reviewText = firstReview.querySelector('p, .review-text, [class*="text"]');
                    if (reviewText) {
                        reviewSelectors['review_text_selector'] = reviewText.tagName.toLowerCase() + 
                            (reviewText.className ? '.' + reviewText.className.split(' ').join('.') : '');
                    }
                    
                    const reviewDate = firstReview.querySelector('time, .date, [class*="date"]');
                    if (reviewDate) {
                        reviewSelectors['review_date_selector'] = reviewDate.tagName.toLowerCase() + 
                            (reviewDate.className ? '.' + reviewDate.className.split(' ').join('.') : '');
                    }
                }
                
                // Look for review rating elements
                const ratingElements = document.querySelectorAll('[class*="star"], [class*="rating"]');
                if (ratingElements.length > 0) {
                    reviewSelectors['rating_elements_count'] = ratingElements.length;
                    reviewSelectors['rating_selector'] = '[class*="star"], [class*="rating"]';
                }
                
                // Look for review filter/sort elements
                const filterElements = document.querySelectorAll('select, [class*="filter"], [class*="sort"]');
                if (filterElements.length > 0) {
                    reviewSelectors['filter_elements'] = filterElements.length;
                    reviewSelectors['filter_selector'] = 'select, [class*="filter"], [class*="sort"]';
                }
                
                return reviewSelectors;
            }
        """)
        
        return selectors
    
    async def _extract_pricing_selectors(self) -> Dict[str, str]:
        """Extract selectors for pricing information"""
        print("   💰 Extracting pricing selectors...")
        
        selectors = await self.page.evaluate("""
            () => {
                const pricingSelectors = {};
                
                // Look for pricing elements
                const pricingElements = document.querySelectorAll('[class*="price"], [class*="cost"], [class*="pricing"]');
                
                if (pricingElements.length > 0) {
                    pricingSelectors['pricing_elements_count'] = pricingElements.length;
                    pricingSelectors['pricing_selector'] = '[class*="price"], [class*="cost"], [class*="pricing"]';
                    
                    // Get first pricing element
                    const firstPricing = pricingElements[0];
                    pricingSelectors['first_pricing_html'] = firstPricing.outerHTML.substring(0, 300);
                }
                
                // Look for pricing text patterns
                const text = document.body.textContent;
                const pricingPatterns = [
                    /Starting from:\\s*\\$?([\\d,]+)/i,
                    /From\\s*\\$?([\\d,]+)/i,
                    /\\$([\\d,]+)\\s*per\\s*month/i,
                    /\\$([\\d,]+)\\s*\\/month/i
                ];
                
                for (let i = 0; i < pricingPatterns.length; i++) {
                    const match = text.match(pricingPatterns[i]);
                    if (match) {
                        pricingSelectors[`pricing_pattern_${i}`] = match[0];
                        break;
                    }
                }
                
                return pricingSelectors;
            }
        """)
        
        return selectors
    
    async def _extract_alternatives_selectors(self) -> Dict[str, str]:
        """Extract selectors for alternatives section"""
        print("   🔄 Extracting alternatives selectors...")
        
        selectors = await self.page.evaluate("""
            () => {
                const alternativesSelectors = {};
                
                // Look for alternatives section
                const alternativesSection = document.querySelector('[class*="alternative"], [class*="competitor"], #alternatives');
                
                if (alternativesSection) {
                    alternativesSelectors['alternatives_section'] = alternativesSection.outerHTML.substring(0, 500);
                    
                    // Look for alternative product cards
                    const alternativeCards = alternativesSection.querySelectorAll('.card, [class*="product"], [class*="alternative"]');
                    
                    if (alternativeCards.length > 0) {
                        alternativesSelectors['alternative_cards_count'] = alternativeCards.length;
                        alternativesSelectors['alternative_card_selector'] = '.card, [class*="product"], [class*="alternative"]';
                        
                        // Analyze first alternative card
                        const firstCard = alternativeCards[0];
                        alternativesSelectors['first_alternative_html'] = firstCard.outerHTML.substring(0, 400);
                    }
                }
                
                return alternativesSelectors;
            }
        """)
        
        return selectors
    
    async def _analyze_page_structure(self) -> Dict[str, Any]:
        """Analyze overall page structure"""
        print("   🏗️ Analyzing page structure...")
        
        structure = await self.page.evaluate("""
            () => {
                const structure = {
                    total_elements: document.querySelectorAll('*').length,
                    headings: [],
                    common_classes: {},
                    navigation_elements: [],
                    form_elements: [],
                    script_elements: []
                };
                
                // Analyze headings
                const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                headings.forEach((h, i) => {
                    structure.headings.push({
                        tag: h.tagName,
                        text: h.textContent.trim().substring(0, 100),
                        classes: h.className,
                        id: h.id
                    });
                });
                
                // Analyze common classes
                const classCounts = {};
                const allElements = document.querySelectorAll('*');
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
                
                // Get top 20 most common classes
                structure.common_classes = Object.entries(classCounts)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 20)
                    .reduce((obj, [key, value]) => {
                        obj[key] = value;
                        return obj;
                    }, {});
                
                // Analyze navigation elements
                const navElements = document.querySelectorAll('nav, [class*="nav"], [class*="menu"]');
                navElements.forEach((nav, i) => {
                    structure.navigation_elements.push({
                        tag: nav.tagName,
                        classes: nav.className,
                        text: nav.textContent.trim().substring(0, 100)
                    });
                });
                
                // Analyze form elements
                const formElements = document.querySelectorAll('form, input, select, textarea');
                structure.form_elements = formElements.length;
                
                // Analyze script elements
                const scriptElements = document.querySelectorAll('script');
                structure.script_elements = scriptElements.length;
                
                return structure;
            }
        """)
        
        return structure
    
    async def _save_selectors(self, selectors: Dict[str, Any], url: str):
        """Save extracted selectors to file"""
        output_dir = Path("output/selectors")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from URL
        url_parts = url.split('/')
        filename = f"selectors_{url_parts[-2] if len(url_parts) > 1 else 'unknown'}.json"
        
        # Save selectors
        selector_data = {
            'url': url,
            'extraction_timestamp': asyncio.get_event_loop().time(),
            'selectors': selectors
        }
        
        output_file = output_dir / filename
        with open(output_file, 'w') as f:
            json.dump(selector_data, f, indent=2)
        
        print(f"   💾 Selectors saved to: {output_file}")
    
    async def generate_playwright_selectors(self) -> Dict[str, str]:
        """Generate Playwright-compatible selectors from extracted data"""
        print("   🎭 Generating Playwright selectors...")
        
        playwright_selectors = {}
        
        # Company selectors
        if 'company_info' in self.extracted_selectors:
            company = self.extracted_selectors['company_info']
            if 'name' in company:
                playwright_selectors['company_name'] = company['name']
            if 'logo' in company:
                playwright_selectors['company_logo'] = company['logo']
        
        # Rating selectors
        if 'rating_info' in self.extracted_selectors:
            rating = self.extracted_selectors['rating_info']
            if 'review_count_element' in rating:
                playwright_selectors['review_count'] = rating['review_count_element']
        
        # Review selectors
        if 'reviews' in self.extracted_selectors:
            reviews = self.extracted_selectors['reviews']
            if 'container_selector' in reviews:
                playwright_selectors['review_container'] = reviews['container_selector']
            if 'reviewer_name_selector' in reviews:
                playwright_selectors['reviewer_name'] = reviews['reviewer_name_selector']
            if 'review_text_selector' in reviews:
                playwright_selectors['review_text'] = reviews['review_text_selector']
            if 'review_date_selector' in reviews:
                playwright_selectors['review_date'] = reviews['review_date_selector']
        
        # Pricing selectors
        if 'pricing' in self.extracted_selectors:
            pricing = self.extracted_selectors['pricing']
            if 'pricing_selector' in pricing:
                playwright_selectors['pricing'] = pricing['pricing_selector']
        
        # Alternatives selectors
        if 'alternatives' in self.extracted_selectors:
            alternatives = self.extracted_selectors['alternatives']
            if 'alternative_card_selector' in alternatives:
                playwright_selectors['alternative_card'] = alternatives['alternative_card_selector']
        
        return playwright_selectors

async def extract_selectors_from_capterra():
    """Extract selectors from Capterra pages"""
    print("🎯 Capterra Selector Extraction")
    print("=" * 50)
    
    from aura_lite import AuraLite
    
    aura_lite = None
    try:
        # Initialize AURA-LITE
        aura_lite = AuraLite()
        await aura_lite.setup_aura_browser()
        
        # Get targets
        targets = aura_lite.target_manager.get_targets_by_priority("high")
        
        # Extract selectors from each target
        all_selectors = {}
        
        for i, target in enumerate(targets[:3]):  # Test with first 3 targets
            company_name = target['data']['name']
            reviews_url = target['data']['targets']['product_reviews']
            
            print(f"\n{i+1}. Extracting selectors for: {company_name}")
            print(f"   URL: {reviews_url}")
            
            # Create extractor
            extractor = CapterraSelectorExtractor(aura_lite.page)
            
            # Extract selectors
            selectors = await extractor.extract_all_selectors(reviews_url)
            
            if selectors:
                all_selectors[company_name] = selectors
                print(f"   ✅ Successfully extracted selectors for {company_name}")
            else:
                print(f"   ❌ Failed to extract selectors for {company_name}")
        
        # Save combined selectors
        if all_selectors:
            output_file = Path("output/selectors/combined_capterra_selectors.json")
            with open(output_file, 'w') as f:
                json.dump(all_selectors, f, indent=2)
            print(f"\n💾 Combined selectors saved to: {output_file}")
        
        return all_selectors
        
    except Exception as e:
        logger.error(f"Error extracting selectors: {str(e)}")
        return {}
    
    finally:
        if aura_lite:
            await aura_lite.close()

if __name__ == "__main__":
    asyncio.run(extract_selectors_from_capterra())
