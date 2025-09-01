#!/usr/bin/env python3
"""
Pattern Extractor for Capterra HTML Content
Extracts structured data from HTML chunks using comprehensive pattern matching
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup

class CapterraPatternExtractor:
    def __init__(self):
        """Initialize pattern extractor with comprehensive regex patterns"""
        self.patterns = self._initialize_patterns()
        self.extracted_data = {
            'reviews': [],
            'product_info': {},
            'comparisons': [],
            'pricing': {},
            'metadata': {}
        }
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, str]]:
        """Initialize comprehensive regex patterns for data extraction"""
        return {
            'reviews': {
                'container': r'<div[^>]*class="[^"]*review[^"]*"[^>]*>.*?</div>',
                'title': r'<h[1-6][^>]*>([^<]+)</h[1-6]>',
                'quoted_title': r'"([^"]+)"',
                'rating': r'<svg[^>]*class="[^"]*star[^"]*"[^>]*>',
                'rating_value': r'(\d+\.\d+)\s*\((\d+)\)',
                'reviewer_name': r'([A-Z][a-z]+ [A-Z]\.)',
                'reviewer_role': r'([A-Z][a-z]+ [A-Z][a-z]+)',
                'reviewer_company': r'([A-Z][a-z]+(?: [A-Z][a-z]+)*(?: and [A-Z][a-z]+)*)',
                'review_date': r'([A-Z][a-z]+ \d{1,2}, \d{4})',
                'pros': r'Pros\s*(.*?)(?=Cons|Review source|Continue reading|$)',
                'cons': r'Cons\s*(.*?)(?=Review source|Continue reading|$)',
                'review_text': r'([^"]{50,}?)(?=Pros|Cons|Review source|Continue reading|$)',
                'source': r'Review source',
                'continue_reading': r'Continue reading'
            },
            'product_info': {
                'name': r'<title>([^<]+)</title>',
                'description': r'<meta name="description" content="([^"]+)"',
                'category': r'<a[^>]*href="[^"]*/([^/]+)/"[^>]*>([^<]+)</a>',
                'features': r'<li[^>]*>([^<]+)</li>',
                'overall_rating': r'(\d+\.\d+)\s*Based on\s*(\d+)\s*reviews',
                'badges': r'<img[^>]*alt="([^"]*badge[^"]*)"[^>]*>'
            },
            'pricing': {
                'price': r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',
                'price_period': r'per\s+(month|year|user|seat)',
                'free_trial': r'free trial',
                'free_version': r'free version',
                'pricing_plan': r'<h[1-6][^>]*>([^<]*pricing[^<]*)</h[1-6]>'
            },
            'comparisons': {
                'vs_pattern': r'([A-Z][a-z]+)\s+vs\.?\s+([A-Z][a-z]+)',
                'comparison_table': r'<table[^>]*>.*?</table>',
                'feature_comparison': r'<tr[^>]*>.*?<td[^>]*>([^<]+)</td>.*?</tr>',
                'rating_comparison': r'(\d+\.\d+)\s*\((\d+)\)'
            },
            'metadata': {
                'breadcrumb': r'<nav[^>]*aria-label="Breadcrumb"[^>]*>.*?</nav>',
                'last_updated': r'Last updated on\s+([^<]+)',
                'page_type': r'<meta property="og:type" content="([^"]+)"',
                'canonical_url': r'<link rel="canonical" href="([^"]+)"'
            }
        }
    
    def extract_from_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data from a single HTML chunk
        
        Args:
            chunk: Chunk dictionary with content and metadata
            
        Returns:
            Extracted data dictionary
        """
        content = chunk['content']
        chunk_metadata = {
            'chunk_index': chunk['index'],
            'file_path': chunk['file_path'],
            'chunk_size': chunk['size'],
            'has_reviews': chunk['has_reviews'],
            'has_comparison': chunk['has_comparison'],
            'has_pricing': chunk['has_pricing']
        }
        
        extracted = {
            'chunk_metadata': chunk_metadata,
            'reviews': [],
            'product_info': {},
            'comparisons': [],
            'pricing': {},
            'metadata': {}
        }
        
        # Extract reviews if chunk contains review content
        if chunk['has_reviews']:
            extracted['reviews'] = self._extract_reviews(content)
        
        # Extract product information
        extracted['product_info'] = self._extract_product_info(content)
        
        # Extract comparisons if chunk contains comparison content
        if chunk['has_comparison']:
            extracted['comparisons'] = self._extract_comparisons(content)
        
        # Extract pricing information
        if chunk['has_pricing']:
            extracted['pricing'] = self._extract_pricing(content)
        
        # Extract metadata
        extracted['metadata'] = self._extract_metadata(content)
        
        return extracted
    
    def _extract_reviews(self, content: str) -> List[Dict[str, Any]]:
        """Extract review data from content"""
        reviews = []
        
        # Find review containers using multiple strategies
        review_containers = self._find_review_containers(content)
        
        for i, container in enumerate(review_containers):
            review_data = self._extract_single_review(container, i)
            if review_data:
                reviews.append(review_data)
        
        return reviews
    
    def _find_review_containers(self, content: str) -> List[str]:
        """Find review containers using multiple strategies"""
        containers = []
        
        # Strategy 1: Look for divs with review class
        review_divs = re.findall(
            r'<div[^>]*class="[^"]*review[^"]*"[^>]*>.*?</div>',
            content, re.DOTALL | re.IGNORECASE
        )
        containers.extend(review_divs)
        
        # Strategy 2: Look for elements with pros/cons
        pros_cons_elements = re.findall(
            r'<div[^>]*>.*?Pros.*?Cons.*?</div>',
            content, re.DOTALL | re.IGNORECASE
        )
        containers.extend(pros_cons_elements)
        
        # Strategy 3: Look for elements with star ratings
        star_elements = re.findall(
            r'<div[^>]*>.*?<svg[^>]*class="[^"]*star[^"]*"[^>]*>.*?</div>',
            content, re.DOTALL | re.IGNORECASE
        )
        containers.extend(star_elements)
        
        # Strategy 4: Look for elements with reviewer names
        reviewer_elements = re.findall(
            r'<div[^>]*>.*?([A-Z][a-z]+ [A-Z]\.).*?</div>',
            content, re.DOTALL | re.IGNORECASE
        )
        containers.extend(reviewer_elements)
        
        # Remove duplicates and return
        unique_containers = []
        for container in containers:
            if container not in unique_containers:
                unique_containers.append(container)
        
        return unique_containers
    
    def _extract_single_review(self, container: str, index: int) -> Optional[Dict[str, Any]]:
        """Extract data from a single review container"""
        try:
            review_data = {
                'index': index,
                'title': '',
                'rating': '',
                'reviewer_name': '',
                'reviewer_role': '',
                'reviewer_company': '',
                'review_date': '',
                'review_text': '',
                'pros': '',
                'cons': '',
                'source': '',
                'continue_reading': False
            }
            
            # Extract title (quoted text)
            title_match = re.search(self.patterns['reviews']['quoted_title'], container)
            if title_match:
                review_data['title'] = title_match.group(1)
            
            # Extract rating
            rating_matches = re.findall(self.patterns['reviews']['rating'], container)
            if rating_matches:
                review_data['rating'] = f"{len(rating_matches)}.0"
            
            # Extract reviewer information
            name_match = re.search(self.patterns['reviews']['reviewer_name'], container)
            if name_match:
                review_data['reviewer_name'] = name_match.group(1)
            
            role_match = re.search(self.patterns['reviews']['reviewer_role'], container)
            if role_match:
                review_data['reviewer_role'] = role_match.group(1)
            
            company_match = re.search(self.patterns['reviews']['reviewer_company'], container)
            if company_match:
                potential_company = company_match.group(1)
                if len(potential_company.split()) >= 3:
                    review_data['reviewer_company'] = potential_company
            
            # Extract date
            date_match = re.search(self.patterns['reviews']['review_date'], container)
            if date_match:
                review_data['review_date'] = date_match.group(1)
            
            # Extract review text
            text_match = re.search(self.patterns['reviews']['review_text'], container, re.DOTALL)
            if text_match:
                review_data['review_text'] = text_match.group(1).strip()
            
            # Extract pros
            pros_match = re.search(self.patterns['reviews']['pros'], container, re.DOTALL | re.IGNORECASE)
            if pros_match:
                review_data['pros'] = pros_match.group(1).strip()
            
            # Extract cons
            cons_match = re.search(self.patterns['reviews']['cons'], container, re.DOTALL | re.IGNORECASE)
            if cons_match:
                review_data['cons'] = cons_match.group(1).strip()
            
            # Check for review source
            if re.search(self.patterns['reviews']['source'], container, re.IGNORECASE):
                review_data['source'] = 'Capterra'
            
            # Check for continue reading
            if re.search(self.patterns['reviews']['continue_reading'], container, re.IGNORECASE):
                review_data['continue_reading'] = True
            
            # Only return if we have meaningful data
            if any([review_data['title'], review_data['reviewer_name'], review_data['pros'], review_data['cons']]):
                return review_data
            
        except Exception as e:
            print(f"⚠️ Error extracting review {index}: {e}")
        
        return None
    
    def _extract_product_info(self, content: str) -> Dict[str, Any]:
        """Extract product information from content"""
        product_info = {}
        
        # Extract title
        title_match = re.search(self.patterns['product_info']['name'], content)
        if title_match:
            product_info['title'] = title_match.group(1)
        
        # Extract description
        desc_match = re.search(self.patterns['product_info']['description'], content)
        if desc_match:
            product_info['description'] = desc_match.group(1)
        
        # Extract overall rating
        rating_match = re.search(self.patterns['product_info']['overall_rating'], content)
        if rating_match:
            product_info['overall_rating'] = rating_match.group(1)
            product_info['review_count'] = rating_match.group(2)
        
        # Extract categories
        categories = re.findall(self.patterns['product_info']['category'], content)
        if categories:
            product_info['categories'] = [cat[1] for cat in categories]
        
        # Extract features
        features = re.findall(self.patterns['product_info']['features'], content)
        if features:
            product_info['features'] = features[:10]  # Limit to first 10 features
        
        return product_info
    
    def _extract_comparisons(self, content: str) -> List[Dict[str, Any]]:
        """Extract comparison data from content"""
        comparisons = []
        
        # Extract vs patterns
        vs_matches = re.findall(self.patterns['comparisons']['vs_pattern'], content)
        for match in vs_matches:
            comparisons.append({
                'type': 'vs_comparison',
                'product1': match[0],
                'product2': match[1]
            })
        
        # Extract rating comparisons
        rating_matches = re.findall(self.patterns['comparisons']['rating_comparison'], content)
        for match in rating_matches:
            comparisons.append({
                'type': 'rating_comparison',
                'rating': match[0],
                'review_count': match[1]
            })
        
        return comparisons
    
    def _extract_pricing(self, content: str) -> Dict[str, Any]:
        """Extract pricing information from content"""
        pricing = {}
        
        # Extract prices
        prices = re.findall(self.patterns['pricing']['price'], content)
        if prices:
            pricing['prices'] = prices
        
        # Extract price periods
        periods = re.findall(self.patterns['pricing']['price_period'], content, re.IGNORECASE)
        if periods:
            pricing['periods'] = list(set(periods))
        
        # Check for free trial
        if re.search(self.patterns['pricing']['free_trial'], content, re.IGNORECASE):
            pricing['free_trial'] = True
        
        # Check for free version
        if re.search(self.patterns['pricing']['free_version'], content, re.IGNORECASE):
            pricing['free_version'] = True
        
        return pricing
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from content"""
        metadata = {}
        
        # Extract last updated date
        updated_match = re.search(self.patterns['metadata']['last_updated'], content)
        if updated_match:
            metadata['last_updated'] = updated_match.group(1)
        
        # Extract page type
        page_type_match = re.search(self.patterns['metadata']['page_type'], content)
        if page_type_match:
            metadata['page_type'] = page_type_match.group(1)
        
        # Extract canonical URL
        url_match = re.search(self.patterns['metadata']['canonical_url'], content)
        if url_match:
            metadata['canonical_url'] = url_match.group(1)
        
        return metadata
    
    def process_chunks(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple chunks and combine results
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Combined extracted data
        """
        print(f"🔍 Processing {len(chunks)} chunks...")
        
        all_reviews = []
        all_product_info = {}
        all_comparisons = []
        all_pricing = {}
        all_metadata = {}
        
        for chunk in chunks:
            extracted = self.extract_from_chunk(chunk)
            
            # Combine reviews
            all_reviews.extend(extracted['reviews'])
            
            # Merge product info
            all_product_info.update(extracted['product_info'])
            
            # Combine comparisons
            all_comparisons.extend(extracted['comparisons'])
            
            # Merge pricing
            all_pricing.update(extracted['pricing'])
            
            # Merge metadata
            all_metadata.update(extracted['metadata'])
        
        # Deduplicate reviews
        unique_reviews = self._deduplicate_reviews(all_reviews)
        
        result = {
            'extraction_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_chunks_processed': len(chunks),
                'total_reviews_found': len(all_reviews),
                'unique_reviews': len(unique_reviews),
                'extraction_method': 'pattern_based_extraction'
            },
            'reviews': unique_reviews,
            'product_info': all_product_info,
            'comparisons': all_comparisons,
            'pricing': all_pricing,
            'metadata': all_metadata
        }
        
        print(f"✅ Extraction complete: {len(unique_reviews)} unique reviews found")
        return result
    
    def _deduplicate_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate reviews based on title and reviewer"""
        unique_reviews = []
        seen = set()
        
        for review in reviews:
            # Create a unique identifier
            identifier = f"{review.get('title', '')}_{review.get('reviewer_name', '')}_{review.get('review_date', '')}"
            
            if identifier not in seen and identifier.strip():
                seen.add(identifier)
                unique_reviews.append(review)
        
        return unique_reviews

def main():
    """Main function to demonstrate pattern extraction"""
    from html_chunker import HTMLChunker
    
    # Initialize chunker and extractor
    chunker = HTMLChunker(chunk_size=50000, overlap_size=5000)
    extractor = CapterraPatternExtractor()
    
    # Process a sample file
    sample_file = "capterraHTML/Looker Features, Alternatives & More 2025 _ Capterra.html"
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file {sample_file} not found")
        return
    
    print(f"🔍 Processing sample file: {sample_file}")
    
    # Create chunks
    chunks = chunker.create_chunks(sample_file)
    
    # Extract data
    extracted_data = extractor.process_chunks(chunks)
    
    # Save results
    output_file = f"output/pattern_extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs("output", exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Results saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"Total reviews found: {len(extracted_data['reviews'])}")
    print(f"Product info fields: {len(extracted_data['product_info'])}")
    print(f"Comparisons found: {len(extracted_data['comparisons'])}")
    print(f"Pricing info fields: {len(extracted_data['pricing'])}")

if __name__ == "__main__":
    import os
    main()
