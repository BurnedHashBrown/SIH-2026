'use client'

import Link from 'next/link'
import { Icon } from '@/components/icon'

export function SiteHeader() {
  function scrollToCapabilities(e: React.MouseEvent) {
    e.preventDefault()
    document
      .getElementById('capabilities')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <header className="sticky top-0 z-50 border-b border-[#E2E8F0] bg-[#F7FAFC]/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-[6px] bg-[#00193C] text-white">
            <Icon name="verified" filled className="text-[20px]" />
          </span>
          <span className="text-[15px] font-semibold tracking-tight text-[#1A202C]">
            MetrologyAI
          </span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          <a
            href="#process"
            className="text-sm font-medium text-[#4A5568] transition-colors hover:text-[#00193C]"
          >
            How it works
          </a>
          <a
            href="#capabilities"
            onClick={scrollToCapabilities}
            className="text-sm font-medium text-[#4A5568] transition-colors hover:text-[#00193C]"
          >
            Platform
          </a>
          <a
            href="#trust"
            className="text-sm font-medium text-[#4A5568] transition-colors hover:text-[#00193C]"
          >
            Trust
          </a>
        </nav>

      </div>
    </header>
  )
}
