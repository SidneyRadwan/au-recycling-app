import type { Council, CouncilDetail, Material, Page, SearchResult } from '@/types'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8080'
const API_PREFIX = `${API_BASE}/api/v1`

async function fetcher<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_PREFIX}${path}`
  const res = await fetch(url, options)

  if (!res.ok) {
    throw Object.assign(
      new Error(`API error ${res.status}: ${res.statusText} for ${url}`),
      { status: res.status },
    )
  }

  return res.json() as Promise<T>
}

export async function getCouncils(
  state?: string,
  page = 0,
  size = 20,
): Promise<Page<Council>> {
  const params = new URLSearchParams({ page: String(page), size: String(size) })
  if (state) params.set('state', state)
  return fetcher<Page<Council>>(`/councils?${params.toString()}`, {
    next: { revalidate: 3600 },
  })
}

export async function getCouncil(slug: string): Promise<CouncilDetail> {
  return fetcher<CouncilDetail>(`/councils/${slug}`, {
    next: { revalidate: 3600 },
  })
}

export async function getMaterials(category?: string): Promise<Material[]> {
  const params = new URLSearchParams()
  if (category) params.set('category', category)
  const query = params.toString() ? `?${params.toString()}` : ''
  return fetcher<Material[]>(`/materials${query}`, {
    next: { revalidate: 3600 },
  })
}

export async function getMaterial(slug: string): Promise<Material> {
  return fetcher<Material>(`/materials/${slug}`, {
    next: { revalidate: 3600 },
  })
}

export async function search(q: string): Promise<SearchResult> {
  const params = new URLSearchParams({ q })
  return fetcher<SearchResult>(`/search?${params.toString()}`, {
    cache: 'no-store',
  })
}
