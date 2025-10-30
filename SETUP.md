# 🚀 Snap2Recipe Setup Guide

Complete setup instructions for getting Snap2Recipe running locally.

## 📋 Prerequisites

Choose one of the following setups:

### Option A: Docker (Easiest)
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

### Option B: Local Development
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

## 🐳 Quick Start with Docker (Recommended)

This is the fastest way to get started:

```bash
# 1. Navigate to project directory
cd snap2recipe

# 2. Start all services
docker-compose up

# That's it! The app is now running:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

To run in background:
```bash
docker-compose up -d
```

To stop:
```bash
docker-compose down
```

## 💻 Local Development Setup

### Step 1: Backend Setup

```bash
# Navigate to API directory
cd api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (required for text processing)
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Copy environment file
cp .env.example .env

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### Step 2: Frontend Setup

Open a new terminal:

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

The frontend will be available at http://localhost:3000

## 🧪 Running Tests

### Backend Tests

```bash
cd api
pytest tests/ -v
```

### Frontend Tests

```bash
cd web
npm test
```

## 🔧 Configuration

### Backend Configuration

Edit `api/.env`:

```env
# Model settings
MODEL_WEIGHTS_PATH=./model/weights
MODEL_DEVICE=cpu  # Change to 'cuda' if you have GPU
MODEL_CONFIDENCE_THRESHOLD=0.3

# Data paths
RECIPES_PATH=../data/recipes.csv
SYNONYMS_PATH=../data/synonyms.json

# API settings
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration

Edit `web/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Adding Your Own Data

### Adding Recipes

1. Open `data/recipes.csv`
2. Add new rows following this format:

```csv
id,title,ingredients,instructions,cuisine,tags,time_minutes
11,Your Recipe,"ingredient1, ingredient2, ingredient3","Step 1. Step 2. Step 3.",Italian,"vegetarian,quick",30
```

3. Restart the API service

### Adding Ingredient Synonyms

1. Open `data/synonyms.json`
2. Add new mappings:

```json
{
  "existing": "mapping",
  "your_synonym": "standard_name"
}
```

3. Restart the API service

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

**Backend:**
```bash
# Change port in api/.env
API_PORT=8001

# Run with custom port
uvicorn main:app --reload --port 8001
```

**Frontend:**
```bash
# Run on different port
npm run dev -- -p 3001
```

### Module Not Found Errors

**Backend:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

```bash
# Rebuild containers
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v

# Start fresh
docker-compose up
```

### NLTK Data Missing

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

## 🎯 Next Steps

1. **Upload a test image**: Use any food photo to test ingredient detection
2. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
3. **Customize recipes**: Add your favorite recipes to `data/recipes.csv`
4. **Adjust UI**: Modify colors in `web/app/globals.css`
5. **Add custom model**: Place PyTorch weights in `api/model/weights/`

## 📚 Additional Resources

- [Main README](README.md) - Full project documentation
- [API README](api/README.md) - Backend details
- [Web README](web/README.md) - Frontend details
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)

## 💡 Tips

- Use `make dev` for one-command Docker startup
- Use `make test` to run all tests
- Check `docker-compose logs` for debugging
- Frontend hot-reloads on file changes
- Backend auto-reloads with `--reload` flag

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error logs in terminal
3. Ensure all prerequisites are installed
4. Try the Docker setup if local development fails
5. Open an issue on GitHub with error details

---

**Happy cooking! 🍳**
