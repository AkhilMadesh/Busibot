'use client'

import { useSession, signOut } from 'next-auth/react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export function DashboardNav() {
  const { data: session } = useSession()

  return (
    <header className="border-b border-border/40">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg">
          <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
            Busibot
          </span>
        </Link>

        <nav className="flex items-center gap-6">
          <Link href="/dashboard/ideas" className="text-sm hover:text-foreground/80">
            Ideas
          </Link>
          <Link href="/dashboard/plans" className="text-sm hover:text-foreground/80">
            Plans
          </Link>
          <Link href="/dashboard/chat" className="text-sm hover:text-foreground/80">
            Chat
          </Link>
          <Link href="/dashboard/investors" className="text-sm hover:text-foreground/80">
            Investors
          </Link>
        </nav>

        <div className="flex items-center gap-4">
          <span className="text-sm">{session?.user?.email}</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => signOut({ redirect: true, callbackUrl: '/' })}
          >
            Logout
          </Button>
        </div>
      </div>
    </header>
  )
}
