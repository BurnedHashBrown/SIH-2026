'use client'

import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import { inspections as initialInspections } from '@/lib/mock-data/inspections'
import { products as initialProducts } from '@/lib/mock-data/products'
import { reports as initialReports } from '@/lib/mock-data/reports'
import type { Inspection, Product, Report } from '@/lib/types'

interface DataStoreState {
  inspections: Inspection[]
  products: Product[]
  reports: Report[]
  addInspection: (inspection: Inspection) => void
  updateInspection: (id: string, patch: Partial<Inspection>) => void
  addReport: (report: Report) => void
  addProduct: (product: Product) => void
  getInspection: (id: string) => Inspection | undefined
  getProduct: (id: string) => Product | undefined
  getReport: (id: string) => Report | undefined
}

const DataStoreContext = createContext<DataStoreState | null>(null)

export function DataStoreProvider({ children }: { children: React.ReactNode }) {
  const [inspections, setInspections] = useState<Inspection[]>(initialInspections)
  const [products, setProducts] = useState<Product[]>(initialProducts)
  const [reports, setReports] = useState<Report[]>(initialReports)

  const addInspection = useCallback((inspection: Inspection) => {
    setInspections((prev) => [inspection, ...prev])
  }, [])

  const updateInspection = useCallback((id: string, patch: Partial<Inspection>) => {
    setInspections((prev) => prev.map((i) => (i.id === id ? { ...i, ...patch } : i)))
  }, [])

  const addReport = useCallback((report: Report) => {
    setReports((prev) => [report, ...prev])
  }, [])

  const addProduct = useCallback((product: Product) => {
    setProducts((prev) => [product, ...prev])
  }, [])

  const getInspection = useCallback((id: string) => inspections.find((i) => i.id === id), [inspections])
  const getProduct = useCallback((id: string) => products.find((p) => p.id === id), [products])
  const getReport = useCallback((id: string) => reports.find((r) => r.id === id), [reports])

  const value = useMemo(
    () => ({
      inspections,
      products,
      reports,
      addInspection,
      updateInspection,
      addReport,
      addProduct,
      getInspection,
      getProduct,
      getReport,
    }),
    [inspections, products, reports, addInspection, updateInspection, addReport, addProduct, getInspection, getProduct, getReport],
  )

  return <DataStoreContext.Provider value={value}>{children}</DataStoreContext.Provider>
}

export function useDataStore() {
  const ctx = useContext(DataStoreContext)
  if (!ctx) throw new Error('useDataStore must be used within DataStoreProvider')
  return ctx
}
