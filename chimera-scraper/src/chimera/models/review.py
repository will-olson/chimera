from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ReviewSentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Review(BaseModel):
    id: str = Field(..., alias="review_id")
    source: str
    title: str
    content: str
    rating: float
    author: str
    author_role: Optional[str] = None
    date: datetime
    url: str
    raw_data: Optional[dict] = None  # Store original HTML snippet for debugging
    
    class Config:
        allow_population_by_field_name = True


class EnhancedReview(Review):
    """Enhanced review model with additional fields for competitive intelligence."""
    
    # Sentiment analysis
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description="Sentiment score from -1 to 1")
    sentiment_label: Optional[ReviewSentiment] = Field(None, description="Categorized sentiment")
    
    # Competitive intelligence
    competitor_mentions: List[str] = Field(default_factory=list, description="Competitors mentioned in review")
    feature_mentions: List[str] = Field(default_factory=list, description="Features mentioned in review")
    pain_points: List[str] = Field(default_factory=list, description="Pain points mentioned in review")
    
    # Quality metrics
    review_quality_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Review quality score")
    extraction_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence in extraction")
    word_count: Optional[int] = Field(None, ge=0, description="Number of words in review")
    
    # Additional metadata
    pros: List[str] = Field(default_factory=list, description="Pros mentioned in review")
    cons: List[str] = Field(default_factory=list, description="Cons mentioned in review")
    use_case: Optional[str] = Field(None, description="Use case mentioned in review")
    industry: Optional[str] = Field(None, description="Industry mentioned in review")
    
    # Technical metadata
    extraction_method: Optional[str] = Field(None, description="Method used to extract review")
    selector_used: Optional[str] = Field(None, description="CSS selector used for extraction")
    extraction_timestamp: Optional[datetime] = Field(None, description="When extraction occurred")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class ReviewBatch(BaseModel):
    """Model for batch review processing."""
    
    batch_id: str = Field(..., description="Unique batch identifier")
    source_platform: str = Field(..., description="Platform being scraped")
    target_company: str = Field(..., description="Company being reviewed")
    extraction_date: datetime = Field(default_factory=datetime.now, description="Date of extraction")
    
    # Review data
    reviews: List[EnhancedReview] = Field(default_factory=list, description="List of extracted reviews")
    
    # Batch statistics
    total_reviews: int = Field(0, description="Total number of reviews in batch")
    successful_extractions: int = Field(0, description="Number of successfully extracted reviews")
    failed_extractions: int = Field(0, description="Number of failed extractions")
    
    # Quality metrics
    average_rating: Optional[float] = Field(None, description="Average rating across all reviews")
    sentiment_distribution: Optional[dict] = Field(None, description="Distribution of sentiment scores")
    
    # Metadata
    extraction_metadata: Optional[dict] = Field(None, description="Additional extraction metadata")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
    
    def update_statistics(self):
        """Update batch statistics based on current reviews."""
        self.total_reviews = len(self.reviews)
        self.successful_extractions = len([r for r in self.reviews if r.extraction_confidence and r.extraction_confidence > 0.5])
        self.failed_extractions = self.total_reviews - self.successful_extractions
        
        if self.reviews:
            ratings = [r.rating for r in self.reviews if r.rating and r.rating > 0]
            if ratings:
                self.average_rating = sum(ratings) / len(ratings)
            
            # Calculate sentiment distribution
            sentiments = [r.sentiment_label for r in self.reviews if r.sentiment_label]
            if sentiments:
                self.sentiment_distribution = {
                    sentiment.value: sentiments.count(sentiment) 
                    for sentiment in ReviewSentiment
                }
