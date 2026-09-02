'use client'

import Link from 'next/link'
import { Icon } from '@/components/icon'
import { HeroPreview } from '@/components/hero-preview'

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-[#E2E8F0]">
      {/* subtle grid backdrop */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 opacity-[0.4]"
        style={{
          backgroundImage:
            'linear-gradient(#E2E8F0 1px, transparent 1px), linear-gradient(90deg, #E2E8F0 1px, transparent 1px)',
          backgroundSize: '64px 64px',
          maskImage:
            'radial-gradient(ellipse 80% 60% at 50% 0%, #000 40%, transparent 100%)',
        }}
      />

      <div className="relative mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-6 py-16 lg:grid-cols-2 lg:py-24">
        {/* Copy */}
        <div>
          <span className="inline-flex items-center gap-2 rounded-full border border-[#E2E8F0] bg-white px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[#002D62]">
            <span className="h-1.5 w-1.5 rounded-full bg-[#002D62]" />
            AI-Assisted Legal Metrology
          </span>

          <h1 className="mt-6 text-balance text-4xl font-semibold leading-[1.08] tracking-tight text-[#1A202C] sm:text-5xl lg:text-[3.4rem]">
            Smarter Inspections.
            <br />
            <span className="text-[#00193C]">Stronger Compliance.</span>
          </h1>

          <p className="mt-6 max-w-xl text-pretty text-[15px] leading-relaxed text-[#4A5568] sm:text-base">
            MetrologyAI helps inspectors analyze packaged commodity labels using
            AI-assisted image analysis, OCR, and compliance checks — while
            keeping the final decision with the inspector.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/login"
              className="inline-flex h-11 items-center justify-center gap-2 rounded-[6px] bg-[#00193C] px-6 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-[#002D62]"
            >
              <Icon name="login" className="text-[20px]" />
              Log in
            </Link>
            <Link
              href="/signup"
              className="inline-flex h-11 items-center justify-center gap-2 rounded-[6px] border border-[#E2E8F0] bg-white px-6 text-sm font-semibold text-[#1A202C] transition-colors hover:border-[#CBD5E0] hover:bg-[#F7FAFC]"
            >
              <Icon name="person_add" className="text-[18px]" />
              Sign up
            </Link>
          </div>

          <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-[12px] text-[#4A5568]">
            <span className="inline-flex items-center gap-1.5">
              <Icon name="check_circle" filled className="text-[16px] text-[#2F855A]" />
              Evidence-based
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Icon name="check_circle" filled className="text-[16px] text-[#2F855A]" />
              Auditable trail
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Icon name="check_circle" filled className="text-[16px] text-[#2F855A]" />
              Inspector-controlled
            </span>
          </div>
        </div>

        {/* Visual */}
        <div className="lg:pl-4">
          <HeroPreview />
        </div>
      </div>
    </section>
  )
}
