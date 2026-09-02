import type { ComplianceRule } from '@/lib/types'

export const rules: ComplianceRule[] = [
  {
    id: 'RULE-001',
    name: 'Net Quantity Declaration',
    declaration: 'Net Quantity',
    validationType: 'Presence + Unit Format',
    severity: 'Required',
    version: 'v2.3',
    status: 'Active',
    description:
      'Every package must declare the net quantity of the commodity in standard units (g, kg, ml, L, or number of units) in accordance with Legal Metrology (Packaged Commodities) Rules.',
    howChecked:
      'AI extracts printed net quantity value and unit, verifies presence, correct unit format, and text-height compliance based on package size.',
    evidenceRequired: 'Front panel image with net quantity clearly visible.',
    applicability: 'All pre-packaged commodities.',
    lastUpdated: '10 Jun 2026',
  },
  {
    id: 'RULE-002',
    name: 'Maximum Retail Price (MRP) Declaration',
    declaration: 'MRP',
    validationType: 'Presence + Format',
    severity: 'Required',
    version: 'v2.1',
    status: 'Active',
    description:
      'The Maximum Retail Price inclusive of all taxes must be declared prominently, prefixed with "MRP" and the applicable currency symbol.',
    howChecked:
      'AI detects the MRP text pattern and cross-checks that the value is preceded by required qualifiers such as "inclusive of all taxes".',
    evidenceRequired: 'Front or side panel image showing MRP declaration.',
    applicability: 'All pre-packaged commodities intended for retail sale.',
    lastUpdated: '02 May 2026',
  },
  {
    id: 'RULE-003',
    name: 'Manufacturer / Packer / Importer Details',
    declaration: 'Manufacturer Details',
    validationType: 'Presence + Address Completeness',
    severity: 'Required',
    version: 'v1.8',
    status: 'Active',
    description:
      'The name and complete address of the manufacturer, packer, or importer must be declared on the package.',
    howChecked:
      'AI performs OCR on back/side panels to locate manufacturer name and address block, checking for completeness (city, state, PIN code).',
    evidenceRequired: 'Back panel image with manufacturer address block.',
    applicability: 'All pre-packaged commodities.',
    lastUpdated: '18 Apr 2026',
  },
  {
    id: 'RULE-004',
    name: 'Consumer Care Details',
    declaration: 'Consumer Care',
    validationType: 'Presence',
    severity: 'Required',
    version: 'v1.4',
    status: 'Active',
    description:
      'A telephone number, email address, or postal address for consumer complaints must be declared on the package.',
    howChecked:
      'AI searches all panel images for phone number patterns, email formats, or a dedicated "Consumer Care" label.',
    evidenceRequired: 'Any panel image showing the consumer care block.',
    applicability: 'All pre-packaged commodities.',
    lastUpdated: '30 Mar 2026',
  },
  {
    id: 'RULE-005',
    name: 'Date of Manufacture / Import / Packing',
    declaration: 'Date Information',
    validationType: 'Presence + Format',
    severity: 'Required',
    version: 'v2.0',
    status: 'Active',
    description:
      'The month and year of manufacture, packing, or import must be declared in MM/YYYY format.',
    howChecked:
      'AI extracts date-like tokens near "MFD", "PKD", or "Mfg. Date" labels and validates the format and plausibility of the date.',
    evidenceRequired: 'Back or side panel image showing date declaration.',
    applicability: 'All pre-packaged commodities.',
    lastUpdated: '22 Feb 2026',
  },
  {
    id: 'RULE-006',
    name: 'Country of Origin',
    declaration: 'Country of Origin',
    validationType: 'Presence',
    severity: 'Required',
    version: 'v1.2',
    status: 'Active',
    description:
      'Imported pre-packaged commodities must clearly declare the country of origin, manufacture, or assembly.',
    howChecked:
      'AI checks for a printed "Country of Origin" declaration when importer details are present on the package.',
    evidenceRequired: 'Any panel image showing origin declaration.',
    applicability: 'Imported pre-packaged commodities.',
    lastUpdated: '05 Jan 2026',
  },
  {
    id: 'RULE-007',
    name: 'Unit Sale Price Declaration',
    declaration: 'Unit Sale Price',
    validationType: 'Recommended Disclosure',
    severity: 'Recommended',
    version: 'v1.0',
    status: 'Active',
    description:
      'For certain commodity categories, the sale price per standard unit (e.g. per kg, per litre) is recommended for consumer clarity.',
    howChecked:
      'AI flags absence of a per-unit price for applicable product categories as an informational note rather than a violation.',
    evidenceRequired: 'Any panel image showing pricing information.',
    applicability: 'Select bulk and household product categories.',
    lastUpdated: '14 Dec 2025',
  },
  {
    id: 'RULE-008',
    name: 'Legible Font Size for Declarations',
    declaration: 'Font Legibility',
    validationType: 'Visual Legibility Heuristic',
    severity: 'Informational',
    version: 'v1.1',
    status: 'Deprecated',
    description:
      'Mandatory declarations should be printed in a font size that is legible relative to the package surface area, per prior guidance now superseded by RULE-001.',
    howChecked:
      'Superseded by embedded checks within RULE-001 text-height compliance validation.',
    evidenceRequired: 'N/A',
    applicability: 'Deprecated - retained for historical reference.',
    lastUpdated: '11 Nov 2025',
  },
]

export function getRuleById(id: string) {
  return rules.find((r) => r.id === id)
}
