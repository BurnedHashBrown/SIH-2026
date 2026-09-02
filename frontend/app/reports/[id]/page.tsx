'use client'

import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Download, Printer, ShieldCheck } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { StatusBadge } from '@/components/status-badge'
import { DeclarationList } from '@/components/declaration-list'
import { useDataStore } from '@/lib/data-store'

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 py-1.5">
      <span className="text-xs text-text-secondary">{label}</span>
      <span className="text-right text-sm font-medium text-foreground">{value}</span>
    </div>
  )
}

export default function ReportDetailPage() {
  const params = useParams<{ id: string }>()
  const router = useRouter()
  const { reports, inspections, products } = useDataStore()

  const report = reports.find((r) => r.id === params.id)
  const inspection = report ? inspections.find((i) => i.id === report.inspectionId) : undefined
  const product = inspection ? products.find((p) => p.id === inspection.productId) : undefined

  if (!report || !inspection || !product) {
    return (
      <AppShell title="Report Not Found">
        <div className="flex flex-col items-center gap-4 py-24 text-center">
          <p className="text-sm text-text-secondary">We couldn&apos;t find a report with ID {params.id}.</p>
          <Button variant="outline" onClick={() => router.push('/reports')}>
            <ArrowLeft className="size-4" /> Back to Reports
          </Button>
        </div>
      </AppShell>
    )
  }

  const confirmedFindings = inspection.findings.filter((f) => f.status === 'confirmed')
  const rejectedFindings = inspection.findings.filter((f) => f.status === 'rejected')
  const pendingFindings = inspection.findings.filter((f) => f.status === 'pending')

  return (
    <AppShell title="Report Detail">
      <PageHeader
        title={`Compliance Report ${report.id}`}
        description={`Generated ${report.generatedDate} by ${report.generatedBy}`}
        actions={
          <>
            <Button variant="outline" asChild>
              <Link href="/reports">
                <ArrowLeft className="size-4" /> All Reports
              </Link>
            </Button>
            <Button variant="outline">
              <Printer className="size-4" /> Print
            </Button>
            <Button>
              <Download className="size-4" /> Export PDF
            </Button>
          </>
        }
      />

      <Card className="mb-6 border-l-4 border-l-primary">
        <CardContent className="flex flex-wrap items-center justify-between gap-4 py-5">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-full bg-primary/10">
              <ShieldCheck className="size-5 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">
                {product.brand} — {product.name}
              </p>
              <p className="text-xs text-text-secondary">
                Inspection{' '}
                <Link href={`/inspections/${inspection.id}`} className="text-primary hover:underline">
                  {inspection.id}
                </Link>{' '}
                · {inspection.location} · {inspection.date}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-2xl font-semibold text-foreground">{inspection.aiScore ?? '—'}%</p>
              <p className="text-xs text-text-secondary">AI Compliance Score</p>
            </div>
            <StatusBadge status={inspection.status} />
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Product & Inspection Details</CardTitle>
          </CardHeader>
          <CardContent className="divide-y divide-border">
            <InfoRow label="Manufacturer" value={product.manufacturer} />
            <InfoRow label="Net Quantity" value={product.netQuantity} />
            <InfoRow label="MRP" value={product.mrp} />
            <InfoRow label="Batch Number" value={product.batchNumber} />
            <InfoRow label="Inspection Type" value={inspection.type} />
            <InfoRow label="Inspector" value={inspection.inspector} />
            <InfoRow label="Report Status" value={report.status === 'final' ? 'Final' : 'Draft'} />
          </CardContent>
        </Card>

        <div className="flex flex-col gap-6 lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Findings Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="rounded-lg bg-status-danger-bg py-4">
                  <p className="text-2xl font-semibold text-status-danger">{confirmedFindings.length}</p>
                  <p className="text-xs text-status-danger">Confirmed Violations</p>
                </div>
                <div className="rounded-lg bg-status-warning-bg py-4">
                  <p className="text-2xl font-semibold text-status-warning">{pendingFindings.length}</p>
                  <p className="text-xs text-status-warning">Pending Review</p>
                </div>
                <div className="rounded-lg bg-status-success-bg py-4">
                  <p className="text-2xl font-semibold text-status-success">{rejectedFindings.length}</p>
                  <p className="text-xs text-status-success">Dismissed</p>
                </div>
              </div>

              {inspection.findings.length > 0 ? (
                <ul className="mt-5 flex flex-col gap-3">
                  {inspection.findings.map((finding) => (
                    <li key={finding.id} className="flex items-start justify-between gap-3 rounded-lg border border-border p-3">
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-foreground">{finding.title}</p>
                        <p className="mt-0.5 text-xs text-text-secondary">{finding.reason}</p>
                        {finding.inspectorRemarks && (
                          <p className="mt-1 text-xs italic text-text-secondary">
                            Inspector note: {finding.inspectorRemarks}
                          </p>
                        )}
                      </div>
                      <Badge
                        variant="outline"
                        className={
                          finding.status === 'confirmed'
                            ? 'shrink-0 border-status-danger/30 text-status-danger'
                            : finding.status === 'rejected'
                              ? 'shrink-0 border-status-success/30 text-status-success'
                              : 'shrink-0 border-status-warning/30 text-status-warning'
                        }
                      >
                        {finding.status.replace('_', ' ')}
                      </Badge>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-5 text-center text-sm text-text-secondary">No findings flagged for this inspection.</p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Detected Declarations</CardTitle>
            </CardHeader>
            <CardContent>
              <DeclarationList declarations={inspection.declarations} />
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  )
}
