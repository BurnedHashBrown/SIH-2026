'use client'

import Link from 'next/link'
import { useMemo, useState } from 'react'
import { Search, Package } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Input } from '@/components/ui/input'
import { StatusBadge } from '@/components/status-badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useDataStore } from '@/lib/data-store'

export default function ProductsPage() {
  const { products } = useDataStore()
  const [query, setQuery] = useState('')

  const filtered = useMemo(() => {
    const q = query.toLowerCase()
    return products.filter((p) =>
      `${p.brand} ${p.name} ${p.manufacturer} ${p.category} ${p.id}`.toLowerCase().includes(q),
    )
  }, [products, query])

  return (
    <AppShell title="Products">
      <PageHeader
        title="Products"
        description="Registry of all products encountered across inspections, with compliance history."
      />

      <div className="relative mb-4 max-w-sm">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-text-secondary" />
        <Input
          placeholder="Search by brand, name, manufacturer, or ID"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-9"
        />
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Product</TableHead>
              <TableHead>Manufacturer</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Inspections</TableHead>
              <TableHead>Latest Score</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Inspected</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.length === 0 && (
              <TableRow>
                <TableCell colSpan={7} className="py-10 text-center text-sm text-text-secondary">
                  <div className="flex flex-col items-center gap-2">
                    <Package className="size-6 text-text-secondary/60" />
                    No products match your search.
                  </div>
                </TableCell>
              </TableRow>
            )}
            {filtered.map((product) => (
              <TableRow key={product.id} className="cursor-pointer hover:bg-muted/40">
                <TableCell>
                  <Link href={`/products/${product.id}`} className="flex flex-col hover:underline">
                    <span className="font-medium text-foreground">{product.name}</span>
                    <span className="text-xs text-text-secondary">
                      {product.brand} · {product.id}
                    </span>
                  </Link>
                </TableCell>
                <TableCell className="text-sm text-text-secondary">{product.manufacturer}</TableCell>
                <TableCell className="text-sm text-text-secondary">{product.category}</TableCell>
                <TableCell className="text-sm text-text-secondary">{product.inspectionCount}</TableCell>
                <TableCell className="text-sm font-medium text-foreground">
                  {product.latestScore != null ? `${product.latestScore}%` : '—'}
                </TableCell>
                <TableCell>
                  <StatusBadge status={product.status} size="sm" />
                </TableCell>
                <TableCell className="text-sm text-text-secondary">{product.lastInspectionDate ?? '—'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </AppShell>
  )
}
