"""Tests for storage utilities."""
import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime
from chimera.models.review import Review
from chimera.utils.storage import save_to_json, save_to_csv


@pytest.fixture
def sample_reviews():
    """Create sample review data for testing."""
    return [
        Review(
            review_id="test_1",
            source="G2",
            title="Test Review 1",
            content="This is a test review",
            rating=4.5,
            author="Test User 1",
            date=datetime.now(),
            url="https://g2.com/test1"
        ),
        Review(
            review_id="test_2",
            source="G2",
            title="Test Review 2",
            content="This is another test review",
            rating=3.0,
            author="Test User 2",
            date=datetime.now(),
            url="https://g2.com/test2"
        )
    ]


@pytest.mark.asyncio
async def test_save_to_json(sample_reviews):
    """Test saving reviews to JSON."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            filepath = await save_to_json(sample_reviews, "test_reviews.json")
            
            assert os.path.exists(filepath)
            assert filepath.endswith("test_reviews.json")
            
            # Verify file content
            with open(filepath, 'r') as f:
                content = f.read()
                assert "Test Review 1" in content
                assert "Test Review 2" in content
                
        finally:
            os.chdir(original_cwd)


@pytest.mark.asyncio
async def test_save_to_csv(sample_reviews):
    """Test saving reviews to CSV."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            filepath = await save_to_csv(sample_reviews, "test_reviews.csv")
            
            assert os.path.exists(filepath)
            assert filepath.endswith("test_reviews.csv")
            
            # Verify CSV content
            with open(filepath, 'r') as f:
                content = f.read()
                assert "review_id,source,title,content,rating,author,date,url" in content
                assert "test_1,G2,Test Review 1" in content
                
        finally:
            os.chdir(original_cwd)


@pytest.mark.asyncio
async def test_save_to_json_default_filename(sample_reviews):
    """Test saving reviews with default filename."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            filepath = await save_to_json(sample_reviews)
            
            assert os.path.exists(filepath)
            # Should contain timestamp
            assert "reviews_" in filepath
            assert filepath.endswith(".json")
            
        finally:
            os.chdir(original_cwd)


@pytest.mark.asyncio
async def test_save_empty_reviews():
    """Test saving empty review list."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory for testing
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            csv_filepath = await save_to_csv([])
            assert csv_filepath is None
            
        finally:
            os.chdir(original_cwd)
