import Link from 'next/link'
import { cn } from '@/lib/utils'
import type { BinType, CouncilMaterial } from '@/types'

interface BinTypeConfig {
  label: string
  emoji: string
  containerClass: string
  headerClass: string
  badgeClass: string
}

export const BIN_TYPE_CONFIG: Record<BinType, BinTypeConfig> = {
  RECYCLING: {
    label: 'Yellow Lid — Recycling Bin',
    emoji: '🟡',
    containerClass: 'border-bin-recycling-border bg-bin-recycling-bg',
    headerClass: 'bg-bin-recycling-header text-bin-recycling-text',
    badgeClass: 'bg-bin-recycling-header text-bin-recycling-text border-bin-recycling-border hover:bg-bin-recycling-hover',
  },
  GENERAL_WASTE: {
    label: 'Red Lid — General Waste',
    emoji: '🔴',
    containerClass: 'border-bin-general-border bg-bin-general-bg',
    headerClass: 'bg-bin-general-header text-bin-general-text',
    badgeClass: 'bg-bin-general-header text-bin-general-text border-bin-general-border hover:bg-bin-general-hover',
  },
  GREEN_WASTE: {
    label: 'Green Lid — Green Waste',
    emoji: '🟢',
    containerClass: 'border-bin-green-border bg-bin-green-bg',
    headerClass: 'bg-bin-green-header text-bin-green-text',
    badgeClass: 'bg-bin-green-header text-bin-green-text border-bin-green-border hover:bg-bin-green-hover',
  },
  SOFT_PLASTICS: {
    label: 'Soft Plastics',
    emoji: '🟣',
    containerClass: 'border-bin-soft-border bg-bin-soft-bg',
    headerClass: 'bg-bin-soft-header text-bin-soft-text',
    badgeClass: 'bg-bin-soft-header text-bin-soft-text border-bin-soft-border hover:bg-bin-soft-hover',
  },
  SPECIAL_DROP_OFF: {
    label: 'Special Drop-off',
    emoji: '🔵',
    containerClass: 'border-bin-special-border bg-bin-special-bg',
    headerClass: 'bg-bin-special-header text-bin-special-text',
    badgeClass: 'bg-bin-special-header text-bin-special-text border-bin-special-border hover:bg-bin-special-hover',
  },
  NOT_ACCEPTED: {
    label: 'Not Accepted',
    emoji: '⛔',
    containerClass: 'border-bin-none-border bg-bin-none-bg',
    headerClass: 'bg-bin-none-header text-bin-none-text',
    badgeClass: 'bg-bin-none-header text-bin-none-text border-bin-none-border hover:bg-bin-none-hover',
  },
}

interface MaterialBadgeProps {
  material: CouncilMaterial
  binType: BinType
}

export function MaterialBadge({ material, binType }: MaterialBadgeProps) {
  const config = BIN_TYPE_CONFIG[binType]
  return (
    <Link
      href={`/materials/${material.materialSlug}`}
      className={cn(
        'inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium transition-colors',
        config.badgeClass,
      )}
      title={material.instructions ?? undefined}
    >
      {material.materialName}
    </Link>
  )
}

interface BinSectionProps {
  binType: BinType
  materials: CouncilMaterial[]
}

export function BinSection({ binType, materials }: BinSectionProps) {
  if (materials.length === 0) return null
  const config = BIN_TYPE_CONFIG[binType]

  return (
    <div className={cn('rounded-lg border overflow-hidden', config.containerClass)}>
      <div className={cn('px-4 py-3 font-semibold text-sm', config.headerClass)}>
        <span className="mr-2" aria-hidden="true">{config.emoji}</span>
        {config.label}
        <span className="ml-2 font-normal opacity-70">({materials.length} items)</span>
      </div>
      <div className="p-4 flex flex-wrap gap-2">
        {materials.map((m) => (
          <MaterialBadge key={m.materialId} material={m} binType={binType} />
        ))}
      </div>
    </div>
  )
}
