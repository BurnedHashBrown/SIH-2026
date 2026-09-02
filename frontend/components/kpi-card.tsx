import { cn } from '@/lib/utils'

export function KpiCard({
  label,
  value,
  helpText,
  tone = 'default',
  icon,
}: {
  label: string
  value: string
  helpText?: string
  tone?: 'default' | 'success' | 'warning' | 'danger'
  icon?: React.ReactNode
}) {
  const toneClass = {
    default: 'text-text-primary',
    success: 'text-status-success',
    warning: 'text-status-warning',
    danger: 'text-status-danger',
  }[tone]

  return (
    <div className="rounded-xl border border-border-subtle bg-surface-container-lowest p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-text-secondary">{label}</span>
        {icon ? <span className="text-text-secondary">{icon}</span> : null}
      </div>
      <p className={cn('mt-2 text-3xl font-semibold tracking-tight', toneClass)}>{value}</p>
      {helpText ? <p className="mt-1 text-xs text-text-secondary">{helpText}</p> : null}
    </div>
  )
}
