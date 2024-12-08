/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [

    './templates/**/*.html',   
    './accounts/templates/**/*.html',  
    './groups/templates/**/*.html',     
    './*/templates/**/*.html',        
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
