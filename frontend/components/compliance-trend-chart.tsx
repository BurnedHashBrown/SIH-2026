'use client'

import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from 'recharts'
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from '@/components/ui/chart'

const chartConfig = {
  score: {
    label: 'Avg. Compliance Score',
    color: 'var(--chart-1)',
  },
} satisfies ChartConfig

export function ComplianceTrendChart({ data }: { data: { date: string; score: number }[] }) {
  return (
    <ChartContainer config={chartConfig} className="h-64 w-full">
      <AreaChart data={data} margin={{ left: -20, right: 8, top: 8, bottom: 0 }}>
        <defs>
          <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="var(--color-score)" stopOpacity={0.35} />
            <stop offset="95%" stopColor="var(--color-score)" stopOpacity={0.02} />
          </linearGradient>
        </defs>
        <CartesianGrid vertical={false} stroke="var(--border-subtle)" />
        <XAxis dataKey="date" tickLine={false} axisLine={false} tickMargin={8} className="text-xs" />
        <YAxis domain={[0, 100]} tickLine={false} axisLine={false} tickMargin={8} className="text-xs" width={40} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Area
          dataKey="score"
          type="monotone"
          stroke="var(--color-score)"
          fill="url(#scoreFill)"
          strokeWidth={2}
        />
      </AreaChart>
    </ChartContainer>
  )
}
