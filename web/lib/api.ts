/**
 * API client for Snap2Recipe backend
 */
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

console.log('API_URL configured as:', API_URL)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120 second timeout (2 minutes) for slow CPU inference
})

// Log all requests
api.interceptors.request.use(request => {
  console.log('Starting Request:', request.method?.toUpperCase(), request.url)
  return request
})

// Log all responses
api.interceptors.response.use(
  response => {
    console.log('Response:', response.status, response.config.url)
    return response
  },
  error => {
    console.error('API Error:', error.message)
    console.error('Error details:', error.response?.data || error)
    return Promise.reject(error)
  }
)

export interface IngredientDetection {
  name: string
  score: number
}

export interface DetectResponse {
  ingredients: IngredientDetection[]
  processing_time_ms: number
}

export interface Recipe {
  id: number
  title: string
  ingredients: string[]
  instructions: string
  cuisine: string
  tags: string[]
  time_minutes?: number
  score?: number
}

export interface RecipeSearchResponse {
  recipes: Recipe[]
  query_ingredients: string[]
  total_results: number
}

/**
 * Detect ingredients from an image file
 */
export async function detectIngredients(file: File): Promise<DetectResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<DetectResponse>('/detect', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/**
 * Search for recipes by ingredients
 */
export async function searchRecipes(
  ingredients: string[],
  limit: number = 20
): Promise<RecipeSearchResponse> {
  console.log('searchRecipes called with:', ingredients, 'limit:', limit)
  const ingredientsString = ingredients.join(',')
  console.log('Ingredients string:', ingredientsString)
  
  console.log('About to make API call to /recipes')
  const response = await api.get<RecipeSearchResponse>('/recipes', {
    params: {
      s: ingredientsString,
      limit,
    },
  })
  console.log('API call completed, response:', response)

  return response.data
}

/**
 * Suggest recipes based on ingredients (POST endpoint)
 */
export async function suggestRecipes(
  ingredients: string[],
  maxResults: number = 20
): Promise<RecipeSearchResponse> {
  const response = await api.post<RecipeSearchResponse>('/suggest', {
    ingredients,
    max_results: maxResults,
  })

  return response.data
}

/**
 * Get a specific recipe by ID
 */
export async function getRecipe(id: number): Promise<Recipe> {
  const response = await api.get<Recipe>(`/recipes/${id}`)
  return response.data
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await api.get('/health')
  return response.data
}
