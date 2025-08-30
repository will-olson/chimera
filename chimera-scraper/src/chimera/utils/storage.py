import json
import csv
import aiofiles
from typing import List
from datetime import datetime
from pathlib import Path

from chimera.models.review import Review

async def save_to_json(reviews: List[Review], filename: str = None):
    """Save reviews to JSON file."""
    if not filename:
        filename = f"reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Create directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    filepath = f"output/{filename}"
    data = [review.dict(by_alias=True) for review in reviews]
    
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, indent=2, default=str))
        
    return filepath

async def save_to_csv(reviews: List[Review], filename: str = None):
    """Save reviews to CSV file."""
    if not filename:
        filename = f"reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Create directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)
    
    filepath = f"output/{filename}"
    
    if not reviews:
        return None
        
    # Extract field names from the first review
    fieldnames = list(reviews[0].dict(by_alias=True).keys())
    
    async with aiofiles.open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        await writer.writeheader()
        for review in reviews:
            await writer.writerow(review.dict(by_alias=True, exclude_none=True))
            
    return filepath
