# Snap2Recipe Web

Next.js 14 frontend for Snap2Recipe.

## Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm test` - Run Playwright tests

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Components

- **UploadBox** - Image upload with drag-and-drop
- **IngredientChips** - Selectable ingredient tags
- **RecipeCard** - Recipe display with expand/collapse
- **LoadingOverlay** - Loading state indicator
- **HistoryDrawer** - Recent detections sidebar

## Testing

```bash
npm test
```
