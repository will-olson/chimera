# Four-Way Comparison Scraping Guide

## Overview

This guide explains the comprehensive four-way comparison scraping capabilities added to Chimera, addressing the critical gap identified in the `SCRAPER_CAPABILITY_ANALYSIS.md`. The four-way comparison scraper captures detailed competitive intelligence data from G2.com comparison pages, providing insights that go far beyond basic review scraping.

## What is Four-Way Comparison Scraping?

Four-way comparison pages on G2.com (e.g., `https://www.g2.com/compare/microsoft-microsoft-power-bi-vs-qlik-sense-vs-tableau-vs-domo`) provide structured data comparing four products side-by-side across multiple dimensions:

- **At a Glance**: Star ratings, review counts, market segments, entry-level pricing
- **Ratings**: Detailed scores across criteria like "Meets Requirements", "Ease of Use", "Quality of Support"
- **Features by Category**: Product performance in specific feature areas
- **Pricing**: Comprehensive pricing information and strategies

## Key Capabilities

### 1. Comprehensive Data Extraction

The four-way comparison scraper extracts:

- **Product Information**: Names, G2 IDs, vendor IDs, star ratings, review counts
- **Market Intelligence**: Market segments, competitive positioning, pricing strategies
- **Feature Analysis**: Category-by-category performance ratings
- **Competitive Insights**: Market leaders, emerging players, competitive advantages

### 2. Intelligent Parsing

Based on analysis of actual G2.com comparison pages, the parser uses:

- **Multiple Selector Strategies**: Primary selectors, fallback methods, pattern matching
- **Aria-Label Parsing**: Leverages G2's accessibility attributes for reliable data extraction
- **Content Validation**: Quality scoring and confidence metrics for extracted data
- **Fallback Mechanisms**: Alternative extraction methods when primary methods fail

### 3. Market Intelligence Generation

Automatically generates insights including:

- **Competitive Positioning**: Market leaders vs. emerging players
- **Market Trends**: Enterprise focus, mid-market adoption patterns
- **Feature Competitiveness**: Strength areas, weakness areas, competitive advantages
- **Pricing Analysis**: Pricing tiers, strategies, competitive positioning

## Architecture

### Core Components

1. **`G2FourWayComparisonParser`** (`src/chimera/parsers/four_way_comparison.py`)
   - Specialized parser for four-way comparison pages
   - Handles complex HTML structures and data relationships
   - Provides quality scoring and confidence metrics

2. **`FourWayComparisonScraper`** (`src/chimera/core/four_way_comparison_scraper.py`)
   - Dedicated scraper for four-way comparison pages
   - Integrates with competitive intelligence system
   - Handles anti-detection and Cloudflare bypass

3. **Integrated Competitive Intelligence** (`src/chimera/core/competitive_intelligence_scraper.py`)
   - Automatically includes four-way comparisons in scraping workflows
   - Generates comprehensive market insights
   - Exports structured competitive intelligence data

### Data Models

```python
@dataclass
class FourWayComparisonData:
    comparison_id: str
    extraction_date: datetime
    url: str
    products: List[Dict[str, Any]]
    at_a_glance: Dict[str, Any]
    pricing: Dict[str, Any]
    ratings: Dict[str, Any]
    features_by_category: Dict[str, Any]
    total_products: int
    comparison_categories: List[str]
    data_quality_score: float
    extraction_confidence: float

@dataclass
class ProductComparison:
    name: str
    g2_product_id: str
    vendor_id: str
    star_rating: float
    review_count: int
    market_segments: Dict[str, float]
    entry_level_pricing: str
    pricing_details: Dict[str, Any]
    ratings_by_criteria: Dict[str, float]
    feature_scores: Dict[str, float]
```

## Usage Examples

### 1. Basic Four-Way Comparison Scraping

```python
from chimera.core.competitive_intelligence_scraper import CompetitiveIntelligenceScraper

# Initialize scraper
scraper = CompetitiveIntelligenceScraper()

# Scrape all competitive intelligence (including four-way comparisons)
insights = await scraper.scrape_competitive_intelligence()

# Filter for four-way comparison insights
four_way_insights = [i for i in insights if i.data_type == "four_way_comparison"]
```

