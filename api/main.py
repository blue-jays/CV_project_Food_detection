"""FastAPI application for Snap2Recipe backend."""
import os
import time
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from schemas import (
    DetectResponse, IngredientDetection, Recipe,
    RecipeSearchRequest, RecipeSearchResponse, HealthResponse
)
from model.loader import get_detector
from model.food_classifier import get_food_classifier
from recipes.indexer import get_indexer
from recipes.openai_generator import get_openai_generator

# Load environment variables
load_dotenv()

# Configuration
MODEL_WEIGHTS_PATH = os.getenv('MODEL_WEIGHTS_PATH')
MODEL_DEVICE = os.getenv('MODEL_DEVICE', 'cpu')
MODEL_CONFIDENCE_THRESHOLD = float(os.getenv('MODEL_CONFIDENCE_THRESHOLD', '0.3'))
RECIPES_PATH = os.getenv('RECIPES_PATH', '../data/recipes.csv')
SYNONYMS_PATH = os.getenv('SYNONYMS_PATH', '../data/synonyms.json')
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

# Initialize FastAPI app
app = FastAPI(
    title="Snap2Recipe API",
    description="Ingredient detection and recipe suggestion API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (lazy loaded)
detector = None
indexer = None


def get_or_create_detector():
    """Get or create detector instance."""
    global detector
    if detector is None:
        detector = get_detector(
            weights_path=MODEL_WEIGHTS_PATH,
            device=MODEL_DEVICE,
            confidence_threshold=MODEL_CONFIDENCE_THRESHOLD
        )
    return detector


def get_or_create_indexer():
    """Get or create indexer instance."""
    global indexer
    if indexer is None:
        indexer = get_indexer(RECIPES_PATH, SYNONYMS_PATH)
    return indexer


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("Starting Snap2Recipe API...")
    
    # Initialize food classifier
    classifier = get_food_classifier(device=MODEL_DEVICE)
    print("✓ Food classifier loaded")
    
    # Initialize recipe indexer
    get_or_create_indexer()
    print("✓ Recipe index built")
    
    print("API ready!")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Snap2Recipe API",
        "version": "1.0.0",
        "endpoints": {
            "detect": "/detect",
            "recipes": "/recipes",
            "suggest": "/suggest",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    det = get_or_create_detector()
    idx = get_or_create_indexer()
    
    return HealthResponse(
        status="healthy",
        model_loaded=det.is_loaded(),
        recipes_loaded=idx.get_recipe_count()
    )


@app.post("/detect", response_model=DetectResponse, tags=["Detection"])
async def detect_ingredients(file: UploadFile = File(...)):
    """
    Detect ingredients from uploaded image.
    
    Args:
        file: Image file (JPEG, PNG)
        
    Returns:
        List of detected ingredients with confidence scores
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image bytes
    try:
        image_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image: {str(e)}")
    
    # Run food classification
    start_time = time.time()
    classifier = get_food_classifier(device=MODEL_DEVICE)
    
    try:
        detections = classifier.predict(image_bytes, top_k=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")
    
    processing_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Format response
    ingredients = [
        IngredientDetection(name=name, score=score)
        for name, score in detections
    ]
    
    return DetectResponse(
        ingredients=ingredients,
        processing_time_ms=processing_time
    )


@app.get("/recipes", response_model=RecipeSearchResponse, tags=["Recipes"])
async def search_recipes(s: str = Query(..., description="Comma-separated ingredients"),
                        limit: int = Query(20, description="Maximum results")):
    """
    Search for recipes by ingredients (GET endpoint).
    
    Args:
        s: Comma-separated ingredient names
        limit: Maximum number of results
        
    Returns:
        List of matching recipes
    """
    print(f"\n{'='*50}")
    print(f"RECIPE SEARCH REQUEST RECEIVED")
    print(f"Raw ingredients string: {s}")
    print(f"Limit: {limit}")
    print(f"{'='*50}\n")
    
    # Parse ingredients
    ingredients = [ing.strip() for ing in s.split(',') if ing.strip()]
    
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
    
    # Try OpenAI first, fallback to local search
    recipes = []
    try:
        openai_gen = get_openai_generator()
        print(f"OpenAI generator: {openai_gen}")
        if openai_gen and openai_gen.is_available():
            print(f"Generating recipes with OpenAI for ingredients: {ingredients}")
            recipes = openai_gen.generate_recipes(ingredients, max_recipes=limit)
            print(f"OpenAI returned {len(recipes)} recipes")
        else:
            print("OpenAI not available, using local search")
    except Exception as e:
        print(f"OpenAI generation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Fallback to local BM25 search if no OpenAI recipes
    if not recipes:
        print(f"Falling back to local BM25 search for: {ingredients}")
        idx = get_or_create_indexer()
        recipes = idx.search(ingredients, k=limit)
        print(f"Local search returned {len(recipes)} recipes")
        
        # Filter out recipes with very low scores (< 0.5)
        recipes = [r for r in recipes if r.score >= 0.5]
        print(f"After filtering low scores: {len(recipes)} recipes")
        
        # If still no good matches, return empty
        if not recipes:
            print("No recipes with good match scores found")
    
    return RecipeSearchResponse(
        recipes=recipes,
        query_ingredients=ingredients,
        total_results=len(recipes)
    )


@app.post("/suggest", response_model=RecipeSearchResponse, tags=["Recipes"])
async def suggest_recipes(request: RecipeSearchRequest):
    """
    Suggest recipes based on ingredients (POST endpoint).
    
    Args:
        request: Search request with ingredients list
        
    Returns:
        List of matching recipes
    """
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
    
    # Try OpenAI first, fallback to local search
    recipes = []
    try:
        openai_gen = get_openai_generator()
        if openai_gen and openai_gen.is_available():
            recipes = openai_gen.generate_recipes(request.ingredients, max_recipes=request.max_results)
    except Exception as e:
        print(f"OpenAI generation failed: {e}")
    
    # Fallback to local BM25 search if no OpenAI recipes
    if not recipes:
        idx = get_or_create_indexer()
        recipes = idx.search(request.ingredients, k=request.max_results)
        
        # Filter out recipes with very low scores (< 0.5)
        recipes = [r for r in recipes if r.score >= 0.5]
    
    return RecipeSearchResponse(
        recipes=recipes,
        query_ingredients=request.ingredients,
        total_results=len(recipes)
    )


@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
async def get_recipe(recipe_id: int):
    """
    Get a specific recipe by ID.
    
    Args:
        recipe_id: Recipe ID
        
    Returns:
        Recipe details
    """
    idx = get_or_create_indexer()
    recipe = idx.get_recipe_by_id(recipe_id)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', '8000')),
        reload=True
    )
