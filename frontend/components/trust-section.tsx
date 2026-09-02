import { Icon } from '@/components/icon'

const points = [
  {
    icon: 'auto_awesome',
    title: 'AI surfaces potential findings',
    text: 'The system highlights possible discrepancies and the evidence behind them.',
  },
  {
    icon: 'gavel',
    title: 'Inspectors make the determination',
    text: 'No legal conclusion is issued automatically — a qualified inspector decides.',
  },
  {
    icon: 'history_edu',
    title: 'Every decision is auditable',
    text: 'Findings, overrides, and outcomes are recorded with their supporting evidence.',
  },
]

export function TrustSection() {
  return (
    <section id="trust" className="bg-[#00193C] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:py-24">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:items-center">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-white/70">
              <Icon name="balance" className="text-[16px]" />
              Human-in-the-loop
            </span>
            <h2 className="mt-6 text-balance text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
              AI Assists. Inspectors Decide.
            </h2>
            <p className="mt-5 max-w-lg text-pretty text-[15px] leading-relaxed text-white/70">
              MetrologyAI provides potential findings and supporting evidence to
              assist inspectors in their work. It does not make final legal
              determinations. Authority — and accountability — remains with the
              inspector at every stage.
            </p>
          </div>

          <div className="space-y-3">
            {points.map((p) => (
              <div
                key={p.title}
                className="flex items-start gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-5"
              >
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[6px] bg-white/10 text-white">
                  <Icon name={p.icon} className="text-[20px]" />
                </span>
                <div>
                  <h3 className="text-[15px] font-semibold text-white">
                    {p.title}
                  </h3>
                  <p className="mt-1 text-[13px] leading-relaxed text-white/65">
                    {p.text}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
