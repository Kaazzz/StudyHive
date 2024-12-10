/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [

    './templates/**/*.html',   
    './accounts/templates/**/*.html',  
    './groups/templates/**/*.html',     
    './*/templates/**/*.html',
    "./node_modules/flowbite/**/*.js",     
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
