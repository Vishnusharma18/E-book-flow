/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        plough: {
          bg: "#FAF8F5",
          accent: "#C29B38",
          dark: "#1C1917",
          card: "#FFFFFF"
        }
      }
    },
  },
  plugins: [],
}
