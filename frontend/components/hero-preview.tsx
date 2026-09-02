import Image from 'next/image'
import { Icon } from '@/components/icon'

const declarations = [
  { label: 'Net Quantity', value: '500 g', status: 'ok' },
  { label: 'MRP (incl. taxes)', value: '₹ 145.00', status: 'ok' },
  { label: 'Mfg. Date', value: '02 / 2026', status: 'ok' },
  { label: 'Consumer Care', value: 'Not detected', status: 'review' },
]

export function HeroPreview() {
  return (
    <div className="relative">
      {/* App window */}
      <div className="overflow-hidden rounded-lg border border-[#E2E8F0] bg-white shadow-[0_20px_50px_-24px_rgba(0,25,60,0.35)]">
        {/* Window title bar */}
        <div className="flex items-center justify-between border-b border-[#E2E8F0] bg-[#F7FAFC] px-4 py-3">
          <div className="flex items-center gap-2">
            <Icon name="document_scanner" className="text-[18px] text-[#00193C]" />
            <span className="text-[13px] font-semibold text-[#1A202C]">
              Inspection #INS-2048
            </span>
          </div>
          <span className="inline-flex items-center gap-1.5 rounded-full border border-[#E2E8F0] bg-white px-2.5 py-1 text-[11px] font-medium text-[#4A5568]">
            <span className="h-1.5 w-1.5 rounded-full bg-[#00193C]" />
            Analyzing
          </span>
        </div>

        <div className="grid grid-cols-1 gap-0 sm:grid-cols-5">
          {/* Image with OCR boxes */}
          <div className="relative border-b border-[#E2E8F0] bg-[#F7FAFC] p-4 sm:col-span-3 sm:border-b-0 sm:border-r">
            <div className="relative aspect-4/3 overflow-hidden rounded-[6px] border border-[#E2E8F0] bg-white">
              <Image
                src="/packaged-product.png"
                alt="Packaged commodity being analyzed by MetrologyAI"
                fill
                className="object-cover"
                sizes="(max-width: 640px) 100vw, 40vw"
                priority
              />

              {/* OCR detection boxes */}
              <div className="absolute left-[14%] top-[30%] h-[11%] w-[42%] rounded-[3px] border-2 border-[#00193C]/80 bg-[#00193C]/5">
                <span className="absolute -top-[18px] left-0 rounded-t-[3px] bg-[#00193C] px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-white">
                  Net Qty
                </span>
              </div>
              <div className="absolute left-[16%] top-[52%] h-[10%] w-[34%] rounded-[3px] border-2 border-[#00193C]/80 bg-[#00193C]/5">
                <span className="absolute -top-[18px] left-0 rounded-t-[3px] bg-[#00193C] px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-white">
                  MRP
                </span>
              </div>
              <div className="absolute left-[52%] top-[68%] h-[9%] w-[36%] rounded-[3px] border-2 border-dashed border-[#B7791F] bg-[#B7791F]/5">
                <span className="absolute -top-[18px] left-0 rounded-t-[3px] bg-[#B7791F] px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-white">
                  Review
                </span>
              </div>
            </div>

            {/* AI-Assisted score */}
            <div className="mt-4 flex items-center justify-between rounded-[6px] border border-[#E2E8F0] bg-white px-3 py-2.5">
              <div className="flex items-center gap-2">
                <Icon name="auto_awesome" filled className="text-[18px] text-[#00193C]" />
                <span className="text-[12px] font-medium text-[#4A5568]">
                  AI-Assisted Score
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-24 overflow-hidden rounded-full bg-[#E2E8F0]">
                  <div className="h-full w-[86%] rounded-full bg-[#00193C]" />
                </div>
                <span className="text-[13px] font-semibold tabular-nums text-[#00193C]">
                  86%
                </span>
              </div>
            </div>
          </div>

          {/* Extracted declarations + compliance */}
          <div className="flex flex-col p-4 sm:col-span-2">
            <p className="mb-3 text-[11px] font-semibold uppercase tracking-wider text-[#4A5568]">
              Extracted Declarations
            </p>
            <ul className="space-y-2">
              {declarations.map((d) => (
                <li
                  key={d.label}
                  className="flex items-center justify-between rounded-[6px] border border-[#E2E8F0] bg-white px-3 py-2"
                >
                  <div className="min-w-0">
                    <p className="truncate text-[11px] text-[#4A5568]">{d.label}</p>
                    <p
                      className={`truncate text-[13px] font-semibold ${
                        d.status === 'review' ? 'text-[#B7791F]' : 'text-[#1A202C]'
                      }`}
                    >
                      {d.value}
                    </p>
                  </div>
                  <Icon
                    name={d.status === 'review' ? 'error' : 'check_circle'}
                    filled
                    className={`shrink-0 text-[18px] ${
                      d.status === 'review' ? 'text-[#B7791F]' : 'text-[#2F855A]'
                    }`}
                  />
                </li>
              ))}
            </ul>

            {/* Requires human review banner */}
            <div className="mt-4 flex items-start gap-2.5 rounded-[6px] border border-[#B7791F]/30 bg-[#B7791F]/8 px-3 py-2.5">
              <Icon
                name="gavel"
                className="mt-0.5 shrink-0 text-[18px] text-[#B7791F]"
              />
              <div>
                <p className="text-[12px] font-semibold text-[#1A202C]">
                  Requires Human Review
                </p>
                <p className="mt-0.5 text-[11px] leading-relaxed text-[#4A5568]">
                  Final compliance decision rests with the inspector.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