### 2. Dedicated Four-Way Comparison Scraping

```python
from chimera.core.four_way_comparison_scraper import FourWayComparisonScraper
from chimera.core.competitive_intelligence_scraper import CompetitiveIntelligenceScraper

# Initialize scrapers
competitive_scraper = CompetitiveIntelligenceScraper()
four_way_scraper = FourWayComparisonScraper(competitive_scraper)

# Scrape all four-way comparisons
four_way_insights = await four_way_scraper.scrape_all_four_way_comparisons(
    competitive_scraper.competitive_targets
)

# Export data
export_files = await four_way_scraper.export_four_way_data(four_way_insights)
```

### 3. Direct Parser Usage

```python
from chimera.parsers.four_way_comparison import G2FourWayComparisonParser

# Initialize parser
parser = G2FourWayComparisonParser()

# Parse HTML content
comparison_data = await parser.parse_four_way_comparison(html_content, url)

# Access extracted data
print(f"Products: {len(comparison_data.products)}")
print(f"Quality Score: {comparison_data.data_quality_score}")
print(f"Extraction Confidence: {comparison_data.extraction_confidence}")
```

## Data Extraction Strategy

### 1. Product Identification

The parser uses multiple strategies to identify products:

- **Header Analysis**: Examines comparison container headers for product information
- **Aria-Label Parsing**: Extracts data from accessibility attributes
- **URL Pattern Matching**: Identifies products from comparison URLs
- **Fallback Text Extraction**: Searches for known product names in page content

### 2. Rating Extraction

Ratings are extracted using:

- **Aria-Label Patterns**: `"Product Name, Criterion X.X out of 10, based on Y reviews"`
- **Visual Element Analysis**: Donut charts, progress bars, numerical displays
- **Contextual Relationships**: Links between ratings and product information

### 3. Feature Analysis

Feature category ratings are extracted by:

- **Category Identification**: Recognizes standard G2 feature categories
- **Rating Matrix Parsing**: Maps products to categories to ratings
- **Data Quality Assessment**: Identifies "Not enough data" entries

## Anti-Detection Features

### 1. Stealth Navigation

- **Maximum Stealth Mode**: Uses all available anti-detection measures
- **Human Behavior Simulation**: Mimics competitive research behavior
- **Randomized Delays**: 8-15 second delays between comparisons

### 2. Cloudflare Bypass

- **Automatic Detection**: Identifies Cloudflare protection
- **Bypass Strategies**: Multiple approaches for different protection levels
- **Platform-Specific Handling**: Different strategies for G2 vs. Capterra

### 3. Session Management

- **Competitive Research Simulation**: Realistic browsing patterns
- **Performance Monitoring**: Tracks success rates and detection attempts
- **Adaptive Behavior**: Adjusts strategy based on success patterns

## Data Quality and Validation

### 1. Quality Scoring

The system provides comprehensive quality metrics:

- **Data Completeness**: Percentage of expected data successfully extracted
- **Extraction Confidence**: Confidence in the parsing process
- **Validation Results**: Checks for data consistency and completeness

### 2. Validation Checks

- **Product Count Validation**: Ensures expected number of products
- **Data Type Validation**: Verifies numerical ratings, text content
- **Relationship Validation**: Checks product-to-data mappings

### 3. Confidence Metrics

- **Structural Confidence**: Based on HTML structure recognition
- **Content Confidence**: Based on successful data extraction
- **Overall Confidence**: Combined metric for decision making

## Export and Analysis

### 1. Data Export Formats

The scraper exports data in multiple formats:

- **JSON Export**: Complete comparison data with metadata
- **Summary Report**: High-level insights and statistics
- **Statistics Export**: Scraping performance metrics

### 2. Market Intelligence Reports

Automatically generates:

- **Competitive Positioning Analysis**: Market leaders, emerging players
- **Feature Competitiveness**: Strength areas, weakness areas
- **Pricing Strategy Analysis**: Pricing tiers, competitive positioning
- **Market Trend Identification**: Enterprise focus, adoption patterns

