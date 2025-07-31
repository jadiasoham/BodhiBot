module.exports = {
  darkMode: 'media',
  content: ['./src/**/*.{js,jsx,ts,tsx,html}'],
  theme: {
    extend: {
      colors: {
        primary: '#0A192F',
        secondary: '#FF5C33',
        accent: '#66FCF1',
        light: '#F8F9FA',
        dark: '#333333',
        white: '#FFFFFF',
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        comic: ['"comic sans ms"', 'cursive', 'sans-serif'],
      },
    },
  },
  plugins: [],
};