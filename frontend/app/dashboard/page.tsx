'use client'

import Link from 'next/link'
import { useMemo } from 'react'
import { FilePlus2, ClipboardCheck, AlertTriangle, ShieldAlert } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { KpiCard } from '@/components/kpi-card'
import { Button } from '@/components/ui/button'
import { InspectionsTable } from '@/components/inspections-table'
import { ComplianceTrendChart } from '@/components/compliance-trend-chart'
import { useDataStore } from '@/lib/data-store'
import { useAuth } from '@/lib/auth-context'

export default function DashboardPage() {
  const { inspections, products } = useDataStore()
  const { profile } = useAuth()

  const kpis = useMemo(() => {
    const total = inspections.length
    const compliant = inspections.filter((i) => i.status === 'compliant').length
    const review = inspections.filter((i) => i.status === 'requires_review').length
    const violations = inspections.filter((i) => i.status === 'potential_violation').length
    return { total, compliant, review, violations }
  }, [inspections])

  const trendData = useMemo(() => {
    const byMonth = new Map<string, { total: number; count: number }>()
    for (const product of products) {
      for (const point of product.scoreHistory) {
        const entry = byMonth.get(point.date) ?? { total: 0, count: 0 }
        entry.total += point.score
        entry.count += 1
        byMonth.set(point.date, entry)
      }
    }
    return Array.from(byMonth.entries()).map(([date, { total, count }]) => ({
      date,
      score: Math.round(total / count),
    }))
  }, [products])

  const recentInspections = inspections.slice(0, 6)

  function getProductName(productId: string) {
    return products.find((p) => p.id === productId)
  }

  return (
    <AppShell title="Dashboard">
      <PageHeader
        title={`Welcome back, ${profile.name.split(' ')[0]}`}
        description="Overview of compliance inspections and AI-assisted review activity."
        actions={
          <Button asChild>
            <Link href="/inspections/new">
              <FilePlus2 className="size-4" /> New Inspection
            </Link>
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Total Inspections" value={String(kpis.total)} helpText="All time" icon={<ClipboardCheck className="size-4" />} />
        <KpiCard
          label="Compliant"
          value={String(kpis.compliant)}
          helpText={`${Math.round((kpis.compliant / Math.max(kpis.total, 1)) * 100)}% of total`}
          tone="success"
          icon={<ClipboardCheck className="size-4" />}
        />
        <KpiCard
          label="Requires Review"
          value={String(kpis.review)}
          helpText="Awaiting inspector decision"
          tone="warning"
          icon={<AlertTriangle className="size-4" />}
        />
        <KpiCard
          label="Potential Violations"
          value={String(kpis.violations)}
          helpText="Needs escalation"
          tone="danger"
          icon={<ShieldAlert className="size-4" />}
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="rounded-xl border border-border-subtle bg-surface-container-lowest p-5 lg:col-span-2">
          <h3 className="text-sm font-semibold text-text-primary">Average Compliance Score Trend</h3>
          <p className="text-xs text-text-secondary">Across all monitored products, by month</p>
          <div className="mt-4">
            <ComplianceTrendChart data={trendData} />
          </div>
        </div>

        <div className="rounded-xl border border-border-subtle bg-surface-container-lowest p-5">
          <h3 className="text-sm font-semibold text-text-primary">Quick Actions</h3>
          <div className="mt-4 flex flex-col gap-2">
            <Button asChild variant="outline" className="justify-start">
              <Link href="/inspections/new">
                <FilePlus2 className="size-4" /> Start a new inspection
              </Link>
            </Button>
            <Button asChild variant="outline" className="justify-start">
              <Link href="/inspections?status=requires_review">
                <AlertTriangle className="size-4" /> Review flagged findings
              </Link>
            </Button>
            <Button asChild variant="outline" className="justify-start">
              <Link href="/rules">
                <ClipboardCheck className="size-4" /> Browse compliance rules
              </Link>
            </Button>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-text-primary">Recent Inspections</h3>
          <Link href="/inspections" className="text-sm font-medium text-primary hover:underline">
            View all
          </Link>
        </div>
        <InspectionsTable inspections={recentInspections} getProductName={getProductName} />
      </div>
    </AppShell>
  )
}