### 3. Integration with Competitive Intelligence

Four-way comparison data is automatically integrated into:

- **Cross-Platform Analysis**: G2 and Capterra data correlation
- **Market Landscape Mapping**: Comprehensive competitive view
- **Strategic Recommendations**: Actionable competitive insights

## Testing and Validation

### 1. Test Script

Run the comprehensive test suite:

```bash
cd chimera-scraper
python test_four_way_comparison.py
```

The test script validates:
- Parser functionality with sample HTML
- Scraper initialization and configuration
- Integration with competitive intelligence system
- Data export capabilities

### 2. Sample Data Validation

The parser includes sample HTML based on actual G2.com comparison pages, ensuring:

- **Realistic Testing**: Uses actual HTML structure patterns
- **Edge Case Coverage**: Handles various data presentation formats
- **Quality Assurance**: Validates extraction accuracy

## Performance Considerations

### 1. Scraping Efficiency

- **Batch Processing**: Handles multiple comparisons efficiently
- **Resource Management**: Optimizes memory and CPU usage
- **Progress Tracking**: Real-time monitoring of scraping progress

### 2. Anti-Detection Optimization

- **Intelligent Delays**: Balances speed with stealth requirements
- **Session Reuse**: Maximizes data extraction per session
- **Error Recovery**: Continues processing despite individual failures

### 3. Data Storage

- **Incremental Export**: Saves data as it's extracted
- **Compression**: Efficient storage of large datasets
- **Backup Strategies**: Multiple export formats for data safety

## Troubleshooting

### 1. Common Issues

**Parser Failures**
- Check HTML structure changes on G2.com
- Verify selector patterns are still valid
- Review aria-label attribute patterns

**Scraping Failures**
- Monitor for Cloudflare protection changes
- Check anti-detection measure effectiveness
- Verify proxy and session configuration

**Data Quality Issues**
- Review quality scoring thresholds
- Check for new data presentation formats
- Validate extraction confidence metrics

### 2. Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use loguru
from loguru import logger
logger.add("debug.log", level="DEBUG")
```

### 3. Performance Monitoring

Monitor scraping performance:

```python
# Get scraping summary
summary = four_way_scraper.get_scraping_summary()
print(f"Success Rate: {summary['success_rate']:.1f}%")
print(f"Uptime: {summary['uptime_seconds']:.0f} seconds")
```

## Future Enhancements

### 1. Planned Features

- **Dynamic Selector Adaptation**: Automatic selector pattern updates
- **Machine Learning Integration**: Pattern recognition for new data formats
- **Real-Time Monitoring**: Live competitive intelligence dashboards

### 2. Scalability Improvements

- **Distributed Scraping**: Multi-instance coordination
- **Cloud Integration**: AWS/GCP deployment options
- **API Development**: RESTful API for data access

### 3. Advanced Analytics

- **Predictive Modeling**: Market trend forecasting
- **Competitive Alerting**: Real-time competitive intelligence
- **Custom Report Generation**: Tailored analysis outputs

## Conclusion

The four-way comparison scraping capabilities transform Chimera from a basic review scraper into a comprehensive competitive intelligence platform. By capturing the detailed comparison data that the benchmark scrapers attempted but failed to deliver, Chimera now provides:

- **Comprehensive Market Analysis**: Complete competitive landscape mapping
- **Strategic Intelligence**: Actionable competitive positioning insights
- **Data Quality Assurance**: Reliable extraction with confidence metrics
- **Scalable Architecture**: Enterprise-grade competitive intelligence platform

This implementation addresses the critical gap identified in the capability analysis and positions Chimera as the definitive solution for competitive intelligence data capture in the business software market.

## Next Steps

1. **Test the Implementation**: Run the test script to validate functionality
2. **Deploy in Production**: Integrate with existing competitive intelligence workflows
3. **Monitor Performance**: Track success rates and data quality metrics
4. **Iterate and Improve**: Refine selectors and parsing logic based on real-world usage
5. **Expand Coverage**: Add support for additional comparison types and platforms
