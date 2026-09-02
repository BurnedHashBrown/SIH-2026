'use client'

import { useEffect, useState } from 'react'
import { Loader2, CheckCircle2 } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

const STAGES = [
  'Uploading evidence images',
  'Detecting package panels',
  'Extracting declared quantity, MRP, and dates',
  'Cross-checking against Legal Metrology rules',
  'Compiling findings and confidence scores',
]

export function StepAnalyzing({ onComplete }: { onComplete: () => void }) {
  const [stageIndex, setStageIndex] = useState(0)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const stageTimer = setInterval(() => {
      setStageIndex((prev) => (prev < STAGES.length - 1 ? prev + 1 : prev))
    }, 500)

    const progressTimer = setInterval(() => {
      setProgress((prev) => {
        const next = prev + 5
        if (next >= 100) {
          clearInterval(progressTimer)
          clearInterval(stageTimer)
          setStageIndex(STAGES.length)
          return 100
        }
        return next
      })
    }, 100)

    return () => {
      clearInterval(stageTimer)
      clearInterval(progressTimer)
    }
  }, [])

  useEffect(() => {
    if (progress >= 100) {
      const timer = setTimeout(() => {
        onComplete()
      }, 400)
      return () => clearTimeout(timer)
    }
  }, [progress, onComplete])

  return (
    <Card>
      <CardContent className="flex flex-col items-center gap-6 py-12 text-center">
        <div className="flex size-16 items-center justify-center rounded-full bg-primary/10">
          <Loader2 className="size-8 animate-spin text-primary" />
        </div>
        <div className="flex flex-col gap-1">
          <h2 className="text-lg font-semibold text-foreground">Running AI Compliance Analysis</h2>
          <p className="text-sm text-text-secondary">
            Analyzing package declarations against Legal Metrology (Packaged Commodities) Rules
          </p>
        </div>

        <div className="w-full max-w-md">
          <Progress value={progress} className="h-2" />
          <p className="mt-2 text-xs text-text-secondary">{progress}% complete</p>
        </div>

        <ul className="flex w-full max-w-md flex-col gap-2.5 text-left">
          {STAGES.map((stage, idx) => (
            <li
              key={stage}
              className={cn(
                'flex items-center gap-2.5 text-sm transition-colors',
                idx < stageIndex
                  ? 'text-foreground'
                  : idx === stageIndex
                    ? 'text-primary'
                    : 'text-text-secondary/60',
              )}
            >
              {idx < stageIndex ? (
                <CheckCircle2 className="size-4 shrink-0 text-success" />
              ) : idx === stageIndex ? (
                <Loader2 className="size-4 shrink-0 animate-spin" />
              ) : (
                <span className="size-4 shrink-0 rounded-full border border-border" />
              )}
              {stage}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
