export interface Council {
  id: number
  name: string
  slug: string
  state: string
  website: string | null
  recyclingInfoUrl: string | null
  description: string | null
}

export interface Material {
  id: number
  name: string
  slug: string
  category: string | null
  description: string | null
}

export interface CouncilMaterial {
  materialId: number
  materialName: string
  materialSlug: string
  binType: BinType
  instructions: string | null
  notes: string | null
}

export type BinType =
  | 'RECYCLING'
  | 'GENERAL_WASTE'
  | 'GREEN_WASTE'
  | 'SOFT_PLASTICS'
  | 'SPECIAL_DROP_OFF'
  | 'NOT_ACCEPTED'

export interface CouncilDetail extends Council {
  materialsByBinType: Record<BinType, CouncilMaterial[]>
}

export interface SearchResult {
  councils: Array<{ id: number; name: string; slug: string; state: string }>
  suburbs: Array<{ name: string; postcode: string; councilSlug: string; councilName: string }>
  materials: Array<{ id: number; name: string; slug: string; category: string | null }>
}

export interface Page<T> {
  content: T[]
  totalElements: number
  totalPages: number
  number: number
  size: number
}
