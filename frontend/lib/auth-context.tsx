'use client'

import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import type { InspectorProfile } from '@/lib/types'

const DEFAULT_PROFILE: InspectorProfile = {
  name: 'Aarav Mehta',
  designation: 'Legal Metrology Inspector',
  employeeId: 'LMI-2291',
  email: 'aarav.mehta@metrology.gov.in',
  phone: '+91 98XXXXXX21',
  organization: 'Department of Consumer Affairs',
  department: 'Legal Metrology Division',
  stateRegion: 'National Capital Region',
}

interface AuthState {
  isAuthenticated: boolean
  profile: InspectorProfile
  login: (email: string) => void
  signup: (profile: Partial<InspectorProfile>) => void
  logout: () => void
}

const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [profile, setProfile] = useState<InspectorProfile>(DEFAULT_PROFILE)

  const login = useCallback((email: string) => {
    setProfile((prev) => ({ ...prev, email: email || prev.email }))
    setIsAuthenticated(true)
  }, [])

  const signup = useCallback((partial: Partial<InspectorProfile>) => {
    setProfile((prev) => ({ ...prev, ...partial }))
    setIsAuthenticated(true)
  }, [])

  const logout = useCallback(() => {
    setIsAuthenticated(false)
  }, [])

  const value = useMemo(
    () => ({ isAuthenticated, profile, login, signup, logout }),
    [isAuthenticated, profile, login, signup, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
