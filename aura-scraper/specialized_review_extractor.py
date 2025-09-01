#!/usr/bin/env python3
"""
Specialized Review Extractor for Capterra
Uses targeted pattern matching to extract review data from minified HTML
"""

import re
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime

class SpecializedReviewExtractor:
    def __init__(self, html_file: str):
        self.html_file = html_file
        self.soup = None
        
    def load_html(self) -> bool:
        """Load and parse the HTML file"""
        try:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.soup = BeautifulSoup(content, 'html.parser')
            print(f"✅ Loaded HTML file: {self.html_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading HTML file: {e}")
            return False
    
    def extract_reviews_by_pattern(self) -> Dict[str, Any]:
        """Extract reviews using pattern-based approach"""
        if not self.soup:
            return {"error": "HTML not loaded"}
        
        print("🔍 Extracting reviews using pattern-based approach...")
        
        # Get all text content
        all_text = self.soup.get_text()
        
        # Find review patterns using regex
        reviews = self._find_reviews_by_regex(all_text)
        
        return {
            "total_reviews": len(reviews),
            "reviews": reviews,
            "extraction_metadata": {
                "timestamp": datetime.now().isoformat(),
                "html_file": self.html_file,
                "method": "pattern_based_extraction"
            }
        }
    
    def _find_reviews_by_regex(self, text: str) -> List[Dict[str, Any]]:
        """Find reviews using regex patterns"""
        reviews = []
        
        # Pattern to find review blocks
        # Look for quoted titles followed by reviewer info and review text
        review_pattern = r'"([^"]+)"\s*([A-Z][a-z]+ [A-Z]\.)\s*([A-Z][a-z]+ [A-Z][a-z]+)\s*([A-Z][a-z]+(?: [A-Z][a-z]+)*(?: and [A-Z][a-z]+)*)\s*([A-Z][a-z]+ \d{1,2}, \d{4})\s*(.*?)(?="[^"]+"|$)'
        
        matches = re.finditer(review_pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            review_data = {
                "index": i,
                "title": match.group(1),
                "reviewer_name": match.group(2),
                "reviewer_role": match.group(3),
                "reviewer_company": match.group(4),
                "review_date": match.group(5),
                "review_text": match.group(6).strip()[:500] + "..." if len(match.group(6).strip()) > 500 else match.group(6).strip()
            }
            reviews.append(review_data)
        
        return reviews
    
    def extract_reviews_by_structure(self) -> Dict[str, Any]:
        """Extract reviews by analyzing HTML structure"""
        if not self.soup:
            return {"error": "HTML not loaded"}
        
        print("🔍 Extracting reviews by analyzing HTML structure...")
        
        # Find all elements that might contain reviews
        potential_reviews = []
        
        # Look for elements with review-like content
        all_elements = self.soup.find_all(['div', 'article', 'section'])
        
        for element in all_elements:
            text = element.get_text(strip=True)
            
            # Check if this element contains review-like content
            if self._is_review_element(text):
                review_data = self._extract_review_from_element(element)
                if review_data:
                    potential_reviews.append(review_data)
        
        return {
            "total_reviews": len(potential_reviews),
            "reviews": potential_reviews,
            "extraction_metadata": {
                "timestamp": datetime.now().isoformat(),
                "html_file": self.html_file,
                "method": "structure_based_extraction"
            }
        }
    
    def _is_review_element(self, text: str) -> bool:
        """Check if an element contains review-like content"""
        # Look for patterns that indicate a review
        review_indicators = [
            r'"[^"]+"',  # Quoted title
            r'[A-Z][a-z]+ [A-Z]\.',  # Name pattern
            r'[A-Z][a-z]+ [A-Z][a-z]+',  # Role pattern
            r'[A-Z][a-z]+ \d{1,2}, \d{4}',  # Date pattern
            r'Pros\s+',  # Pros section
            r'Cons\s+',  # Cons section
            r'Review source',  # Review source
            r'Continue reading'  # Continue reading
        ]
        
        # Count how many indicators are present
        indicator_count = sum(1 for pattern in review_indicators if re.search(pattern, text))
        
        # If we have at least 3 indicators, it's likely a review
        return indicator_count >= 3
    
    def _extract_review_from_element(self, element) -> Optional[Dict[str, Any]]:
        """Extract review data from a single element"""
        try:
            text = element.get_text(strip=True)
            
            review_data = {
                "title": "",
                "reviewer_name": "",
                "reviewer_role": "",
                "reviewer_company": "",
                "review_date": "",
                "review_text": "",
                "pros": "",
                "cons": "",
                "review_source": "",
                "continue_reading": False
            }
            
            # Extract title (quoted text)
            title_match = re.search(r'"([^"]+)"', text)
            if title_match:
                review_data["title"] = title_match.group(1)
            
            # Extract reviewer name
            name_match = re.search(r'([A-Z][a-z]+ [A-Z]\.)', text)
            if name_match:
                review_data["reviewer_name"] = name_match.group(1)
            
            # Extract reviewer role
            role_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
            if role_match:
                review_data["reviewer_role"] = role_match.group(1)
            
            # Extract reviewer company
            company_match = re.search(r'([A-Z][a-z]+(?: [A-Z][a-z]+)*(?: and [A-Z][a-z]+)*)', text)
            if company_match:
                potential_company = company_match.group(1)
                if len(potential_company.split()) >= 3:
                    review_data["reviewer_company"] = potential_company
            
            # Extract date
            date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', text)
            if date_match:
                review_data["review_date"] = date_match.group(1)
            
            # Extract review text (between title and pros/cons)
            if review_data["title"]:
                text_start = text.find(review_data["title"]) + len(review_data["title"])
                pros_start = text.find("Pros", text_start)
                cons_start = text.find("Cons", text_start)
                
                if pros_start > 0 or cons_start > 0:
                    end_pos = min(pros_start, cons_start) if pros_start > 0 and cons_start > 0 else (pros_start if pros_start > 0 else cons_start)
                    review_text = text[text_start:end_pos].strip()
                    if len(review_text) > 50:
                        review_data["review_text"] = review_text
            
            # Extract pros
            pros_match = re.search(r'Pros\s*(.*?)(?=Cons|Review source|Continue reading|$)', text, re.DOTALL | re.IGNORECASE)
            if pros_match:
                pros_text = pros_match.group(1).strip()
                if len(pros_text) > 10:
                    review_data["pros"] = pros_text
            
            # Extract cons
            cons_match = re.search(r'Cons\s*(.*?)(?=Review source|Continue reading|$)', text, re.DOTALL | re.IGNORECASE)
            if cons_match:
                cons_text = cons_match.group(1).strip()
                if len(cons_text) > 10:
                    review_data["cons"] = cons_text
            
            # Check for review source
            if "Review source" in text:
                review_data["review_source"] = "Capterra"
            
            # Check for continue reading
            if "Continue reading" in text:
                review_data["continue_reading"] = True
            
            return review_data
            
        except Exception as e:
            print(f"⚠️ Error extracting review from element: {e}")
            return None
    
    def run_comprehensive_extraction(self) -> Dict[str, Any]:
        """Run comprehensive extraction using multiple methods"""
        if not self.load_html():
            return {"error": "Failed to load HTML"}
        
        print("🚀 Starting comprehensive review extraction...")
        
        # Try pattern-based extraction
        pattern_results = self.extract_reviews_by_pattern()
        
        # Try structure-based extraction
        structure_results = self.extract_reviews_by_structure()
        
        # Combine results
        combined_results = {
            "pattern_based": pattern_results,
            "structure_based": structure_results,
            "extraction_metadata": {
                "timestamp": datetime.now().isoformat(),
                "html_file": self.html_file,
                "method": "comprehensive_extraction"
            }
        }
        
        return combined_results

def main():
    """Main function to run the specialized review extraction"""
    html_file = "Looker Features, Alternatives & More 2025 _ Capterra.html"
    
    extractor = SpecializedReviewExtractor(html_file)
    results = extractor.run_comprehensive_extraction()
    
    # Save results
    output_file = f"output/specialized_review_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Extraction results saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"Pattern-based reviews: {results.get('pattern_based', {}).get('total_reviews', 0)}")
    print(f"Structure-based reviews: {results.get('structure_based', {}).get('total_reviews', 0)}")
    
    # Print sample reviews
    if results.get('structure_based', {}).get('reviews'):
        print(f"\n📝 SAMPLE REVIEWS (Structure-based):")
        for i, review in enumerate(results['structure_based']['reviews'][:3]):
            print(f"\nReview {i+1}:")
            print(f"  Title: {review.get('title', 'N/A')}")
            print(f"  Reviewer: {review.get('reviewer_name', 'N/A')}")
            print(f"  Role: {review.get('reviewer_role', 'N/A')}")
            print(f"  Company: {review.get('reviewer_company', 'N/A')}")
            print(f"  Date: {review.get('review_date', 'N/A')}")
            print(f"  Text: {review.get('review_text', 'N/A')[:100]}...")
            print(f"  Pros: {review.get('pros', 'N/A')[:50]}...")
            print(f"  Cons: {review.get('cons', 'N/A')[:50]}...")

if __name__ == "__main__":
    main()
