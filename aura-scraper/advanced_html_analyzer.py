#!/usr/bin/env python3
"""
Advanced HTML Analyzer for Capterra Review Extraction
Analyzes the provided HTML file to extract comprehensive review data
"""

import re
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime

class AdvancedCapterraHTMLAnalyzer:
    def __init__(self, html_file: str):
        self.html_file = html_file
        self.soup = None
        self.analysis_results = {}
        
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
    
    def analyze_comprehensive_reviews(self) -> Dict[str, Any]:
        """Analyze reviews with comprehensive data extraction"""
        if not self.soup:
            return {}
        
        print("🔍 Analyzing comprehensive review structure...")
        
        # Find all potential review containers
        review_containers = self._find_review_containers()
        print(f"📊 Found {len(review_containers)} potential review containers")
        
        if not review_containers:
            return {"error": "No review containers found"}
        
        # Analyze the first few reviews in detail
        detailed_reviews = []
        for i, container in enumerate(review_containers[:5]):  # Analyze first 5 reviews
            review_data = self._extract_detailed_review(container, i)
            if review_data:
                detailed_reviews.append(review_data)
        
        return {
            "total_containers": len(review_containers),
            "analyzed_reviews": len(detailed_reviews),
            "detailed_reviews": detailed_reviews,
            "container_patterns": self._analyze_container_patterns(review_containers)
        }
    
    def _find_review_containers(self) -> List[Any]:
        """Find all potential review containers using multiple strategies"""
        containers = []
        
        # Strategy 1: Look for divs with specific class patterns
        class_patterns = [
            r'flex.*md:flex-row.*md:items-start.*gap-3.*mb-2',
            r'flex.*gap-3.*mb-2',
            r'.*review.*',
            r'.*user.*review.*'
        ]
        
        for pattern in class_patterns:
            elements = self.soup.find_all('div', class_=re.compile(pattern, re.I))
            containers.extend(elements)
        
        # Strategy 2: Look for elements containing review titles
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
        
        # Remove duplicates
        unique_containers = []
        for container in containers:
            if container not in unique_containers:
                unique_containers.append(container)
        
        return unique_containers
    
    def _extract_detailed_review(self, container, index: int) -> Optional[Dict[str, Any]]:
        """Extract detailed information from a single review container"""
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
                "html_structure": {}
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
            
            # Extract reviewer information - look for patterns in the container
            reviewer_info = self._extract_reviewer_info(container)
            review_data.update(reviewer_info)
            
            # Extract review text
            review_text = self._extract_review_text(container)
            review_data.update(review_text)
            
            # Extract pros and cons
            pros_cons = self._extract_pros_cons(container)
            review_data.update(pros_cons)
            
            # Store HTML structure for analysis
            review_data["html_structure"] = {
                "container_classes": container.get('class', []),
                "container_tag": container.name,
                "child_elements": [child.name for child in container.find_all()[:10]]
            }
            
            return review_data
            
        except Exception as e:
            print(f"⚠️ Error extracting review {index}: {e}")
            return None
    
    def _extract_reviewer_info(self, container) -> Dict[str, str]:
        """Extract reviewer name, role, company, and date"""
        info = {
            "reviewer_name": "",
            "reviewer_role": "",
            "reviewer_company": "",
            "review_date": ""
        }
        
        # Look for spans with specific class patterns
        spans = container.find_all('span', class_=re.compile(r'text-typo-0.*text-neutral-90'))
        
        for span in spans:
            text = span.get_text(strip=True)
            
            # Check for name pattern (e.g., "Erika G.")
            if re.match(r'^[A-Z][a-z]+ [A-Z]\.$', text):
                info["reviewer_name"] = text
            
            # Check for role pattern (e.g., "Data Analyst")
            elif re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', text) and len(text.split()) == 2:
                info["reviewer_role"] = text
            
            # Check for company pattern (e.g., "Information Technology and Services")
            elif len(text.split()) >= 3 and any(word in text.lower() for word in ['technology', 'services', 'software', 'marketing', 'advertising']):
                info["reviewer_company"] = text
            
            # Check for date pattern (e.g., "August 9, 2025")
            elif re.match(r'^[A-Z][a-z]+ \d{1,2}, \d{4}$', text):
                info["review_date"] = text
        
        return info
    
    def _extract_review_text(self, container) -> Dict[str, str]:
        """Extract the main review text"""
        text_info = {"review_text": ""}
        
        # Look for paragraphs with review text
        paragraphs = container.find_all('p', class_=re.compile(r'text-typo-20.*text-neutral-90'))
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Skip short text that's likely not the main review
            if len(text) > 50 and not any(keyword in text.lower() for keyword in ['pros', 'cons', 'review source', 'continue reading']):
                text_info["review_text"] = text
                break
        
        return text_info
    
    def _extract_pros_cons(self, container) -> Dict[str, str]:
        """Extract pros and cons sections"""
        pros_cons = {"pros": "", "cons": ""}
        
        # Look for pros
        pros_elem = container.find('div', class_=re.compile(r'flex.*items-center.*gap-2.*mb-2'))
        if pros_elem:
            pros_text = pros_elem.find('p', class_=re.compile(r'text-typo-20.*text-neutral-90'))
            if pros_text:
                pros_cons["pros"] = pros_text.get_text(strip=True)
        
        # Look for cons
        cons_elem = container.find('div', class_=re.compile(r'flex.*items-center.*gap-2.*mb-2'))
        if cons_elem:
            cons_text = cons_elem.find('p', class_=re.compile(r'text-typo-20.*text-neutral-90'))
            if cons_text:
                pros_cons["cons"] = cons_text.get_text(strip=True)
        
        return pros_cons
    
    def _analyze_container_patterns(self, containers: List[Any]) -> Dict[str, Any]:
        """Analyze patterns in review containers"""
        patterns = {
            "common_classes": {},
            "common_structures": [],
            "element_counts": {}
        }
        
        for container in containers:
            # Analyze classes
            classes = container.get('class', [])
            for cls in classes:
                patterns["common_classes"][cls] = patterns["common_classes"].get(cls, 0) + 1
            
            # Analyze structure
            children = container.find_all()
            patterns["element_counts"][len(children)] = patterns["element_counts"].get(len(children), 0) + 1
        
        return patterns
    
    def generate_improved_selectors(self) -> Dict[str, str]:
        """Generate improved selectors based on analysis"""
        selectors = {
            "review_container": "div.flex.md\\:flex-row.md\\:items-start.gap-3.mb-2",
            "review_title": "h4.text-typo-20.font-semibold.text-neutral-99.flex-1",
            "star_rating": "div.flex.items-center.gap-1.mr-1",
            "reviewer_name": "span.text-typo-0.text-neutral-90",
            "reviewer_role": "span.text-typo-0.text-neutral-90",
            "reviewer_company": "span.text-typo-0.text-neutral-90",
            "review_date": "span.text-typo-0.text-neutral-90",
            "review_text": "p.text-typo-20.text-neutral-90",
            "pros_section": "div.flex.items-center.gap-2.mb-2",
            "cons_section": "div.flex.items-center.gap-2.mb-2"
        }
        
        return selectors
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run the complete analysis"""
        if not self.load_html():
            return {"error": "Failed to load HTML"}
        
        print("🚀 Starting comprehensive HTML analysis...")
        
        # Analyze reviews
        review_analysis = self.analyze_comprehensive_reviews()
        
        # Generate improved selectors
        improved_selectors = self.generate_improved_selectors()
        
        # Combine results
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "html_file": self.html_file,
            "review_analysis": review_analysis,
            "improved_selectors": improved_selectors,
            "recommendations": self._generate_recommendations(review_analysis)
        }
        
        return results
    
    def _generate_recommendations(self, review_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if review_analysis.get("analyzed_reviews", 0) > 0:
            recommendations.append("✅ Review containers found - extraction logic is working")
        
        if review_analysis.get("analyzed_reviews", 0) < 3:
            recommendations.append("⚠️ Limited review data extracted - may need selector refinement")
        
        recommendations.extend([
            "🔧 Use improved selectors for better data extraction",
            "📊 Implement fallback selectors for different page layouts",
            "🎯 Focus on extracting reviewer details and full review text"
        ])
        
        return recommendations

def main():
    """Main function to run the advanced HTML analysis"""
    html_file = "Looker Features, Alternatives & More 2025 _ Capterra.html"
    
    analyzer = AdvancedCapterraHTMLAnalyzer(html_file)
    results = analyzer.run_comprehensive_analysis()
    
    # Save results
    output_file = f"output/advanced_html_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Analysis results saved to: {output_file}")
    
    # Print summary
    print("\n📊 ANALYSIS SUMMARY:")
    print(f"Total review containers: {results.get('review_analysis', {}).get('total_containers', 0)}")
    print(f"Analyzed reviews: {results.get('review_analysis', {}).get('analyzed_reviews', 0)}")
    
    print("\n🎯 RECOMMENDATIONS:")
    for rec in results.get('recommendations', []):
        print(f"  {rec}")

if __name__ == "__main__":
    main()
