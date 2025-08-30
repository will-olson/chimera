# How to Use Chimera: Complete Testing and Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Git for cloning the repository
- Modern web browser (Chrome/Firefox recommended)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd chimera-scraper

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium firefox

# Set up environment variables
cp .env.example .env
# Edit .env with your proxy settings if needed
```

## 📋 Critical Dependencies

### Core Dependencies
- **Playwright**: Browser automation and stealth
- **BeautifulSoup4 + lxml**: HTML parsing
- **Pydantic**: Data validation and modeling
- **Loguru**: Advanced logging
- **psutil**: Performance monitoring
- **PyYAML**: Configuration management

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **CPU**: Multi-core processor recommended
- **Storage**: 2GB+ free space for logs and data
- **Network**: Stable internet connection

### Browser Dependencies
```bash
# Install Playwright browsers
playwright install chromium
playwright install firefox

# Verify installation
playwright --version
```

## 🧪 Testing Chimera

### 1. Basic Functionality Test

#### Test Individual Components
```python
# Test G2 Parser
python -c "
from src.chimera.parsers.g2 import G2Parser
parser = G2Parser()
print('G2 Parser initialized successfully')
"

# Test Capterra Parser
python -c "
from src.chimera.parsers.capterra import CapterraParser
parser = CapterraParser()
print('Capterra Parser initialized successfully')
"

# Test Sentiment Analyzer
python -c "
from src.chimera.analysis.sentiment import AdvancedSentimentAnalyzer
analyzer = AdvancedSentimentAnalyzer()
print('Sentiment Analyzer initialized successfully')
"
```

#### Test Enterprise Scraper
```python
# Create test script: test_scraper.py
import asyncio
from src.chimera.core.enterprise_scraper import ChimeraEnterpriseScraper

async def test_scraper():
    scraper = ChimeraEnterpriseScraper()
    try:
        await scraper.initialize()
        print("✅ Scraper initialized successfully")
        
        # Test with a simple target
        test_target = {
            "id": "test_1",
            "name": "Test Company",
            "url": "https://www.g2.com/products/tableau",
            "platform": "g2"
        }
        
        reviews = await scraper.scrape_target(test_target)
        print(f"✅ Extracted {len(reviews)} reviews")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(test_scraper())
```

### 2. Configuration Testing

#### Test Configuration Loading
```python
# Test YAML configuration
python -c "
import yaml
with open('config/scraping_profiles.yaml', 'r') as f:
    config = yaml.safe_load(f)
print('✅ Configuration loaded successfully')
print(f'Profiles: {list(config.keys())}')
"
```

#### Test Environment Variables
```python
# Test environment setup
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ Environment variables loaded')
print(f'Proxy enabled: {bool(os.getenv(\"PROXY_URL\"))}')
"
```

### 3. Performance Testing

#### Test Performance Monitor
```python
# Test performance monitoring
python -c "
import asyncio
from src.chimera.monitoring.performance import PerformanceMonitor

async def test_monitor():
    monitor = PerformanceMonitor()
    await monitor.start_monitoring()
    print('✅ Performance monitoring started')
    await asyncio.sleep(10)
    summary = monitor.get_metrics_summary()
    print(f'✅ Metrics collected: {summary}')
    await monitor.stop_monitoring()

asyncio.run(test_monitor())
"
```

## 🎯 Expected Outputs

### Successful Scraping Output
```
[INFO] Chimera Enterprise Scraper initialized
[INFO] Performance monitoring started
[INFO] Browser initialized with advanced stealth measures
[INFO] Loaded 5 targets for scraping
[INFO] Starting scraping of 5 targets
[INFO] Scraping target: Tableau
[INFO] Successfully navigated to https://www.g2.com/products/tableau
[INFO] Advanced human behavior simulation completed
[INFO] Successfully extracted 15420 characters of content
[INFO] Successfully parsed 25 enhanced reviews
[INFO] Successfully scraped 25 reviews from Tableau
[INFO] Anti-detection delay: 4.23s
[INFO] Scraping completed. Total reviews: 125
```

### Expected File Outputs
```
chimera-scraper/
├── output/
│   ├── reviews_tableau_20241201.json
│   ├── reviews_powerbi_20241201.json
│   └── batch_summary_20241201.json
├── logs/
│   ├── chimera_20241201.log
│   └── performance_metrics_20241201.json
└── session_summary_20241201.json
```

### Expected Data Structure
```json
{
  "batch_id": "batch_1701388800_1234",
  "source_platform": "g2",
  "target_company": "Tableau",
  "extraction_date": "2024-12-01T10:00:00",
  "reviews": [
    {
      "id": "g2_123456789",
      "source": "G2",
      "title": "Excellent visualization tool...",
      "content": "Tableau has transformed our data analysis...",
      "rating": 4.5,
      "author": "John D.",
      "date": "2024-11-15T00:00:00",
      "sentiment_score": 0.8,
      "sentiment_label": "positive",
      "competitor_mentions": ["power bi", "qlik"],
      "review_quality_score": 0.9,
      "extraction_confidence": 0.95
    }
  ],
  "total_reviews": 25,
  "successful_extractions": 25,
  "failed_extractions": 0,
  "average_rating": 4.3,
  "sentiment_distribution": {
    "positive": 18,
    "neutral": 5,
    "negative": 2
  }
}
```

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Browser Initialization Failures

**Problem**: `Failed to initialize browser`
```bash
# Solution 1: Reinstall Playwright
playwright uninstall
playwright install chromium

