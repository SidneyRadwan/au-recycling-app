import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { ExternalLink, ChevronRight, MapPin } from 'lucide-react'
import { getCouncil, getCouncils } from '@/lib/api'
import { BinSection, BIN_TYPE_CONFIG } from '@/components/council/MaterialBadge'
import { Button } from '@/components/ui/button'
import { formatState } from '@/lib/utils'
import AdUnit from '@/components/ui/ad-unit'
import { ErrorState } from '@/components/ui/error-state'
import AskAI from '@/components/ai/AskAI'
import type { BinType } from '@/types'

interface Props {
  params: Promise<{ slug: string }>
}

export const dynamicParams = true

export async function generateStaticParams() {
  try {
    const page = await getCouncils(undefined, 0, 1000)
    return page.content.map((c) => ({ slug: c.slug }))
  } catch {
    return []
  }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  try {
    const council = await getCouncil(slug)
    return {
      title: `${council.name} Recycling Guide`,
      description: `Find out what goes in each bin for ${council.name}, ${council.state}. Complete recycling guide covering yellow lid, red lid, green waste, and more.`,
      openGraph: {
        title: `${council.name} Recycling Guide`,
        description: `What can you recycle in ${council.name}? Full bin guide for residents.`,
      },
    }
  } catch {
    return {
      title: 'Council Recycling Guide',
    }
  }
}

const BIN_ORDER: BinType[] = [
  'RECYCLING',
  'GREEN_WASTE',
  'SOFT_PLASTICS',
  'SPECIAL_DROP_OFF',
  'GENERAL_WASTE',
  'NOT_ACCEPTED',
]

export default async function CouncilDetailPage({ params }: Props) {
  const { slug } = await params

  let council: Awaited<ReturnType<typeof getCouncil>>
  try {
    council = await getCouncil(slug)
  } catch (e) {
    if ((e as { status?: number }).status === 404) notFound()
    return <ErrorState />
  }

  const materialsByBinType = council.materialsByBinType ?? {}

  // Build FAQ entries for JSON-LD
  const faqItems = BIN_ORDER.flatMap((binType) => {
    const materials = materialsByBinType[binType] ?? []
    if (materials.length === 0) return []
    const config = BIN_TYPE_CONFIG[binType]
    const names = materials.map((m) => m.materialName).join(', ')
    return [
      {
        '@type': 'Question',
        name: `What goes in the ${config.label} for ${council.name}?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `The following items go in the ${config.label} for ${council.name}: ${names}.`,
        },
      },
    ]
  })

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems,
  }

  const totalMaterials = BIN_ORDER.reduce(
    (sum, bt) => sum + (materialsByBinType[bt]?.length ?? 0),
    0,
  )

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div className="container mx-auto max-w-4xl px-4 py-10">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-1.5 text-sm text-muted-foreground mb-6 flex-wrap">
          <Link href="/" className="hover:text-green-700">Home</Link>
          <ChevronRight className="h-3.5 w-3.5" />
          <Link href="/councils" className="hover:text-green-700">Councils</Link>
          <ChevronRight className="h-3.5 w-3.5" />
          <Link href={`/councils?state=${council.state}`} className="hover:text-green-700">
            {council.state}
          </Link>
          <ChevronRight className="h-3.5 w-3.5" />
          <span className="text-foreground font-medium">{council.name}</span>
        </nav>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h1 className="text-3xl font-bold text-foreground">{council.name}</h1>
              <div className="flex items-center gap-2 mt-2">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <span className="text-muted-foreground">{formatState(council.state)}</span>
                {totalMaterials > 0 && (
                  <>
                    <span className="text-muted-foreground/40">•</span>
                    <span className="text-muted-foreground text-sm">{totalMaterials} items catalogued</span>
                  </>
                )}
              </div>
            </div>

            {council.website && (
              <Button
                asChild
                variant="outline"
                size="sm"
                className="border-green-300 hover:bg-green-50 hover:text-green-700 shrink-0"
              >
                <a href={council.website} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="h-4 w-4 mr-1.5" />
                  Council website
                </a>
              </Button>
            )}
          </div>

          {council.description && (
            <p className="mt-4 text-muted-foreground text-sm leading-relaxed">{council.description}</p>
          )}

          {council.recyclingInfoUrl && (
            <a
              href={council.recyclingInfoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 mt-3 text-sm text-green-600 hover:text-green-800 hover:underline"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              View official recycling information
            </a>
          )}
        </div>

        {/* Bin sections */}
        {totalMaterials > 0 ? (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-foreground">What goes in each bin</h2>
            {BIN_ORDER.map((binType) => {
              const materials = materialsByBinType[binType] ?? []
              return (
                <BinSection key={binType} binType={binType} materials={materials} />
              )
            })}
          </div>
        ) : (
          <div className="rounded-lg border border-dashed border-border p-10 text-center text-muted-foreground">
            <div className="text-3xl mb-3" aria-hidden="true">📋</div>
            <p className="font-medium">No recycling data yet</p>
            <p className="text-sm mt-1">
              We&apos;re still gathering data for this council.
              {council.recyclingInfoUrl && (
                <>
                  {' '}
                  Check the{' '}
                  <a
                    href={council.recyclingInfoUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-green-600 hover:underline"
                  >
                    official council website
                  </a>{' '}
                  in the meantime.
                </>
              )}
            </p>
          </div>
        )}

        {/* AI chat — ask about this council */}
        <div className="mt-10 rounded-xl border border-purple-100 bg-purple-50/50 dark:bg-purple-950/20 dark:border-purple-900 p-6">
          <div className="flex items-center gap-2 mb-3">
            <span aria-hidden="true" className="text-lg">✨</span>
            <h2 className="text-base font-semibold text-foreground">
              Ask AI about {council.name}
            </h2>
          </div>
          <p className="text-sm text-muted-foreground mb-4">
            Ask natural language recycling questions — our AI uses council-specific data to answer.
          </p>
          <AskAI councilName={council.name} />
        </div>

        {/* Ad unit — below fold, after bin sections and AI */}
        <div className="mt-4 border-t">
          <AdUnit size="rectangle" />
        </div>

        {/* Disclaimer */}
        <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
          ⚠️ Data last verified March 2026. Recycling rules can change — always confirm with your council.
        </p>

        {/* Back link */}
        <div className="mt-6 pt-6 border-t">
          <Link
            href={`/councils?state=${council.state}`}
            className="text-sm text-muted-foreground hover:text-green-700 transition-colors"
          >
            ← View all {council.state} councils
          </Link>
        </div>
      </div>
    </>
  )
}
