"""
SessionManager - Session management
Adapted from Chimera-Ultimate's comprehensive tracking
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class SessionManager:
    """Session management adapted from Chimera-Ultimate's comprehensive tracking"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.stats = {
            'total_targets': 0,
            'successful_scrapes': 0,
            'failed_scrapes': 0,
            'cloudflare_bypasses': 0,
            'anti_detection_triggers': 0,
            'errors': [],
            'data_quality_scores': []
        }
        self.scraped_data = {}
        self.session_id = self._generate_session_id()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"aura_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def update_stats(self, success: bool, error: Optional[str] = None, 
                    cloudflare_bypass: bool = False, anti_detection_trigger: bool = False):
        """Update session statistics"""
        if success:
            self.stats['successful_scrapes'] += 1
        else:
            self.stats['failed_scrapes'] += 1
        
        if error:
            self.stats['errors'].append({
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
        
        if cloudflare_bypass:
            self.stats['cloudflare_bypasses'] += 1
        
        if anti_detection_trigger:
            self.stats['anti_detection_triggers'] += 1
        
        logger.debug(f"Stats updated - Success: {success}, Cloudflare: {cloudflare_bypass}, Anti-detection: {anti_detection_trigger}")
    
    def add_scraped_data(self, competitor_id: str, data: Dict[str, Any]):
        """Add scraped data to session"""
        self.scraped_data[competitor_id] = data
        
        # Calculate data quality score
        quality_score = self._calculate_data_quality_score(data)
        self.stats['data_quality_scores'].append(quality_score)
        
        logger.info(f"Added scraped data for {competitor_id} (quality score: {quality_score:.2f})")
    
    def _calculate_data_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score based on extracted data"""
        score = 0.0
        
        # Check for essential data
        if data.get('overall_rating') != 'N/A':
            score += 0.3
        if data.get('review_count') != 'N/A':
            score += 0.2
        if data.get('reviews') and len(data['reviews']) > 0:
            score += 0.3
        if data.get('pricing_info') != 'N/A':
            score += 0.1
        if data.get('rating_categories'):
            score += 0.1
        
        return min(score, 1.0)
    
    def generate_session_report(self) -> Dict[str, Any]:
        """Generate comprehensive session report"""
        duration = (datetime.now() - self.start_time).total_seconds() / 60
        
        return {
            'session_metadata': {
                'session_id': self.session_id,
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration_minutes': duration,
                'total_targets': self.stats['total_targets'],
                'success_rate': self.stats['successful_scrapes'] / max(self.stats['total_targets'], 1),
                'cloudflare_bypass_rate': self.stats['cloudflare_bypasses'] / max(self.stats['total_targets'], 1),
                'anti_detection_trigger_rate': self.stats['anti_detection_triggers'] / max(self.stats['total_targets'], 1)
            },
            'scraping_statistics': self.stats,
            'data_quality': {
                'average_quality_score': sum(self.stats['data_quality_scores']) / max(len(self.stats['data_quality_scores']), 1),
                'total_reviews_extracted': sum(len(data.get('reviews', [])) for data in self.scraped_data.values()),
                'total_alternatives_found': sum(len(data.get('alternatives', [])) for data in self.scraped_data.values()),
                'companies_with_ratings': sum(1 for data in self.scraped_data.values() if data.get('overall_rating') != 'N/A'),
                'companies_with_pricing': sum(1 for data in self.scraped_data.values() if data.get('pricing_info') != 'N/A')
            },
            'scraped_data': self.scraped_data
        }
    
    def save_session_report(self, filename: Optional[str] = None) -> str:
        """Save session report to JSON file"""
        if not filename:
            filename = f"{self.session_id}_report.json"
        
        report = self.generate_session_report()
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Session report saved to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving session report: {str(e)}")
            return ""
    
    def save_scraped_data(self, filename: Optional[str] = None) -> str:
        """Save scraped data to JSON file"""
        if not filename:
            filename = f"{self.session_id}_data.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.scraped_data, f, indent=2)
            
            logger.info(f"Scraped data saved to {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error saving scraped data: {str(e)}")
            return ""
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """Export scraped data to CSV format"""
        if not filename:
            filename = f"{self.session_id}_data.csv"
        
        filepath = self.output_dir / filename
        
        try:
            import pandas as pd
            
            csv_data = []
            for competitor_id, data in self.scraped_data.items():
                if 'error' in data:
                    continue
                
                # Basic company info
                row = {
                    'company_id': competitor_id,
                    'company_name': data.get('company', ''),
                    'overall_rating': data.get('overall_rating', ''),
                    'review_count': data.get('review_count', ''),
                    'pricing_info': data.get('pricing_info', ''),
                    'total_reviews_scraped': len(data.get('reviews', [])),
                    'alternatives_found': len(data.get('alternatives', [])),
                    'scraped_at': data.get('scraped_at', ''),
                    'source_url': data.get('source_url', '')
                }
                
                # Add rating categories
                rating_categories = data.get('rating_categories', {})
                for category, rating in rating_categories.items():
                    row[f'{category.lower().replace(" ", "_")}_rating'] = rating
                
                csv_data.append(row)
            
            df = pd.DataFrame(csv_data)
            df.to_csv(filepath, index=False)
            
            logger.info(f"Data exported to CSV: {filepath}")
            return str(filepath)
            
        except ImportError:
            logger.error("pandas not available for CSV export")
            return ""
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return ""
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get quick session summary"""
        duration = (datetime.now() - self.start_time).total_seconds() / 60
        
        return {
            'session_id': self.session_id,
            'duration_minutes': duration,
            'total_targets': self.stats['total_targets'],
            'successful_scrapes': self.stats['successful_scrapes'],
            'failed_scrapes': self.stats['failed_scrapes'],
            'success_rate': self.stats['successful_scrapes'] / max(self.stats['total_targets'], 1),
            'total_reviews': sum(len(data.get('reviews', [])) for data in self.scraped_data.values()),
            'total_alternatives': sum(len(data.get('alternatives', [])) for data in self.scraped_data.values()),
            'average_quality_score': sum(self.stats['data_quality_scores']) / max(len(self.stats['data_quality_scores']), 1)
        }
    
    def print_session_summary(self):
        """Print session summary to console"""
        summary = self.get_session_summary()
        
        print("\n" + "="*60)
        print("🎯 AURA-LITE SESSION SUMMARY")
        print("="*60)
        print(f"Session ID: {summary['session_id']}")
        print(f"Duration: {summary['duration_minutes']:.1f} minutes")
        print(f"Total Targets: {summary['total_targets']}")
        print(f"Successful Scrapes: {summary['successful_scrapes']}")
        print(f"Failed Scrapes: {summary['failed_scrapes']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Reviews: {summary['total_reviews']}")
        print(f"Total Alternatives: {summary['total_alternatives']}")
        print(f"Average Quality Score: {summary['average_quality_score']:.2f}")
        print("="*60)
        
        if self.stats['errors']:
            print(f"\n❌ Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:3]:
                print(f"   - {error['error'][:100]}...")
        
        print()
