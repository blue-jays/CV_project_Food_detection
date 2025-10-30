'use client'

import { useState } from 'react'
import { ChefHat, Search, History as HistoryIcon } from 'lucide-react'
import UploadBox from '@/components/UploadBox'
import IngredientChips from '@/components/IngredientChips'
import RecipeCard from '@/components/RecipeCard'
import LoadingOverlay from '@/components/LoadingOverlay'
import HistoryDrawer from '@/components/HistoryDrawer'
import { detectIngredients, searchRecipes, Recipe } from '@/lib/api'
import { getHistory, addToHistory, clearHistory, HistoryItem } from '@/lib/history'

interface Ingredient {
  name: string
  score: number
  selected: boolean
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [ingredients, setIngredients] = useState<Ingredient[]>([])
  const [recipes, setRecipes] = useState<Recipe[]>([])
  const [isDetecting, setIsDetecting] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [historyDrawerOpen, setHistoryDrawerOpen] = useState(false)
  const [history, setHistory] = useState<HistoryItem[]>([])

  // Load history on mount
  useState(() => {
    setHistory(getHistory())
  })

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    setError(null)
    setIngredients([])
    setRecipes([])

    // Create preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result as string)
    }
    reader.readAsDataURL(file)
  }

  const handleClear = () => {
    setSelectedFile(null)
    setImagePreview(null)
    setIngredients([])
    setRecipes([])
    setError(null)
  }

  const handleDetect = async () => {
    if (!selectedFile) return

    setIsDetecting(true)
    setError(null)

    try {
      const result = await detectIngredients(selectedFile)
      const detectedIngredients = result.ingredients.map(ing => ({
        ...ing,
        selected: true,
      }))
      setIngredients(detectedIngredients)

      // Add to history
      if (imagePreview) {
        addToHistory(
          imagePreview,
          detectedIngredients.map(i => i.name)
        )
        setHistory(getHistory())
      }
    } catch (err: any) {
      const errorMessage = err?.response?.data?.detail || err?.message || 'Failed to detect ingredients. Please try again.'
      setError(errorMessage)
      console.error('Detection error:', err)
    } finally {
      setIsDetecting(false)
    }
  }

  const handleToggleIngredient = (index: number) => {
    setIngredients(prev =>
      prev.map((ing, i) => (i === index ? { ...ing, selected: !ing.selected } : ing))
    )
  }

  const handleFindRecipes = async () => {
    console.log('=== FIND RECIPES BUTTON CLICKED ===')
    const selectedIngredients = ingredients.filter(ing => ing.selected).map(ing => ing.name)
    console.log('Selected ingredients:', selectedIngredients)

    if (selectedIngredients.length === 0) {
      setError('Please select at least one ingredient')
      console.log('ERROR: No ingredients selected')
      return
    }

    console.log('Starting recipe search...')
    setIsSearching(true)
    setError(null)

    try {
      console.log('Calling searchRecipes API with:', selectedIngredients)
      const result = await searchRecipes(selectedIngredients, 20)
      console.log('Recipe search result:', result)
      setRecipes(result.recipes)

      if (result.recipes.length === 0) {
        setError('No recipes found. Try different ingredients.')
      }
    } catch (err: any) {
      const errorMsg = err?.response?.data?.detail || err?.message || 'Failed to search recipes. Please try again.'
      setError(`Error: ${errorMsg}`)
      console.error('Recipe search error:', err)
      console.error('Error details:', err?.response)
    } finally {
      setIsSearching(false)
    }
  }

  const handleHistorySelect = (item: HistoryItem) => {
    setImagePreview(item.imageUrl)
    setIngredients(
      item.ingredients.map(name => ({
        name,
        score: 0.8,
        selected: true,
      }))
    )
    setRecipes([])
  }

  const handleClearHistory = () => {
    clearHistory()
    setHistory([])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary rounded-lg">
              <ChefHat className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Snap2Recipe</h1>
              <p className="text-sm text-gray-600">Discover recipes from your food photos</p>
            </div>
          </div>
          <button
            onClick={() => setHistoryDrawerOpen(true)}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <HistoryIcon className="w-5 h-5" />
            <span className="hidden sm:inline">History</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="space-y-8">
          {/* Upload Section */}
          <section>
            <UploadBox
              onFileSelect={handleFileSelect}
              selectedFile={selectedFile}
              onClear={handleClear}
            />

            {selectedFile && !ingredients.length && (
              <div className="mt-4 text-center">
                <button
                  onClick={handleDetect}
                  disabled={isDetecting}
                  className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isDetecting ? 'Detecting...' : 'Detect Ingredients'}
                </button>
              </div>
            )}
          </section>

          {/* Error Message */}
          {error && (
            <div className="max-w-2xl mx-auto p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Ingredients Section */}
          {ingredients.length > 0 && (
            <section>
              <IngredientChips ingredients={ingredients} onToggle={handleToggleIngredient} />

              <div className="mt-4 text-center">
                <button
                  onClick={handleFindRecipes}
                  disabled={isSearching}
                  className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center gap-2"
                >
                  <Search className="w-5 h-5" />
                  {isSearching ? 'Searching...' : 'Find Recipes'}
                </button>
              </div>
            </section>
          )}

          {/* Recipes Section */}
          {recipes.length > 0 && (
            <section>
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                Found {recipes.length} Recipe{recipes.length !== 1 ? 's' : ''}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {recipes.map(recipe => (
                  <RecipeCard key={recipe.id} recipe={recipe} />
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      {/* Loading Overlays */}
      {isDetecting && <LoadingOverlay message="Detecting ingredients..." />}
      {isSearching && <LoadingOverlay message="Finding recipes..." />}

      {/* History Drawer */}
      <HistoryDrawer
        isOpen={historyDrawerOpen}
        onClose={() => setHistoryDrawerOpen(false)}
        history={history}
        onSelectItem={handleHistorySelect}
        onClearHistory={handleClearHistory}
      />
    </div>
  )
}
