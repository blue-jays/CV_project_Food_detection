"""OpenAI-powered recipe generation."""
import os
import json
from typing import List, Optional
from openai import OpenAI
from schemas import Recipe


class OpenAIRecipeGenerator:
    """Generate recipes using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI recipe generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {e}")
    
    def generate_recipes(self, ingredients: List[str], max_recipes: int = 5) -> List[Recipe]:
        """
        Generate recipes based on ingredients using OpenAI.
        
        Args:
            ingredients: List of ingredient names
            max_recipes: Maximum number of recipes to generate
            
        Returns:
            List of generated recipes
        """
        if not ingredients:
            return []
        
        # Create prompt
        ingredients_str = ", ".join(ingredients)
        prompt = f"""Generate {max_recipes} delicious recipes using these ingredients: {ingredients_str}

For each recipe, provide:
1. A creative title
2. Full list of ingredients (including the ones provided plus any additional needed)
3. Step-by-step cooking instructions
4. Cuisine type
5. Relevant tags (e.g., quick, vegetarian, healthy, comfort)
6. Estimated cooking time in minutes

Format your response as a JSON object with a "recipes" array:
{{
  "recipes": [
    {{
      "title": "Recipe Name",
      "ingredients": ["ingredient1", "ingredient2", ...],
      "instructions": "Step 1. Step 2. Step 3...",
      "cuisine": "Italian",
      "tags": ["quick", "vegetarian"],
      "time_minutes": 30
    }}
  ]
}}

Make the recipes practical, delicious, and creative. Ensure they prominently feature the provided ingredients."""

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional chef and recipe creator. Generate practical, delicious recipes in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Handle both direct array and wrapped object responses
            try:
                data = json.loads(content)
                if isinstance(data, dict) and 'recipes' in data:
                    recipes_data = data['recipes']
                elif isinstance(data, list):
                    recipes_data = data
                else:
                    recipes_data = [data]
            except json.JSONDecodeError:
                print(f"Failed to parse OpenAI response: {content}")
                return []
            
            # Convert to Recipe objects
            recipes = []
            for idx, recipe_data in enumerate(recipes_data[:max_recipes]):
                try:
                    recipe = Recipe(
                        id=1000 + idx,  # Use high IDs to avoid conflicts with CSV
                        title=recipe_data.get('title', 'Untitled Recipe'),
                        ingredients=recipe_data.get('ingredients', ingredients),
                        instructions=recipe_data.get('instructions', ''),
                        cuisine=recipe_data.get('cuisine', 'International'),
                        tags=recipe_data.get('tags', []),
                        time_minutes=recipe_data.get('time_minutes'),
                        score=1.0  # OpenAI recipes get high relevance score
                    )
                    recipes.append(recipe)
                except Exception as e:
                    print(f"Error creating recipe from data: {e}")
                    continue
            
            return recipes
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        return bool(self.api_key)


# Singleton instance
_generator_instance: Optional[OpenAIRecipeGenerator] = None


def get_openai_generator() -> Optional[OpenAIRecipeGenerator]:
    """Get or create singleton OpenAI generator instance."""
    global _generator_instance
    
    # Only create if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    
    if _generator_instance is None:
        try:
            _generator_instance = OpenAIRecipeGenerator(api_key)
        except ValueError:
            return None
    
    return _generator_instance
