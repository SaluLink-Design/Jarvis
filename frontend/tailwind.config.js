/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'jarvis-blue': '#0ea5e9',
        'jarvis-dark': '#0f172a',
      }
    },
  },
  plugins: [],
}

