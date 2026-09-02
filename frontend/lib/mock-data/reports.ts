import type { Report } from '@/lib/types'

export const reports: Report[] = [
  { id: 'RPT-4401', inspectionId: 'INSP-8801', generatedDate: '24 Aug 2026', generatedBy: 'Aarav Mehta', status: 'final' },
  { id: 'RPT-4388', inspectionId: 'INSP-8790', generatedDate: '23 Aug 2026', generatedBy: 'Priya Nair', status: 'final' },
  { id: 'RPT-4372', inspectionId: 'INSP-8775', generatedDate: '22 Aug 2026', generatedBy: 'Priya Nair', status: 'final' },
  { id: 'RPT-4360', inspectionId: 'INSP-8760', generatedDate: '21 Aug 2026', generatedBy: 'Aarav Mehta', status: 'final' },
  { id: 'RPT-4340', inspectionId: 'INSP-8745', generatedDate: '18 Aug 2026', generatedBy: 'Priya Nair', status: 'final' },
]

export function getReportById(id: string) {
  return reports.find((r) => r.id === id)
}
