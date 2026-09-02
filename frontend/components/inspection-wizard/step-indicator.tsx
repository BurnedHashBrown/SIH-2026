import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Step {
  label: string
  description: string
}

export function StepIndicator({ steps, currentStep }: { steps: Step[]; currentStep: number }) {
  return (
    <ol className="flex flex-col gap-0 sm:flex-row sm:items-start sm:gap-4">
      {steps.map((step, idx) => {
        const stepNumber = idx + 1
        const isComplete = stepNumber < currentStep
        const isCurrent = stepNumber === currentStep
        return (
          <li key={step.label} className="flex flex-1 items-start gap-3 sm:flex-col sm:gap-2">
            <div className="flex items-center gap-3 sm:w-full">
              <div
                className={cn(
                  'flex size-8 shrink-0 items-center justify-center rounded-full border text-sm font-semibold transition-colors',
                  isComplete
                    ? 'border-primary bg-primary text-primary-foreground'
                    : isCurrent
                      ? 'border-primary text-primary'
                      : 'border-border text-text-secondary',
                )}
              >
                {isComplete ? <Check className="size-4" /> : stepNumber}
              </div>
              {idx < steps.length - 1 && (
                <div
                  className={cn(
                    'hidden h-px flex-1 sm:hidden',
                  )}
                />
              )}
            </div>
            <div className="flex flex-col pb-4 sm:pb-0">
              <span className={cn('text-sm font-medium', isCurrent ? 'text-foreground' : 'text-text-secondary')}>
                {step.label}
              </span>
              <span className="text-xs text-text-secondary">{step.description}</span>
            </div>
          </li>
        )
      })}
    </ol>
  )
}
