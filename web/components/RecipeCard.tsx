'use client'

import { useState } from 'react'
import { Clock, ChevronDown, ChevronUp } from 'lucide-react'
import { Recipe } from '@/lib/api'
import { cn } from '@/lib/utils'

interface RecipeCardProps {
  recipe: Recipe
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="bg-white rounded-lg border-2 border-gray-200 overflow-hidden hover:border-primary/50 transition-colors">
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-1">{recipe.title}</h3>
            <div className="flex items-center gap-3 text-sm text-gray-600">
              <span className="px-2 py-1 bg-primary/10 text-primary rounded-md font-medium">
                {recipe.cuisine}
              </span>
              {recipe.time_minutes && (
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {recipe.time_minutes} min
                </span>
              )}
            </div>
          </div>
          {recipe.score && (
            <div className="text-right">
              <div className="text-2xl font-bold text-primary">
                {Math.round(recipe.score * 10) / 10}
              </div>
              <div className="text-xs text-gray-500">match</div>
            </div>
          )}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          {recipe.tags.map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Top Ingredients */}
        <div className="mb-3">
          <p className="text-sm font-semibold text-gray-700 mb-1">Key Ingredients:</p>
          <p className="text-sm text-gray-600">
            {recipe.ingredients.slice(0, 3).join(', ')}
            {recipe.ingredients.length > 3 && ` +${recipe.ingredients.length - 3} more`}
          </p>
        </div>

        {/* Expand/Collapse Button */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full flex items-center justify-center gap-2 py-2 text-primary hover:bg-primary/5 rounded-md transition-colors"
        >
          <span className="font-medium text-sm">
            {isExpanded ? 'Hide' : 'View'} Instructions
          </span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-5 pb-5 pt-0 border-t border-gray-200">
          <div className="mt-4">
            <h4 className="font-semibold text-gray-900 mb-2">All Ingredients:</h4>
            <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h4 className="font-semibold text-gray-900 mb-2">Instructions:</h4>
            <p className="text-sm text-gray-600 leading-relaxed">{recipe.instructions}</p>
          </div>
        </div>
      )}
    </div>
  )
}
