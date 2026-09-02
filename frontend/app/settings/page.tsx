'use client'

import { useState } from 'react'
import { LogOut, Save, ShieldCheck } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { useAuth } from '@/lib/auth-context'
import { toast } from 'sonner'

export default function SettingsPage() {
  const { profile, logout } = useAuth()
  const router = useRouter()
  const [form, setForm] = useState(profile)
  const [notifyFindings, setNotifyFindings] = useState(true)
  const [notifyWeeklyDigest, setNotifyWeeklyDigest] = useState(true)
  const [notifyLowConfidence, setNotifyLowConfidence] = useState(false)

  function handleSave() {
    toast.success('Profile settings saved')
  }

  function handleLogout() {
    logout()
    router.push('/login')
  }

  return (
    <AppShell title="Settings">
      <PageHeader title="Settings" description="Manage your inspector profile and notification preferences." />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Inspector Profile</CardTitle>
            <CardDescription>This information appears on generated compliance reports.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 sm:grid-cols-2">
            <div className="flex flex-col gap-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="designation">Designation</Label>
              <Input
                id="designation"
                value={form.designation}
                onChange={(e) => setForm({ ...form, designation: e.target.value })}
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="employee-id">Employee ID</Label>
              <Input
                id="employee-id"
                value={form.employeeId}
                onChange={(e) => setForm({ ...form, employeeId: e.target.value })}
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="phone">Phone</Label>
              <Input id="phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="state-region">State / Region</Label>
              <Input
                id="state-region"
                value={form.stateRegion}
                onChange={(e) => setForm({ ...form, stateRegion: e.target.value })}
              />
            </div>
            <div className="flex flex-col gap-2 sm:col-span-2">
              <Label htmlFor="organization">Organization</Label>
              <Input
                id="organization"
                value={form.organization}
                onChange={(e) => setForm({ ...form, organization: e.target.value })}
              />
            </div>
            <div className="flex flex-col gap-2 sm:col-span-2">
              <Label htmlFor="department">Department</Label>
              <Input
                id="department"
                value={form.department}
                onChange={(e) => setForm({ ...form, department: e.target.value })}
              />
            </div>
            <div className="sm:col-span-2">
              <Button onClick={handleSave}>
                <Save className="size-4" /> Save Changes
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Notification Preferences</CardTitle>
              <CardDescription>Choose what triggers an alert.</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-foreground">Confirmed findings</p>
                  <p className="text-xs text-text-secondary">Notify when a finding is confirmed as a violation.</p>
                </div>
                <Switch checked={notifyFindings} onCheckedChange={setNotifyFindings} />
              </div>
              <Separator />
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-foreground">Weekly digest</p>
                  <p className="text-xs text-text-secondary">Summary of inspections completed each week.</p>
                </div>
                <Switch checked={notifyWeeklyDigest} onCheckedChange={setNotifyWeeklyDigest} />
              </div>
              <Separator />
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-foreground">Low-confidence evidence</p>
                  <p className="text-xs text-text-secondary">Notify when uploaded photos are low quality.</p>
                </div>
                <Switch checked={notifyLowConfidence} onCheckedChange={setNotifyLowConfidence} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShieldCheck className="size-4 text-primary" /> Session
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-sm text-text-secondary">
                Signed in as {profile.email}. Ending your session will require signing in again.
              </p>
              <Button variant="outline" onClick={handleLogout} className="w-full">
                <LogOut className="size-4" /> Log Out
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  )
}
