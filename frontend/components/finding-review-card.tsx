'use client'

import { useState } from 'react'
import { Check, X, MinusCircle, ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { cn } from '@/lib/utils'
import type { Finding } from '@/lib/types'

const STATUS_STYLE: Record<Finding['status'], string> = {
  pending: 'bg-status-warning-bg text-status-warning',
  confirmed: 'bg-status-danger-bg text-status-danger',
  rejected: 'bg-status-success-bg text-status-success',
  not_applicable: 'bg-surface-container text-text-secondary',
}

const STATUS_LABEL: Record<Finding['status'], string> = {
  pending: 'Pending Review',
  confirmed: 'Confirmed Violation',
  rejected: 'Rejected (False Positive)',
  not_applicable: 'Not Applicable',
}

export function FindingReviewCard({
  finding,
  onUpdate,
  readOnly = false,
}: {
  finding: Finding
  onUpdate?: (patch: Partial<Finding>) => void
  readOnly?: boolean
}) {
  const [remarks, setRemarks] = useState(finding.inspectorRemarks ?? '')
  const [expanded, setExpanded] = useState(finding.status === 'pending')

  function decide(status: Finding['status']) {
    onUpdate?.({ status, inspectorRemarks: remarks, reviewer: 'Aarav Mehta', reviewDate: 'Today' })
  }

  return (
    <div className="rounded-lg border border-border-subtle bg-surface-container-lowest">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left"
      >
        <div>
          <p className="text-sm font-medium text-text-primary">{finding.title}</p>
          <p className="mt-0.5 text-xs text-text-secondary">
            AI confidence: {finding.aiConfidence}% &middot; Evidence: {finding.evidenceFilename}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <span className={cn('rounded-full px-2.5 py-1 text-xs font-medium', STATUS_STYLE[finding.status])}>
            {STATUS_LABEL[finding.status]}
          </span>
          <ChevronDown className={cn('size-4 text-text-secondary transition-transform', expanded && 'rotate-180')} />
        </div>
      </button>

      {expanded ? (
        <div className="space-y-3 border-t border-border-subtle px-4 py-3">
          <p className="text-sm text-text-secondary">{finding.reason}</p>

          {!readOnly ? (
            <>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-text-secondary" htmlFor={`remarks-${finding.id}`}>
                  Inspector remarks
                </label>
                <Textarea
                  id={`remarks-${finding.id}`}
                  value={remarks}
                  onChange={(e) => setRemarks(e.target.value)}
                  placeholder="Add notes about your decision..."
                  className="min-h-20"
                />
              </div>
              <div className="flex flex-wrap gap-2">
                <Button size="sm" variant="destructive" onClick={() => decide('confirmed')}>
                  <Check className="size-3.5" /> Confirm Violation
                </Button>
                <Button size="sm" variant="outline" onClick={() => decide('rejected')}>
                  <X className="size-3.5" /> Reject (False Positive)
                </Button>
                <Button size="sm" variant="ghost" onClick={() => decide('not_applicable')}>
                  <MinusCircle className="size-3.5" /> Not Applicable
                </Button>
              </div>
            </>
          ) : finding.inspectorRemarks ? (
            <div className="rounded-md bg-surface-container p-3 text-sm text-text-secondary">
              <span className="font-medium text-text-primary">Inspector remarks: </span>
              {finding.inspectorRemarks}
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  )
}
