import type { CSSProperties } from 'react'

export function Icon({
  name,
  className,
  filled,
  weight,
  style,
}: {
  name: string
  className?: string
  filled?: boolean
  weight?: number
  style?: CSSProperties
}) {
  return (
    <span
      aria-hidden="true"
      className={`material-symbols-outlined select-none ${className ?? ''}`}
      style={{
        fontVariationSettings: `'FILL' ${filled ? 1 : 0}, 'wght' ${weight ?? 400}, 'GRAD' 0, 'opsz' 24`,
        ...style,
      }}
    >
      {name}
    </span>
  )
}
