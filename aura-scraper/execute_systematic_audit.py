#!/usr/bin/env python3
"""
Systematic HTML Audit Execution Script
Orchestrates the complete audit process for all Capterra HTML files
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from html_chunker import HTMLChunker
from pattern_extractor import CapterraPatternExtractor

class SystematicAuditExecutor:
    def __init__(self, output_dir: str = "output/audit_results"):
        """
        Initialize systematic audit executor
        
        Args:
            output_dir: Directory to save audit results
        """
        self.output_dir = output_dir
        self.chunker = HTMLChunker(chunk_size=50000, overlap_size=5000)
        self.extractor = CapterraPatternExtractor()
        self.audit_results = {
            'execution_metadata': {
                'start_time': datetime.now().isoformat(),
                'total_files_processed': 0,
                'total_chunks_created': 0,
                'total_reviews_extracted': 0,
                'execution_duration': 0
            },
            'file_results': [],
            'summary_statistics': {}
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def execute_full_audit(self, html_dir: str = "capterraHTML") -> Dict[str, Any]:
        """
        Execute complete systematic audit of all HTML files
        
        Args:
            html_dir: Directory containing HTML files
            
        Returns:
            Complete audit results
        """
        print("🚀 Starting Systematic HTML Audit")
        print("=" * 50)
        
        start_time = time.time()
        
        # Get list of HTML files
        html_files = self._get_html_files(html_dir)
        
        if not html_files:
            print(f"❌ No HTML files found in {html_dir}")
            return self.audit_results
        
        print(f"📁 Found {len(html_files)} HTML files to process")
        
        # Process each file
        for i, html_file in enumerate(html_files, 1):
            print(f"\n📄 Processing file {i}/{len(html_files)}: {html_file}")
            file_result = self._process_single_file(html_file)
            self.audit_results['file_results'].append(file_result)
        
        # Calculate final statistics
        end_time = time.time()
        self.audit_results['execution_metadata']['end_time'] = datetime.now().isoformat()
        self.audit_results['execution_metadata']['execution_duration'] = end_time - start_time
        self.audit_results['execution_metadata']['total_files_processed'] = len(html_files)
        
        # Generate summary statistics
        self.audit_results['summary_statistics'] = self._generate_summary_statistics()
        
        # Save results
        self._save_audit_results()
        
        # Print final summary
        self._print_final_summary()
        
        return self.audit_results
    
    def _get_html_files(self, html_dir: str) -> List[str]:
        """Get list of HTML files in directory"""
        if not os.path.exists(html_dir):
            return []
        
        html_files = []
        for file in os.listdir(html_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(html_dir, file))
        
        # Sort by file size (smallest first)
        html_files.sort(key=lambda x: os.path.getsize(x))
        
        return html_files
    
    def _process_single_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single HTML file through the complete audit pipeline
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            File processing results
        """
        file_start_time = time.time()
        file_name = os.path.basename(file_path)
        
        print(f"  🔍 Creating chunks...")
        
        # Step 1: Create chunks
        chunks = self.chunker.create_chunks(file_path)
        
        print(f"  📊 Created {len(chunks)} chunks")
        
        # Step 2: Extract data from chunks
        print(f"  🔍 Extracting data...")
        extracted_data = self.extractor.process_chunks(chunks)
        
        # Step 3: Generate file-specific report
        file_result = {
            'file_name': file_name,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'processing_time': time.time() - file_start_time,
            'chunks_created': len(chunks),
            'reviews_extracted': len(extracted_data['reviews']),
            'product_info_fields': len(extracted_data['product_info']),
            'comparisons_found': len(extracted_data['comparisons']),
            'pricing_fields': len(extracted_data['pricing']),
            'extracted_data': extracted_data
        }
        
        # Step 4: Save file-specific results
        self._save_file_results(file_name, file_result)
        
        print(f"  ✅ Extracted {len(extracted_data['reviews'])} reviews")
        
        return file_result
    
    def _save_file_results(self, file_name: str, file_result: Dict[str, Any]):
        """Save results for a single file"""
        # Create filename without extension
        base_name = Path(file_name).stem
        
        # Save full results
        full_results_file = os.path.join(self.output_dir, f"{base_name}_full_results.json")
        with open(full_results_file, 'w', encoding='utf-8') as f:
            json.dump(file_result, f, indent=2, ensure_ascii=False)
        
        # Save just the extracted data
        extracted_data_file = os.path.join(self.output_dir, f"{base_name}_extracted_data.json")
        with open(extracted_data_file, 'w', encoding='utf-8') as f:
            json.dump(file_result['extracted_data'], f, indent=2, ensure_ascii=False)
        
        print(f"  💾 Saved results to {base_name}_*.json")
    
    def _generate_summary_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        total_reviews = sum(result['reviews_extracted'] for result in self.audit_results['file_results'])
        total_chunks = sum(result['chunks_created'] for result in self.audit_results['file_results'])
        total_processing_time = sum(result['processing_time'] for result in self.audit_results['file_results'])
        
        # Calculate averages
        avg_reviews_per_file = total_reviews / len(self.audit_results['file_results']) if self.audit_results['file_results'] else 0
        avg_chunks_per_file = total_chunks / len(self.audit_results['file_results']) if self.audit_results['file_results'] else 0
        avg_processing_time = total_processing_time / len(self.audit_results['file_results']) if self.audit_results['file_results'] else 0
        
        # File size statistics
        file_sizes = [result['file_size'] for result in self.audit_results['file_results']]
        total_size = sum(file_sizes)
        avg_file_size = total_size / len(file_sizes) if file_sizes else 0
        
        # Review extraction statistics
        reviews_by_file = [(result['file_name'], result['reviews_extracted']) for result in self.audit_results['file_results']]
        best_extraction_file = max(reviews_by_file, key=lambda x: x[1]) if reviews_by_file else ("", 0)
        
        return {
            'total_files_processed': len(self.audit_results['file_results']),
            'total_reviews_extracted': total_reviews,
            'total_chunks_created': total_chunks,
            'total_processing_time': total_processing_time,
            'total_file_size': total_size,
            'averages': {
                'reviews_per_file': avg_reviews_per_file,
                'chunks_per_file': avg_chunks_per_file,
                'processing_time_per_file': avg_processing_time,
                'file_size': avg_file_size
            },
            'best_extraction': {
                'file': best_extraction_file[0],
                'reviews_count': best_extraction_file[1]
            },
            'file_breakdown': [
                {
                    'file': result['file_name'],
                    'size_mb': result['file_size'] / (1024 * 1024),
                    'chunks': result['chunks_created'],
                    'reviews': result['reviews_extracted'],
                    'processing_time': result['processing_time']
                }
                for result in self.audit_results['file_results']
            ]
        }
    
    def _save_audit_results(self):
        """Save complete audit results"""
        # Save main audit results
        main_results_file = os.path.join(self.output_dir, "complete_audit_results.json")
        with open(main_results_file, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
        
        # Save summary only
        summary_file = os.path.join(self.output_dir, "audit_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'execution_metadata': self.audit_results['execution_metadata'],
                'summary_statistics': self.audit_results['summary_statistics']
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Complete audit results saved to: {main_results_file}")
        print(f"📁 Audit summary saved to: {summary_file}")
    
    def _print_final_summary(self):
        """Print comprehensive final summary"""
        print("\n" + "=" * 50)
        print("🎯 SYSTEMATIC AUDIT COMPLETE")
        print("=" * 50)
        
        metadata = self.audit_results['execution_metadata']
        stats = self.audit_results['summary_statistics']
        
        print(f"⏱️  Execution Time: {metadata['execution_duration']:.2f} seconds")
        print(f"📁 Files Processed: {stats['total_files_processed']}")
        print(f"📊 Total Chunks Created: {stats['total_chunks_created']}")
        print(f"⭐ Total Reviews Extracted: {stats['total_reviews_extracted']}")
        print(f"💾 Total Data Processed: {stats['total_file_size'] / (1024 * 1024):.2f} MB")
        
        print(f"\n📈 AVERAGE METRICS:")
        print(f"  Reviews per file: {stats['averages']['reviews_per_file']:.1f}")
        print(f"  Chunks per file: {stats['averages']['chunks_per_file']:.1f}")
        print(f"  Processing time per file: {stats['averages']['processing_time_per_file']:.2f}s")
        print(f"  Average file size: {stats['averages']['file_size'] / (1024 * 1024):.2f} MB")
        
        print(f"\n🏆 BEST EXTRACTION:")
        print(f"  File: {stats['best_extraction']['file']}")
        print(f"  Reviews: {stats['best_extraction']['reviews_count']}")
        
        print(f"\n📋 FILE BREAKDOWN:")
        for file_info in stats['file_breakdown']:
            print(f"  {file_info['file']}: {file_info['reviews']} reviews, {file_info['size_mb']:.2f} MB, {file_info['processing_time']:.2f}s")
        
        print(f"\n📁 Results saved to: {self.output_dir}/")
        print("=" * 50)

def main():
    """Main function to execute systematic audit"""
    print("🔍 Capterra HTML Systematic Audit")
    print("This will process all HTML files in the capterraHTML directory")
    print("Results will be saved to output/audit_results/")
    
    # Initialize executor
    executor = SystematicAuditExecutor()
    
    # Execute full audit
    results = executor.execute_full_audit()
    
    print(f"\n✅ Audit completed successfully!")
    print(f"📊 Total reviews extracted: {results['summary_statistics']['total_reviews_extracted']}")
    print(f"📁 Results directory: {executor.output_dir}")

if __name__ == "__main__":
    main()
