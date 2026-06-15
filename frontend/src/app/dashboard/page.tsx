'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import { DashboardNav } from '@/components/dashboard/nav'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: session, status } = useSession()

  if (status === 'unauthenticated') {
    redirect('/auth/login')
  }

  if (status === 'loading') {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>
  }

  return (
    <div className="flex min-h-screen flex-col">
      <DashboardNav />
      <main className="flex-1">
        <div className="container py-8">
          <div className="grid gap-6">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Welcome back, {session?.user?.name}</h1>
              <p className="text-muted-foreground mt-2">
                Let's help you build and grow your startup
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="border border-border/40 rounded-lg p-6 hover:border-border/80 transition-colors cursor-pointer">
                <h3 className="font-semibold mb-2">💡 Generate Idea</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Get AI-powered business ideas based on your interests
                </p>
                <Button asChild variant="outline" size="sm">
                  <Link href="/dashboard/ideas">Start</Link>
                </Button>
              </div>

              <div className="border border-border/40 rounded-lg p-6 hover:border-border/80 transition-colors cursor-pointer">
                <h3 className="font-semibold mb-2">📋 Create Plan</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Generate comprehensive business plans with AI
                </p>
                <Button asChild variant="outline" size="sm">
                  <Link href="/dashboard/plans">Create</Link>
                </Button>
              </div>

              <div className="border border-border/40 rounded-lg p-6 hover:border-border/80 transition-colors cursor-pointer">
                <h3 className="font-semibold mb-2">🤝 Find Investors</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Get matched with relevant investors
                </p>
                <Button asChild variant="outline" size="sm">
                  <Link href="/dashboard/investors">Explore</Link>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