# Solution 2: Check system dependencies
# On Ubuntu/Debian:
sudo apt-get install libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1

# On macOS:
brew install --cask chromium

# Solution 3: Verify browser installation
playwright install --help
playwright --version
```

#### 2. Memory Issues

**Problem**: `MemoryError` or high memory usage
```python
# Solution: Adjust memory settings in config
# config/scraping_profiles.yaml
scraping_profiles:
  stealth:
    max_reviews_per_target: 10  # Reduce from 25
    memory_limit_mb: 2048       # Add memory limit
```

#### 3. Network Timeouts

**Problem**: `TimeoutError` during scraping
```python
# Solution: Increase timeout values
# In enterprise_scraper.py
await self.page.goto(url, wait_until="networkidle", timeout=60000)  # 60s

# Or adjust retry configuration
retry_config = RetryConfig(
    max_attempts=5,        # Increase from 3
    base_delay=5.0,        # Increase from 2.0
    max_delay=120.0        # Increase from 60.0
)
```

#### 4. Anti-Detection Failures

**Problem**: Getting blocked or detected
```python
# Solution 1: Increase stealth measures
config = {
    "scraping_profile": "stealth",  # Use maximum stealth
    "human_behavior": True,
    "cloudflare_bypass": True,
    "min_delay": 5.0,      # Increase delays
    "max_delay": 15.0
}

# Solution 2: Rotate fingerprints more frequently
# In enterprise_scraper.py
def _should_rotate_fingerprint(self) -> bool:
    time_since_rotation = datetime.now() - self.last_rotation_time
    return time_since_rotation.total_seconds() > 180  # Reduce from 300s
```

#### 5. Parser Failures

**Problem**: No reviews extracted
```python
# Solution: Check selector strategies
# In parsers/g2.py or parsers/capterra.py
# Add debug logging
logger.debug(f"Trying selector: {selector}")
logger.debug(f"Found elements: {len(elements)}")

# Or test with different selectors
test_selectors = [
    'div[class*="review"]',
    '.review-item',
    '[data-testid="review"]',
    'p:contains("like")'  # Pattern matching
]
```

### Debug Mode

#### Enable Verbose Logging
```python
# In your test script
import logging
from loguru import logger

# Set debug level
logger.add("debug.log", level="DEBUG", rotation="1 day")

# Or use environment variable
import os
os.environ["LOG_LEVEL"] = "DEBUG"
```

#### Monitor Anti-Detection Events
```python
# Check anti-detection statistics
scraper = ChimeraEnterpriseScraper()
await scraper.initialize()

# Monitor events in real-time
while True:
    stats = scraper.get_anti_detection_stats()
    print(f"Detection events: {stats['total_events']}")
    print(f"Fingerprint rotations: {stats['fingerprint_rotations']}")
    await asyncio.sleep(30)
```

## 🔍 Areas to Inspect for Improvement

### 1. Selector Strategy Analysis

#### Monitor Selector Success Rates
```python
# Add to parsers to track selector effectiveness
class SelectorAnalyzer:
    def __init__(self):
        self.selector_stats = defaultdict(lambda: {"success": 0, "failure": 0})
    
    def record_selector_result(self, selector: str, success: bool):
        if success:
            self.selector_stats[selector]["success"] += 1
        else:
            self.selector_stats[selector]["failure"] += 1
    
    def get_best_selectors(self) -> List[str]:
        # Return selectors with highest success rates
        return sorted(
            self.selector_stats.items(),
            key=lambda x: x[1]["success"] / max(x[1]["success"] + x[1]["failure"], 1),
            reverse=True
        )
