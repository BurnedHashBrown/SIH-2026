'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowLeft, ArrowRight, ScanSearch } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Button } from '@/components/ui/button'
import { StepIndicator } from '@/components/inspection-wizard/step-indicator'
import { StepProduct, type ProductFormState } from '@/components/inspection-wizard/step-product'
import { StepUpload, type WizardImage } from '@/components/inspection-wizard/step-upload'
import { StepAnalyzing } from '@/components/inspection-wizard/step-analyzing'
import { useDataStore } from '@/lib/data-store'
import { useAuth } from '@/lib/auth-context'
import { runMockAnalysis, scoreToStatus } from '@/lib/analysis-service'
import type { EvidenceImage, Inspection } from '@/lib/types'

const STEPS = [
  { label: 'Product Details', description: 'Identify the product and context' },
  { label: 'Evidence Photos', description: 'Upload package images' },
  { label: 'AI Analysis', description: 'Automated compliance review' },
]

const INITIAL_PRODUCT_STATE: ProductFormState = {
  mode: 'existing',
  existingProductId: '',
  brand: '',
  name: '',
  category: '',
  manufacturer: '',
  netQuantity: '',
  mrp: '',
  batchNumber: '',
  location: '',
  inspectionType: '',
  remarks: '',
}

export default function NewInspectionPage() {
  const router = useRouter()
  const { products, addInspection, addProduct } = useDataStore()
  const { profile } = useAuth()
  const [step, setStep] = useState(1)
  const [productForm, setProductForm] = useState<ProductFormState>(INITIAL_PRODUCT_STATE)
  const [images, setImages] = useState<WizardImage[]>([])

  const selectedExisting = products.find((p) => p.id === productForm.existingProductId)

  function canProceedStep1() {
    if (productForm.mode === 'existing') return Boolean(productForm.existingProductId) && Boolean(productForm.location)
    return Boolean(productForm.brand && productForm.name && productForm.manufacturer && productForm.location)
  }

  function canProceedStep2() {
    return images.length >= 1
  }

  function handleAnalysisComplete() {
    const productName = productForm.mode === 'existing' ? selectedExisting?.name ?? '' : productForm.name
    const manufacturer = productForm.mode === 'existing' ? selectedExisting?.manufacturer ?? '' : productForm.manufacturer
    const netQuantity = productForm.mode === 'existing' ? selectedExisting?.netQuantity ?? '' : productForm.netQuantity
    const mrp = productForm.mode === 'existing' ? selectedExisting?.mrp ?? '' : productForm.mrp

    const evidenceImages: EvidenceImage[] = images.map((img) => ({
      id: img.id,
      url: img.previewUrl,
      filename: img.file.name,
      fileSizeKb: Math.round(img.file.size / 1024),
      panelType: img.panelType,
      quality: img.quality,
    }))

    const result = runMockAnalysis({
      images: evidenceImages,
      productName,
      manufacturer,
      netQuantity,
      mrp,
    })

    const productId = productForm.mode === 'existing' ? productForm.existingProductId : `PRD-${Date.now().toString().slice(-6)}`
    const inspectionId = `INS-${Date.now().toString().slice(-8)}`
    const now = new Date()
    const displayDate = now.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })

    if (productForm.mode === 'new' && typeof addProduct === 'function') {
      addProduct({
        id: productId,
        brand: productForm.brand,
        name: productForm.name,
        category: productForm.category || 'Uncategorized',
        manufacturer: productForm.manufacturer,
        netQuantity: productForm.netQuantity,
        mrp: productForm.mrp,
        batchNumber: productForm.batchNumber || '-',
        mfgDate: '-',
        consumerCare: '-',
        lastInspectionDate: displayDate,
        inspectionCount: 1,
        latestScore: result.score,
        status: scoreToStatus(result.score) as Inspection['status'],
        scoreHistory: [{ date: displayDate, score: result.score }],
      })
    }

    const inspection: Inspection = {
      id: inspectionId,
      productId,
      location: productForm.location,
      date: now.toISOString(),
      type: productForm.inspectionType || 'Routine Market Surveillance',
      remarks: productForm.remarks || undefined,
      inspector: profile?.name ?? 'Inspector',
      status: scoreToStatus(result.score) as Inspection['status'],
      aiScore: result.score,
      images: evidenceImages,
      declarations: result.declarations,
      findings: result.findings,
      createdAt: now.toISOString(),
    }

    addInspection(inspection)
    router.push(`/inspections/${inspectionId}`)
  }

  return (
    <AppShell title="New Inspection">
      <div className="flex flex-col gap-6">
        <PageHeader
          title="New Inspection"
          description="Capture package evidence and let AI cross-check declarations against Legal Metrology rules."
        />

        <div className="rounded-lg border border-border bg-card p-5">
          <StepIndicator steps={STEPS} currentStep={step} />
        </div>

        {step === 1 && (
          <StepProduct
            products={products}
            value={productForm}
            onChange={(patch) => setProductForm((prev) => ({ ...prev, ...patch }))}
          />
        )}

        {step === 2 && <StepUpload images={images} onChange={setImages} />}

        {step === 3 && <StepAnalyzing onComplete={handleAnalysisComplete} />}

        {step < 3 && (
          <div className="flex items-center justify-between border-t border-border pt-4">
            <Button variant="outline" onClick={() => (step === 1 ? router.push('/dashboard') : setStep(step - 1))}>
              <ArrowLeft className="size-4" />
              {step === 1 ? 'Cancel' : 'Back'}
            </Button>
            {step === 1 && (
              <Button onClick={() => setStep(2)} disabled={!canProceedStep1()}>
                Continue to Evidence
                <ArrowRight className="size-4" />
              </Button>
            )}
            {step === 2 && (
              <Button onClick={() => setStep(3)} disabled={!canProceedStep2()}>
                <ScanSearch className="size-4" />
                Run AI Analysis
              </Button>
            )}
          </div>
        )}
      </div>
    </AppShell>
  )
}
