import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { getMaterial, getMaterials } from '@/lib/api'
import AdUnit from '@/components/ui/ad-unit'
import { ErrorState } from '@/components/ui/error-state'

export const dynamicParams = true

export async function generateStaticParams() {
  try {
    const materials = await getMaterials()
    return materials.map((m) => ({ slug: m.slug }))
  } catch {
    return []
  }
}

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  try {
    const material = await getMaterial(slug)
    return {
      title: `Can I Recycle ${material.name}? | Australia Recycling`,
      description: material.description ?? `Find out how to recycle or dispose of ${material.name} in Australia.`,
    }
  } catch {
    return { title: 'Material Not Found | Australia Recycling' }
  }
}

export default async function MaterialPage({ params }: Props) {
  const { slug } = await params

  let material: Awaited<ReturnType<typeof getMaterial>>
  try {
    material = await getMaterial(slug)
  } catch (e) {
    if ((e as { status?: number }).status === 404) notFound()
    return <ErrorState />
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-muted-foreground mb-6">
        <Link href="/" className="hover:text-green-600">Home</Link>
        {' / '}
        <Link href="/materials" className="hover:text-green-600">Materials</Link>
        {' / '}
        <span className="text-foreground">{material.name}</span>
      </nav>

      <div className="mb-6">
        {material.category && (
          <span className="text-sm font-medium text-primary bg-primary/10 px-2 py-1 rounded">
            {material.category}
          </span>
        )}
        <h1 className="text-3xl font-bold text-foreground mt-3">{material.name}</h1>
        {material.description && (
          <p className="mt-2 text-muted-foreground">{material.description}</p>
        )}
      </div>

      <div className="bg-warning-bg border border-warning-border rounded-xl p-6">
        <p className="text-warning-text font-medium">
          Recycling rules vary by council. Search your council above to see specific guidelines for your area.
        </p>
      </div>

      <div className="mt-8">
        <Link
          href="/councils"
          className="inline-flex items-center px-5 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
        >
          Find your council →
        </Link>
      </div>

      {/* Ad unit — below the CTA, after core content */}
      <div className="mt-8 border-t">
        <AdUnit size="rectangle" />
      </div>
    </div>
  )
}
