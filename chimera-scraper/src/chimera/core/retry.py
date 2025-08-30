"""Advanced retry management with circuit breaker pattern and sophisticated strategies."""

import asyncio
import time
import random
from typing import Callable, Any, Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from loguru import logger
import json


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service is recovered


class RetryStrategy(Enum):
    """Retry strategies."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIBONACCI_BACKOFF = "fibonacci_backoff"
    RANDOM_BACKOFF = "random_backoff"
    ADAPTIVE_BACKOFF = "adaptive_backoff"


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    jitter: bool = True
    jitter_factor: float = 0.1


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""
    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    expected_exception: type = Exception
    monitor_interval: float = 10.0


class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance."""
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.last_state_change = datetime.now()
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        async with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    await self._set_half_open()
                else:
                    raise Exception(f"Circuit breaker is OPEN (failures: {self.failure_count})")
            
            try:
                result = await func(*args, **kwargs)
                await self._on_success()
                return result
            except self.config.expected_exception as e:
                await self._on_failure(e)
                raise
    
    async def _on_success(self):
        """Handle successful execution."""
        if self.state == CircuitState.HALF_OPEN:
            await self._set_closed()
        self.failure_count = 0
    
    async def _on_failure(self, error: Exception):
        """Handle execution failure."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.config.failure_threshold:
            await self._set_open()
        
        logger.warning(f"Circuit breaker failure count: {self.failure_count}/{self.config.failure_threshold}")
    
    async def _set_open(self):
        """Set circuit to open state."""
        self.state = CircuitState.OPEN
        self.last_state_change = datetime.now()
        logger.warning("Circuit breaker opened due to failure threshold")
    
    async def _set_half_open(self):
        """Set circuit to half-open state."""
        self.state = CircuitState.HALF_OPEN
        self.last_state_change = datetime.now()
        logger.info("Circuit breaker set to half-open for testing")
    
    async def _set_closed(self):
        """Set circuit to closed state."""
        self.state = CircuitState.CLOSED
        self.last_state_change = datetime.now()
        self.failure_count = 0
        logger.info("Circuit breaker closed - service recovered")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if not self.last_failure_time:
            return False
        
        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.config.recovery_timeout
    
    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status."""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "last_state_change": self.last_state_change.isoformat(),
            "threshold": self.config.failure_threshold,
            "recovery_timeout": self.config.recovery_timeout
        }


