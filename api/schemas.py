"""Pydantic schemas for API request/response models."""
from typing import List, Optional
from pydantic import BaseModel, Field


class IngredientDetection(BaseModel):
    """Single ingredient detection result."""
    name: str = Field(..., description="Ingredient name")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class DetectResponse(BaseModel):
    """Response model for ingredient detection endpoint."""
    ingredients: List[IngredientDetection] = Field(..., description="Detected ingredients")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class Recipe(BaseModel):
    """Recipe model with all details."""
    id: int = Field(..., description="Recipe ID")
    title: str = Field(..., description="Recipe title")
    ingredients: List[str] = Field(..., description="List of ingredients")
    instructions: str = Field(..., description="Cooking instructions")
    cuisine: str = Field(..., description="Cuisine type")
    tags: List[str] = Field(..., description="Recipe tags")
    time_minutes: Optional[int] = Field(None, description="Cooking time in minutes")
    score: Optional[float] = Field(None, description="Relevance score for search results")


class RecipeSearchRequest(BaseModel):
    """Request model for recipe search."""
    ingredients: List[str] = Field(..., min_length=1, description="List of ingredients to search")
    max_results: int = Field(20, ge=1, le=100, description="Maximum number of results")


class RecipeSearchResponse(BaseModel):
    """Response model for recipe search."""
    recipes: List[Recipe] = Field(..., description="Matching recipes")
    query_ingredients: List[str] = Field(..., description="Normalized query ingredients")
    total_results: int = Field(..., description="Total number of results")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    recipes_loaded: int = Field(..., description="Number of recipes loaded")
