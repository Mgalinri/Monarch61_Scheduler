/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Instrument Sans"', 'Roboto'], // Use "Roboto" font
      },
      colors: {
        'orange': '#f36f27',
        'redish-purple': '#583346',
        'pink': '#ff7e7e',
      },
    },
  },
  plugins: [],
}

