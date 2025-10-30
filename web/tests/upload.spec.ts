import { test, expect } from '@playwright/test'
import path from 'path'

test.describe('Snap2Recipe Upload Flow', () => {
  test('should display upload box on homepage', async ({ page }) => {
    await page.goto('/')
    
    // Check for main heading
    await expect(page.getByRole('heading', { name: /Snap2Recipe/i })).toBeVisible()
    
    // Check for upload area
    await expect(page.getByText(/Drop your food photo here/i)).toBeVisible()
  })

  test('should allow file upload and show detect button', async ({ page }) => {
    await page.goto('/')
    
    // Create a test image file
    const testImagePath = path.join(__dirname, 'assets', 'test-food.png')
    
    // Upload file (you would need to create a test image in tests/assets/)
    // For now, this is a placeholder test structure
    
    // await page.setInputFiles('input[type="file"]', testImagePath)
    
    // Check that detect button appears
    // await expect(page.getByRole('button', { name: /Detect Ingredients/i })).toBeVisible()
  })

  test('should show history button', async ({ page }) => {
    await page.goto('/')
    
    await expect(page.getByRole('button', { name: /History/i })).toBeVisible()
  })
})
