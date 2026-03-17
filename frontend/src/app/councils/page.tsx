import type { Metadata } from 'next'
import Link from 'next/link'
import { ChevronRight } from 'lucide-react'
import { getCouncils } from '@/lib/api'
import CouncilCard from '@/components/council/CouncilCard'
import { Button } from '@/components/ui/button'
import { formatState } from '@/lib/utils'
import AdUnit from '@/components/ui/ad-unit'
import { ErrorState } from '@/components/ui/error-state'

interface Props {
  searchParams: Promise<{ state?: string; page?: string }>
}

export async function generateMetadata({ searchParams }: Props): Promise<Metadata> {
  const { state } = await searchParams
  const stateLabel = state ? formatState(state) : 'All'
  return {
    title: `${stateLabel} Councils`,
    description: `Browse recycling information for councils${state ? ` in ${formatState(state)}` : ' across Australia'}.`,
  }
}

const STATES = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'ACT', 'NT']

export default async function CouncilsPage({ searchParams }: Props) {
  const { state, page: pageParam } = await searchParams
  const page = Math.max(0, parseInt(pageParam ?? '0', 10))
  const pageSize = 24

  let councilsPage: Awaited<ReturnType<typeof getCouncils>>
  try {
    councilsPage = await getCouncils(state, page, pageSize)
  } catch {
    return <ErrorState />
  }

  const { content: councils, page: { totalElements, totalPages, number: currentPage } } = councilsPage

  return (
    <div className="container mx-auto max-w-6xl px-4 py-10">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm text-muted-foreground mb-6">
        <Link href="/" className="hover:text-green-700">Home</Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <span className="text-foreground font-medium">Councils</span>
      </nav>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            {state ? `${formatState(state)} Councils` : 'All Councils'}
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">
            {totalElements > 0
              ? `${totalElements} council${totalElements === 1 ? '' : 's'} found`
              : 'No councils found'}
          </p>
        </div>
      </div>

      {/* State filter tabs */}
      <div className="flex flex-wrap gap-2 mb-8">
        <Link
          href="/councils"
          className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors border ${
            !state
              ? 'bg-green-600 text-white border-green-600'
              : 'bg-background text-muted-foreground border-border hover:border-green-400 hover:text-green-700'
          }`}
        >
          All
        </Link>
        {STATES.map((s) => (
          <Link
            key={s}
            href={`/councils?state=${s}`}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors border ${
              state === s
                ? 'bg-green-600 text-white border-green-600'
                : 'bg-background text-muted-foreground border-border hover:border-green-400 hover:text-green-700'
            }`}
          >
            {s}
          </Link>
        ))}
      </div>

      {/* Council grid */}
      {councils.length > 0 ? (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {councils.map((council) => (
              <CouncilCard key={council.id} council={council} />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-10">
              {currentPage > 0 && (
                <Button asChild variant="outline" size="sm">
                  <Link href={`/councils?${state ? `state=${state}&` : ''}page=${currentPage - 1}`}>
                    Previous
                  </Link>
                </Button>
              )}
              <span className="text-sm text-muted-foreground">
                Page {currentPage + 1} of {totalPages}
              </span>
              {currentPage < totalPages - 1 && (
                <Button asChild variant="outline" size="sm">
                  <Link href={`/councils?${state ? `state=${state}&` : ''}page=${currentPage + 1}`}>
                    Next
                  </Link>
                </Button>
              )}
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-16 text-muted-foreground">
          <div className="text-4xl mb-3" aria-hidden="true">♻️</div>
          <p className="text-lg font-medium">No councils found</p>
          <p className="text-sm mt-1">Try selecting a different state or check back soon.</p>
        </div>
      )}

      {/* Ad unit — below fold, after results */}
      <div className="mt-8 border-t pt-4">
        <AdUnit size="banner" />
      </div>
    </div>
  )
}
