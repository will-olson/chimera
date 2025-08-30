"""Target management system for structured scraping operations."""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from pathlib import Path


class TargetManager:
    """Manages scraping targets with metadata and priority handling."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.targets = {}
        self.metadata = {}
        self.scraping_priorities = {}
        self.review_scraping_focus = {}
        
        if config_path:
            self.load_targets(config_path)
    
    def load_targets(self, config_path: str) -> bool:
        """Load targets from JSON configuration file."""
        try:
            if not os.path.exists(config_path):
                logger.error(f"Target configuration file not found: {config_path}")
                return False
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Extract main sections
            self.targets = config_data.get('competitors', {})
            self.metadata = config_data.get('metadata', {})
            self.scraping_priorities = config_data.get('scraping_priorities', {})
            self.review_scraping_focus = config_data.get('review_scraping_focus', {})
            
            logger.info(f"Loaded {len(self.targets)} competitors from {config_path}")
            logger.info(f"Platform: {self.metadata.get('platform', 'unknown')}")
            logger.info(f"Total competitors: {self.metadata.get('total_competitors', 0)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading targets from {config_path}: {e}")
            return False
    
    def get_targets_by_category(self, category: str) -> Dict[str, Any]:
        """Get targets filtered by category."""
        filtered_targets = {}
        
        for target_id, target_data in self.targets.items():
            target_category = target_data.get('metadata', {}).get('category', '')
            if category.lower() in target_category.lower():
                filtered_targets[target_id] = target_data
        
        logger.info(f"Found {len(filtered_targets)} targets in category: {category}")
        return filtered_targets
    
    def get_priority_targets(self, priority: str = "high") -> Dict[str, Any]:
        """Get targets by priority level."""
        priority_targets = {}
        
        for target_id, target_data in self.targets.items():
            market_position = target_data.get('metadata', {}).get('market_position', '')
            
            if priority == "high" and market_position in ["leader", "innovator"]:
                priority_targets[target_id] = target_data
            elif priority == "medium" and market_position in ["established", "emerging"]:
                priority_targets[target_id] = target_data
            elif priority == "low" and market_position in ["established", "emerging"]:
                priority_targets[target_id] = target_data
        
        logger.info(f"Found {len(priority_targets)} {priority} priority targets")
        return priority_targets
    
    def get_targets_by_platform(self, platform: str) -> Dict[str, Any]:
        """Get targets filtered by platform."""
        if self.metadata.get('platform', '').lower() == platform.lower():
            return self.targets
        return {}
    
    def get_target_urls(self, target_id: str, url_type: str = "product_reviews") -> List[str]:
        """Get specific URLs for a target."""
        if target_id not in self.targets:
            logger.warning(f"Target {target_id} not found")
            return []
        
        target_data = self.targets[target_id]
        targets = target_data.get('targets', {})
        
        if url_type in targets:
            url_value = targets[url_type]
            if isinstance(url_value, list):
                return url_value
            else:
                return [url_value]
        
        return []
    
    def get_all_review_urls(self) -> Dict[str, List[str]]:
        """Get all product review URLs for all targets."""
        review_urls = {}
        
        for target_id, target_data in self.targets.items():
            urls = self.get_target_urls(target_id, "product_reviews")
            if urls:
                review_urls[target_id] = urls
        
        return review_urls
    
    def get_comparison_urls(self, target_id: str) -> Dict[str, List[str]]:
        """Get comparison URLs for a target."""
        if target_id not in self.targets:
            return {}
        
        target_data = self.targets[target_id]
        targets = target_data.get('targets', {})
        
        comparison_urls = {}
        
        # Head-to-head comparisons
        if 'head_to_head' in targets:
            comparison_urls['head_to_head'] = targets['head_to_head']
        
        # Four-way comparisons
        if 'four_way' in targets:
            comparison_urls['four_way'] = targets['four_way']
        
        return comparison_urls
    
    def get_competitor_metadata(self, target_id: str) -> Dict[str, Any]:
        """Get metadata for a specific competitor."""
        if target_id not in self.targets:
            return {}
        
        return self.targets[target_id].get('metadata', {})
    
    def validate_targets(self) -> Dict[str, List[str]]:
        """Validate target URLs and metadata."""
        validation_results = {
            'valid': [],
            'invalid': [],
            'warnings': []
        }
        
        for target_id, target_data in self.targets.items():
            try:
                # Check required fields
                required_fields = ['name', 'targets']
                missing_fields = [field for field in required_fields if field not in target_data]
                
                if missing_fields:
                    validation_results['invalid'].append(f"{target_id}: Missing fields {missing_fields}")
                    continue
                
                # Check targets
                targets = target_data['targets']
                if 'product_reviews' not in targets:
                    validation_results['warnings'].append(f"{target_id}: No product reviews target")
                
                # Validate URLs
                for target_type, url_value in targets.items():
                    if isinstance(url_value, list):
                        for url in url_value:
                            if not self._is_valid_url(url):
                                validation_results['warnings'].append(f"{target_id}: Invalid URL {url}")
                    else:
                        if not self._is_valid_url(url_value):
                            validation_results['warnings'].append(f"{target_id}: Invalid URL {url_value}")
                
                validation_results['valid'].append(target_id)
                
            except Exception as e:
                validation_results['invalid'].append(f"{target_id}: Validation error {e}")
        
        logger.info(f"Target validation complete: {len(validation_results['valid'])} valid, "
                   f"{len(validation_results['invalid'])} invalid, {len(validation_results['warnings'])} warnings")
        
        return validation_results
    
    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation."""
        if not url or not isinstance(url, str):
            return False
        
        # Check for basic URL structure
        valid_domains = ['g2.com', 'capterra.com', 'trustradius.com', 'softwareadvice.com']
        return any(domain in url.lower() for domain in valid_domains)
    
    def get_scraping_strategy(self, target_id: str) -> Dict[str, Any]:
        """Get recommended scraping strategy for a target."""
        if target_id not in self.targets:
            return {}
        
        target_data = self.targets[target_id]
        metadata = target_data.get('metadata', {})
        
        # Determine strategy based on market position and category
        strategy = {
            'anti_detection_level': 'medium',
            'human_behavior': True,
            'cloudflare_bypass': True,
            'delays': {'min': 2.0, 'max': 5.0},
            'max_reviews': 30,
            'retry_attempts': 3
        }
        
        # Adjust strategy based on market position
        market_position = metadata.get('market_position', '')
        if market_position == 'leader':
            strategy['anti_detection_level'] = 'high'
            strategy['delays'] = {'min': 3.0, 'max': 8.0}
            strategy['max_reviews'] = 25
        elif market_position == 'innovator':
            strategy['anti_detection_level'] = 'high'
            strategy['delays'] = {'min': 2.5, 'max': 6.0}
            strategy['max_reviews'] = 20
        
        # Adjust for category
        category = metadata.get('category', '')
        if 'enterprise' in category.lower():
            strategy['anti_detection_level'] = 'high'
            strategy['delays'] = {'min': 4.0, 'max': 10.0}
        
        return strategy
    
    def export_targets_summary(self, output_path: str = None) -> str:
        """Export a summary of all targets."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"targets_summary_{timestamp}.json"
        
        summary = {
            'exported_at': datetime.now().isoformat(),
            'metadata': self.metadata,
            'targets_summary': {},
            'statistics': {
                'total_targets': len(self.targets),
                'categories': {},
                'market_positions': {}
            }
        }
        
        # Build targets summary
        for target_id, target_data in self.targets.items():
            summary['targets_summary'][target_id] = {
                'name': target_data.get('name', ''),
                'category': target_data.get('metadata', {}).get('category', ''),
                'market_position': target_data.get('metadata', {}).get('market_position', ''),
                'has_reviews': 'product_reviews' in target_data.get('targets', {}),
                'has_comparisons': any(key in target_data.get('targets', {}) for key in ['head_to_head', 'four_way']),
                'primary_competitors': target_data.get('metadata', {}).get('primary_competitors', [])
            }
        
        # Build statistics
        for target_data in self.targets.values():
            metadata = target_data.get('metadata', {})
            category = metadata.get('category', 'unknown')
            market_position = metadata.get('market_position', 'unknown')
            
            summary['statistics']['categories'][category] = summary['statistics']['categories'].get(category, 0) + 1
            summary['statistics']['market_positions'][market_position] = summary['statistics']['market_positions'].get(market_position, 0) + 1
        
        # Save to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, default=str)
            
            logger.info(f"Targets summary exported to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting targets summary: {e}")
            return ""


class TargetFactory:
    """Factory for creating target configurations."""
    
    @staticmethod
    def create_g2_targets() -> Dict[str, Any]:
        """Create G2.com target configuration template."""
        return {
            "metadata": {
                "version": "1.0",
                "description": "G2 sentiment scraping targets for competitive intelligence",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_competitors": 0,
                "scraping_categories": [
                    "product_reviews",
                    "head_to_head_comparisons",
                    "four_way_comparisons",
                    "competitor_alternatives"
                ],
                "priority_focus": "high_volume_review_scraping_for_foundational_insights"
            },
            "competitors": {},
            "scraping_priorities": {
                "high_priority": ["product_reviews"],
                "medium_priority": ["head_to_head_comparisons", "four_way_comparisons"],
                "low_priority": ["competitor_alternatives"]
            }
        }
    
    @staticmethod
    def create_capterra_targets() -> Dict[str, Any]:
        """Create Capterra.com target configuration template."""
        return {
            "metadata": {
                "version": "1.0",
                "description": "Capterra sentiment scraping targets for competitive intelligence",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "total_competitors": 0,
                "scraping_categories": [
                    "product_reviews",
                    "product_alternatives",
                    "comparison_insights"
                ],
                "priority_focus": "high_volume_review_scraping_for_foundational_insights",
                "platform": "capterra",
                "url_structure": "https://www.capterra.com/p/{product_id}/{product_name}/",
                "anti_detection_focus": "cloudflare_bypass_and_human_behavior_simulation"
            },
            "competitors": {},
            "scraping_priorities": {
                "high_priority": ["product_reviews"],
                "medium_priority": ["product_profile", "alternatives"],
                "low_priority": ["comparison_insights"]
            }
        }
