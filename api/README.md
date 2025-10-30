# Snap2Recipe API

FastAPI backend for ingredient detection and recipe suggestion.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Run server
uvicorn main:app --reload
```

## Endpoints

- `POST /detect` - Detect ingredients from image
- `GET /recipes` - Search recipes by ingredients
- `POST /suggest` - Suggest recipes (POST body)
- `GET /health` - Health check

## Testing

```bash
pytest tests/ -v
```

## Environment Variables

See `.env.example` for configuration options.
