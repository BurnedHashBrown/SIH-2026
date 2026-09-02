'use client'

import { useMemo, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { ChevronLeft, FileText, Loader2 } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { StatusBadge } from '@/components/status-badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { EvidenceGallery } from '@/components/evidence-gallery'
import { DeclarationList } from '@/components/declaration-list'
import { FindingReviewCard } from '@/components/finding-review-card'
import { useDataStore } from '@/lib/data-store'
import { scoreToStatus } from '@/lib/analysis-service'
import type { Declaration, Finding, Report } from '@/lib/types'

export default function InspectionDetailPage() {
  const params = useParams<{ id: string }>()
  const router = useRouter()
  const { getInspection, getProduct, updateInspection, addReport, getReport } = useDataStore()
  const inspection = getInspection(params.id)
  const [activeDeclaration, setActiveDeclaration] = useState<Declaration | undefined>(undefined)
  const [activeImageId, setActiveImageId] = useState<string | undefined>(inspection?.images[0]?.id)
  const [generating, setGenerating] = useState(false)

  const product = inspection ? getProduct(inspection.productId) : undefined
  const report = inspection?.reportId ? getReport(inspection.reportId) : undefined

  const pendingCount = useMemo(
    () => inspection?.findings.filter((f) => f.status === 'pending').length ?? 0,
    [inspection],
  )

  if (!inspection) {
    return (
      <AppShell title="Inspection Not Found">
        <p className="text-sm text-text-secondary">This inspection could not be found.</p>
        <Button asChild variant="outline" className="mt-4">
          <Link href="/inspections">Back to Inspections</Link>
        </Button>
      </AppShell>
    )
  }

  function handleSelectDeclaration(decl: Declaration) {
    setActiveDeclaration(decl)
    if (decl.evidenceImageId) setActiveImageId(decl.evidenceImageId)
  }

  function updateFinding(findingId: string, patch: Partial<Finding>) {
    const nextFindings = inspection!.findings.map((f) => (f.id === findingId ? { ...f, ...patch } : f))
    updateInspection(inspection!.id, { findings: nextFindings })
  }

  function handleGenerateReport() {
    setGenerating(true)
    setTimeout(() => {
      const newReport: Report = {
        id: `RPT-${Math.floor(1000 + Math.random() * 9000)}`,
        inspectionId: inspection!.id,
        generatedDate: 'Today',
        generatedBy: 'Aarav Mehta',
        status: 'final',
      }
      addReport(newReport)
      updateInspection(inspection!.id, { reportId: newReport.id })
      setGenerating(false)
      router.push(`/reports/${newReport.id}`)
    }, 1200)
  }

  const allFindingsResolved = inspection.findings.every((f) => f.status !== 'pending')

  return (
    <AppShell title={`Inspection ${inspection.id}`}>
      <Link href="/inspections" className="mb-4 inline-flex items-center gap-1 text-sm text-text-secondary hover:text-text-primary">
        <ChevronLeft className="size-4" /> Back to Inspections
      </Link>

      <PageHeader
        title={inspection.id}
        description={`${product?.name ?? 'Unknown product'} \u2014 ${product?.brand ?? ''}`}
        actions={
          <div className="flex items-center gap-2">
            <StatusBadge status={inspection.status} />
            {report ? (
              <Button asChild variant="outline">
                <Link href={`/reports/${report.id}`}>
                  <FileText className="size-4" /> View Report
                </Link>
              </Button>
            ) : (
              <Button onClick={handleGenerateReport} disabled={!allFindingsResolved || generating}>
                {generating ? <Loader2 className="size-4 animate-spin" /> : <FileText className="size-4" />}
                Generate Report
              </Button>
            )}
          </div>
        }
      />

      {!allFindingsResolved && !report ? (
        <div className="mb-6 rounded-lg border border-status-warning/30 bg-status-warning-bg px-4 py-3 text-sm text-status-warning">
          {pendingCount} finding{pendingCount === 1 ? '' : 's'} still require your review before a report can be generated.
        </div>
      ) : null}

      <div className="mb-6 grid grid-cols-2 gap-4 rounded-xl border border-border-subtle bg-surface-container-lowest p-5 sm:grid-cols-4">
        <Meta label="Location" value={inspection.location} />
        <Meta label="Inspection Date" value={inspection.date} />
        <Meta label="Type" value={inspection.type} />
        <Meta label="Inspector" value={inspection.inspector} />
        <Meta label="Batch Number" value={product?.batchNumber ?? '—'} />
        <Meta label="Net Quantity" value={product?.netQuantity ?? '—'} />
        <Meta label="MRP" value={product?.mrp ?? '—'} />
        <Meta label="AI Score" value={inspection.aiScore != null ? `${inspection.aiScore}%` : '—'} />
      </div>

      <Tabs defaultValue="evidence">
        <TabsList>
          <TabsTrigger value="evidence">Evidence & Declarations</TabsTrigger>
          <TabsTrigger value="findings">
            Findings{pendingCount > 0 ? ` (${pendingCount})` : ''}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="evidence" className="mt-4">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <EvidenceGallery
              images={inspection.images}
              activeImageId={activeImageId}
              onSelect={setActiveImageId}
              highlightRegion={activeDeclaration?.region}
            />
            <div>
              <h3 className="mb-2 text-sm font-semibold text-text-primary">Extracted Declarations</h3>
              <DeclarationList
                declarations={inspection.declarations}
                activeId={activeDeclaration?.id}
                onSelect={handleSelectDeclaration}
              />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="findings" className="mt-4">
          {inspection.findings.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border-subtle p-8 text-center text-sm text-text-secondary">
              No findings were flagged for this inspection. All declarations were detected with high confidence.
            </div>
          ) : (
            <div className="space-y-3">
              {inspection.findings.map((finding) => (
                <FindingReviewCard
                  key={finding.id}
                  finding={finding}
                  readOnly={Boolean(report)}
                  onUpdate={(patch) => updateFinding(finding.id, patch)}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </AppShell>
  )
}

function Meta({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-text-secondary">{label}</p>
      <p className="mt-0.5 text-sm font-medium text-text-primary">{value}</p>
    </div>
  )
}
