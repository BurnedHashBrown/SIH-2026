'use client'

import Image from 'next/image'
import { useState } from 'react'
import { cn } from '@/lib/utils'
import type { EvidenceImage } from '@/lib/types'
import { AlertCircle } from 'lucide-react'

const QUALITY_LABEL: Record<EvidenceImage['quality'], string> = {
  good: 'Good quality',
  low_resolution: 'Low resolution',
  blur: 'Motion blur detected',
  low_light: 'Low light',
}

export function EvidenceGallery({
  images,
  activeImageId,
  onSelect,
  highlightRegion,
}: {
  images: EvidenceImage[]
  activeImageId?: string
  onSelect?: (imageId: string) => void
  highlightRegion?: { x: number; y: number; w: number; h: number }
}) {
  const [internalActive, setInternalActive] = useState(images[0]?.id)
  const activeId = activeImageId ?? internalActive
  const active = images.find((i) => i.id === activeId) ?? images[0]

  function selectImage(id: string) {
    setInternalActive(id)
    onSelect?.(id)
  }

  if (!active) {
    return (
      <div className="flex aspect-[4/3] items-center justify-center rounded-lg border border-dashed border-border-subtle text-sm text-text-secondary">
        No images available
      </div>
    )
  }

  return (
    <div>
      <div className="relative overflow-hidden rounded-lg border border-border-subtle bg-surface-container">
        <div className="relative aspect-[4/3] w-full">
          <Image src={active.url || '/placeholder.svg'} alt={`${active.panelType} panel evidence`} fill className="object-cover" />
          {highlightRegion && active.id === activeImageId ? (
            <div
              className="absolute rounded-sm border-2 border-status-warning bg-status-warning/20 shadow-[0_0_0_9999px_rgba(0,0,0,0.15)]"
              style={{
                left: `${highlightRegion.x}%`,
                top: `${highlightRegion.y}%`,
                width: `${highlightRegion.w}%`,
                height: `${highlightRegion.h}%`,
              }}
            />
          ) : null}
        </div>
        <div className="flex items-center justify-between gap-2 border-t border-border-subtle bg-surface-container-lowest px-3 py-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-text-primary">{active.panelType}</span>
            <span className="text-xs text-text-secondary">{active.filename}</span>
          </div>
          {active.quality !== 'good' ? (
            <span className="inline-flex items-center gap-1 rounded-full bg-status-warning-bg px-2 py-0.5 text-xs font-medium text-status-warning">
              <AlertCircle className="size-3" /> {QUALITY_LABEL[active.quality]}
            </span>
          ) : null}
        </div>
      </div>

      <div className="mt-3 flex gap-2 overflow-x-auto pb-1">
        {images.map((img) => (
          <button
            key={img.id}
            onClick={() => selectImage(img.id)}
            className={cn(
              'relative size-16 shrink-0 overflow-hidden rounded-md border-2 transition-colors',
              img.id === activeId ? 'border-primary' : 'border-transparent hover:border-border-subtle',
            )}
            aria-label={`View ${img.panelType} panel`}
          >
            <Image src={img.url || '/placeholder.svg'} alt="" fill className="object-cover" />
          </button>
        ))}
      </div>
    </div>
  )
}
