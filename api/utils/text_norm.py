"""Text normalization utilities for ingredient matching."""
import json
import re
import string
from pathlib import Path
from typing import Dict, List, Set, Optional
import nltk
from nltk.stem import WordNetLemmatizer


# Download required NLTK data
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)


class TextNormalizer:
    """Handles text normalization for ingredient matching."""
    
    def __init__(self, synonyms_path: str, stopwords: Optional[Set[str]] = None):
        """
        Initialize text normalizer.
        
        Args:
            synonyms_path: Path to synonyms JSON file
            stopwords: Optional set of stopwords to remove
        """
        self.lemmatizer = WordNetLemmatizer()
        self.synonyms = self._load_synonyms(synonyms_path)
        
        # Common stopwords that don't affect recipe matching
        self.stopwords = stopwords or {
            'water', 'salt', 'pepper', 'oil', 'optional', 
            'to', 'taste', 'fresh', 'dried', 'ground'
        }
        
        # Plural to singular common mappings
        self.plural_map = {
            'tomatoes': 'tomato',
            'potatoes': 'potato',
            'onions': 'onion',
            'peppers': 'pepper',
            'mushrooms': 'mushroom',
            'beans': 'bean',
            'peas': 'pea',
            'carrots': 'carrot',
            'eggs': 'egg',
            'noodles': 'noodle',
        }
    
    def _load_synonyms(self, path: str) -> Dict[str, str]:
        """Load synonym mappings from JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Synonyms file not found at {path}")
            return {}
    
    def normalize(self, text: str, remove_stopwords: bool = False) -> str:
        """
        Normalize a single text string.
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stopwords
            
        Returns:
            Normalized text
        """
        # Lowercase
        text = text.lower().strip()
        
        # Remove punctuation except hyphens (for compound words)
        text = re.sub(r'[^\w\s-]', ' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        # Apply synonym mapping
        if text in self.synonyms:
            text = self.synonyms[text]
        
        # Handle common plurals
        if text in self.plural_map:
            text = self.plural_map[text]
        
        # Lemmatize
        words = text.split()
        words = [self.lemmatizer.lemmatize(word) for word in words]
        
        # Remove stopwords if requested
        if remove_stopwords:
            words = [w for w in words if w not in self.stopwords]
        
        return ' '.join(words)
    
    def normalize_list(self, items: List[str], remove_stopwords: bool = False) -> List[str]:
        """
        Normalize a list of text items.
        
        Args:
            items: List of text items
            remove_stopwords: Whether to remove stopwords
            
        Returns:
            List of normalized items
        """
        return [self.normalize(item, remove_stopwords) for item in items]
    
    def tokenize_ingredients(self, ingredients_str: str) -> List[str]:
        """
        Tokenize comma-separated ingredients string.
        
        Args:
            ingredients_str: Comma-separated ingredients
            
        Returns:
            List of normalized ingredient tokens
        """
        # Split by comma
        items = [item.strip() for item in ingredients_str.split(',')]
        
        # Normalize each ingredient
        normalized = []
        for item in items:
            # Remove quantities and measurements
            item = re.sub(r'\d+(\.\d+)?\s*(cup|tbsp|tsp|oz|lb|g|kg|ml|l)s?', '', item)
            item = re.sub(r'\d+/\d+', '', item)  # Remove fractions
            item = re.sub(r'\d+', '', item)  # Remove numbers
            
            # Normalize
            norm = self.normalize(item, remove_stopwords=True)
            if norm:  # Only add non-empty results
                normalized.append(norm)
        
        return normalized
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms from text for indexing.
        
        Args:
            text: Input text
            
        Returns:
            List of key terms
        """
        # Normalize
        normalized = self.normalize(text, remove_stopwords=True)
        
        # Split into words
        words = normalized.split()
        
        # Filter short words
        words = [w for w in words if len(w) > 2]
        
        return words


# Singleton instance
_normalizer_instance = None


def get_normalizer(synonyms_path: str = "../data/synonyms.json") -> TextNormalizer:
    """Get or create singleton normalizer instance."""
    global _normalizer_instance
    if _normalizer_instance is None:
        _normalizer_instance = TextNormalizer(synonyms_path)
    return _normalizer_instance
