import { Metadata } from 'next'
import Link from 'next/link'
import { getMaterials } from '@/lib/api'

export const metadata: Metadata = {
  title: 'What Can I Recycle? | Australia Recycling',
  description: 'Find out how to dispose of common household items — what goes in the recycling bin, general waste, green waste, or special drop-off.',
}

const CATEGORIES = [
  'Paper & Cardboard',
  'Plastics',
  'Glass',
  'Metals',
  'Organic',
  'Hazardous',
  'Electronics',
  'Textiles',
  'Sanitary',
]

interface Props {
  searchParams: Promise<{ category?: string }>
}

export default async function MaterialsPage({ searchParams }: Props) {
  const { category } = await searchParams
  const materials = await getMaterials(category)

  const grouped = materials.reduce<Record<string, typeof materials>>((acc, m) => {
    const cat = m.category ?? 'Other'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(m)
    return acc
  }, {})

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">What Can I Recycle?</h1>
      <p className="text-gray-600 mb-8">
        Browse common household items and find out how to dispose of them responsibly.
      </p>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2 mb-8">
        <a
          href="/materials"
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            !category ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          All
        </a>
        {CATEGORIES.map((c) => (
          <a
            key={c}
            href={`/materials?category=${encodeURIComponent(c)}`}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              category === c
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {c}
          </a>
        ))}
      </div>

      {/* Materials grouped by category */}
      <div className="space-y-10">
        {Object.entries(grouped).sort(([a], [b]) => a.localeCompare(b)).map(([cat, items]) => (
          <section key={cat}>
            <h2 className="text-xl font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">
              {cat}
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {items.map((material) => (
                <Link
                  key={material.id}
                  href={`/materials/${material.slug}`}
                  className="flex items-start gap-3 p-4 rounded-lg border border-gray-200 hover:border-green-300 hover:bg-green-50 transition-colors"
                >
                  <div>
                    <p className="font-medium text-gray-900">{material.name}</p>
                    {material.description && (
                      <p className="text-sm text-gray-500 mt-0.5 line-clamp-2">{material.description}</p>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
