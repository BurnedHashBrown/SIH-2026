'use client'

import { AuthProvider } from '@/lib/auth-context'
import { DataStoreProvider } from '@/lib/data-store'
import { TooltipProvider } from '@/components/ui/tooltip'
import { Toaster } from 'sonner'

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <DataStoreProvider>
        <TooltipProvider delayDuration={200}>
          {children}
          <Toaster position="top-right" richColors />
        </TooltipProvider>
      </DataStoreProvider>
    </AuthProvider>
  )
}
