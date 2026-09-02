'use client'

import Link from 'next/link'
import { ChevronRight } from 'lucide-react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { StatusBadge } from '@/components/status-badge'
import type { Inspection, Product } from '@/lib/types'

export function InspectionsTable({
  inspections,
  getProductName,
  hideProductColumn = false,
}: {
  inspections: Inspection[]
  getProductName: (productId: string) => Pick<Product, 'name' | 'brand'> | undefined
  hideProductColumn?: boolean
}) {
  if (inspections.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-border-subtle p-10 text-center text-sm text-text-secondary">
        No inspections found.
      </div>
    )
  }

  return (
    <div className="overflow-hidden rounded-xl border border-border-subtle bg-surface-container-lowest">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Inspection ID</TableHead>
            {!hideProductColumn && <TableHead>Product</TableHead>}
            <TableHead>Location</TableHead>
            <TableHead>Date</TableHead>
            <TableHead>AI Score</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-10" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {inspections.map((inspection) => {
            const product = getProductName(inspection.productId)
            return (
              <TableRow key={inspection.id} className="group">
                <TableCell>
                  <Link href={`/inspections/${inspection.id}`} className="font-medium text-primary hover:underline">
                    {inspection.id}
                  </Link>
                </TableCell>
                {!hideProductColumn && (
                  <TableCell>
                    <div className="flex flex-col">
                      <span className="font-medium text-text-primary">{product?.name ?? 'Unknown product'}</span>
                      <span className="text-xs text-text-secondary">{product?.brand}</span>
                    </div>
                  </TableCell>
                )}
                <TableCell className="text-text-secondary">{inspection.location}</TableCell>
                <TableCell className="text-text-secondary">{inspection.date}</TableCell>
                <TableCell className="font-medium text-text-primary">
                  {inspection.aiScore != null ? `${inspection.aiScore}%` : '—'}
                </TableCell>
                <TableCell>
                  <StatusBadge status={inspection.status} size="sm" />
                </TableCell>
                <TableCell>
                  <Link href={`/inspections/${inspection.id}`}>
                    <ChevronRight className="size-4 text-text-secondary transition-colors group-hover:text-text-primary" />
                  </Link>
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
