/**
 * Local storage utilities for detection history
 */

export interface HistoryItem {
  id: string
  timestamp: number
  imageUrl: string
  ingredients: string[]
}

const HISTORY_KEY = 'snap2recipe_history'
const MAX_HISTORY_ITEMS = 5

/**
 * Get detection history from localStorage
 */
export function getHistory(): HistoryItem[] {
  if (typeof window === 'undefined') return []

  try {
    const stored = localStorage.getItem(HISTORY_KEY)
    return stored ? JSON.parse(stored) : []
  } catch (error) {
    console.error('Failed to load history:', error)
    return []
  }
}

/**
 * Add a new item to history
 */
export function addToHistory(imageUrl: string, ingredients: string[]): void {
  if (typeof window === 'undefined') return

  try {
    const history = getHistory()
    const newItem: HistoryItem = {
      id: Date.now().toString(),
      timestamp: Date.now(),
      imageUrl,
      ingredients,
    }

    // Add to beginning and limit to MAX_HISTORY_ITEMS
    const updatedHistory = [newItem, ...history].slice(0, MAX_HISTORY_ITEMS)

    localStorage.setItem(HISTORY_KEY, JSON.stringify(updatedHistory))
  } catch (error) {
    console.error('Failed to save history:', error)
  }
}

/**
 * Clear all history
 */
export function clearHistory(): void {
  if (typeof window === 'undefined') return

  try {
    localStorage.removeItem(HISTORY_KEY)
  } catch (error) {
    console.error('Failed to clear history:', error)
  }
}

/**
 * Remove a specific history item
 */
export function removeHistoryItem(id: string): void {
  if (typeof window === 'undefined') return

  try {
    const history = getHistory()
    const updatedHistory = history.filter(item => item.id !== id)
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updatedHistory))
  } catch (error) {
    console.error('Failed to remove history item:', error)
  }
}
