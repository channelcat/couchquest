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
          '50': '#EBF6FC',
          '100': '#C9E5F6',
          '200': '#A7D5F1',
          '300': '#82C3EB',
          '400': '#60B2E5',
          '500': '#42A3E0',
          '600': '#3E8FCB',
          '700': '#3A7BB6',
          '800': '#35639D',
          '900': '#304E86',
          '950': '#2b366d',
          'heading': '#2b366d',
          'text': '#1c1c1c'
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