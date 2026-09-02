'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { SidebarNav } from '@/components/app-shell/sidebar-nav'
import { Topbar } from '@/components/app-shell/topbar'
import { useAuth } from '@/lib/auth-context'

export function AppShell({ title, children }: { title?: string; children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="flex min-h-dvh bg-surface">
      <aside className="hidden w-64 shrink-0 border-r border-sidebar-border bg-sidebar lg:block">
        <SidebarNav />
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar title={title} />
        <main className="flex-1 p-4 md:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  )
}
