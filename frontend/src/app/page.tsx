import type { Metadata } from 'next'
import Link from 'next/link'
import { Search, MapPin, Recycle, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import SearchBar from '@/components/search/SearchBar'
import AskAI from '@/components/ai/AskAI'

export const metadata: Metadata = {
  title: 'Australia Recycling — Find Recycling Info for Your Area',
  description:
    'Find out exactly what goes in which bin for your Australian council. Search by suburb, postcode, or council name for accurate recycling information.',
}

const STATES = [
  { code: 'NSW', name: 'New South Wales' },
  { code: 'VIC', name: 'Victoria' },
  { code: 'QLD', name: 'Queensland' },
  { code: 'SA', name: 'South Australia' },
  { code: 'WA', name: 'Western Australia' },
  { code: 'TAS', name: 'Tasmania' },
  { code: 'ACT', name: 'ACT' },
  { code: 'NT', name: 'Northern Territory' },
]

const HOW_IT_WORKS = [
  {
    icon: Search,
    step: '1',
    title: 'Search your suburb or council',
    description:
      'Enter your suburb name, postcode, or council name to find your local recycling rules.',
  },
  {
    icon: MapPin,
    step: '2',
    title: 'See what goes in each bin',
    description:
      'View a clear breakdown of items accepted in your yellow lid, red lid, and green waste bins.',
  },
  {
    icon: CheckCircle2,
    step: '3',
    title: 'Recycle right',
    description:
      "Follow your council's specific guidelines to reduce contamination and improve recycling rates.",
  },
]

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="bg-gradient-to-b from-green-50 to-white dark:from-green-950 dark:to-background py-16 px-4">
        <div className="container mx-auto max-w-4xl text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-green-100 dark:bg-green-900 px-4 py-1.5 text-sm font-medium text-green-800 dark:text-green-400 mb-6">
            <Recycle className="h-4 w-4" />
            Free recycling information for all Australians
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4 leading-tight">
            Find recycling information
            <br />
            <span className="text-green-600 dark:text-green-400">for your area</span>
          </h1>
          <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
            Search by suburb, postcode, or council name to see exactly what goes in each bin.
            Recycling rules vary — get the right information for your council.
          </p>

          <div className="flex justify-center">
            <SearchBar />
          </div>

          <p className="mt-4 text-sm text-muted-foreground">
            Covering 500+ councils across Australia
          </p>

          {/* AI search — Phase 2 */}
          <div className="mt-8 flex justify-center">
            <div className="w-full max-w-2xl">
              <div className="flex items-center gap-3 mb-3">
                <div className="h-px flex-1 bg-border" />
                <span className="text-xs text-muted-foreground flex items-center gap-1.5">
                  <span aria-hidden="true">✨</span>
                  or try AI search
                </span>
                <div className="h-px flex-1 bg-border" />
              </div>
              <AskAI />
              <p className="mt-2 text-xs text-center text-muted-foreground">
                Ask natural language questions — our AI uses council data to answer recycling queries
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="pt-6 pb-16 px-4 bg-background">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-2xl font-bold text-center text-foreground mb-10">How it works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {HOW_IT_WORKS.map(({ icon: Icon, step, title, description }) => (
              <div key={step} className="flex flex-col items-center text-center gap-4">
                <div className="relative">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-green-100 dark:bg-green-900">
                    <Icon className="h-7 w-7 text-green-600 dark:text-green-400" />
                  </div>
                  <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-green-600 dark:bg-green-900 dark:border dark:border-green-400 text-xs font-bold text-white dark:text-green-400">
                    {step}
                  </span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-1">{title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Browse by state */}
      <section className="py-16 px-4 bg-muted">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-2xl font-bold text-center text-foreground mb-3">
            Browse by state
          </h2>
          <p className="text-center text-muted-foreground mb-8 text-sm">
            Select your state to browse councils in your area
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {STATES.map((state) => (
              <Link
                key={state.code}
                href={`/councils?state=${state.code}`}
                className="group flex flex-col items-center justify-center rounded-xl border-2 border-border dark:border-green-900 bg-card p-4 text-center hover:border-green-400 hover:bg-green-50 dark:hover:bg-green-950 transition-all"
              >
                <span className="text-2xl font-bold text-green-600 dark:text-green-400 group-hover:scale-110 transition-transform">
                  {state.code}
                </span>
                <span className="mt-1 text-xs text-muted-foreground leading-tight">{state.name}</span>
              </Link>
            ))}
          </div>

          <div className="mt-8 text-center">
            <Button asChild variant="outline" className="border-green-300 hover:bg-green-50 hover:text-green-700">
              <Link href="/councils">View all councils</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Materials CTA */}
      <section className="py-12 px-4 bg-background border-t">
        <div className="container mx-auto max-w-2xl text-center">
          <h2 className="text-xl font-semibold text-foreground mb-2">
            Not sure about a specific item?
          </h2>
          <p className="text-muted-foreground text-sm mb-6">
            Browse our materials database to find out how to dispose of specific items across Australia.
          </p>
          <Button asChild className="bg-green-600 hover:bg-green-700">
            <Link href="/materials">Browse materials</Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
