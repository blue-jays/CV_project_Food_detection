"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data
    assert "recipes_loaded" in data


def test_recipes_search():
    """Test recipe search endpoint."""
    response = client.get("/recipes?s=chicken,tomato&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "recipes" in data
    assert "query_ingredients" in data
    assert "total_results" in data
    assert len(data["recipes"]) <= 5


def test_recipes_search_invalid():
    """Test recipe search with no ingredients."""
    response = client.get("/recipes?s=")
    assert response.status_code == 400


def test_suggest_recipes():
    """Test recipe suggestion endpoint."""
    payload = {
        "ingredients": ["chicken", "rice", "garlic"],
        "max_results": 10
    }
    response = client.post("/suggest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "recipes" in data
    assert len(data["recipes"]) <= 10


def test_suggest_recipes_invalid():
    """Test recipe suggestion with empty ingredients."""
    payload = {
        "ingredients": [],
        "max_results": 10
    }
    response = client.post("/suggest", json=payload)
    assert response.status_code == 400


def test_get_recipe():
    """Test get recipe by ID."""
    response = client.get("/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "ingredients" in data


def test_get_recipe_not_found():
    """Test get recipe with invalid ID."""
    response = client.get("/recipes/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_detect_endpoint():
    """Test ingredient detection endpoint."""
    # Create a minimal test image (1x1 pixel PNG)
    import io
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {"file": ("test.png", img_bytes, "image/png")}
    response = client.post("/detect", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "ingredients" in data
    assert "processing_time_ms" in data
    assert isinstance(data["ingredients"], list)


def test_detect_invalid_file():
    """Test detection with non-image file."""
    files = {"file": ("test.txt", b"not an image", "text/plain")}
    response = client.post("/detect", files=files)
    assert response.status_code == 400
