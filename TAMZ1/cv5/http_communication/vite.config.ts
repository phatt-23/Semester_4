/// <reference types="vitest" />

import legacy from '@vitejs/plugin-legacy'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { chunkSplitPlugin } from 'vite-plugin-chunk-split';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    legacy(),
    chunkSplitPlugin(),
  ],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
  },
  build: {
    chunkSizeWarningLimit: 1600
  }
})
