'use client'

import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, ClipboardList, FilePlus2 } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { StatusBadge } from '@/components/status-badge'
import { ComplianceTrendChart } from '@/components/compliance-trend-chart'
import { InspectionsTable } from '@/components/inspections-table'
import { useDataStore } from '@/lib/data-store'

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 py-2">
      <span className="text-sm text-text-secondary">{label}</span>
      <span className="text-right text-sm font-medium text-foreground">{value}</span>
    </div>
  )
}

export default function ProductDetailPage() {
  const params = useParams<{ id: string }>()
  const router = useRouter()
  const { products, inspections } = useDataStore()
  const product = products.find((p) => p.id === params.id)
  const productInspections = inspections
    .filter((i) => i.productId === params.id)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())

  if (!product) {
    return (
      <AppShell title="Product Not Found">
        <div className="flex flex-col items-center gap-4 py-24 text-center">
          <p className="text-sm text-text-secondary">We couldn&apos;t find a product with ID {params.id}.</p>
          <Button variant="outline" onClick={() => router.push('/products')}>
            <ArrowLeft className="size-4" /> Back to Products
          </Button>
        </div>
      </AppShell>
    )
  }

  return (
    <AppShell title="Product Detail">
      <PageHeader
        title={product.name}
        description={`${product.brand} · ${product.id}`}
        actions={
          <>
            <Button variant="outline" asChild>
              <Link href="/products">
                <ArrowLeft className="size-4" /> All Products
              </Link>
            </Button>
            <Button asChild>
              <Link href="/inspections/new">
                <FilePlus2 className="size-4" /> New Inspection
              </Link>
            </Button>
          </>
        }
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Declared Information</CardTitle>
          </CardHeader>
          <CardContent className="divide-y divide-border">
            <DetailRow label="Brand" value={product.brand} />
            <DetailRow label="Category" value={product.category} />
            <DetailRow label="Manufacturer" value={product.manufacturer} />
            {product.packer && <DetailRow label="Packer" value={product.packer} />}
            {product.importer && <DetailRow label="Importer" value={product.importer} />}
            {product.countryOfOrigin && <DetailRow label="Country of Origin" value={product.countryOfOrigin} />}
            <DetailRow label="Net Quantity" value={product.netQuantity} />
            <DetailRow label="MRP" value={product.mrp} />
            <DetailRow label="Batch Number" value={product.batchNumber} />
            <DetailRow label="Mfg. Date" value={product.mfgDate} />
            <DetailRow label="Consumer Care" value={product.consumerCare} />
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between gap-4">
            <CardTitle>Compliance Score Trend</CardTitle>
            <StatusBadge status={product.status} size="sm" />
          </CardHeader>
          <CardContent>
            {product.scoreHistory.length > 0 ? (
              <ComplianceTrendChart data={product.scoreHistory} />
            ) : (
              <p className="py-10 text-center text-sm text-text-secondary">No score history yet.</p>
            )}
            <div className="mt-4 grid grid-cols-3 gap-4 border-t border-border pt-4 text-center">
              <div>
                <p className="text-2xl font-semibold text-foreground">{product.inspectionCount}</p>
                <p className="text-xs text-text-secondary">Total Inspections</p>
              </div>
              <div>
                <p className="text-2xl font-semibold text-foreground">
                  {product.latestScore != null ? `${product.latestScore}%` : '—'}
                </p>
                <p className="text-xs text-text-secondary">Latest Score</p>
              </div>
              <div>
                <p className="text-2xl font-semibold text-foreground">{product.lastInspectionDate ?? '—'}</p>
                <p className="text-xs text-text-secondary">Last Inspected</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-6">
        <div className="mb-3 flex items-center gap-2">
          <ClipboardList className="size-4 text-text-secondary" />
          <h3 className="text-sm font-semibold text-foreground">Inspection History</h3>
        </div>
        {productInspections.length > 0 ? (
          <InspectionsTable inspections={productInspections} getProductName={() => product} hideProductColumn />
        ) : (
          <Card>
            <CardContent className="py-10 text-center text-sm text-text-secondary">
              No inspections recorded for this product yet.
            </CardContent>
          </Card>
        )}
      </div>
    </AppShell>
  )
}
