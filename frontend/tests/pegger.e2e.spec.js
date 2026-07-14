import { expect, test } from '@playwright/test'

test.describe('Pegger payment flow', () => {
  test('loads the home flow and previews a sample invoice', async ({ page }) => {
    await page.goto('/')

    await expect(page.getByRole('heading', { name: 'Scan. Confirm. Done.' })).toBeVisible()
    await expect(page.getByText('Waiting for scan')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Scan your invoice' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Invoice preview' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Continue with this data' })).toBeDisabled()

    await page.getByRole('button', { name: 'Try a sample' }).click()
    await expect(page.getByRole('button', { name: 'Continue with this data' })).toBeEnabled()

    await page.getByRole('button', { name: 'Continue with this data' }).click()

    await expect(page.getByRole('heading', { name: 'Invoice details' })).toBeVisible()
    await expect(page.getByText('Northline Cafe')).toBeVisible()
    await expect(page.getByText('€18.40')).toBeVisible()
    await expect(page.getByText('INV-2026-0007')).toBeVisible()
    await expect(page.getByText('Sign in to enable payment')).toBeVisible()
    await expect(page.getByText('Invoice loaded').first()).toBeVisible()

    await page.getByRole('button', { name: 'Start over' }).click()
    await expect(page.getByRole('heading', { name: 'Invoice preview' })).toBeVisible()
    await expect(page.getByRole('button', { name: 'Continue with this data' })).toBeDisabled()
  })

  test('switches between sign in and registration entry points', async ({ page }) => {
    await page.goto('/')

    await expect(page.getByLabel('Email or username')).toBeVisible()
    await expect(page.getByLabel('Password')).toBeVisible()

    await page.getByRole('button', { name: 'New here' }).click()

    await expect(page.getByLabel('Choose a username')).toBeVisible()
    await expect(page.getByLabel('Your name')).toBeVisible()
    await expect(page.getByLabel('Email address')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Create account' })).toBeVisible()

    await page.getByRole('button', { name: 'I have an account' }).click()

    await expect(page.getByLabel('Email or username')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Sign in' })).toBeVisible()
  })

  test('redirects unknown paths back to the payment flow', async ({ page }) => {
    await page.goto('/missing-page')

    await expect(page).toHaveURL(/\/$/)
    await expect(page.getByRole('heading', { name: 'Scan. Confirm. Done.' })).toBeVisible()
  })
})
