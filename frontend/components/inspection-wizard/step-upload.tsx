'use client'

import { useRef } from 'react'
import Image from 'next/image'
import { UploadCloud, X } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import type { PanelType } from '@/lib/types'
import { cn } from '@/lib/utils'

export interface WizardImage {
  id: string
  file: File
  previewUrl: string
  panelType: PanelType
  quality: 'good' | 'low_resolution' | 'blur' | 'low_light'
}

const PANEL_TYPES: PanelType[] = ['Front', 'Back', 'Left Side', 'Right Side', 'Top', 'Bottom', 'Close-up', 'Other']

function simulateQuality(file: File): WizardImage['quality'] {
  if (file.size < 80_000) return 'low_resolution'
  const r = Math.random()
  if (r < 0.12) return 'blur'
  if (r < 0.2) return 'low_light'
  return 'good'
}

export function StepUpload({
  images,
  onChange,
}: {
  images: WizardImage[]
  onChange: (images: WizardImage[]) => void
}) {
  const inputRef = useRef<HTMLInputElement>(null)

  function handleFiles(fileList: FileList | null) {
    if (!fileList) return
    const newImages: WizardImage[] = Array.from(fileList).map((file, idx) => ({
      id: `${Date.now()}-${idx}`,
      file,
      previewUrl: URL.createObjectURL(file),
      panelType: images.length + idx === 0 ? 'Front' : images.length + idx === 1 ? 'Back' : 'Other',
      quality: simulateQuality(file),
    }))
    onChange([...images, ...newImages])
  }

  function removeImage(id: string) {
    onChange(images.filter((img) => img.id !== id))
  }

  function updatePanelType(id: string, panelType: PanelType) {
    onChange(images.map((img) => (img.id === id ? { ...img, panelType } : img)))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Package Evidence Photos</CardTitle>
        <CardDescription>
          Upload clear photos of each package panel. Include Front, Back, and any Close-up shots of declarations for
          best accuracy.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-border bg-muted/40 px-6 py-10 text-center transition-colors hover:border-primary/50 hover:bg-muted/60"
        >
          <UploadCloud className="size-8 text-text-secondary" aria-hidden="true" />
          <p className="text-sm font-medium text-foreground">Click to upload photos</p>
          <p className="text-xs text-text-secondary">JPG or PNG, multiple files supported</p>
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            multiple
            className="sr-only"
            onChange={(e) => handleFiles(e.target.files)}
          />
        </button>

        {images.length > 0 && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {images.map((img) => (
              <div key={img.id} className="flex flex-col gap-2 rounded-lg border border-border bg-card p-3">
                <div className="relative aspect-[4/3] w-full overflow-hidden rounded-md bg-muted">
                  <Image src={img.previewUrl || '/placeholder.svg'} alt={`Evidence upload ${img.file.name}`} fill className="object-cover" unoptimized />
                  <button
                    type="button"
                    onClick={() => removeImage(img.id)}
                    aria-label={`Remove ${img.file.name}`}
                    className="absolute right-1.5 top-1.5 flex size-6 items-center justify-center rounded-full bg-background/90 text-foreground shadow-sm hover:bg-background"
                  >
                    <X className="size-3.5" />
                  </button>
                  <Badge
                    variant="outline"
                    className={cn(
                      'absolute bottom-1.5 left-1.5 border-0 bg-background/90 text-[10px]',
                      img.quality !== 'good' && 'text-warning',
                    )}
                  >
                    {img.quality === 'good' ? 'Good quality' : img.quality.replace('_', ' ')}
                  </Badge>
                </div>
                <p className="truncate text-xs text-text-secondary" title={img.file.name}>
                  {img.file.name}
                </p>
                <Select value={img.panelType} onValueChange={(v) => updatePanelType(img.id, v as PanelType)}>
                  <SelectTrigger className="h-8 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {PANEL_TYPES.map((p) => (
                      <SelectItem key={p} value={p} className="text-xs">
                        {p}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            ))}
          </div>
        )}

        {images.length > 0 && images.length < 2 && (
          <p className="text-xs text-warning">
            Add at least one more panel (Back or Close-up) for a more complete automated review.
          </p>
        )}

        <div>
          <Button type="button" variant="outline" size="sm" onClick={() => inputRef.current?.click()}>
            Add more photos
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
