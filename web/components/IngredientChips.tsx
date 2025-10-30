'use client'

import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Ingredient {
  name: string
  score: number
  selected?: boolean
}

interface IngredientChipsProps {
  ingredients: Ingredient[]
  onToggle: (index: number) => void
}

export default function IngredientChips({ ingredients, onToggle }: IngredientChipsProps) {
  if (ingredients.length === 0) return null

  return (
    <div className="w-full max-w-2xl mx-auto">
      <h3 className="text-lg font-semibold mb-3">Detected Ingredients</h3>
      <div className="flex flex-wrap gap-2">
        {ingredients.map((ingredient, index) => (
          <button
            key={index}
            onClick={() => onToggle(index)}
            className={cn(
              'px-4 py-2 rounded-full text-sm font-medium transition-all',
              'border-2 flex items-center gap-2',
              ingredient.selected
                ? 'bg-primary text-white border-primary'
                : 'bg-white text-gray-700 border-gray-300 hover:border-primary'
            )}
          >
            {ingredient.selected && <Check className="w-4 h-4" />}
            <span>{ingredient.name}</span>
            <span className="text-xs opacity-75">
              {Math.round(ingredient.score * 100)}%
            </span>
          </button>
        ))}
      </div>
      <p className="text-sm text-gray-500 mt-3">
        Click ingredients to include/exclude them from recipe search
      </p>
    </div>
  )
}
