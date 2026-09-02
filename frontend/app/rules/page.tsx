'use client'

import { useMemo, useState } from 'react'
import { BookText, Search } from 'lucide-react'
import { AppShell } from '@/components/app-shell/app-shell'
import { PageHeader } from '@/components/page-header'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { rules } from '@/lib/mock-data/rules'
import type { ComplianceRule } from '@/lib/types'
import { cn } from '@/lib/utils'

const SEVERITY_CLASSNAMES: Record<ComplianceRule['severity'], string> = {
  Required: 'border-status-danger/30 text-status-danger',
  Recommended: 'border-status-warning/30 text-status-warning',
  Informational: 'border-status-info/30 text-status-info',
}

export default function RulesPage() {
  const [query, setQuery] = useState('')
  const [severityFilter, setSeverityFilter] = useState<string>('all')
  const [selected, setSelected] = useState<ComplianceRule | null>(null)

  const filtered = useMemo(() => {
    return rules.filter((rule) => {
      const matchesQuery = `${rule.name} ${rule.declaration} ${rule.id}`.toLowerCase().includes(query.toLowerCase())
      const matchesSeverity = severityFilter === 'all' || rule.severity === severityFilter
      return matchesQuery && matchesSeverity
    })
  }, [query, severityFilter])

  return (
    <AppShell title="Compliance Rules">
      <PageHeader
        title="Compliance Rules"
        description="Legal Metrology (Packaged Commodities) Rules used by the AI engine to validate package declarations."
      />

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="relative max-w-sm flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-text-secondary" />
          <Input
            placeholder="Search rules by name or declaration"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={severityFilter} onValueChange={setSeverityFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filter by severity" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Severities</SelectItem>
            <SelectItem value="Required">Required</SelectItem>
            <SelectItem value="Recommended">Recommended</SelectItem>
            <SelectItem value="Informational">Informational</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="overflow-hidden rounded-lg border border-border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Rule</TableHead>
              <TableHead>Declaration</TableHead>
              <TableHead>Severity</TableHead>
              <TableHead>Version</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Updated</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="py-10 text-center text-sm text-text-secondary">
                  <div className="flex flex-col items-center gap-2">
                    <BookText className="size-6 text-text-secondary/60" />
                    No rules match your filters.
                  </div>
                </TableCell>
              </TableRow>
            )}
            {filtered.map((rule) => (
              <TableRow
                key={rule.id}
                className="cursor-pointer hover:bg-muted/40"
                onClick={() => setSelected(rule)}
              >
                <TableCell>
                  <div className="flex flex-col">
                    <span className="font-medium text-foreground">{rule.name}</span>
                    <span className="text-xs text-text-secondary">{rule.id}</span>
                  </div>
                </TableCell>
                <TableCell className="text-sm text-text-secondary">{rule.declaration}</TableCell>
                <TableCell>
                  <Badge variant="outline" className={SEVERITY_CLASSNAMES[rule.severity]}>
                    {rule.severity}
                  </Badge>
                </TableCell>
                <TableCell className="text-sm text-text-secondary">{rule.version}</TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={cn(rule.status === 'Deprecated' && 'text-text-secondary')}
                  >
                    {rule.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-sm text-text-secondary">{rule.lastUpdated}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Sheet open={Boolean(selected)} onOpenChange={(open) => !open && setSelected(null)}>
        <SheetContent className="overflow-y-auto sm:max-w-lg">
          {selected && (
            <>
              <SheetHeader>
                <SheetTitle>{selected.name}</SheetTitle>
                <SheetDescription>{selected.id} · Version {selected.version}</SheetDescription>
              </SheetHeader>
              <div className="flex flex-col gap-5 px-4 pb-6">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="outline" className={SEVERITY_CLASSNAMES[selected.severity]}>
                    {selected.severity}
                  </Badge>
                  <Badge variant="outline" className={cn(selected.status === 'Deprecated' && 'text-text-secondary')}>
                    {selected.status}
                  </Badge>
                  <Badge variant="outline">{selected.validationType}</Badge>
                </div>

                <div>
                  <h4 className="mb-1 text-xs font-semibold uppercase tracking-wide text-text-secondary">
                    Description
                  </h4>
                  <p className="text-sm leading-relaxed text-foreground">{selected.description}</p>
                </div>

                <div>
                  <h4 className="mb-1 text-xs font-semibold uppercase tracking-wide text-text-secondary">
                    How the AI Checks This
                  </h4>
                  <p className="text-sm leading-relaxed text-foreground">{selected.howChecked}</p>
                </div>

                <div>
                  <h4 className="mb-1 text-xs font-semibold uppercase tracking-wide text-text-secondary">
                    Evidence Required
                  </h4>
                  <p className="text-sm leading-relaxed text-foreground">{selected.evidenceRequired}</p>
                </div>

                <div>
                  <h4 className="mb-1 text-xs font-semibold uppercase tracking-wide text-text-secondary">
                    Applicability
                  </h4>
                  <p className="text-sm leading-relaxed text-foreground">{selected.applicability}</p>
                </div>

                <p className="text-xs text-text-secondary">Last updated {selected.lastUpdated}</p>
              </div>
            </>
          )}
        </SheetContent>
      </Sheet>
    </AppShell>
  )
}
