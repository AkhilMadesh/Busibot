import type { Metadata } from 'next'
import { SessionProvider } from 'next-auth/react'
import '@/styles/globals.css'

export const metadata: Metadata = {
  title: 'Busibot - AI-Powered Business Assistant',
  description: 'Generate, validate, and grow your startup with AI-driven guidance',
  keywords: [
    'startup',
    'AI',
    'business',
    'entrepreneurship',
    'funding',
    'investors',
  ],
  authors: [{ name: 'Busibot Team' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXT_PUBLIC_APP_DOMAIN,
    siteName: 'Busibot',
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@busibot',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}
