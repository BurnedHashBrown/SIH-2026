'use client'

import Link from 'next/link'
import { useMemo, useState, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { FilePlus2, Search } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { InspectionsTable } from '@/components/inspections-table'
import { useDataStore } from '@/lib/data-store'
import type { InspectionStatus } from '@/lib/types'

const STATUS_OPTIONS: { value: InspectionStatus | 'all'; label: string }[] = [
  { value: 'all', label: 'All Statuses' },
  { value: 'compliant', label: 'Compliant' },
  { value: 'requires_review', label: 'Requires Review' },
  { value: 'potential_violation', label: 'Potential Violation' },
  { value: 'processing', label: 'Processing' },
]

function InspectionsContent() {
  const { inspections, products } = useDataStore()
  const searchParams = useSearchParams()
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState<InspectionStatus | 'all'>(
    (searchParams.get('status') as InspectionStatus | null) ?? 'all',
  )

  function getProductName(productId: string) {
    return products.find((p) => p.id === productId)
  }

  const filtered = useMemo(() => {
    return inspections.filter((inspection) => {
      const product = getProductName(inspection.productId)
      const matchesStatus = status === 'all' || inspection.status === status
      const haystack = `${inspection.id} ${product?.name ?? ''} ${product?.brand ?? ''} ${inspection.location}`.toLowerCase()
      const matchesQuery = haystack.includes(query.toLowerCase())
      return matchesStatus && matchesQuery
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [inspections, products, query, status])

  return (
    <>
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[220px] max-w-sm">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-text-secondary" />
          <Input
            placeholder="Search by ID, product, or location"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={status} onValueChange={(v) => setStatus(v as InspectionStatus | 'all')}>
          <SelectTrigger className="w-48">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {STATUS_OPTIONS.map((opt) => (
              <SelectItem key={opt.value} value={opt.value}>
                {opt.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <InspectionsTable inspections={filtered} getProductName={getProductName} />
    </>
  )
}

export default function InspectionsListPage() {
  return (
    <AppShell title="Inspections">
      <PageHeader
        title="Inspections"
        description="All logged compliance inspections across products and locations."
        actions={
          <Button asChild>
            <Link href="/inspections/new">
              <FilePlus2 className="size-4" /> New Inspection
            </Link>
          </Button>
        }
      />
      <Suspense fallback={<div className="py-8 text-center text-slate-500">Loading inspections...</div>}>
        <InspectionsContent />
      </Suspense>
    </AppShell>
  )
}

