"""Performance monitoring and optimization for Chimera scraper."""

import asyncio
import time
import psutil
import threading
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
from loguru import logger
import json
import os


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    active_threads: int
    active_connections: int
    response_time_ms: float
    requests_per_second: float
    success_rate: float
    error_rate: float


@dataclass
class PerformanceAlert:
    """Performance alert data structure."""
    timestamp: datetime
    alert_type: str
    severity: str
    message: str
    metrics: Dict[str, Any]
    threshold: float
    current_value: float


@dataclass
class OptimizationRecommendation:
    """Performance optimization recommendation."""
    timestamp: datetime
    category: str
    priority: str
    description: str
    impact: str
    implementation: str
    estimated_improvement: str


class PerformanceThresholds:
    """Configurable performance thresholds."""
    
    def __init__(self):
        self.cpu_threshold = 80.0
        self.memory_threshold = 85.0
        self.disk_io_threshold = 100.0  # MB/s
        self.network_threshold = 50.0   # MB/s
        self.response_time_threshold = 5000.0  # ms
        self.error_rate_threshold = 0.1  # 10%
        self.success_rate_threshold = 0.8  # 80%


class PerformanceMonitor:
    """Real-time performance monitoring with alerts and optimization recommendations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.thresholds = PerformanceThresholds()
        self.metrics_history: deque = deque(maxlen=1000)
        self.alerts_history: deque = deque(maxlen=500)
        self.recommendations: deque = deque(maxlen=100)
        
        # Performance tracking
        self.start_time = datetime.now()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times: deque = deque(maxlen=1000)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        self.monitor_interval = self.config.get("monitor_interval", 5.0)
        
        # Alert callbacks
        self.alert_callbacks: List[Callable] = []
        
        # Performance baselines
        self.baselines = self._initialize_baselines()
        
        # Thread safety
        self._lock = threading.Lock()
    
    def _initialize_baselines(self) -> Dict[str, float]:
        """Initialize performance baselines."""
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "response_time_ms": 0.0,
            "requests_per_second": 0.0,
            "success_rate": 1.0
        }
    
    async def start_monitoring(self):
        """Start performance monitoring."""
        if self.is_monitoring:
            logger.warning("Performance monitoring is already running")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("Performance monitoring started")
    
    async def stop_monitoring(self):
        """Stop performance monitoring."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.is_monitoring:
            try:
                # Collect metrics
                metrics = self._collect_metrics()
                
                # Store metrics
                with self._lock:
                    self.metrics_history.append(metrics)
                
                # Check for alerts
                alerts = self._check_thresholds(metrics)
                for alert in alerts:
                    self._handle_alert(alert)
                
                # Generate optimization recommendations
                recommendations = self._generate_recommendations(metrics)
                for recommendation in recommendations:
                    self._store_recommendation(recommendation)
                
                # Update baselines
                self._update_baselines(metrics)
                
                # Sleep until next collection
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                logger.error(f"Error in performance monitoring loop: {e}")
                time.sleep(self.monitor_interval)
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics."""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            
            # Calculate derived metrics
            response_time_ms = self._calculate_average_response_time()
            requests_per_second = self._calculate_requests_per_second()
            success_rate = self._calculate_success_rate()
            error_rate = 1.0 - success_rate
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=process_memory.rss / 1024 / 1024,
                disk_io_read_mb=disk_io.read_bytes / 1024 / 1024 if disk_io else 0,
                disk_io_write_mb=disk_io.write_bytes / 1024 / 1024 if disk_io else 0,
                network_sent_mb=network_io.bytes_sent / 1024 / 1024 if network_io else 0,
                network_recv_mb=network_io.bytes_recv / 1024 / 1024 if network_io else 0,
                active_threads=threading.active_count(),
                active_connections=len(psutil.net_connections()),
                response_time_ms=response_time_ms,
                requests_per_second=requests_per_second,
                success_rate=success_rate,
                error_rate=error_rate
            )
            
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
            # Return default metrics on error
            return PerformanceMetrics(
                timestamp=datetime.now(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                disk_io_read_mb=0.0,
                disk_io_write_mb=0.0,
                network_sent_mb=0.0,
                network_recv_mb=0.0,
                active_threads=0,
                active_connections=0,
                response_time_ms=0.0,
                requests_per_second=0.0,
                success_rate=1.0,
                error_rate=0.0
            )
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average response time from recent requests."""
        if not self.response_times:
            return 0.0
        
        return sum(self.response_times) / len(self.response_times)
    
    def _calculate_requests_per_second(self) -> float:
        """Calculate requests per second."""
        if not self.metrics_history:
            return 0.0
        
        # Calculate based on recent metrics
        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 measurements
        if len(recent_metrics) < 2:
            return 0.0
        
        time_diff = (recent_metrics[-1].timestamp - recent_metrics[0].timestamp).total_seconds()
        if time_diff == 0:
            return 0.0
        
        return len(recent_metrics) / time_diff
    
    def _calculate_success_rate(self) -> float:
        """Calculate success rate from total requests."""
        if self.total_requests == 0:
            return 1.0
        
        return self.successful_requests / self.total_requests
    
    def _check_thresholds(self, metrics: PerformanceMetrics) -> List[PerformanceAlert]:
        """Check if metrics exceed thresholds and generate alerts."""
        alerts = []
        
        # CPU threshold check
        if metrics.cpu_percent > self.thresholds.cpu_threshold:
            alerts.append(PerformanceAlert(
                timestamp=metrics.timestamp,
                alert_type="high_cpu",
                severity="warning" if metrics.cpu_percent < 90 else "critical",
                message=f"CPU usage is {metrics.cpu_percent:.1f}% (threshold: {self.thresholds.cpu_threshold}%)",
                metrics=asdict(metrics),
                threshold=self.thresholds.cpu_threshold,
                current_value=metrics.cpu_percent
            ))
        
        # Memory threshold check
        if metrics.memory_percent > self.thresholds.memory_threshold:
            alerts.append(PerformanceAlert(
                timestamp=metrics.timestamp,
                alert_type="high_memory",
                severity="warning" if metrics.memory_percent < 95 else "critical",
                message=f"Memory usage is {metrics.memory_percent:.1f}% (threshold: {self.thresholds.memory_threshold}%)",
                metrics=asdict(metrics),
                threshold=self.thresholds.memory_threshold,
                current_value=metrics.memory_percent
            ))
        
        # Response time threshold check
        if metrics.response_time_ms > self.thresholds.response_time_threshold:
            alerts.append(PerformanceAlert(
                timestamp=metrics.timestamp,
                alert_type="high_response_time",
                severity="warning" if metrics.response_time_ms < 10000 else "critical",
                message=f"Response time is {metrics.response_time_ms:.1f}ms (threshold: {self.thresholds.response_time_threshold}ms)",
                metrics=asdict(metrics),
                threshold=self.thresholds.response_time_threshold,
                current_value=metrics.response_time_ms
            ))
        
        # Error rate threshold check
        if metrics.error_rate > self.thresholds.error_rate_threshold:
            alerts.append(PerformanceAlert(
                timestamp=metrics.timestamp,
                alert_type="high_error_rate",
                severity="warning" if metrics.error_rate < 0.2 else "critical",
                message=f"Error rate is {metrics.error_rate:.1%} (threshold: {self.thresholds.error_rate_threshold:.1%})",
                metrics=asdict(metrics),
                threshold=self.thresholds.error_rate_threshold,
                current_value=metrics.error_rate
            ))
        
        return alerts
    
    def _handle_alert(self, alert: PerformanceAlert):
        """Handle performance alert."""
        # Store alert
        with self._lock:
            self.alerts_history.append(alert)
        
        # Log alert
        logger.warning(f"Performance Alert [{alert.severity.upper()}]: {alert.message}")
        
        # Execute alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")
    
    def _generate_recommendations(self, metrics: PerformanceMetrics) -> List[OptimizationRecommendation]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        # CPU optimization recommendations
        if metrics.cpu_percent > 70:
            recommendations.append(OptimizationRecommendation(
                timestamp=metrics.timestamp,
                category="cpu_optimization",
                priority="high" if metrics.cpu_percent > 85 else "medium",
                description="High CPU usage detected",
                impact="Reduced performance and potential timeouts",
                implementation="Consider reducing concurrent requests, optimizing parsing logic, or implementing request throttling",
                estimated_improvement="20-40% CPU reduction"
            ))
        
        # Memory optimization recommendations
        if metrics.memory_percent > 80:
            recommendations.append(OptimizationRecommendation(
                timestamp=metrics.timestamp,
                category="memory_optimization",
                priority="high" if metrics.memory_percent > 90 else "medium",
                description="High memory usage detected",
                impact="Potential memory leaks and system instability",
                implementation="Implement memory pooling, reduce data retention, or add garbage collection",
                estimated_improvement="15-30% memory reduction"
            ))
        
        # Response time optimization recommendations
        if metrics.response_time_ms > 3000:
            recommendations.append(OptimizationRecommendation(
                timestamp=metrics.timestamp,
                category="response_time_optimization",
                priority="high" if metrics.response_time_ms > 8000 else "medium",
                description="High response time detected",
                impact="Poor user experience and potential timeouts",
                implementation="Optimize parsing algorithms, implement caching, or reduce data processing",
                estimated_improvement="30-50% response time improvement"
            ))
        
        # Error rate optimization recommendations
        if metrics.error_rate > 0.05:
            recommendations.append(OptimizationRecommendation(
                timestamp=metrics.timestamp,
                category="error_rate_optimization",
                priority="high" if metrics.error_rate > 0.15 else "medium",
                description="High error rate detected",
                impact="Reduced data quality and reliability",
                implementation="Improve error handling, add retry logic, or enhance validation",
                estimated_improvement="50-80% error rate reduction"
            ))
        
        return recommendations
    
    def _store_recommendation(self, recommendation: OptimizationRecommendation):
        """Store optimization recommendation."""
        with self._lock:
            self.recommendations.append(recommendation)
    
    def _update_baselines(self, metrics: PerformanceMetrics):
        """Update performance baselines."""
        # Simple moving average for baselines
        alpha = 0.1  # Smoothing factor
        
        self.baselines["cpu_percent"] = (
            alpha * metrics.cpu_percent + (1 - alpha) * self.baselines["cpu_percent"]
        )
        self.baselines["memory_percent"] = (
            alpha * metrics.memory_percent + (1 - alpha) * self.baselines["memory_percent"]
        )
        self.baselines["response_time_ms"] = (
            alpha * metrics.response_time_ms + (1 - alpha) * self.baselines["response_time_ms"]
        )
        self.baselines["requests_per_second"] = (
            alpha * metrics.requests_per_second + (1 - alpha) * self.baselines["requests_per_second"]
        )
        self.baselines["success_rate"] = (
            alpha * metrics.success_rate + (1 - alpha) * self.baselines["success_rate"]
        )
    
    def record_request(self, success: bool, response_time_ms: float):
        """Record request metrics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        self.response_times.append(response_time_ms)
    
    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]):
        """Add callback function for performance alerts."""
        self.alert_callbacks.append(callback)
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """Get the most recent performance metrics."""
        if not self.metrics_history:
            return None
        
        with self._lock:
            return self.metrics_history[-1] if self.metrics_history else None
    
    def get_metrics_summary(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Get performance metrics summary for the specified duration."""
        if not self.metrics_history:
            return {"message": "No metrics available"}
        
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        
        with self._lock:
            recent_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= cutoff_time
            ]
        
        if not recent_metrics:
            return {"message": f"No metrics available for the last {duration_minutes} minutes"}
        
        # Calculate summary statistics
        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        response_times = [m.response_time_ms for m in recent_metrics]
        success_rates = [m.success_rate for m in recent_metrics]
        
        return {
            "duration_minutes": duration_minutes,
            "metrics_count": len(recent_metrics),
            "cpu": {
                "average": sum(cpu_values) / len(cpu_values),
                "min": min(cpu_values),
                "max": max(cpu_values),
                "baseline": self.baselines["cpu_percent"]
            },
            "memory": {
                "average": sum(memory_values) / len(memory_values),
                "min": min(memory_values),
                "max": max(memory_values),
                "baseline": self.baselines["memory_percent"]
            },
            "response_time": {
                "average_ms": sum(response_times) / len(response_times),
                "min_ms": min(response_times),
                "max_ms": max(response_times),
                "baseline_ms": self.baselines["response_time_ms"]
            },
            "success_rate": {
                "average": sum(success_rates) / len(success_rates),
                "min": min(success_rates),
                "max": max(success_rates),
                "baseline": self.baselines["success_rate"]
            },
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }
    
    def get_alerts_summary(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Get alerts summary for the specified duration."""
        if not self.alerts_history:
            return {"message": "No alerts available"}
        
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        
        with self._lock:
            recent_alerts = [
                a for a in self.alerts_history 
                if a.timestamp >= cutoff_time
            ]
        
        if not recent_alerts:
            return {"message": f"No alerts in the last {duration_minutes} minutes"}
        
        # Group alerts by type and severity
        alert_counts = defaultdict(lambda: defaultdict(int))
        for alert in recent_alerts:
            alert_counts[alert.alert_type][alert.severity] += 1
        
        return {
            "duration_minutes": duration_minutes,
            "total_alerts": len(recent_alerts),
            "alerts_by_type": dict(alert_counts),
            "recent_alerts": [
                {
                    "timestamp": alert.timestamp.isoformat(),
                    "type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message
                }
                for alert in recent_alerts[-10:]  # Last 10 alerts
            ]
        }
    
    def get_recommendations_summary(self) -> Dict[str, Any]:
        """Get optimization recommendations summary."""
        if not self.recommendations:
            return {"message": "No recommendations available"}
        
        with self._lock:
            recommendations = list(self.recommendations)
        
        # Group by category and priority
        recommendations_by_category = defaultdict(list)
        recommendations_by_priority = defaultdict(list)
        
        for rec in recommendations:
            recommendations_by_category[rec.category].append(rec)
            recommendations_by_priority[rec.priority].append(rec)
        
        return {
            "total_recommendations": len(recommendations),
            "by_category": {
                category: len(recs) for category, recs in recommendations_by_category.items()
            },
            "by_priority": {
                priority: len(recs) for priority, recs in recommendations_by_priority.items()
            },
            "recent_recommendations": [
                {
                    "timestamp": rec.timestamp.isoformat(),
                    "category": rec.category,
                    "priority": rec.priority,
                    "description": rec.description,
                    "impact": rec.impact,
                    "implementation": rec.implementation,
                    "estimated_improvement": rec.estimated_improvement
                }
                for rec in recommendations[-10:]  # Last 10 recommendations
            ]
        }
    
    def export_metrics(self, filepath: str, duration_minutes: int = 1440):  # Default: 24 hours
        """Export performance metrics to JSON file."""
        try:
            cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
            
            with self._lock:
                export_metrics = [
                    asdict(m) for m in self.metrics_history 
                    if m.timestamp >= cutoff_time
                ]
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "duration_minutes": duration_minutes,
                "metrics_count": len(export_metrics),
                "metrics": export_metrics,
                "summary": self.get_metrics_summary(duration_minutes),
                "alerts": self.get_alerts_summary(duration_minutes),
                "recommendations": self.get_recommendations_summary()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Performance metrics exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to export performance metrics: {e}")
    
    def reset_metrics(self):
        """Reset all performance metrics and history."""
        with self._lock:
            self.metrics_history.clear()
            self.alerts_history.clear()
            self.recommendations.clear()
        
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times.clear()
        self.start_time = datetime.now()
        self.baselines = self._initialize_baselines()
        
        logger.info("Performance metrics reset")
