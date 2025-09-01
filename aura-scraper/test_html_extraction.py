#!/usr/bin/env python3
"""
Test HTML Extraction
Tests the extraction logic using the local HTML file to validate selectors and extraction logic.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLTestExtractor:
    def __init__(self, html_file_path: str):
        self.html_file_path = html_file_path
        self.soup = None
        
        # Precise selectors from HTML analysis (with escaped colons)
        self.selectors = {
            'company_info': {
                'name': 'h1.text-typo-70.lg\\:text-typo-95.font-bold.text-neutral-100',
                'logo': 'img.mr-2.object-contain.w-6.h-6.lg\\:w-8.lg\\:h-8.inline-flex.align-baseline'
            },
            'rating_info': {
                'overall_rating': 'div.flex.items-center.gap-1.mr-1',  # Star rating container
                'review_count': 'span.text-typo-0.text-neutral-90'  # Review count text
            },
            'reviews': {
                'container': 'div.flex.md\\:flex-row.md\\:items-start.gap-3.mb-2',
                'title': 'h4.text-typo-20.font-semibold.text-neutral-99.flex-1',
                'reviewer_name': 'span.text-typo-0.text-neutral-90',  # Pattern: "EGErika G."
                'reviewer_role': 'span.text-typo-0.text-neutral-90',  # Pattern: "Data Analyst"
                'reviewer_company': 'span.text-typo-0.text-neutral-90',  # Pattern: "Information Technology and Services"
                'review_date': 'span.text-typo-0.text-neutral-90',  # Pattern: "August 9, 2025"
                'star_rating': 'div.flex.items-center.gap-1.mr-1',  # Star rating
                'review_text': 'p.text-typo-20.text-neutral-90',  # Main review text
                'pros': 'div.flex.items-center.gap-2.mb-2',  # Pros section
                'cons': 'div.flex.items-center.gap-2.mb-2',  # Cons section
                'continue_reading': 'button.inline-flex.items-center.justify-center.rounded-lg.font-semibold.transition-colors'  # Continue reading button
            }
        }
    
    def load_html(self) -> bool:
        """Load and parse the HTML file"""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.soup = BeautifulSoup(content, 'html.parser')
            return True
        except Exception as e:
            logger.error(f"Error loading HTML: {e}")
            return False
    
    def extract_looker_data(self) -> Dict[str, Any]:
        """Extract comprehensive data from Looker HTML"""
        try:
            logger.info("Extracting data from HTML file")
            
            # Extract company info
            company_info = self._extract_company_info()
            
            # Extract rating info
            rating_info = self._extract_rating_info()
            
            # Extract all reviews
            reviews = self._extract_all_reviews()
            
            return {
                'company_info': company_info,
                'rating_info': rating_info,
                'reviews': reviews,
                'extraction_metadata': {
                    'html_file': self.html_file_path,
                    'total_reviews_found': len(reviews),
                    'extraction_method': 'html_file_analysis'
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return {}
    
    def _extract_company_info(self) -> Dict[str, Any]:
        """Extract company information"""
        company_info = {}
        
        try:
            # Company name
            name_element = self.soup.select_one(self.selectors['company_info']['name'])
            if name_element:
                company_info['name'] = name_element.get_text().strip()
            
            # Company logo
            logo_element = self.soup.select_one(self.selectors['company_info']['logo'])
            if logo_element:
                company_info['logo_url'] = logo_element.get('src', '')
            
        except Exception as e:
            logger.error(f"Failed to extract company info: {e}")
        
        return company_info
    
    def _extract_rating_info(self) -> Dict[str, Any]:
        """Extract rating information"""
        rating_info = {}
        
        try:
            # Overall rating
            rating_element = self.soup.select_one(self.selectors['rating_info']['overall_rating'])
            if rating_element:
                rating_info['overall_rating'] = rating_element.get_text().strip()
            
            # Review count
            count_elements = self.soup.select(self.selectors['rating_info']['review_count'])
            for element in count_elements:
                text = element.get_text().strip()
                if 'Based on' in text and 'reviews' in text:
                    rating_info['review_count'] = text
                    break
            
        except Exception as e:
            logger.error(f"Failed to extract rating info: {e}")
        
        return rating_info
    
    def _extract_all_reviews(self) -> List[Dict[str, Any]]:
        """Extract all reviews from the page"""
        reviews = []
        
        try:
            # Find all review containers
            review_containers = self.soup.select(self.selectors['reviews']['container'])
            logger.info(f"Found {len(review_containers)} review containers")
            
            for i, container in enumerate(review_containers):
                try:
                    review_data = self._extract_single_review(container, i)
                    if review_data:
                        reviews.append(review_data)
                except Exception as e:
                    logger.error(f"Failed to extract review {i}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Failed to extract reviews: {e}")
        
        return reviews
    
    def _extract_single_review(self, container, index: int) -> Dict[str, Any]:
        """Extract data from a single review container"""
        review_data = {
            'index': index,
            'title': '',
            'reviewer_name': '',
            'reviewer_role': '',
            'reviewer_company': '',
            'review_date': '',
            'star_rating': '',
            'review_text': '',
            'pros': '',
            'cons': '',
            'continue_reading_available': False
        }
        
        try:
            # Extract review title
            title_element = container.select_one(self.selectors['reviews']['title'])
            if title_element:
                review_data['title'] = title_element.get_text().strip()
            
            # Extract reviewer information
            reviewer_elements = container.select(self.selectors['reviews']['reviewer_name'])
            for element in reviewer_elements:
                text = element.get_text().strip()
                if text:
                    # Check if it's a name pattern (e.g., "EGErika G.")
                    if len(text.split()) == 2 and text.split()[1].endswith('.'):
                        review_data['reviewer_name'] = text
                    # Check if it's a role pattern
                    elif any(word in text.lower() for word in ['analyst', 'manager', 'director', 'engineer', 'developer', 'consultant']):
                        review_data['reviewer_role'] = text
                    # Check if it's a company pattern
                    elif any(word in text.lower() for word in ['services', 'technology', 'marketing', 'software', 'health', 'financial']):
                        review_data['reviewer_company'] = text
                    # Check if it's a date pattern
                    elif any(word in text.lower() for word in ['august', 'july', 'june', 'may', 'april', 'march', 'february', 'january', '2024', '2023', '2022']):
                        review_data['review_date'] = text
            
            # Extract star rating
            rating_element = container.select_one(self.selectors['reviews']['star_rating'])
            if rating_element:
                review_data['star_rating'] = rating_element.get_text().strip()
            
            # Extract review text
            text_elements = container.select(self.selectors['reviews']['review_text'])
            for element in text_elements:
                text = element.get_text().strip()
                if text and len(text) > 50 and not text.startswith('Pros') and not text.startswith('Cons'):
                    review_data['review_text'] = text
                    break
            
            # Extract pros and cons
            pros_cons_elements = container.select(self.selectors['reviews']['pros'])
            for element in pros_cons_elements:
                text = element.get_text().strip()
                if text:
                    if 'Pros' in text:
                        review_data['pros'] = text
                    elif 'Cons' in text:
                        review_data['cons'] = text
            
            # Check for continue reading button
            continue_button = container.select_one(self.selectors['reviews']['continue_reading'])
            if continue_button:
                review_data['continue_reading_available'] = True
            
        except Exception as e:
            logger.error(f"Failed to extract single review {index}: {e}")
        
        return review_data

def main():
    """Main function to test the HTML extraction"""
    html_file = "Looker Features, Alternatives & More 2025 _ Capterra.html"
    output_file = "output/looker_html_test_extraction.json"
    
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    extractor = HTMLTestExtractor(html_file)
    
    if extractor.load_html():
        logger.info("HTML loaded successfully")
        
        data = extractor.extract_looker_data()
        
        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Extraction complete. Results saved to {output_file}")
        logger.info(f"Extracted {len(data.get('reviews', []))} reviews")
        
        # Print summary
        if data.get('reviews'):
            print(f"\n=== EXTRACTION SUMMARY ===")
            print(f"Company: {data.get('company_info', {}).get('name', 'N/A')}")
            print(f"Total Reviews: {len(data['reviews'])}")
            
            # Show first few reviews
            for i, review in enumerate(data['reviews'][:3]):
                print(f"\n--- Review {i+1} ---")
                print(f"Title: {review.get('title', 'N/A')}")
                print(f"Reviewer: {review.get('reviewer_name', 'N/A')}")
                print(f"Role: {review.get('reviewer_role', 'N/A')}")
                print(f"Company: {review.get('reviewer_company', 'N/A')}")
                print(f"Date: {review.get('review_date', 'N/A')}")
                print(f"Rating: {review.get('star_rating', 'N/A')}")
                print(f"Text: {review.get('review_text', 'N/A')[:100]}...")
                print(f"Pros: {review.get('pros', 'N/A')}")
                print(f"Cons: {review.get('cons', 'N/A')}")
        
    else:
        logger.error("Failed to load HTML file")

if __name__ == "__main__":
    main()
