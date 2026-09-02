import Link from 'next/link'
import { Icon } from '@/components/icon'

export function CtaSection() {
  return (
    <section className="border-b border-[#E2E8F0] bg-[#F7FAFC]">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:py-20">
        <div className="flex flex-col items-center gap-6 rounded-lg border border-[#E2E8F0] bg-white px-6 py-12 text-center shadow-sm">
          <span className="flex h-12 w-12 items-center justify-center rounded-[6px] bg-[#00193C] text-white">
            <Icon name="frame_inspect" className="text-[24px]" />
          </span>
          <h2 className="text-balance text-2xl font-semibold tracking-tight text-[#1A202C] sm:text-3xl">
            Start Your Next Inspection
          </h2>
          <p className="max-w-xl text-pretty text-[15px] leading-relaxed text-[#4A5568]">
            Bring AI-assisted analysis into your compliance workflow — with
            evidence, transparency, and the inspector always in control.
          </p>
          <Link
            href="/inspections/new"
            className="inline-flex h-11 items-center justify-center gap-2 rounded-[6px] bg-[#00193C] px-8 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-[#002D62]"
          >
            Get Started
            <Icon name="arrow_forward" className="text-[18px]" />
          </Link>
        </div>
      </div>
    </section>
  )
}
