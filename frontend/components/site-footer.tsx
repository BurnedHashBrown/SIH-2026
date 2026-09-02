import { Icon } from '@/components/icon'

export function SiteFooter() {
  return (
    <footer className="bg-[#F7FAFC]">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-4 px-6 py-10 text-center sm:flex-row sm:justify-between sm:text-left">
        <div className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-[6px] bg-[#00193C] text-white">
            <Icon name="verified" filled className="text-[20px]" />
          </span>
          <div>
            <p className="text-[14px] font-semibold tracking-tight text-[#1A202C]">
              MetrologyAI
            </p>
            <p className="text-[12px] text-[#4A5568]">
              AI-assisted analysis • Human-verified decisions
            </p>
          </div>
        </div>
        <p className="text-[12px] text-[#4A5568]">
          © {new Date().getFullYear()} MetrologyAI. All rights reserved.
        </p>
      </div>
    </footer>
  )
}
