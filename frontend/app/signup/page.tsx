'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ScanSearch } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/lib/auth-context'

export default function SignupPage() {
  const { signup } = useAuth()
  const router = useRouter()
  const [form, setForm] = useState({
    name: '',
    employeeId: '',
    email: '',
    organization: 'Department of Consumer Affairs',
    password: '',
  })
  const [error, setError] = useState('')

  function update(field: keyof typeof form, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!form.name || !form.employeeId || !form.email || !form.password) {
      setError('Please complete all required fields.')
      return
    }
    setError('')
    signup({
      name: form.name,
      employeeId: form.employeeId,
      email: form.email,
      organization: form.organization,
    })
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
          <h2 className="text-lg font-semibold text-text-primary">Register as Inspector</h2>
          <p className="mt-1 text-sm text-text-secondary">Create your account to start logging inspections.</p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" value={form.name} onChange={(e) => update('name', e.target.value)} placeholder="e.g. Priya Nair" />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="employeeId">Employee ID</Label>
              <Input
                id="employeeId"
                value={form.employeeId}
                onChange={(e) => update('employeeId', e.target.value)}
                placeholder="LMI-XXXX"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="email">Official Email</Label>
              <Input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => update('email', e.target.value)}
                placeholder="you@metrology.gov.in"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={form.password}
                onChange={(e) => update('password', e.target.value)}
                placeholder="••••••••"
              />
            </div>

            {error ? <p className="text-sm text-destructive">{error}</p> : null}

            <Button type="submit" className="w-full">
              Create Account
            </Button>
          </form>

          <p className="mt-5 text-center text-sm text-text-secondary">
            Already registered?{' '}
            <Link href="/login" className="font-medium text-primary hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
