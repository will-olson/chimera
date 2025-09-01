"""
CapterraTargetManager - Target management system
Adapted from Chimera-Ultimate's precision targeting
"""

import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class CapterraTargetManager:
    """Target management system adapted from Chimera-Ultimate's precision targeting"""
    
    def __init__(self, targets_file: str = 'capterra_sentiment_targets.json'):
        self.targets_file = targets_file
        self.targets = self._load_targets()
        self.current_target = None
        self.scraping_priorities = self._extract_priorities()
        self.validation_results = None
    
    def _load_targets(self) -> Dict[str, Any]:
        """Load Capterra targets with validation"""
        try:
            # Try to load from current directory first
            targets_path = Path(self.targets_file)
            if not targets_path.exists():
                # Try to load from parent directory (chimera-scraper/benchmarkSRCs/)
                parent_path = Path("../chimera-scraper/benchmarkSRCs") / self.targets_file
                if parent_path.exists():
                    targets_path = parent_path
                else:
                    logger.error(f"Targets file not found: {self.targets_file}")
                    return {}
            
            with open(targets_path, 'r') as file:
                targets = json.load(file)
                logger.info(f"Loaded {targets['metadata']['total_competitors']} competitors from {targets_path}")
                return targets
        except Exception as e:
            logger.error(f"Error loading targets: {str(e)}")
            return {}
    
    def _extract_priorities(self) -> Dict[str, List[str]]:
        """Extract scraping priorities from targets"""
        if not self.targets:
            return {}
        
        priorities = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        for competitor_id, competitor_data in self.targets.get('competitors', {}).items():
            # Determine priority based on market position and category
            market_position = competitor_data.get('metadata', {}).get('market_position', 'medium')
            category = competitor_data.get('metadata', {}).get('category', '')
            
            if market_position == 'leader' or 'modern' in category:
                priorities['high'].append(competitor_id)
            elif market_position == 'established':
                priorities['medium'].append(competitor_id)
            else:
                priorities['low'].append(competitor_id)
        
        return priorities
    
    def get_targets_by_priority(self, priority: str = "high") -> List[Dict[str, Any]]:
        """Get targets filtered by priority level"""
        priority_targets = []
        
        if priority not in self.scraping_priorities:
            logger.warning(f"Invalid priority level: {priority}")
            return priority_targets
        
        for competitor_id in self.scraping_priorities[priority]:
            if competitor_id in self.targets.get('competitors', {}):
                competitor_data = self.targets['competitors'][competitor_id]
                priority_targets.append({
                    'id': competitor_id,
                    'data': competitor_data
                })
        
        logger.info(f"Found {len(priority_targets)} targets with priority '{priority}'")
        return priority_targets
    
    def get_targets_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get targets filtered by category"""
        category_targets = []
        
        for competitor_id, competitor_data in self.targets.get('competitors', {}).items():
            competitor_category = competitor_data.get('metadata', {}).get('category', '')
            if category.lower() in competitor_category.lower():
                category_targets.append({
                    'id': competitor_id,
                    'data': competitor_data
                })
        
        logger.info(f"Found {len(category_targets)} targets in category '{category}'")
        return category_targets
    
    def get_target_by_id(self, competitor_id: str) -> Optional[Dict[str, Any]]:
        """Get specific target by ID"""
        if competitor_id in self.targets.get('competitors', {}):
            return {
                'id': competitor_id,
                'data': self.targets['competitors'][competitor_id]
            }
        return None
    
    def validate_target_urls(self) -> Dict[str, Any]:
        """Validate target URLs and metadata"""
        validation_results = {
            'valid_targets': 0,
            'invalid_targets': 0,
            'validation_errors': [],
            'target_details': {}
        }
        
        for competitor_id, competitor_data in self.targets.get('competitors', {}).items():
            target_details = {
                'name': competitor_data.get('name', 'Unknown'),
                'valid_urls': 0,
                'invalid_urls': 0,
                'url_errors': []
            }
            
            try:
                # Validate URL structure
                for target_type, url in competitor_data.get('targets', {}).items():
                    if not url.startswith('https://www.capterra.com/'):
                        validation_results['invalid_targets'] += 1
                        target_details['invalid_urls'] += 1
                        error_msg = f"Invalid URL for {competitor_id} ({target_type}): {url}"
                        validation_results['validation_errors'].append(error_msg)
                        target_details['url_errors'].append(error_msg)
                    else:
                        validation_results['valid_targets'] += 1
                        target_details['valid_urls'] += 1
                        
            except Exception as e:
                validation_results['invalid_targets'] += 1
                target_details['invalid_urls'] += 1
                error_msg = f"Validation error for {competitor_id}: {str(e)}"
                validation_results['validation_errors'].append(error_msg)
                target_details['url_errors'].append(error_msg)
            
            validation_results['target_details'][competitor_id] = target_details
        
        self.validation_results = validation_results
        logger.info(f"Validation complete: {validation_results['valid_targets']} valid, {validation_results['invalid_targets']} invalid")
        return validation_results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        if not self.validation_results:
            self.validate_target_urls()
        
        return {
            'total_targets': len(self.targets.get('competitors', {})),
            'valid_targets': self.validation_results['valid_targets'],
            'invalid_targets': self.validation_results['invalid_targets'],
            'validation_rate': self.validation_results['valid_targets'] / max(len(self.targets.get('competitors', {})), 1),
            'error_count': len(self.validation_results['validation_errors'])
        }
    
    def get_target_statistics(self) -> Dict[str, Any]:
        """Get target statistics"""
        if not self.targets:
            return {}
        
        competitors = self.targets.get('competitors', {})
        categories = {}
        market_positions = {}
        
        for competitor_id, competitor_data in competitors.items():
            # Count categories
            category = competitor_data.get('metadata', {}).get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
            
            # Count market positions
            position = competitor_data.get('metadata', {}).get('market_position', 'unknown')
            market_positions[position] = market_positions.get(position, 0) + 1
        
        return {
            'total_competitors': len(competitors),
            'categories': categories,
            'market_positions': market_positions,
            'priority_distribution': {
                'high': len(self.scraping_priorities.get('high', [])),
                'medium': len(self.scraping_priorities.get('medium', [])),
                'low': len(self.scraping_priorities.get('low', []))
            }
        }
