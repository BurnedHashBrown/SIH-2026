'use client'

import { cn } from '@/lib/utils'
import type { Declaration } from '@/lib/types'
import { CheckCircle2, AlertTriangle, HelpCircle } from 'lucide-react'

const STATUS_CONFIG: Record<Declaration['status'], { label: string; className: string; icon: typeof CheckCircle2 }> = {
  detected: { label: 'Detected', className: 'text-status-success', icon: CheckCircle2 },
  review_required: { label: 'Review Required', className: 'text-status-warning', icon: AlertTriangle },
  not_detected: { label: 'Not Detected', className: 'text-status-danger', icon: HelpCircle },
}

export function DeclarationList({
  declarations,
  activeId,
  onSelect,
}: {
  declarations: Declaration[]
  activeId?: string
  onSelect?: (declaration: Declaration) => void
}) {
  return (
    <ul className="divide-y divide-border-subtle rounded-lg border border-border-subtle bg-surface-container-lowest">
      {declarations.map((decl) => {
        const config = STATUS_CONFIG[decl.status]
        const Icon = config.icon
        return (
          <li key={decl.id}>
            <button
              onClick={() => onSelect?.(decl)}
              className={cn(
                'flex w-full items-start justify-between gap-3 px-4 py-3 text-left transition-colors hover:bg-surface-container',
                activeId === decl.id && 'bg-primary-container/10',
              )}
            >
              <div className="min-w-0">
                <p className="text-sm font-medium text-text-primary">{decl.label}</p>
                <p className="mt-0.5 truncate text-sm text-text-secondary">{decl.value}</p>
              </div>
              <div className="flex shrink-0 flex-col items-end gap-1">
                <span className={cn('inline-flex items-center gap-1 text-xs font-medium', config.className)}>
                  <Icon className="size-3.5" /> {config.label}
                </span>
                <span className="text-xs text-text-secondary">{decl.confidence}% confidence</span>
              </div>
            </button>
          </li>
        )
      })}
    </ul>
  )
}
