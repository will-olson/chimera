#!/usr/bin/env python3
"""
HTML Chunker for Large Capterra Files
Intelligently splits large HTML files into manageable chunks while preserving structure
"""

import re
import os
from typing import List, Dict, Any, Tuple
from pathlib import Path

class HTMLChunker:
    def __init__(self, chunk_size: int = 50000, overlap_size: int = 5000):
        """
        Initialize HTML chunker
        
        Args:
            chunk_size: Maximum characters per chunk
            overlap_size: Characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.html_structure_markers = [
            r'<div[^>]*class="[^"]*review[^"]*"[^>]*>',
            r'<section[^>]*>',
            r'<article[^>]*>',
            r'<main[^>]*>',
            r'<header[^>]*>',
            r'<footer[^>]*>',
            r'<nav[^>]*>',
            r'<aside[^>]*>'
        ]
    
    def create_chunks(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Create intelligent chunks from HTML file
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            List of chunk dictionaries with metadata
        """
        print(f"📁 Processing file: {file_path}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size = len(content)
        print(f"📊 File size: {file_size:,} characters")
        
        # Create chunks
        chunks = self._split_into_chunks(content, file_path)
        
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    def _split_into_chunks(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Split content into intelligent chunks
        
        Args:
            content: HTML content
            file_path: Original file path
            
        Returns:
            List of chunk dictionaries
        """
        chunks = []
        start_pos = 0
        chunk_index = 0
        
        while start_pos < len(content):
            # Calculate end position
            end_pos = min(start_pos + self.chunk_size, len(content))
            
            # Try to find a good break point
            if end_pos < len(content):
                end_pos = self._find_break_point(content, start_pos, end_pos)
            
            # Extract chunk content
            chunk_content = content[start_pos:end_pos]
            
            # Create chunk metadata
            chunk = {
                'index': chunk_index,
                'file_path': file_path,
                'start_pos': start_pos,
                'end_pos': end_pos,
                'size': len(chunk_content),
                'content': chunk_content,
                'has_reviews': self._contains_reviews(chunk_content),
                'has_comparison': self._contains_comparison(chunk_content),
                'has_pricing': self._contains_pricing(chunk_content),
                'structure_elements': self._identify_structure_elements(chunk_content)
            }
            
            chunks.append(chunk)
            
            # Move to next chunk with overlap
            start_pos = max(end_pos - self.overlap_size, start_pos + 1)
            chunk_index += 1
        
        return chunks
    
    def _find_break_point(self, content: str, start_pos: int, end_pos: int) -> int:
        """
        Find a good break point within the chunk size limit
        
        Args:
            content: HTML content
            start_pos: Start position of current chunk
            end_pos: Maximum end position
            
        Returns:
            Optimal end position
        """
        # Look for HTML tag boundaries
        search_start = max(end_pos - 1000, start_pos)
        search_end = end_pos
        
        # Find the last complete HTML tag
        last_tag_end = content.rfind('>', search_start, search_end)
        if last_tag_end > start_pos:
            return last_tag_end + 1
        
        # Find the last complete word
        last_space = content.rfind(' ', search_start, search_end)
        if last_space > start_pos:
            return last_space
        
        # Fall back to original end position
        return end_pos
    
    def _contains_reviews(self, content: str) -> bool:
        """Check if chunk contains review-related content"""
        review_indicators = [
            r'class="[^"]*review[^"]*"',
            r'Pros</span>',
            r'Cons</span>',
            r'Review Source',
            r'<svg[^>]*class="[^"]*star[^"]*"',
            r'([A-Z][a-z]+ [A-Z]\.)',
            r'([A-Z][a-z]+ \d{1,2}, \d{4})'
        ]
        
        for pattern in review_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _contains_comparison(self, content: str) -> bool:
        """Check if chunk contains comparison-related content"""
        comparison_indicators = [
            r'vs\.',
            r'comparison',
            r'compare',
            r'versus',
            r'alternative',
            r'better than',
            r'worse than'
        ]
        
        for pattern in comparison_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _contains_pricing(self, content: str) -> bool:
        """Check if chunk contains pricing-related content"""
        pricing_indicators = [
            r'\$\d+',
            r'price',
            r'cost',
            r'pricing',
            r'plan',
            r'subscription',
            r'free trial',
            r'per month',
            r'per user'
        ]
        
        for pattern in pricing_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _identify_structure_elements(self, content: str) -> List[str]:
        """Identify HTML structure elements in chunk"""
        elements = []
        
        for pattern in self.html_structure_markers:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                elements.extend(matches)
        
        return list(set(elements))
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_dir: str = "output/chunks"):
        """
        Save chunks to individual files
        
        Args:
            chunks: List of chunk dictionaries
            output_dir: Directory to save chunk files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for chunk in chunks:
            filename = f"chunk_{chunk['index']:03d}_{Path(chunk['file_path']).stem}.html"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(chunk['content'])
            
            print(f"💾 Saved chunk {chunk['index']} to {filepath}")
    
    def generate_chunk_report(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive report about chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Report dictionary with statistics
        """
        total_chunks = len(chunks)
        total_size = sum(chunk['size'] for chunk in chunks)
        
        review_chunks = [c for c in chunks if c['has_reviews']]
        comparison_chunks = [c for c in chunks if c['has_comparison']]
        pricing_chunks = [c for c in chunks if c['has_pricing']]
        
        report = {
            'total_chunks': total_chunks,
            'total_size': total_size,
            'average_chunk_size': total_size / total_chunks if total_chunks > 0 else 0,
            'review_chunks': len(review_chunks),
            'comparison_chunks': len(comparison_chunks),
            'pricing_chunks': len(pricing_chunks),
            'chunk_details': [
                {
                    'index': chunk['index'],
                    'size': chunk['size'],
                    'has_reviews': chunk['has_reviews'],
                    'has_comparison': chunk['has_comparison'],
                    'has_pricing': chunk['has_pricing'],
                    'structure_elements': len(chunk['structure_elements'])
                }
                for chunk in chunks
            ]
        }
        
        return report

def main():
    """Main function to demonstrate HTML chunking"""
    chunker = HTMLChunker(chunk_size=50000, overlap_size=5000)
    
    # Process all HTML files in capterraHTML directory
    html_dir = "capterraHTML"
    output_dir = "output/chunks"
    
    if not os.path.exists(html_dir):
        print(f"❌ Directory {html_dir} not found")
        return
    
    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
    
    if not html_files:
        print(f"❌ No HTML files found in {html_dir}")
        return
    
    print(f"🔍 Found {len(html_files)} HTML files to process")
    
    all_chunks = []
    all_reports = []
    
    for html_file in html_files:
        file_path = os.path.join(html_dir, html_file)
        print(f"\n📄 Processing: {html_file}")
        
        # Create chunks
        chunks = chunker.create_chunks(file_path)
        all_chunks.extend(chunks)
        
        # Generate report
        report = chunker.generate_chunk_report(chunks)
        all_reports.append({
            'file': html_file,
            'report': report
        })
        
        # Save chunks
        chunker.save_chunks(chunks, output_dir)
    
    # Generate overall report
    print(f"\n📊 OVERALL PROCESSING SUMMARY:")
    print(f"Total files processed: {len(html_files)}")
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Total size processed: {sum(chunk['size'] for chunk in all_chunks):,} characters")
    
    # Save overall report
    import json
    with open("output/chunk_processing_report.json", 'w', encoding='utf-8') as f:
        json.dump(all_reports, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Chunk processing report saved to: output/chunk_processing_report.json")

if __name__ == "__main__":
    main()
