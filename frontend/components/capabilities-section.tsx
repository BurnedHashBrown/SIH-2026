import { Icon } from '@/components/icon'

const capabilities = [
  {
    icon: 'image_search',
    title: 'AI-Assisted Image Analysis',
    text: 'Detect labels, packaging regions, and declaration zones from product imagery.',
  },
  {
    icon: 'document_scanner',
    title: 'OCR & Declaration Extraction',
    text: 'Read net quantity, MRP, manufacturer, and date declarations with confidence scoring.',
  },
  {
    icon: 'rule',
    title: 'Compliance Rule Checks',
    text: 'Compare extracted declarations against configurable Legal Metrology requirements.',
  },
  {
    icon: 'fact_check',
    title: 'Evidence-Based Review',
    text: 'Every potential finding is linked to the exact image region and extracted text.',
  },
  {
    icon: 'verified_user',
    title: 'Inspector Verification',
    text: 'Inspectors confirm, override, or dismiss findings — the decision is always theirs.',
  },
  {
    icon: 'description',
    title: 'Inspection Reports',
    text: 'Generate clear, auditable reports documenting evidence, findings, and outcomes.',
  },
]

export function CapabilitiesSection() {
  return (
    <section id="capabilities" className="scroll-mt-16 border-b border-[#E2E8F0] bg-white">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:py-20">
        <div className="max-w-2xl">
          <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-[#002D62]">
            Platform capabilities
          </p>
          <h2 className="mt-3 text-balance text-2xl font-semibold tracking-tight text-[#1A202C] sm:text-3xl">
            Purpose-built for compliance workflows
          </h2>
          <p className="mt-3 text-[15px] leading-relaxed text-[#4A5568]">
            Each capability is designed to assist — surfacing evidence and
            findings so inspectors can decide faster and with greater confidence.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.map((cap) => (
            <div
              key={cap.title}
              className="rounded-lg border border-[#E2E8F0] bg-[#F7FAFC] p-6 transition-colors hover:border-[#CBD5E0] hover:bg-white"
            >
              <span className="flex h-11 w-11 items-center justify-center rounded-[6px] bg-[#00193C] text-white">
                <Icon name={cap.icon} className="text-[22px]" />
              </span>
              <h3 className="mt-5 text-[15px] font-semibold text-[#1A202C]">
                {cap.title}
              </h3>
              <p className="mt-2 text-[13px] leading-relaxed text-[#4A5568]">
                {cap.text}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
