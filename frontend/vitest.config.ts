import { defineConfig } from 'vitest/config'
import Vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [Vue()],
    test: {
        globals: true
    },
    server: {
        host: '0.0.0.0', // Allows external access
        cors: true, // Enables CORS
        allowedHosts: [
          'all'
        ]
      }
})