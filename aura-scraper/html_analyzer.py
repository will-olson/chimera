#!/usr/bin/env python3
"""
HTML Analyzer for Capterra Review Structure
Analyzes the provided HTML file to extract precise selectors for comprehensive review data extraction.
"""

import re
import json
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from pathlib import Path

class CapterraHTMLAnalyzer:
    def __init__(self, html_file_path: str):
        self.html_file_path = html_file_path
        self.soup = None
        self.selectors = {}
        
    def load_html(self) -> bool:
        """Load and parse the HTML file"""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.soup = BeautifulSoup(content, 'html.parser')
            return True
        except Exception as e:
            print(f"Error loading HTML: {e}")
            return False
    
    def analyze_review_structure(self) -> Dict[str, Any]:
        """Analyze the review structure and extract selectors"""
        if not self.soup:
            return {}
        
        analysis = {
            'company_info': self._analyze_company_info(),
            'rating_info': self._analyze_rating_info(),
            'reviews': self._analyze_reviews(),
            'pricing': self._analyze_pricing(),
            'alternatives': self._analyze_alternatives(),
            'page_structure': self._analyze_page_structure()
        }
        
        return analysis
    
    def _analyze_company_info(self) -> Dict[str, Any]:
        """Analyze company information selectors"""
        company_info = {}
        
        # Company name
        h1_elements = self.soup.find_all('h1')
        for h1 in h1_elements:
            if 'Reviews of' in h1.get_text():
                company_info['name_selector'] = self._get_selector(h1)
                company_info['name_text'] = h1.get_text().strip()
                break
        
        # Logo
        logo_elements = self.soup.find_all('img', alt=True)
        for img in logo_elements:
            if 'logo' in img.get('alt', '').lower():
                company_info['logo_selector'] = self._get_selector(img)
                company_info['logo_url'] = img.get('src', '')
                break
        
        return company_info
    
    def _analyze_rating_info(self) -> Dict[str, Any]:
        """Analyze rating information selectors"""
        rating_info = {}
        
        # Overall rating
        rating_elements = self.soup.find_all(['div', 'span'], class_=re.compile(r'rating|star'))
        for element in rating_elements:
            if 'star' in element.get('class', []) or 'rating' in element.get('class', []):
                rating_info['overall_rating_selector'] = self._get_selector(element)
                break
        
        # Review count
        text_elements = self.soup.find_all(['p', 'span', 'div'])
        for element in text_elements:
            text = element.get_text().strip()
            if 'Based on' in text and 'reviews' in text:
                rating_info['review_count_selector'] = self._get_selector(element)
                rating_info['review_count_text'] = text
                break
        
        return rating_info
    
    def _analyze_reviews(self) -> Dict[str, Any]:
        """Analyze review structure and selectors"""
        reviews_info = {}
        
        # Find review containers using multiple strategies
        review_containers = []
        
        # Strategy 1: Look for common review container patterns
        container_selectors = [
            'article',
            '[class*="review"]',
            '[data-testid*="review"]',
            '.review',
            '[class*="user-review"]',
            '[class*="testimonial"]'
        ]
        
        for selector in container_selectors:
            elements = self.soup.select(selector)
            if elements:
                review_containers.extend(elements)
        
        # Strategy 2: Look for review titles (H4 elements with quotes)
        review_titles = self.soup.find_all('h4', class_=re.compile(r'text-typo-20.*font-semibold.*text-neutral-99.*flex-1'))
        if review_titles:
            # Find parent containers of these titles
            for title in review_titles:
                parent = title.find_parent()
                if parent and parent not in review_containers:
                    review_containers.append(parent)
        
        # Strategy 3: Look for elements containing review text patterns
        text_elements = self.soup.find_all(['div', 'p'], string=re.compile(r'Pros|Cons|Review source|Continue reading'))
        for element in text_elements:
            parent = element.find_parent()
            if parent and parent not in review_containers:
                review_containers.append(parent)
        
        # Remove duplicates
        review_containers = list(set(review_containers))
        reviews_info['container_count'] = len(review_containers)
        
        if review_containers:
            # Analyze first review container
            first_review = review_containers[0]
            reviews_info['container_selector'] = self._get_selector(first_review)
            reviews_info['first_review_html'] = str(first_review)[:500] + "..."
            
            # Extract review elements
            review_elements = self._extract_review_elements(first_review)
            reviews_info.update(review_elements)
        
        return reviews_info
    
    def _extract_review_elements(self, review_container) -> Dict[str, Any]:
        """Extract specific review elements from a review container"""
        elements = {}
        
        # Review title (H4 with specific classes)
        title_elements = review_container.find_all('h4', class_=re.compile(r'text-typo-20.*font-semibold.*text-neutral-99.*flex-1'))
        for element in title_elements:
            text = element.get_text().strip()
            if text.startswith('"') and text.endswith('"'):
                elements['review_title_selector'] = self._get_selector(element)
                elements['review_title_text'] = text
                break
        
        # Reviewer name (look for patterns like "EGErika G." or "Parsa G.")
        name_elements = review_container.find_all(['span', 'div', 'p'], class_=re.compile(r'text-typo-0.*text-neutral-90'))
        for element in name_elements:
            text = element.get_text().strip()
            # Look for patterns like "EGErika G." or "Parsa G."
            if re.match(r'^[A-Z]{1,3}[A-Za-z]+\s+[A-Z]\.$', text):
                elements['reviewer_name_selector'] = self._get_selector(element)
                elements['reviewer_name_text'] = text
                break
        
        # Reviewer role/company
        role_elements = review_container.find_all(['span', 'div', 'p'], class_=re.compile(r'text-typo-0.*text-neutral-90'))
        for element in role_elements:
            text = element.get_text().strip()
            # Look for role patterns like "Data Analyst" or "Information Technology and Services"
            if any(word in text.lower() for word in ['analyst', 'manager', 'director', 'engineer', 'developer', 'consultant', 'services', 'technology', 'marketing', 'sales']):
                elements['reviewer_role_selector'] = self._get_selector(element)
                elements['reviewer_role_text'] = text
                break
        
        # Review date
        date_elements = review_container.find_all(['span', 'div', 'p'], class_=re.compile(r'text-typo-0.*text-neutral-90'))
        for element in date_elements:
            text = element.get_text().strip()
            if any(word in text.lower() for word in ['august', 'july', 'june', 'may', 'april', 'march', 'february', 'january', '2024', '2023', '2022']):
                elements['review_date_selector'] = self._get_selector(element)
                elements['review_date_text'] = text
                break
        
        # Review text (look for longer text content)
        text_elements = review_container.find_all(['p', 'div'], class_=re.compile(r'text-typo-20.*text-neutral-90'))
        for element in text_elements:
            text = element.get_text().strip()
            if len(text) > 100 and not text.startswith('Pros') and not text.startswith('Cons'):
                elements['review_text_selector'] = self._get_selector(element)
                elements['review_text_preview'] = text[:200] + "..."
                break
        
        # Star rating (look for rating patterns)
        rating_elements = review_container.find_all(['span', 'div'], class_=re.compile(r'text-typo-0.*text-neutral-90'))
        for element in rating_elements:
            text = element.get_text().strip()
            if re.match(r'^\d+\.\d+$', text) or text in ['5.0', '4.0', '3.0', '2.0', '1.0']:
                elements['star_rating_selector'] = self._get_selector(element)
                elements['star_rating_text'] = text
                break
        
        # Pros and Cons
        pros_cons = self._extract_pros_cons(review_container)
        elements.update(pros_cons)
        
        return elements
    
    def _extract_pros_cons(self, review_container) -> Dict[str, Any]:
        """Extract pros and cons from review container"""
        pros_cons = {}
        
        # Look for pros
        pros_elements = review_container.find_all(['div', 'p'], class_=re.compile(r'pro|positive|advantage'))
        for element in pros_elements:
            text = element.get_text().strip()
            if 'pro' in text.lower() or 'positive' in text.lower():
                pros_cons['pros_selector'] = self._get_selector(element)
                pros_cons['pros_text'] = text
                break
        
        # Look for cons
        cons_elements = review_container.find_all(['div', 'p'], class_=re.compile(r'con|negative|disadvantage'))
        for element in cons_elements:
            text = element.get_text().strip()
            if 'con' in text.lower() or 'negative' in text.lower():
                pros_cons['cons_selector'] = self._get_selector(element)
                pros_cons['cons_text'] = text
                break
        
        return pros_cons
    
    def _analyze_pricing(self) -> Dict[str, Any]:
        """Analyze pricing information selectors"""
        pricing_info = {}
        
        # Look for pricing elements
        pricing_elements = self.soup.find_all(['div', 'span', 'p'], class_=re.compile(r'price|cost|pricing'))
        for element in pricing_elements:
            text = element.get_text().strip()
            if any(char in text for char in ['$', '€', '£', '¥']) or 'free' in text.lower():
                pricing_info['pricing_selector'] = self._get_selector(element)
                pricing_info['pricing_text'] = text
                break
        
        return pricing_info
    
    def _analyze_alternatives(self) -> Dict[str, Any]:
        """Analyze alternatives section selectors"""
        alternatives_info = {}
        
        # Look for alternatives section
        alt_elements = self.soup.find_all(['div', 'section'], class_=re.compile(r'alternative|competitor|similar'))
        for element in alt_elements:
            if 'alternative' in element.get('class', []) or 'competitor' in element.get('class', []):
                alternatives_info['alternatives_selector'] = self._get_selector(element)
                break
        
        return alternatives_info
    
    def _analyze_page_structure(self) -> Dict[str, Any]:
        """Analyze overall page structure"""
        structure = {}
        
        # Count elements
        structure['total_elements'] = len(self.soup.find_all())
        structure['headings'] = []
        
        # Analyze headings
        for i in range(1, 7):
            headings = self.soup.find_all(f'h{i}')
            for heading in headings:
                structure['headings'].append({
                    'tag': f'H{i}',
                    'text': heading.get_text().strip()[:100],
                    'classes': ' '.join(heading.get('class', []))
                })
        
        # Analyze common classes
        class_counts = {}
        all_elements = self.soup.find_all()
        for element in all_elements:
            classes = element.get('class', [])
            for cls in classes:
                if len(cls) > 2:  # Filter out very short class names
                    class_counts[cls] = class_counts.get(cls, 0) + 1
        
        # Get top 10 most common classes
        structure['common_classes'] = dict(sorted(class_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return structure
    
    def _get_selector(self, element) -> str:
        """Generate a CSS selector for an element"""
        if not element:
            return ""
        
        # Try to create a unique selector
        tag = element.name
        classes = element.get('class', [])
        
        if classes:
            class_selector = '.' + '.'.join(classes)
            return f"{tag}{class_selector}"
        else:
            return tag
    
    def save_analysis(self, output_file: str) -> bool:
        """Save the analysis to a JSON file"""
        try:
            analysis = self.analyze_review_structure()
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return False

def main():
    """Main function to analyze the HTML file"""
    html_file = "Looker Features, Alternatives & More 2025 _ Capterra.html"
    output_file = "output/looker_html_analysis.json"
    
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    analyzer = CapterraHTMLAnalyzer(html_file)
    
    if analyzer.load_html():
        print("HTML loaded successfully")
        
        analysis = analyzer.analyze_review_structure()
        print(f"Analysis complete. Found {analysis.get('reviews', {}).get('container_count', 0)} review containers")
        
        if analyzer.save_analysis(output_file):
            print(f"Analysis saved to {output_file}")
        else:
            print("Failed to save analysis")
    else:
        print("Failed to load HTML file")

if __name__ == "__main__":
    main()
