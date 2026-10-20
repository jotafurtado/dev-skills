import { defineConfig } from '@playwright/test';
import { resolve } from 'node:path';
export default defineConfig({
  testDir: './tests', workers: 1, timeout: 120_000,
  expect: { timeout: 20_000 },
  reporter: [['list'], ['json', { outputFile: process.env.LAB_RESULTS ?? resolve(import.meta.dirname, '../../.agent-native-fixture/evidence/browser-results.json') }]],
  use: { baseURL: process.env.LAB_URL ?? 'http://localhost:4311', headless: true, trace: 'off', screenshot: 'only-on-failure' },
  outputDir: resolve(import.meta.dirname, `../../.agent-native-fixture/playwright-output-${process.env.LAB_VARIANT ?? 'candidate'}`),
});
