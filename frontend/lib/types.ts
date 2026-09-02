export type InspectionStatus =
  | 'draft'
  | 'processing'
  | 'compliant'
  | 'requires_review'
  | 'potential_violation'

export type FindingStatus = 'pending' | 'confirmed' | 'rejected' | 'not_applicable'

export type DeclarationStatus = 'detected' | 'review_required' | 'not_detected'

export type PanelType =
  | 'Front'
  | 'Back'
  | 'Left Side'
  | 'Right Side'
  | 'Top'
  | 'Bottom'
  | 'Close-up'
  | 'Other'

export type ImageQuality = 'good' | 'low_resolution' | 'blur' | 'low_light'

export interface EvidenceImage {
  id: string
  url: string
  filename: string
  fileSizeKb: number
  panelType: PanelType
  quality: ImageQuality
}

export interface Declaration {
  id: string
  label: string
  value: string
  confidence: number
  status: DeclarationStatus
  region?: { x: number; y: number; w: number; h: number }
  evidenceImageId?: string
}

export interface Finding {
  id: string
  title: string
  status: FindingStatus
  aiConfidence: number
  reason: string
  evidenceFilename: string
  inspectorRemarks?: string
  reviewer?: string
  reviewDate?: string
}

export interface Product {
  id: string
  brand: string
  name: string
  category: string
  productType?: string
  manufacturer: string
  packer?: string
  importer?: string
  countryOfOrigin?: string
  netQuantity: string
  mrp: string
  batchNumber: string
  mfgDate: string
  consumerCare: string
  lastInspectionDate?: string
  inspectionCount: number
  latestScore?: number
  status: InspectionStatus
  scoreHistory: { date: string; score: number }[]
}

export interface Inspection {
  id: string
  productId: string
  location: string
  date: string
  type: string
  remarks?: string
  inspector: string
  status: InspectionStatus
  aiScore?: number
  images: EvidenceImage[]
  declarations: Declaration[]
  findings: Finding[]
  reportId?: string
  createdAt: string
}

export interface Report {
  id: string
  inspectionId: string
  generatedDate: string
  generatedBy: string
  status: 'final' | 'draft'
}

export interface ComplianceRule {
  id: string
  name: string
  declaration: string
  validationType: string
  severity: 'Required' | 'Recommended' | 'Informational'
  version: string
  status: 'Active' | 'Deprecated'
  description: string
  howChecked: string
  evidenceRequired: string
  applicability: string
  lastUpdated: string
}

export interface InspectorProfile {
  name: string
  designation: string
  employeeId: string
  email: string
  phone: string
  organization: string
  department: string
  stateRegion: string
}
