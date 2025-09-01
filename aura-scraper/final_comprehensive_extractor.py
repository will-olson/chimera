#!/usr/bin/env python3
"""
Final Comprehensive Extractor for Capterra Reviews
Uses the specialized pattern matching approach for comprehensive review data extraction
"""

import re
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime

class FinalComprehensiveExtractor:
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
    
    def extract_all_reviews(self) -> Dict[str, Any]:
        """Extract all reviews with comprehensive data using specialized approach"""
        if not self.soup:
            return {"error": "HTML not loaded"}
        
        print("🔍 Extracting all reviews with comprehensive data...")
        
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
                "method": "final_comprehensive_extraction"
            }
        }
    
    def _find_all_review_containers(self) -> List[Any]:
        """Find all review containers using multiple strategies"""
        containers = []
        
        # Strategy 1: Look for divs with the specific review container pattern
        main_containers = self.soup.find_all('div', class_=re.compile(r'flex.*md:flex-row.*md:items-start.*gap-3.*mb-2'))
        containers.extend(main_containers)
        
        # Strategy 2: Look for elements containing review titles (quoted text)
        title_elements = self.soup.find_all('h4', string=re.compile(r'".*"'))
        for title in title_elements:
            parent = title.find_parent()
            if parent and parent not in containers:
                containers.append(parent)
        
        # Strategy 3: Look for elements with star ratings
        star_elements = self.soup.find_all('div', class_=re.compile(r'flex.*items-center.*gap-1'))
        for star in star_elements:
            if star.find('svg', class_=re.compile(r'star')):
                parent = star.find_parent()
                if parent and parent not in containers:
                    containers.append(parent)
        
        # Remove duplicates and return
        unique_containers = []
        for container in containers:
            if container not in unique_containers:
                unique_containers.append(container)
        
        return unique_containers
    
    def _extract_comprehensive_review(self, container, index: int) -> Optional[Dict[str, Any]]:
        """Extract comprehensive data from a single review container"""
        try:
            review_data = {
                "index": index,
                "title": "",
                "reviewer_name": "",
                "reviewer_role": "",
                "reviewer_company": "",
                "review_date": "",
                "star_rating": "",
                "review_text": "",
                "pros": "",
                "cons": "",
                "review_source": "",
                "continue_reading": False
            }
            
            # Extract title
            title_elem = container.find('h4', class_=re.compile(r'text-typo-20.*font-semibold.*text-neutral-99.*flex-1'))
            if title_elem:
                review_data["title"] = title_elem.get_text(strip=True)
            
            # Extract star rating
            star_elem = container.find('div', class_=re.compile(r'flex.*items-center.*gap-1.*mr-1'))
            if star_elem:
                stars = star_elem.find_all('svg', class_=re.compile(r'star'))
                if stars:
                    review_data["star_rating"] = f"{len(stars)}.0"
            
            # Extract reviewer information using advanced pattern matching
            reviewer_info = self._extract_reviewer_info_advanced(container)
            review_data.update(reviewer_info)
            
            # Extract review text using multiple strategies
            review_text = self._extract_review_text_advanced(container)
            review_data.update(review_text)
            
            # Extract pros and cons
            pros_cons = self._extract_pros_cons_advanced(container)
            review_data.update(pros_cons)
            
            # Extract review source and continue reading
            source_info = self._extract_source_info(container)
            review_data.update(source_info)
            
            return review_data
            
        except Exception as e:
            print(f"⚠️ Error extracting review {index}: {e}")
            return None
    
    def _extract_reviewer_info_advanced(self, container) -> Dict[str, str]:
        """Extract reviewer information using advanced pattern matching"""
        info = {
            "reviewer_name": "",
            "reviewer_role": "",
            "reviewer_company": "",
            "review_date": ""
        }
        
        # Get all text content from the container
        all_text = container.get_text()
        
        # Look for name pattern (e.g., "Erika G.")
        name_match = re.search(r'([A-Z][a-z]+ [A-Z]\.)', all_text)
        if name_match:
            info["reviewer_name"] = name_match.group(1)
        
        # Look for role pattern (e.g., "Data Analyst")
        role_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', all_text)
        if role_match:
            info["reviewer_role"] = role_match.group(1)
        
        # Look for company pattern (e.g., "Information Technology and Services")
        company_match = re.search(r'([A-Z][a-z]+(?: [A-Z][a-z]+)*(?: and [A-Z][a-z]+)*)', all_text)
        if company_match:
            potential_company = company_match.group(1)
            if len(potential_company.split()) >= 3 and any(word in potential_company.lower() for word in ['technology', 'services', 'software', 'marketing', 'advertising', 'health', 'wellness', 'fitness', 'financial', 'hospitality', 'machinery']):
                info["reviewer_company"] = potential_company
        
        # Look for date pattern (e.g., "August 9, 2025")
        date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', all_text)
        if date_match:
            info["review_date"] = date_match.group(1)
        
        return info
    
    def _extract_review_text_advanced(self, container) -> Dict[str, str]:
        """Extract review text using advanced strategies"""
        text_info = {"review_text": ""}
        
        # Strategy 1: Look for paragraphs with substantial text
        paragraphs = container.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 100 and not any(keyword in text.lower() for keyword in ['pros', 'cons', 'review source', 'continue reading', 'view less']):
                text_info["review_text"] = text
                break
        
        # Strategy 2: Look for divs with substantial text
        if not text_info["review_text"]:
            divs = container.find_all('div')
            for div in divs:
                text = div.get_text(strip=True)
                if len(text) > 100 and not any(keyword in text.lower() for keyword in ['pros', 'cons', 'review source', 'continue reading', 'view less']):
                    text_info["review_text"] = text
                    break
        
        return text_info
    
    def _extract_pros_cons_advanced(self, container) -> Dict[str, str]:
        """Extract pros and cons using advanced strategies"""
        pros_cons = {"pros": "", "cons": ""}
        
        # Get all text content
        all_text = container.get_text()
        
        # Look for pros section
        pros_match = re.search(r'Pros\s*(.*?)(?=Cons|Review source|Continue reading|$)', all_text, re.DOTALL | re.IGNORECASE)
        if pros_match:
            pros_text = pros_match.group(1).strip()
            if len(pros_text) > 10:
                pros_cons["pros"] = pros_text
        
        # Look for cons section
        cons_match = re.search(r'Cons\s*(.*?)(?=Review source|Continue reading|$)', all_text, re.DOTALL | re.IGNORECASE)
        if cons_match:
            cons_text = cons_match.group(1).strip()
            if len(cons_text) > 10:
                pros_cons["cons"] = cons_text
        
        return pros_cons
    
    def _extract_source_info(self, container) -> Dict[str, Any]:
        """Extract review source and continue reading information"""
        source_info = {
            "review_source": "",
            "continue_reading": False
        }
        
        # Check for review source
        if "Review source" in container.get_text():
            source_info["review_source"] = "Capterra"
        
        # Check for continue reading button
        if "Continue reading" in container.get_text():
            source_info["continue_reading"] = True
        
        return source_info
    
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
    
    def run_extraction(self) -> Dict[str, Any]:
        """Run the complete extraction process"""
        if not self.load_html():
            return {"error": "Failed to load HTML"}
        
        print("🚀 Starting final comprehensive review extraction...")
        
        # Extract all reviews
        results = self.extract_all_reviews()
        
        # Add summary statistics
        if "reviews" in results:
            total_reviews = len(results["reviews"])
            reviews_with_text = len([r for r in results["reviews"] if r.get("review_text")])
            reviews_with_reviewer = len([r for r in results["reviews"] if r.get("reviewer_name")])
            reviews_with_pros_cons = len([r for r in results["reviews"] if r.get("pros") or r.get("cons")])
            
            results["extraction_summary"] = {
                "total_reviews": total_reviews,
                "reviews_with_text": reviews_with_text,
                "reviews_with_reviewer": reviews_with_reviewer,
                "reviews_with_pros_cons": reviews_with_pros_cons,
                "extraction_success_rate": f"{(reviews_with_text / total_reviews * 100):.1f}%" if total_reviews > 0 else "0%"
            }
        
        return results

