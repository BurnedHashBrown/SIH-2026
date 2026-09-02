import { cn } from '@/lib/utils'
import type { InspectionStatus } from '@/lib/types'
import { CheckCircle2, AlertTriangle, XCircle, Loader2, FileEdit } from 'lucide-react'

const STATUS_CONFIG: Record<
  InspectionStatus,
  { label: string; className: string; icon: React.ComponentType<{ className?: string }> }
> = {
  compliant: {
    label: 'Compliant',
    className: 'bg-status-success-bg text-status-success',
    icon: CheckCircle2,
  },
  requires_review: {
    label: 'Requires Review',
    className: 'bg-status-warning-bg text-status-warning',
    icon: AlertTriangle,
  },
  potential_violation: {
    label: 'Potential Violation',
    className: 'bg-status-danger-bg text-status-danger',
    icon: XCircle,
  },
  processing: {
    label: 'Processing',
    className: 'bg-status-info-bg text-status-info',
    icon: Loader2,
  },
  draft: {
    label: 'Draft',
    className: 'bg-surface-container text-text-secondary',
    icon: FileEdit,
  },
}

export function StatusBadge({
  status,
  className,
  size = 'md',
}: {
  status: InspectionStatus
  className?: string
  size?: 'sm' | 'md'
}) {
  const config = STATUS_CONFIG[status]
  const Icon = config.icon
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full font-medium whitespace-nowrap',
        size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs',
        config.className,
        className,
      )}
    >
      <Icon className={cn('size-3.5', status === 'processing' && 'animate-spin')} />
      {config.label}
    </span>
  )
}
