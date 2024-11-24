/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './accounts/templates/**/*.html',  
    './*/templates/**/*.html',
    './posts/templates/*.html',        
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}