def main():
    """Main function to run the final comprehensive extraction"""
    html_file = "Looker Features, Alternatives & More 2025 _ Capterra.html"
    
    extractor = FinalComprehensiveExtractor(html_file)
    results = extractor.run_extraction()
    
    # Save results
    output_file = f"output/final_comprehensive_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Extraction results saved to: {output_file}")
    
    # Print summary
    if "extraction_summary" in results:
        summary = results["extraction_summary"]
        print(f"\n📊 EXTRACTION SUMMARY:")
        print(f"Total reviews: {summary['total_reviews']}")
        print(f"Reviews with text: {summary['reviews_with_text']}")
        print(f"Reviews with reviewer: {summary['reviews_with_reviewer']}")
        print(f"Reviews with pros/cons: {summary['reviews_with_pros_cons']}")
        print(f"Success rate: {summary['extraction_success_rate']}")
    
    # Print first few reviews as examples
    if "reviews" in results and results["reviews"]:
        print(f"\n📝 SAMPLE REVIEWS:")
        for i, review in enumerate(results["reviews"][:3]):
            print(f"\nReview {i+1}:")
            print(f"  Title: {review.get('title', 'N/A')}")
            print(f"  Reviewer: {review.get('reviewer_name', 'N/A')}")
            print(f"  Role: {review.get('reviewer_role', 'N/A')}")
            print(f"  Company: {review.get('reviewer_company', 'N/A')}")
            print(f"  Date: {review.get('review_date', 'N/A')}")
            print(f"  Rating: {review.get('star_rating', 'N/A')}")
            print(f"  Text: {review.get('review_text', 'N/A')[:100]}...")
            print(f"  Pros: {review.get('pros', 'N/A')[:50]}...")
            print(f"  Cons: {review.get('cons', 'N/A')[:50]}...")

if __name__ == "__main__":
    main()