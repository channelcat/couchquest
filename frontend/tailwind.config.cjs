export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1440px'
      }
    },
    extend: {
      colors: {
        primary: {
          '50': 'oklch(0.98 0.016 73.684)',
          '100': 'oklch(0.954 0.038 75.164)',
          '200': 'oklch(0.901 0.076 70.697)',
          '300': 'oklch(0.837 0.128 66.29)',
          '400': 'oklch(0.75 0.183 55.934)',
          '500': 'oklch(0.705 0.213 47.604)',
          '600': 'oklch(0.646 0.222 41.116)',
          '700': 'oklch(0.553 0.195 38.402)',
          '800': 'oklch(0.47 0.157 37.304)',
          '900': 'oklch(0.408 0.123 38.172)',
          '950': 'oklch(0.266 0.079 36.259)',
          'heading': '#2b366d',
          'text': '#ffffff'
        },
        accent: {
          'bold': '#eD7015'
        }
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Oxygen',
          'Ubuntu',
          'Cantarell',
          'Fira Sans',
          'Droid Sans',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
          'Apple Color Emoji',
          'Segoe UI Emoji',
          'Segoe UI Symbol'
        ],
        mono: [
          'ui-monospace',
          'SFMono-Regular',
          'SF Mono',
          'Menlo',
          'Consolas',
          'Liberation Mono',
          'monospace'
        ]
      }
    }
  }
}