import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        warning: {
          bg: 'hsl(var(--warning-bg))',
          border: 'hsl(var(--warning-border))',
          text: 'hsl(var(--warning-text))',
        },
        bin: {
          recycling: {
            bg: 'hsl(var(--bin-recycling-bg))',
            border: 'hsl(var(--bin-recycling-border))',
            header: 'hsl(var(--bin-recycling-header))',
            hover: 'hsl(var(--bin-recycling-hover))',
            text: 'hsl(var(--bin-recycling-text))',
          },
          general: {
            bg: 'hsl(var(--bin-general-bg))',
            border: 'hsl(var(--bin-general-border))',
            header: 'hsl(var(--bin-general-header))',
            hover: 'hsl(var(--bin-general-hover))',
            text: 'hsl(var(--bin-general-text))',
          },
          green: {
            bg: 'hsl(var(--bin-green-bg))',
            border: 'hsl(var(--bin-green-border))',
            header: 'hsl(var(--bin-green-header))',
            hover: 'hsl(var(--bin-green-hover))',
            text: 'hsl(var(--bin-green-text))',
          },
          soft: {
            bg: 'hsl(var(--bin-soft-bg))',
            border: 'hsl(var(--bin-soft-border))',
            header: 'hsl(var(--bin-soft-header))',
            hover: 'hsl(var(--bin-soft-hover))',
            text: 'hsl(var(--bin-soft-text))',
          },
          special: {
            bg: 'hsl(var(--bin-special-bg))',
            border: 'hsl(var(--bin-special-border))',
            header: 'hsl(var(--bin-special-header))',
            hover: 'hsl(var(--bin-special-hover))',
            text: 'hsl(var(--bin-special-text))',
          },
          none: {
            bg: 'hsl(var(--bin-none-bg))',
            border: 'hsl(var(--bin-none-border))',
            header: 'hsl(var(--bin-none-header))',
            hover: 'hsl(var(--bin-none-hover))',
            text: 'hsl(var(--bin-none-text))',
          },
        },
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
}

export default config