```

#### Implement Dynamic Selector Learning
```python
# Automatically adjust selectors based on success rates
class AdaptiveSelector:
    def __init__(self):
        self.selector_weights = {}
        self.learning_rate = 0.1
    
    def update_weights(self, selector: str, success: bool):
        current_weight = self.selector_weights.get(selector, 1.0)
        if success:
            new_weight = current_weight + self.learning_rate
        else:
            new_weight = current_weight - self.learning_rate
        
        self.selector_weights[selector] = max(0.1, new_weight)
    
    def get_weighted_selectors(self) -> List[Tuple[str, float]]:
        return sorted(
            self.selector_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )
```

### 2. Anti-Detection Pattern Analysis

#### Track Detection Patterns
```python
# Analyze what triggers detection
class DetectionPatternAnalyzer:
    def __init__(self):
        self.detection_patterns = []
        self.success_patterns = []
    
    def analyze_detection(self, page_content: str, url: str, success: bool):
        if success:
            self.success_patterns.append({
                "url": url,
                "content_length": len(page_content),
                "timestamp": datetime.now()
            })
        else:
            self.detection_patterns.append({
                "url": url,
                "content_length": len(page_content),
                "timestamp": datetime.now(),
                "indicators": self._extract_detection_indicators(page_content)
            })
    
    def _extract_detection_indicators(self, content: str) -> List[str]:
        indicators = []
        if "captcha" in content.lower():
            indicators.append("captcha")
        if "blocked" in content.lower():
            indicators.append("blocked")
        if "suspicious" in content.lower():
            indicators.append("suspicious_activity")
        return indicators
    
    def get_detection_trends(self) -> Dict[str, Any]:
        # Analyze patterns to identify common detection triggers
        return {
            "total_detections": len(self.detection_patterns),
            "common_indicators": self._count_common_indicators(),
            "time_based_patterns": self._analyze_time_patterns(),
            "url_patterns": self._analyze_url_patterns()
        }
```

### 3. Performance Optimization

#### Monitor Resource Usage
```python
# Track performance bottlenecks
class PerformanceAnalyzer:
    def __init__(self):
        self.operation_times = defaultdict(list)
        self.resource_usage = []
    
    def record_operation_time(self, operation: str, duration: float):
        self.operation_times[operation].append(duration)
    
    def record_resource_usage(self, cpu: float, memory: float):
        self.resource_usage.append({
            "timestamp": datetime.now(),
            "cpu": cpu,
            "memory": memory
        })
    
    def identify_bottlenecks(self) -> List[str]:
        bottlenecks = []
        for operation, times in self.operation_times.items():
            avg_time = sum(times) / len(times)
            if avg_time > 5.0:  # Operations taking >5 seconds
                bottlenecks.append(f"{operation}: {avg_time:.2f}s avg")
        return bottlenecks
    
    def get_optimization_recommendations(self) -> List[str]:
        recommendations = []
        
        # CPU optimization
        cpu_usage = [r["cpu"] for r in self.resource_usage[-100:]]
        if cpu_usage and sum(cpu_usage) / len(cpu_usage) > 80:
            recommendations.append("High CPU usage detected. Consider reducing concurrent operations.")
        
        # Memory optimization
        memory_usage = [r["memory"] for r in self.resource_usage[-100:]]
        if memory_usage and sum(memory_usage) / len(memory_usage) > 85:
            recommendations.append("High memory usage detected. Consider implementing memory pooling.")
        
        return recommendations
```

### 4. Content Quality Analysis

#### Implement Quality Metrics
```python
# Track content extraction quality
class ContentQualityAnalyzer:
    def __init__(self):
        self.quality_metrics = defaultdict(list)
    
    def analyze_content_quality(self, reviews: List[Any]) -> Dict[str, Any]:
        quality_scores = []
        
        for review in reviews:
            score = self._calculate_quality_score(review)
            quality_scores.append(score)
        
        return {
            "average_quality": sum(quality_scores) / len(quality_scores),
            "quality_distribution": self._analyze_quality_distribution(quality_scores),
            "low_quality_count": len([s for s in quality_scores if s < 0.5]),
            "improvement_suggestions": self._generate_improvement_suggestions(quality_scores)
        }
    
    def _calculate_quality_score(self, review: Any) -> float:
        score = 0.0
        
        # Text length quality
        if hasattr(review, 'content'):
            content_length = len(review.content)
            if 50 <= content_length <= 1000:
                score += 0.3
            elif content_length > 1000:
                score += 0.2
        
        # Sentiment analysis quality
        if hasattr(review, 'sentiment_score') and review.sentiment_score is not None:
            score += 0.2
        
        # Metadata completeness
        if hasattr(review, 'author') and review.author != "Anonymous":
            score += 0.2
        
        if hasattr(review, 'rating') and review.rating > 0:
            score += 0.2
        
        if hasattr(review, 'date'):
            score += 0.1
        
        return min(1.0, score)
    
    def _generate_improvement_suggestions(self, quality_scores: List[float]) -> List[str]:
        suggestions = []
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        if avg_quality < 0.6:
            suggestions.append("Content quality is low. Review extraction selectors and validation logic.")
        
        low_quality_count = len([s for s in quality_scores if s < 0.5])
        if low_quality_count > len(quality_scores) * 0.3:
            suggestions.append("High percentage of low-quality content. Implement stricter validation.")
        
        return suggestions
