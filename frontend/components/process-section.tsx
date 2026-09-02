import { Icon } from '@/components/icon'

const steps = [
  {
    num: '01',
    title: 'Capture Evidence',
    icon: 'photo_camera',
    text: 'Upload or capture a clear image of the packaged commodity and its declarations.',
  },
  {
    num: '02',
    title: 'Extract Declarations',
    icon: 'document_scanner',
    text: 'OCR extracts net quantity, MRP, dates, and mandatory declarations from the label.',
  },
  {
    num: '03',
    title: 'Analyze Compliance',
    icon: 'rule',
    text: 'AI checks extracted data against Legal Metrology rules and flags potential findings.',
  },
  {
    num: '04',
    title: 'Inspector Verification',
    icon: 'verified_user',
    text: 'The inspector reviews evidence and findings, then records the final decision.',
  },
]

export function ProcessSection() {
  return (
    <section id="process" className="border-b border-[#E2E8F0]">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:py-20">
        <div className="max-w-2xl">
          <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-[#002D62]">
            The workflow
          </p>
          <h2 className="mt-3 text-balance text-2xl font-semibold tracking-tight text-[#1A202C] sm:text-3xl">
            From Package Image to Verified Inspection
          </h2>
          <p className="mt-3 text-[15px] leading-relaxed text-[#4A5568]">
            A structured, evidence-first pipeline that keeps every step
            transparent and the inspector firmly in control.
          </p>
        </div>

        <ol className="mt-12 grid grid-cols-1 gap-px overflow-hidden rounded-lg border border-[#E2E8F0] bg-[#E2E8F0] sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step) => (
            <li key={step.num} className="group bg-white p-6">
              <div className="flex items-center justify-between">
                <span className="flex h-10 w-10 items-center justify-center rounded-[6px] border border-[#E2E8F0] bg-[#F7FAFC] text-[#00193C]">
                  <Icon name={step.icon} className="text-[22px]" />
                </span>
                <span className="text-[13px] font-semibold tabular-nums text-[#CBD5E0]">
                  {step.num}
                </span>
              </div>
              <h3 className="mt-5 text-[15px] font-semibold text-[#1A202C]">
                {step.title}
              </h3>
              <p className="mt-2 text-[13px] leading-relaxed text-[#4A5568]">
                {step.text}
              </p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
