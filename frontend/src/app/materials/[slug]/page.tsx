import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { getMaterial, getMaterials } from '@/lib/api'

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

  let material
  try {
    material = await getMaterial(slug)
  } catch {
    notFound()
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-green-600">Home</Link>
        {' / '}
        <Link href="/materials" className="hover:text-green-600">Materials</Link>
        {' / '}
        <span className="text-gray-900">{material.name}</span>
      </nav>

      <div className="mb-6">
        {material.category && (
          <span className="text-sm font-medium text-green-700 bg-green-100 px-2 py-1 rounded">
            {material.category}
          </span>
        )}
        <h1 className="text-3xl font-bold text-gray-900 mt-3">{material.name}</h1>
        {material.description && (
          <p className="mt-2 text-gray-600">{material.description}</p>
        )}
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
        <p className="text-amber-800 font-medium">
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
    </div>
  )
}
