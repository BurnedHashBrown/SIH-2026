import type { Declaration, EvidenceImage, Finding } from '@/lib/types'

export interface AnalysisInput {
  images: EvidenceImage[]
  productName: string
  manufacturer: string
  netQuantity: string
  mrp: string
}

export interface AnalysisResult {
  score: number
  declarations: Declaration[]
  findings: Finding[]
}

/**
 * Simulated AI analysis. Deterministic-ish, seeded lightly by input so
 * results feel connected to what the inspector entered, without needing
 * a real vision model call.
 */
export function runMockAnalysis(input: AnalysisInput): AnalysisResult {
  const frontImage = input.images.find((i) => i.panelType === 'Front') ?? input.images[0]
  const backImage = input.images.find((i) => i.panelType === 'Back') ?? input.images[0]
  const hasLowQualityImage = input.images.some((i) => i.quality !== 'good')
  const hasCloseUp = input.images.some((i) => i.panelType === 'Close-up')
  const imageCount = input.images.length

  const declarations: Declaration[] = [
    {
      id: 'decl-name',
      label: 'Product Name',
      value: input.productName || 'Not detected',
      confidence: input.productName ? 97 : 40,
      status: input.productName ? 'detected' : 'review_required',
      region: { x: 16, y: 12, w: 66, h: 10 },
      evidenceImageId: frontImage?.id,
    },
    {
      id: 'decl-mfr',
      label: 'Manufacturer',
      value: input.manufacturer || 'Not detected',
      confidence: input.manufacturer ? 95 : 38,
      status: input.manufacturer ? 'detected' : 'review_required',
      region: { x: 10, y: 66, w: 72, h: 10 },
      evidenceImageId: backImage?.id,
    },
    {
      id: 'decl-qty',
      label: 'Net Quantity',
      value: input.netQuantity || 'Not detected',
      confidence: input.netQuantity ? 96 : 35,
      status: input.netQuantity ? 'detected' : 'review_required',
      region: { x: 60, y: 80, w: 26, h: 9 },
      evidenceImageId: frontImage?.id,
    },
    {
      id: 'decl-mrp',
      label: 'MRP',
      value: input.mrp || 'Not detected',
      confidence: input.mrp ? (hasLowQualityImage ? 88 : 96) : 33,
      status: input.mrp ? (hasLowQualityImage ? 'review_required' : 'detected') : 'review_required',
      region: { x: 10, y: 80, w: 22, h: 9 },
      evidenceImageId: frontImage?.id,
    },
    {
      id: 'decl-date',
      label: 'Date Information',
      value: hasCloseUp ? 'MFD detected on close-up panel' : 'Partially legible',
      confidence: hasCloseUp ? 93 : 61,
      status: hasCloseUp ? 'detected' : 'review_required',
      region: { x: 14, y: 30, w: 42, h: 9 },
      evidenceImageId: backImage?.id,
    },
    {
      id: 'decl-care',
      label: 'Consumer Care',
      value: imageCount >= 3 ? 'Detected on side panel' : 'Not confidently detected',
      confidence: imageCount >= 3 ? 90 : 58,
      status: imageCount >= 3 ? 'detected' : 'review_required',
      region: { x: 14, y: 46, w: 60, h: 10 },
      evidenceImageId: backImage?.id,
    },
    {
      id: 'decl-origin',
      label: 'Country of Origin',
      value: 'India (inferred from manufacturer address)',
      confidence: 84,
      status: 'detected',
      region: { x: 12, y: 58, w: 40, h: 8 },
      evidenceImageId: backImage?.id,
    },
  ]

  const findings: Finding[] = declarations
    .filter((d) => d.status === 'review_required')
    .map((d, idx) => ({
      id: `find-${idx + 1}`,
      title: d.label,
      status: 'pending' as const,
      aiConfidence: d.confidence,
      reason:
        d.confidence < 50
          ? `${d.label} could not be reliably detected in the submitted images. Manual verification is required.`
          : `${d.label} was detected with reduced confidence, possibly due to image quality or partial occlusion.`,
      evidenceFilename:
        input.images.find((i) => i.id === d.evidenceImageId)?.filename ?? input.images[0]?.filename ?? 'unknown.jpg',
    }))

  if (imageCount < 2) {
    findings.push({
      id: 'find-coverage',
      title: 'Insufficient Package Coverage',
      status: 'pending',
      aiConfidence: 45,
      reason:
        'Fewer than the recommended number of package panels were submitted, limiting the completeness of the automated review.',
      evidenceFilename: input.images[0]?.filename ?? 'unknown.jpg',
    })
  }

  const detectedCount = declarations.filter((d) => d.status === 'detected').length
  const baseScore = Math.round((detectedCount / declarations.length) * 100)
  const penalty = hasLowQualityImage ? 6 : 0
  const score = Math.max(0, Math.min(100, baseScore - penalty))

  return { score, declarations, findings }
}

export function scoreToStatus(score: number): 'compliant' | 'requires_review' | 'potential_violation' {
  if (score >= 90) return 'compliant'
  if (score >= 60) return 'requires_review'
  return 'potential_violation'
}
