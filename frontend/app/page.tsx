import { SiteHeader } from '@/components/site-header'
import { Hero } from '@/components/hero'
import { ProcessSection } from '@/components/process-section'
import { CapabilitiesSection } from '@/components/capabilities-section'
import { TrustSection } from '@/components/trust-section'
import { CtaSection } from '@/components/cta-section'
import { SiteFooter } from '@/components/site-footer'

export default function Page() {
  return (
    <div className="min-h-screen bg-[#F7FAFC] text-[#1A202C]">
      <SiteHeader />
      <main>
        <Hero />
        <ProcessSection />
        <CapabilitiesSection />
        <TrustSection />
        <CtaSection />
      </main>
      <SiteFooter />
    </div>
  )
}
