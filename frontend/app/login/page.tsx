'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ScanSearch } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/lib/auth-context'

export default function LoginPage() {
  const { login } = useAuth()
  const router = useRouter()
  const [email, setEmail] = useState('aarav.mehta@metrology.gov.in')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!email || !password) {
      setError('Enter your email and password to continue.')
      return
    }
    setError('')
    login(email)
    router.push('/dashboard')
  }

  return (
    <div className="flex min-h-dvh items-center justify-center bg-surface px-4 py-12">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="flex size-12 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <ScanSearch className="size-6" />
          </div>
          <h1 className="mt-4 text-xl font-semibold text-text-primary">MetrologyAI</h1>
          <p className="mt-1 text-sm text-text-secondary">Legal Metrology Compliance Portal</p>
        </div>

        <div className="rounded-xl border border-border-subtle bg-surface-container-lowest p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-text-primary">Inspector Sign In</h2>
          <p className="mt-1 text-sm text-text-secondary">Sign in with your department credentials.</p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="email">Official Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@metrology.gov.in"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </div>

            {error ? <p className="text-sm text-destructive">{error}</p> : null}

            <Button type="submit" className="w-full">
              Sign In
            </Button>
          </form>

          <p className="mt-5 text-center text-sm text-text-secondary">
            {"Don't have an account? "}
            <Link href="/signup" className="font-medium text-primary hover:underline">
              Register as an inspector
            </Link>
          </p>
        </div>

        <p className="mt-6 text-center text-xs text-text-secondary">
          This is a demonstration portal. No real credentials are required — enter any email and password.
        </p>
      </div>
    </div>
  )
}
