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
    containerClass: 'border-yellow-200 bg-yellow-50',
    headerClass: 'bg-yellow-100 text-yellow-900',
    badgeClass: 'bg-yellow-100 text-yellow-800 border-yellow-200 hover:bg-yellow-200',
  },
  GENERAL_WASTE: {
    label: 'Red Lid — General Waste',
    emoji: '🔴',
    containerClass: 'border-red-200 bg-red-50',
    headerClass: 'bg-red-100 text-red-900',
    badgeClass: 'bg-red-100 text-red-800 border-red-200 hover:bg-red-200',
  },
  GREEN_WASTE: {
    label: 'Green Lid — Green Waste',
    emoji: '🟢',
    containerClass: 'border-green-200 bg-green-50',
    headerClass: 'bg-green-100 text-green-900',
    badgeClass: 'bg-green-100 text-green-800 border-green-200 hover:bg-green-200',
  },
  SOFT_PLASTICS: {
    label: 'Soft Plastics',
    emoji: '🟣',
    containerClass: 'border-purple-200 bg-purple-50',
    headerClass: 'bg-purple-100 text-purple-900',
    badgeClass: 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200',
  },
  SPECIAL_DROP_OFF: {
    label: 'Special Drop-off',
    emoji: '🔵',
    containerClass: 'border-blue-200 bg-blue-50',
    headerClass: 'bg-blue-100 text-blue-900',
    badgeClass: 'bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-200',
  },
  NOT_ACCEPTED: {
    label: 'Not Accepted',
    emoji: '⛔',
    containerClass: 'border-gray-200 bg-gray-50',
    headerClass: 'bg-gray-100 text-gray-900',
    badgeClass: 'bg-gray-100 text-gray-700 border-gray-200 hover:bg-gray-200',
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
