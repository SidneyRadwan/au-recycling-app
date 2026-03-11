import type { MetadataRoute } from 'next'
import { getCouncils, getMaterials } from '@/lib/api'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://australiarecycling.com.au'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: SITE_URL,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${SITE_URL}/councils`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${SITE_URL}/materials`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
  ]

  let councilRoutes: MetadataRoute.Sitemap = []
  let materialRoutes: MetadataRoute.Sitemap = []

  try {
    // Fetch first page of councils (up to 100)
    const councilsPage = await getCouncils(undefined, 0, 100)
    councilRoutes = councilsPage.content.map((council) => ({
      url: `${SITE_URL}/councils/${council.slug}`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    }))
  } catch {
    // Silently fall back if API unavailable
  }

  try {
    const materials = await getMaterials()
    materialRoutes = materials.map((material) => ({
      url: `${SITE_URL}/materials/${material.slug}`,
      lastModified: new Date(),
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    }))
  } catch {
    // Silently fall back if API unavailable
  }

  return [...staticRoutes, ...councilRoutes, ...materialRoutes]
}
