'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import type { Product } from '@/lib/types'

export interface ProductFormState {
  mode: 'existing' | 'new'
  existingProductId: string
  brand: string
  name: string
  category: string
  manufacturer: string
  netQuantity: string
  mrp: string
  batchNumber: string
  location: string
  inspectionType: string
  remarks: string
}

export function StepProduct({
  products,
  value,
  onChange,
}: {
  products: Product[]
  value: ProductFormState
  onChange: (patch: Partial<ProductFormState>) => void
}) {
  const selectedExisting = products.find((p) => p.id === value.existingProductId)

  return (
    <div className="flex flex-col gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Product Identification</CardTitle>
          <CardDescription>Select a previously registered product or enter details for a new one.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-5">
          <RadioGroup
            value={value.mode}
            onValueChange={(v) => onChange({ mode: v as 'existing' | 'new' })}
            className="flex flex-col gap-3 sm:flex-row sm:gap-6"
          >
            <div className="flex items-center gap-2">
              <RadioGroupItem value="existing" id="mode-existing" />
              <Label htmlFor="mode-existing" className="font-normal">
                Existing product in registry
              </Label>
            </div>
            <div className="flex items-center gap-2">
              <RadioGroupItem value="new" id="mode-new" />
              <Label htmlFor="mode-new" className="font-normal">
                New product / first inspection
              </Label>
            </div>
          </RadioGroup>

          {value.mode === 'existing' ? (
            <div className="flex flex-col gap-2">
              <Label htmlFor="existing-product">Product</Label>
              <Select value={value.existingProductId} onValueChange={(v) => onChange({ existingProductId: v })}>
                <SelectTrigger id="existing-product">
                  <SelectValue placeholder="Search and select a product" />
                </SelectTrigger>
                <SelectContent>
                  {products.map((p) => (
                    <SelectItem key={p.id} value={p.id}>
                      {p.brand} — {p.name} ({p.id})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {selectedExisting && (
                <p className="mt-1 text-xs text-text-secondary">
                  Manufacturer: {selectedExisting.manufacturer} · Net Qty: {selectedExisting.netQuantity} · MRP:{' '}
                  {selectedExisting.mrp} · Last inspected {selectedExisting.lastInspectionDate ?? 'never'}
                </p>
              )}
            </div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="flex flex-col gap-2">
                <Label htmlFor="brand">Brand Name</Label>
                <Input id="brand" value={value.brand} onChange={(e) => onChange({ brand: e.target.value })} placeholder="e.g. ABC Foods" />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="product-name">Product Name</Label>
                <Input
                  id="product-name"
                  value={value.name}
                  onChange={(e) => onChange({ name: e.target.value })}
                  placeholder="e.g. Premium Biscuits 500g"
                />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="category">Category</Label>
                <Input id="category" value={value.category} onChange={(e) => onChange({ category: e.target.value })} placeholder="e.g. Food" />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="manufacturer">Manufacturer</Label>
                <Input
                  id="manufacturer"
                  value={value.manufacturer}
                  onChange={(e) => onChange({ manufacturer: e.target.value })}
                  placeholder="Legal manufacturer name"
                />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="net-qty">Declared Net Quantity</Label>
                <Input id="net-qty" value={value.netQuantity} onChange={(e) => onChange({ netQuantity: e.target.value })} placeholder="e.g. 500 g" />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="mrp">Declared MRP</Label>
                <Input id="mrp" value={value.mrp} onChange={(e) => onChange({ mrp: e.target.value })} placeholder="e.g. ₹199" />
              </div>
              <div className="flex flex-col gap-2 sm:col-span-2">
                <Label htmlFor="batch">Batch Number</Label>
                <Input id="batch" value={value.batchNumber} onChange={(e) => onChange({ batchNumber: e.target.value })} placeholder="e.g. BATCH-09A" />
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Inspection Context</CardTitle>
          <CardDescription>Where and how this inspection is being conducted.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 sm:grid-cols-2">
          <div className="flex flex-col gap-2">
            <Label htmlFor="location">Inspection Location</Label>
            <Input id="location" value={value.location} onChange={(e) => onChange({ location: e.target.value })} placeholder="e.g. Retail Market, Sector 18" />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="inspection-type">Inspection Type</Label>
            <Select value={value.inspectionType} onValueChange={(v) => onChange({ inspectionType: v })}>
              <SelectTrigger id="inspection-type">
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Routine Market Surveillance">Routine Market Surveillance</SelectItem>
                <SelectItem value="Complaint-Based">Complaint-Based</SelectItem>
                <SelectItem value="Follow-up Verification">Follow-up Verification</SelectItem>
                <SelectItem value="Random Sampling">Random Sampling</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex flex-col gap-2 sm:col-span-2">
            <Label htmlFor="remarks">Inspector Remarks (optional)</Label>
            <Textarea
              id="remarks"
              value={value.remarks}
              onChange={(e) => onChange({ remarks: e.target.value })}
              placeholder="Any context worth noting before analysis..."
              rows={3}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
