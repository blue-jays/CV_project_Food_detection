"""Recipe indexing and search using BM25."""
import csv
from pathlib import Path
from typing import List, Optional
from rank_bm25 import BM25Okapi
from schemas import Recipe
from utils.text_norm import get_normalizer


class RecipeIndexer:
    """Handles recipe loading, indexing, and search."""
    
    def __init__(self, recipes_path: str, synonyms_path: str):
        """
        Initialize recipe indexer.
        
        Args:
            recipes_path: Path to recipes CSV file
            synonyms_path: Path to synonyms JSON file
        """
        self.recipes_path = Path(recipes_path)
        self.normalizer = get_normalizer(synonyms_path)
        self.recipes: List[Recipe] = []
        self.bm25: Optional[BM25Okapi] = None
        self.tokenized_corpus: List[List[str]] = []
        
        # Load and index recipes
        self._load_recipes()
        self._build_index()
    
    def _load_recipes(self):
        """Load recipes from CSV file."""
        if not self.recipes_path.exists():
            raise FileNotFoundError(f"Recipes file not found: {self.recipes_path}")
        
        with open(self.recipes_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Parse ingredients list
                    ingredients = [ing.strip() for ing in row['ingredients'].split(',')]
                    
                    # Parse tags
                    tags = [tag.strip() for tag in row['tags'].split(',')]
                    
                    # Parse time (optional)
                    time_minutes = None
                    if row.get('time_minutes'):
                        try:
                            time_minutes = int(row['time_minutes'])
                        except ValueError:
                            pass
                    
                    recipe = Recipe(
                        id=int(row['id']),
                        title=row['title'],
                        ingredients=ingredients,
                        instructions=row['instructions'],
                        cuisine=row['cuisine'],
                        tags=tags,
                        time_minutes=time_minutes
                    )
                    self.recipes.append(recipe)
                except (KeyError, ValueError) as e:
                    print(f"Warning: Skipping invalid recipe row: {e}")
                    continue
        
        print(f"Loaded {len(self.recipes)} recipes")
    
    def _build_index(self):
        """Build BM25 index from recipes."""
        # Tokenize each recipe's ingredients for indexing
        self.tokenized_corpus = []
        
        for recipe in self.recipes:
            # Combine ingredients into searchable tokens
            ingredient_text = ' '.join(recipe.ingredients)
            tokens = self.normalizer.tokenize_ingredients(ingredient_text)
            
            # Also add title tokens for better matching
            title_tokens = self.normalizer.extract_key_terms(recipe.title)
            
            # Combine all tokens
            all_tokens = tokens + title_tokens
            self.tokenized_corpus.append(all_tokens)
        
        # Build BM25 index
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        print(f"Built BM25 index for {len(self.tokenized_corpus)} recipes")
    
    def search(self, ingredients: List[str], k: int = 20) -> List[Recipe]:
        """
        Search for recipes matching given ingredients.
        
        Args:
            ingredients: List of ingredient names
            k: Maximum number of results to return
            
        Returns:
            List of matching recipes with scores
        """
        if not self.bm25:
            return []
        
        # Normalize query ingredients
        print(f"Original ingredients: {ingredients}")
        normalized_ingredients = self.normalizer.normalize_list(ingredients, remove_stopwords=True)
        print(f"Normalized ingredients: {normalized_ingredients}")
        
        # Tokenize query
        query_tokens = []
        for ing in normalized_ingredients:
            query_tokens.extend(ing.split())
        
        # Remove duplicates while preserving order
        seen = set()
        query_tokens = [t for t in query_tokens if not (t in seen or seen.add(t))]
        print(f"Query tokens: {query_tokens}")
        
        if not query_tokens:
            print("No query tokens after normalization!")
            return []
        
        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)
        print(f"BM25 scores: {scores}")
        
        # Get top-k results (include ALL results, even with score 0, then filter later)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        
        # Build results with scores
        results = []
        for idx in top_indices:
            # Lower threshold - include recipes with any score >= 0
            recipe = self.recipes[idx].model_copy()
            recipe.score = float(scores[idx])
            results.append(recipe)
            print(f"  Recipe: {recipe.title}, Score: {recipe.score}")
        
        print(f"Returning {len(results)} recipes")
        return results
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get a recipe by its ID."""
        for recipe in self.recipes:
            if recipe.id == recipe_id:
                return recipe
        return None
    
    def get_all_recipes(self, limit: Optional[int] = None) -> List[Recipe]:
        """Get all recipes, optionally limited."""
        if limit:
            return self.recipes[:limit]
        return self.recipes
    
    def get_recipe_count(self) -> int:
        """Get total number of recipes."""
        return len(self.recipes)


# Singleton instance
_indexer_instance: Optional[RecipeIndexer] = None


def get_indexer(recipes_path: str, synonyms_path: str) -> RecipeIndexer:
    """Get or create singleton indexer instance."""
    global _indexer_instance
    if _indexer_instance is None:
        _indexer_instance = RecipeIndexer(recipes_path, synonyms_path)
    return _indexer_instance