```

## 📊 Monitoring and Maintenance

### Daily Health Checks
```python
# Create a health check script
async def daily_health_check():
    scraper = ChimeraEnterpriseScraper()
    
    # Check system resources
    import psutil
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    
    print(f"System Health:")
    print(f"  CPU: {cpu_percent}%")
    print(f"  Memory: {memory_percent}%")
    
    # Check scraper statistics
    if scraper.is_initialized:
        stats = scraper.get_scraping_summary()
        print(f"Scraper Health:")
        print(f"  Total targets: {stats['scraping_stats']['total_targets']}")
        print(f"  Success rate: {stats['scraping_stats']['completed_targets'] / stats['scraping_stats']['total_targets'] * 100:.1f}%")
        print(f"  Anti-detection events: {stats['anti_detection_events']}")
    
    # Check log files
    import os
    log_dir = "logs"
    if os.path.exists(log_dir):
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        print(f"Log Files: {len(log_files)} found")
        
        # Check for errors in recent logs
        for log_file in log_files[-3:]:  # Last 3 log files
            log_path = os.path.join(log_dir, log_file)
            with open(log_path, 'r') as f:
                content = f.read()
                error_count = content.lower().count('error')
                warning_count = content.lower().count('warning')
                print(f"  {log_file}: {error_count} errors, {warning_count} warnings")
```

### Weekly Performance Review
```python
# Analyze weekly performance trends
async def weekly_performance_review():
    # Export performance metrics for the week
    monitor = PerformanceMonitor()
    
    # Export last 7 days of data
    metrics_file = f"weekly_performance_{datetime.now().strftime('%Y%m%d')}.json"
    monitor.export_metrics(metrics_file, duration_minutes=10080)  # 7 days
    
    # Analyze trends
    summary = monitor.get_metrics_summary(duration_minutes=10080)
    
    print(f"Weekly Performance Summary:")
    print(f"  Average CPU: {summary.get('cpu', {}).get('average', 0):.1f}%")
    print(f"  Average Memory: {summary.get('memory', {}).get('average', 0):.1f}%")
    print(f"  Average Response Time: {summary.get('response_time', {}).get('average_ms', 0):.1f}ms")
    print(f"  Success Rate: {summary.get('success_rate', {}).get('average', 0):.1%}")
    
    # Check for performance degradation
    if summary.get('cpu', {}).get('average', 0) > 70:
        print("⚠️  High CPU usage detected. Consider optimization.")
    
    if summary.get('memory', {}).get('average', 0) > 80:
        print("⚠️  High memory usage detected. Check for memory leaks.")
    
    if summary.get('response_time', {}).get('average_ms', 0) > 5000:
        print("⚠️  Slow response times detected. Review network configuration.")
```

## 🎯 Success Metrics and KPIs

### Key Performance Indicators
- **Detection Rate**: Target <5% (vs. 100% for benchmarks)
- **Success Rate**: Target >90% successful extractions
- **Response Time**: Target <3 seconds average
- **Resource Usage**: CPU <70%, Memory <80%
- **Content Quality**: Average quality score >0.8

### Continuous Improvement
- Monitor selector success rates weekly
- Analyze detection patterns monthly
- Review performance metrics quarterly
- Update anti-detection strategies based on new threats

## 🆘 Getting Help

### Common Support Channels
1. **Check logs first**: Most issues are logged with detailed information
2. **Review this guide**: Solutions to common problems are documented above
3. **Check GitHub issues**: Look for similar problems and solutions
4. **Enable debug mode**: Use verbose logging to identify specific issues

### Debug Information to Collect
When reporting issues, include:
- Python version and platform
- Chimera version
- Complete error traceback
- Log files (with sensitive information removed)
- System resource usage at time of error
- Target URL and platform being scraped

---

**Remember**: Chimera is designed to be self-healing and adaptive. Most issues can be resolved by adjusting configuration parameters or waiting for the system to learn and adapt to new anti-detection measures.
