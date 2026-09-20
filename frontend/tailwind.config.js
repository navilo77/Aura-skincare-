/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: 'var(--background)',
          dark: '#0F0F0F',
        },
        foreground: {
          DEFAULT: 'var(--foreground)',
          dark: '#F5F5F5',
        },
        primary: {
          DEFAULT: 'var(--foreground)',
          light: 'var(--secondary-text)',
          dark: '#F5F5F5',
        },
        accent: {
          DEFAULT: '#C8A96A',
          light: '#D4BA8A',
          dark: '#B89A5A',
        },
        surface: {
          DEFAULT: 'var(--surface)',
          dark: '#1A1A1A',
        },
        border: {
          DEFAULT: 'var(--border)',
          dark: '#2A2A2A',
        },
        success: '#6AAE8A',
        error: '#D9534F',
        'secondary-text': {
          DEFAULT: 'var(--secondary-text)',
          dark: '#A0A0A0',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)'],
        serif: ['var(--font-playfair)'],
      },
      borderRadius: {
        'card': '20px',
        'button': '14px',
        'input': '14px',
        'product': '18px',
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(0, 0, 0, 0.04)',
        'soft-lg': '0 8px 30px -4px rgba(0, 0, 0, 0.06)',
        'premium': '0 20px 40px -8px rgba(0, 0, 0, 0.08)',
      },
      animation: {
        'fade-in': 'fadeIn 0.25s ease-out',
        'fade-in-up': 'fadeInUp 0.25s ease-out',
        'scale-in': 'scaleIn 0.25s ease-out',
        'slide-in-right': 'slideInRight 0.25s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(10px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },
    },
  },
  plugins: [],
}
