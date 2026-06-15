'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'

export default function Home() {
  const { data: session } = useSession()

  if (session) {
    redirect('/dashboard')
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 max-w-screen-2xl items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              Busibot
            </span>
          </div>
          <nav className="flex items-center gap-4">
            <Link href="#features" className="text-sm hover:text-foreground/80">
              Features
            </Link>
            <Link href="#pricing" className="text-sm hover:text-foreground/80">
              Pricing
            </Link>
            <Button asChild variant="outline" size="sm">
              <Link href="/auth/login">Login</Link>
            </Button>
            <Button asChild size="sm">
              <Link href="/auth/signup">Sign Up</Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-24 sm:py-32">
        <div className="container max-w-screen-lg">
          <div className="flex flex-col items-center text-center gap-8">
            <h1 className="text-4xl sm:text-6xl font-bold tracking-tighter leading-tight">
              Turn Your Business Idea Into Reality
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl">
              Busibot is an AI-powered platform that helps entrepreneurs generate validated ideas,
              create business plans, analyze markets, and connect with investors.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button asChild size="lg">
                <Link href="/auth/signup">Get Started Free</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="#features">Learn More</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="border-t border-border/40 py-24 sm:py-32">
        <div className="container max-w-screen-lg">
          <div className="flex flex-col items-center text-center gap-4 mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tighter">Powerful Features</h2>
            <p className="text-muted-foreground max-w-2xl">
              Everything you need to build and grow your startup
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => (
              <div key={feature.title} className="group relative overflow-hidden rounded-lg border border-border/40 p-6 hover:border-border/80 transition-colors">
                <div className="text-3xl mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border/40 py-24 sm:py-32 bg-muted/30">
        <div className="container max-w-screen-lg text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to build your startup?</h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of entrepreneurs using Busibot to validate ideas and attract investors.
          </p>
          <Button asChild size="lg">
            <Link href="/auth/signup">Start Free Today</Link>
          </Button>
        </div>
      </section>
    </div>
  )
}

const features = [
  {
    icon: '💡',
    title: 'AI Idea Generator',
    description: 'Generate innovative business ideas based on your interests and market trends',
  },
  {
    icon: '✅',
    title: 'Idea Validation',
    description: 'Validate your idea with market analysis, competitor research, and feasibility scores',
  },
  {
    icon: '📋',
    title: 'Business Plan Generator',
    description: 'Create comprehensive business plans with AI assistance in minutes',
  },
  {
    icon: '📊',
    title: 'Market Research',
    description: 'Get deep market insights, trends, and competitive analysis for your industry',
  },
  {
    icon: '💰',
    title: 'Financial Forecasts',
    description: 'Generate accurate financial projections and analyze unit economics',
  },
  {
    icon: '🤝',
    title: 'Investor Matching',
    description: 'Get matched with relevant investors based on your startup profile',
  },
]
