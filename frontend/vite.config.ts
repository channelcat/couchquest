import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import postcss from './postcss.config.cjs';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 3000,
  },
  esbuild: {
    target: "es2018"
  },
  resolve: {
    alias: {
      '@': '/js',
    }
  },
  build: {
    emptyOutDir: true,
  },
  base: "https://drinkarr.hill.tools",
  css: { postcss },
  plugins: [svelte(),],
})
