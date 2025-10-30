# 🍽️ Snap2Recipe

**Detect ingredients from food photos and discover delicious recipes**

A production-ready, open-source web application that uses computer vision to identify ingredients from food images and suggests matching recipes using intelligent search algorithms.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-14-black.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)

## ✨ Features

- 📸 **Image Upload**: Drag-and-drop or click to upload food photos
- 🔍 **Ingredient Detection**: AI-powered ingredient recognition using PyTorch
- 🍳 **Recipe Suggestions**: Smart recipe matching with BM25 ranking
- 🏷️ **Ingredient Selection**: Toggle detected ingredients to refine search
- 📚 **Recipe Details**: View full ingredients, instructions, cooking time, and cuisine
- 📜 **History**: Keep track of your last 5 detections (localStorage)
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS and shadcn/ui
- 🐳 **Docker Ready**: One-command deployment with docker-compose

## 🏗️ Architecture

```
snap2recipe/
├── api/                    # FastAPI backend
│   ├── model/             # ML model loader (PyTorch)
│   ├── recipes/           # Recipe indexing (BM25)
│   ├── utils/             # Text normalization
│   ├── main.py            # FastAPI app
│   ├── schemas.py         # Pydantic models
│   └── tests/             # Backend tests
├── web/                   # Next.js 14 frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/               # API client & utilities
│   └── tests/             # E2E tests (Playwright)
├── data/                  # Recipe data & synonyms
│   ├── recipes.csv        # Recipe database
│   └── synonyms.json      # Ingredient synonyms
├── docker-compose.yml     # Orchestration
└── Makefile              # Development commands
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OR: Python 3.11+ and Node.js 18+

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd snap2recipe

# Start all services
make dev
# or
docker-compose up
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

```bash
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

## 📖 Usage

1. **Upload a Food Photo**
   - Drag and drop an image or click to browse
   - Supports JPG, PNG, WebP formats

2. **Detect Ingredients**
   - Click "Detect Ingredients" button
   - AI model analyzes the image and identifies ingredients

3. **Refine Selection**
   - Toggle ingredients on/off by clicking chips
   - Confidence scores shown as percentages

4. **Find Recipes**
   - Click "Find Recipes" to search
   - Results ranked by ingredient match score

5. **Explore Recipes**
   - View recipe cards with key details
   - Expand to see full ingredients and instructions
   - Filter by cuisine, tags, and cooking time

## 🧪 Testing

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

## 🛠️ Development

### Available Commands

```bash
make install    # Install all dependencies
make dev        # Start development environment
make build      # Build Docker images
make test       # Run all tests
make clean      # Clean build artifacts
```

### Backend API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /detect` - Detect ingredients from image
- `GET /recipes?s=ing1,ing2` - Search recipes by ingredients
- `POST /suggest` - Suggest recipes (POST body)
- `GET /recipes/{id}` - Get specific recipe

### Environment Variables

**Backend (`api/.env`)**
```env
MODEL_WEIGHTS_PATH=./model/weights
MODEL_DEVICE=cpu
MODEL_CONFIDENCE_THRESHOLD=0.3
RECIPES_PATH=../data/recipes.csv
SYNONYMS_PATH=../data/synonyms.json
CORS_ORIGINS=http://localhost:3000
```

**Frontend (`web/.env.local`)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤖 ML Model

The ingredient detection uses a PyTorch-based model with fallback to COCO-pretrained Faster R-CNN:

- **Primary**: Custom food recognition model (when weights provided)
- **Fallback**: torchvision's Faster R-CNN with food-related COCO classes
- **Inference**: CPU by default, configurable to GPU
- **Caching**: LRU cache for recent predictions

To use custom weights:
1. Place model weights in `api/model/weights/`
2. Set `MODEL_WEIGHTS_PATH` environment variable

## 🔍 Recipe Search

The recipe search uses **BM25 (Best Matching 25)** ranking algorithm:

- **Text Normalization**: Lowercasing, lemmatization, stopword removal
- **Synonym Mapping**: Handles ingredient variations (e.g., "capsicum" → "bell pepper")
- **Plural Handling**: Automatic singular/plural normalization
- **Scoring**: Relevance-based ranking with configurable parameters

## 📊 Data

### Recipe Format (`data/recipes.csv`)

```csv
id,title,ingredients,instructions,cuisine,tags,time_minutes
1,Margherita Pizza,"tomato sauce, mozzarella, basil","Roll dough...",Italian,"vegetarian,quick",30
```

### Synonym Mapping (`data/synonyms.json`)

```json
{
  "capsicum": "bell pepper",
  "garbanzo": "chickpea",
  "scallion": "green onion"
}
```

## 🎨 Frontend Components

- **UploadBox**: Drag-and-drop image upload with preview
- **IngredientChips**: Selectable ingredient tags with confidence scores
- **RecipeCard**: Expandable recipe cards with details
- **LoadingOverlay**: Loading states for async operations
- **HistoryDrawer**: Sidebar with recent detection history

## 🐳 Docker Deployment

### Production Build

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose up -d
```

### Scaling

```bash
# Scale API service
docker-compose up -d --scale api=3
```

## 🔧 Configuration

### Adding More Recipes

1. Edit `data/recipes.csv`
2. Follow the CSV format
3. Restart the API service

### Adding Synonyms

1. Edit `data/synonyms.json`
2. Add key-value pairs
3. Restart the API service

### Customizing UI

- Colors: Edit `web/app/globals.css` CSS variables
- Components: Modify files in `web/components/`
- Styling: Tailwind classes in component files

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- FastAPI for the excellent Python web framework
- Next.js team for the React framework
- Vercel for shadcn/ui components
- COCO dataset for pretrained models

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Next.js, and PyTorch**
