import type { Metadata } from 'next'
import localFont from 'next/font/local'
import './globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { ThemeProvider } from '@/components/ui/theme-provider'

const inter = localFont({
  src: '../../public/fonts/InterVariable.woff2',
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'https://australiarecycling.com.au'),
  title: {
    default: 'Australia Recycling — Find Recycling Info for Your Area',
    template: '%s | Australia Recycling',
  },
  description:
    'Find out what goes in which bin for your Australian council. Search by suburb, postcode, or council name to get accurate recycling information.',
  keywords: ['recycling', 'Australia', 'council', 'bin', 'waste', 'yellow lid', 'green waste'],
  openGraph: {
    type: 'website',
    siteName: 'Australia Recycling',
    locale: 'en_AU',
  },
  twitter: {
    card: 'summary_large_image',
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} flex min-h-screen flex-col antialiased`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  )
}