class AdvancedRetryManager:
    """Advanced retry manager with multiple strategies and circuit breaker integration."""
    
    def __init__(self, retry_config: RetryConfig, circuit_config: Optional[CircuitBreakerConfig] = None):
        self.retry_config = retry_config
        self.circuit_breaker = CircuitBreaker(circuit_config) if circuit_config else None
        self.retry_history: List[Dict[str, Any]] = []
        self.success_rate = 1.0
        self.total_attempts = 0
        self.total_successes = 0
    
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with advanced retry logic."""
        attempt = 0
        last_error = None
        start_time = time.time()
        
        while attempt < self.retry_config.max_attempts:
            attempt += 1
            self.total_attempts += 1
            
            try:
                # Use circuit breaker if configured
                if self.circuit_breaker:
                    result = await self.circuit_breaker.call(func, *args, **kwargs)
                else:
                    result = await func(*args, **kwargs)
                
                # Success
                self.total_successes += 1
                self._update_success_rate()
                self._record_attempt(attempt, True, time.time() - start_time, None)
                
                logger.info(f"Function executed successfully on attempt {attempt}")
                return result
                
            except Exception as e:
                last_error = e
                execution_time = time.time() - start_time
                self._record_attempt(attempt, False, execution_time, str(e))
                
                logger.warning(f"Attempt {attempt} failed: {e}")
                
                # Check if we should retry
                if attempt >= self.retry_config.max_attempts:
                    logger.error(f"All {self.retry_config.max_attempts} attempts failed")
                    break
                
                # Calculate delay for next attempt
                delay = self._calculate_delay(attempt)
                
                # Add jitter if enabled
                if self.retry_config.jitter:
                    delay = self._add_jitter(delay)
                
                logger.info(f"Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
        
        # All attempts failed
        raise last_error or Exception("All retry attempts failed")
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay based on retry strategy."""
        base_delay = self.retry_config.base_delay
        
        if self.retry_config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = base_delay * (2 ** (attempt - 1))
        elif self.retry_config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = base_delay * attempt
        elif self.retry_config.strategy == RetryStrategy.FIBONACCI_BACKOFF:
            delay = base_delay * self._fibonacci(attempt)
        elif self.retry_config.strategy == RetryStrategy.RANDOM_BACKOFF:
            delay = base_delay * random.uniform(0.5, 2.0)
        elif self.retry_config.strategy == RetryStrategy.ADAPTIVE_BACKOFF:
            delay = base_delay * (2 ** (attempt - 1)) * (1 - self.success_rate)
        else:
            delay = base_delay
        
        return min(delay, self.retry_config.max_delay)
    
    def _fibonacci(self, n: int) -> int:
        """Calculate Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def _add_jitter(self, delay: float) -> float:
        """Add jitter to delay to prevent thundering herd."""
        jitter = delay * self.retry_config.jitter_factor * random.uniform(-1, 1)
        return max(0, delay + jitter)
    
    def _update_success_rate(self):
        """Update success rate based on recent attempts."""
        if self.total_attempts > 0:
            self.success_rate = self.total_successes / self.total_attempts
    
    def _record_attempt(self, attempt: int, success: bool, execution_time: float, error: Optional[str]):
        """Record attempt details for analysis."""
        record = {
            "attempt": attempt,
            "success": success,
            "execution_time": execution_time,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "success_rate": self.success_rate
        }
        
        self.retry_history.append(record)
        
        # Keep only recent history to prevent memory issues
        if len(self.retry_history) > 1000:
            self.retry_history = self.retry_history[-500:]
    
    async def execute_with_fallback(self, primary_func: Callable, fallback_func: Callable, 
                                  *args, **kwargs) -> Any:
        """Execute function with fallback strategy."""
        try:
            return await self.execute_with_retry(primary_func, *args, **kwargs)
        except Exception as e:
            logger.warning(f"Primary function failed, trying fallback: {e}")
            try:
                return await fallback_func(*args, **kwargs)
            except Exception as fallback_error:
                logger.error(f"Both primary and fallback functions failed: {fallback_error}")
                raise fallback_error
    
    async def execute_with_timeout(self, func: Callable, timeout: float, *args, **kwargs) -> Any:
        """Execute function with timeout protection."""
        try:
            return await asyncio.wait_for(
                self.execute_with_retry(func, *args, **kwargs),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.error(f"Function execution timed out after {timeout} seconds")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get retry statistics and performance metrics."""
        if not self.retry_history:
            return {"message": "No retry history available"}
        
        recent_history = self.retry_history[-100:]  # Last 100 attempts
        
        success_count = sum(1 for record in recent_history if record["success"])
        failure_count = len(recent_history) - success_count
        
        execution_times = [record["execution_time"] for record in recent_history]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            "total_attempts": self.total_attempts,
            "total_successes": self.total_successes,
            "overall_success_rate": self.success_rate,
            "recent_attempts": len(recent_history),
            "recent_successes": success_count,
            "recent_failures": failure_count,
            "recent_success_rate": success_count / len(recent_history) if recent_history else 0,
            "average_execution_time": avg_execution_time,
            "max_execution_time": max(execution_times) if execution_times else 0,
            "min_execution_time": min(execution_times) if execution_times else 0,
            "circuit_breaker_status": self.circuit_breaker.get_status() if self.circuit_breaker else None,
            "retry_config": {
                "max_attempts": self.retry_config.max_attempts,
                "strategy": self.retry_config.strategy.value,
                "base_delay": self.retry_config.base_delay,
                "max_delay": self.retry_config.max_delay
            }
        }
    
    def reset_statistics(self):
        """Reset all statistics and history."""
        self.retry_history.clear()
        self.success_rate = 1.0
        self.total_attempts = 0
        self.total_successes = 0
        
        if self.circuit_breaker:
            # Reset circuit breaker state
            self.circuit_breaker.state = CircuitState.CLOSED
            self.circuit_breaker.failure_count = 0
            self.circuit_breaker.last_failure_time = None
        
        logger.info("Retry manager statistics reset")
    
    def export_history(self, filepath: str):
        """Export retry history to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    "retry_history": self.retry_history,
                    "statistics": self.get_statistics(),
                    "export_timestamp": datetime.now().isoformat()
                }, f, indent=2)
            logger.info(f"Retry history exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export retry history: {e}")


# Convenience functions for backward compatibility
async def execute_with_retry(func: Callable, max_attempts: int = 3, 
                           base_delay: float = 1.0, *args, **kwargs) -> Any:
    """Simple retry function for backward compatibility."""
    config = RetryConfig(max_attempts=max_attempts, base_delay=base_delay)
    retry_manager = AdvancedRetryManager(config)
    return await retry_manager.execute_with_retry(func, *args, **kwargs)


async def execute_with_circuit_breaker(func: Callable, failure_threshold: int = 5,
                                     recovery_timeout: float = 60.0, *args, **kwargs) -> Any:
    """Simple circuit breaker function for backward compatibility."""
    circuit_config = CircuitBreakerConfig(failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
    circuit_breaker = CircuitBreaker(circuit_config)
    return await circuit_breaker.call(func, *args, **kwargs)
