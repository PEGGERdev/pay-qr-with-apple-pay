import { expect, test } from '@playwright/test'

test.describe('Pegger optical verification', () => {
  test('desktop landing page keeps the guided payment layout', async ({ page }) => {
    await page.goto('/')

    await expect(page.getByRole('heading', { name: 'Scan. Confirm. Done.' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Scan your invoice' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Payment timeline' })).toBeVisible()

    await expect(page).toHaveScreenshot('desktop-landing.png', {
      fullPage: true,
      animations: 'disabled',
    })
  })

  test('mobile sample invoice keeps the preview and checkout cards readable', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 })
    await page.goto('/')

    await page.getByRole('button', { name: 'Try a sample' }).click()
    await page.getByRole('button', { name: 'Continue with this data' }).click()

    await expect(page.getByRole('heading', { name: 'Invoice details' })).toBeVisible()
    await expect(page.getByText('Northline Cafe')).toBeVisible()
    await expect(page.getByText('Sign in to enable payment')).toBeVisible()

    await expect(page).toHaveScreenshot('mobile-sample-invoice.png', {
      fullPage: true,
      animations: 'disabled',
    })
  })
})
