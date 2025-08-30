"""Session management and statistics tracking for scraping operations."""
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from loguru import logger
import asyncio


@dataclass
class ScrapingMetrics:
    """Individual scraping metrics for a target."""
    target_id: str
    company_name: str
    url: str
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    reviews_extracted: int = 0
    extraction_time: float = 0.0
    anti_detection_triggers: int = 0
    cloudflare_bypass_attempts: int = 0
    errors: List[str] = None
    http_status: Optional[int] = None
    response_size: Optional[int] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def complete(self, success: bool, reviews_extracted: int = 0, errors: List[str] = None):
        """Mark scraping operation as complete."""
        self.end_time = datetime.now()
        self.success = success
        self.reviews_extracted = reviews_extracted
        self.extraction_time = (self.end_time - self.start_time).total_seconds()
        
        if errors:
            self.errors.extend(errors)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class ScrapingSession:
    """Manages scraping session with comprehensive statistics and monitoring."""
    
    def __init__(self, session_name: str = None):
        self.session_id = f"session_{int(time.time())}"
        self.session_name = session_name or f"Chimera_Scraping_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now()
        
        # Session statistics
        self.stats = {
            'total_targets': 0,
            'successful_scrapes': 0,
            'failed_scrapes': 0,
            'total_reviews_extracted': 0,
            'total_extraction_time': 0.0,
            'anti_detection_triggers': 0,
            'cloudflare_bypass_attempts': 0,
            'errors': [],
            'warnings': []
        }
        
        # Individual target metrics
        self.target_metrics: Dict[str, ScrapingMetrics] = {}
        
        # Performance tracking
        self.performance_metrics = {
            'average_extraction_time': 0.0,
            'fastest_extraction': float('inf'),
            'slowest_extraction': 0.0,
            'success_rate': 0.0,
            'reviews_per_minute': 0.0
        }
        
        # Anti-detection tracking
        self.anti_detection_events = []
        
        logger.info(f"Started new scraping session: {self.session_name} (ID: {self.session_id})")
    
    def add_target(self, target_id: str, company_name: str, url: str) -> str:
        """Add a new target to the session."""
        if target_id in self.target_metrics:
            logger.warning(f"Target {target_id} already exists in session")
            return target_id
        
        metrics = ScrapingMetrics(
            target_id=target_id,
            company_name=company_name,
            url=url,
            start_time=datetime.now()
        )
        
        self.target_metrics[target_id] = metrics
        self.stats['total_targets'] += 1
        
        logger.debug(f"Added target {target_id} ({company_name}) to session")
        return target_id
    
    def start_target_scraping(self, target_id: str) -> bool:
        """Mark target scraping as started."""
        if target_id not in self.target_metrics:
            logger.warning(f"Target {target_id} not found in session")
            return False
        
        # Target is already started when added
        logger.debug(f"Started scraping target: {target_id}")
        return True
    
    def complete_target_scraping(self, target_id: str, success: bool, 
                               reviews_extracted: int = 0, errors: List[str] = None) -> bool:
        """Mark target scraping as complete."""
        if target_id not in self.target_metrics:
            logger.warning(f"Target {target_id} not found in session")
            return False
        
        metrics = self.target_metrics[target_id]
        metrics.complete(success, reviews_extracted, errors or [])
        
        # Update session statistics
        if success:
            self.stats['successful_scrapes'] += 1
            self.stats['total_reviews_extracted'] += reviews_extracted
        else:
            self.stats['failed_scrapes'] += 1
        
        self.stats['total_extraction_time'] += metrics.extraction_time
        
        # Update performance metrics
        self._update_performance_metrics()
        
        logger.debug(f"Completed scraping target: {target_id} (Success: {success}, Reviews: {reviews_extracted})")
        return True
    
    def record_anti_detection_event(self, target_id: str, event_type: str, details: str = None):
        """Record an anti-detection event."""
        event = {
            'timestamp': datetime.now().isoformat(),
            'target_id': target_id,
            'event_type': event_type,
            'details': details
        }
        
        self.anti_detection_events.append(event)
        self.stats['anti_detection_triggers'] += 1
        
        # Update target metrics
        if target_id in self.target_metrics:
            self.target_metrics[target_id].anti_detection_triggers += 1
        
        logger.info(f"Anti-detection event recorded: {event_type} for {target_id}")
    
    def record_cloudflare_bypass_attempt(self, target_id: str, success: bool, strategy: str = None):
        """Record a Cloudflare bypass attempt."""
        self.stats['cloudflare_bypass_attempts'] += 1
        
        if target_id in self.target_metrics:
            self.target_metrics[target_id].cloudflare_bypass_attempts += 1
        
        event_type = "cloudflare_bypass_success" if success else "cloudflare_bypass_failure"
        details = f"Strategy: {strategy}" if strategy else None
        
        self.record_anti_detection_event(target_id, event_type, details)
    
    def add_error(self, target_id: str, error: str):
        """Add an error to the session."""
        self.stats['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'target_id': target_id,
            'error': error
        })
        
        if target_id in self.target_metrics:
            self.target_metrics[target_id].errors.append(error)
        
        logger.error(f"Error recorded for {target_id}: {error}")
    
    def add_warning(self, target_id: str, warning: str):
        """Add a warning to the session."""
        self.stats['warnings'].append({
            'timestamp': datetime.now().isoformat(),
            'target_id': target_id,
            'warning': warning
        })
        
        logger.warning(f"Warning recorded for {target_id}: {warning}")
    
    def _update_performance_metrics(self):
        """Update performance metrics based on current data."""
        if not self.target_metrics:
            return
        
        # Calculate average extraction time
        extraction_times = [m.extraction_time for m in self.target_metrics.values() if m.end_time]
        if extraction_times:
            self.performance_metrics['average_extraction_time'] = sum(extraction_times) / len(extraction_times)
            self.performance_metrics['fastest_extraction'] = min(extraction_times)
            self.performance_metrics['slowest_extraction'] = max(extraction_times)
        
        # Calculate success rate
        if self.stats['total_targets'] > 0:
            self.performance_metrics['success_rate'] = self.stats['successful_scrapes'] / self.stats['total_targets']
        
        # Calculate reviews per minute
        session_duration = (datetime.now() - self.start_time).total_seconds() / 60
        if session_duration > 0:
            self.performance_metrics['reviews_per_minute'] = self.stats['total_reviews_extracted'] / session_duration
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary."""
        self._update_performance_metrics()
        
        summary = {
            'session_id': self.session_id,
            'session_name': self.session_name,
            'start_time': self.start_time.isoformat(),
            'current_time': datetime.now().isoformat(),
            'duration_minutes': (datetime.now() - self.start_time).total_seconds() / 60,
            'statistics': self.stats.copy(),
            'performance_metrics': self.performance_metrics.copy(),
            'target_summary': {}
        }
        
        # Build target summary
        for target_id, metrics in self.target_metrics.items():
            summary['target_summary'][target_id] = {
                'company_name': metrics.company_name,
                'success': metrics.success,
                'reviews_extracted': metrics.reviews_extracted,
                'extraction_time': metrics.extraction_time,
                'anti_detection_triggers': metrics.anti_detection_triggers,
                'cloudflare_bypass_attempts': metrics.cloudflare_bypass_attempts,
                'error_count': len(metrics.errors)
            }
        
        return summary
    
    def get_target_metrics(self, target_id: str) -> Optional[ScrapingMetrics]:
        """Get metrics for a specific target."""
        return self.target_metrics.get(target_id)
    
    def get_failed_targets(self) -> List[str]:
        """Get list of failed target IDs."""
        return [target_id for target_id, metrics in self.target_metrics.items() 
                if not metrics.success]
    
    def get_successful_targets(self) -> List[str]:
        """Get list of successful target IDs."""
        return [target_id for target_id, metrics in self.target_metrics.items() 
                if metrics.success]
    
    def get_targets_by_status(self, status: str) -> List[str]:
        """Get targets by status (success/failed)."""
        if status.lower() == 'success':
            return self.get_successful_targets()
        elif status.lower() == 'failed':
            return self.get_failed_targets()
        else:
            return list(self.target_metrics.keys())
    
    def export_session_report(self, output_path: str = None) -> str:
        """Export comprehensive session report to JSON."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"session_report_{self.session_id}_{timestamp}.json"
        
        try:
            report = self.get_session_summary()
            
            # Add detailed target metrics
            report['detailed_target_metrics'] = {
                target_id: metrics.to_dict() 
                for target_id, metrics in self.target_metrics.items()
            }
            
            # Add anti-detection events
            report['anti_detection_events'] = self.anti_detection_events
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Session report exported to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting session report: {e}")
            return ""
    
    def print_summary(self):
        """Print session summary to console."""
        summary = self.get_session_summary()
        
        print(f"\n{'='*80}")
        print(f"📊 CHIMERA SCRAPING SESSION SUMMARY")
        print(f"{'='*80}")
        print(f"Session ID: {summary['session_id']}")
        print(f"Session Name: {summary['session_name']}")
        print(f"Duration: {summary['duration_minutes']:.1f} minutes")
        print(f"Start Time: {summary['start_time']}")
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   Total Targets: {summary['statistics']['total_targets']}")
        print(f"   Successful: {summary['statistics']['successful_scrapes']}")
        print(f"   Failed: {summary['statistics']['failed_scrapes']}")
        print(f"   Success Rate: {summary['performance_metrics']['success_rate']:.1%}")
        print(f"   Total Reviews: {summary['statistics']['total_reviews_extracted']}")
        print(f"   Reviews/Minute: {summary['performance_metrics']['reviews_per_minute']:.1f}")
        print(f"   Average Extraction Time: {summary['performance_metrics']['average_extraction_time']:.1f}s")
        print(f"\n🛡️ ANTI-DETECTION:")
        print(f"   Anti-Detection Triggers: {summary['statistics']['anti_detection_triggers']}")
        print(f"   Cloudflare Bypass Attempts: {summary['statistics']['cloudflare_bypass_attempts']}")
        
        if summary['statistics']['errors']:
            print(f"\n❌ ERRORS ({len(summary['statistics']['errors'])}):")
            for error in summary['statistics']['errors'][:5]:  # Show first 5
                print(f"   - {error['target_id']}: {error['error'][:100]}...")
        
        if summary['statistics']['warnings']:
            print(f"\n⚠️ WARNINGS ({len(summary['statistics']['warnings'])}):")
            for warning in summary['statistics']['warnings'][:3]:  # Show first 3
                print(f"   - {warning['target_id']}: {warning['warning'][:100]}...")
        
        print(f"{'='*80}")
    
    def is_complete(self) -> bool:
        """Check if all targets in the session are complete."""
        if not self.target_metrics:
            return False
        
        return all(metrics.end_time is not None for metrics in self.target_metrics.values())
    
    def get_remaining_targets(self) -> List[str]:
        """Get list of targets that haven't been completed."""
        return [target_id for target_id, metrics in self.target_metrics.items() 
                if metrics.end_time is None]
    
    def estimate_completion_time(self) -> Optional[float]:
        """Estimate time to completion based on current performance."""
        if not self.target_metrics:
            return None
        
        remaining_targets = len(self.get_remaining_targets())
        if remaining_targets == 0:
            return 0.0
        
        # Use average extraction time for estimation
        avg_time = self.performance_metrics['average_extraction_time']
        if avg_time == 0:
            return None
        
        # Add some buffer for anti-detection delays
        estimated_time = remaining_targets * avg_time * 1.5
        return estimated_time / 60  # Convert to minutes
    
    async def wait_for_completion(self, timeout_minutes: int = None) -> bool:
        """Wait for session completion with optional timeout."""
        start_wait = time.time()
        
        while not self.is_complete():
            if timeout_minutes and (time.time() - start_wait) / 60 > timeout_minutes:
                logger.warning(f"Session completion timeout after {timeout_minutes} minutes")
                return False
            
            # Print progress every 30 seconds
            if int(time.time() - start_wait) % 30 == 0:
                remaining = len(self.get_remaining_targets())
                completed = self.stats['successful_scrapes'] + self.stats['failed_scrapes']
                logger.info(f"Session progress: {completed}/{self.stats['total_targets']} completed, {remaining} remaining")
            
            await asyncio.sleep(1)
        
        logger.info("Session completed successfully")
        return True
