import { test, expect } from '@playwright/test';

test('Happy Path: Vote and see results', async ({ page }) => {
  // 1. Go to Vote App
  await page.goto('http://localhost:3000');
  await expect(page.getByRole('heading', { name: 'Vote for your favorite!' })).toBeVisible();

  // 2. Cast a vote for Cats
  await page.getByRole('button', { name: 'Option A (Cats)' }).click();
  await expect(page.getByText('Thanks for voting for Cats!')).toBeVisible();

  // 3. Go to Result App
  await page.goto('http://localhost:3001');
  await expect(page.getByRole('heading', { name: 'Voting Results' })).toBeVisible();

  // 4. Verify that Cats has at least 1 vote
  // (We use a loop or wait for the UI to update as the worker might take a second)
  await expect(page.getByText(/Cats \(Option A\): [1-9]\d* votes/)).toBeVisible({ timeout: 10000 });
});
