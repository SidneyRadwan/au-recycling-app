import type { Metadata } from 'next'
import Link from 'next/link'
import { Search, MapPin, Recycle, CheckCircle2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import SearchBar from '@/components/search/SearchBar'

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
      'Follow your council's specific guidelines to reduce contamination and improve recycling rates.',
  },
]

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="bg-gradient-to-b from-green-50 to-white py-16 px-4">
        <div className="container mx-auto max-w-4xl text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-green-100 px-4 py-1.5 text-sm font-medium text-green-800 mb-6">
            <Recycle className="h-4 w-4" />
            Free recycling information for all Australians
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4 leading-tight">
            Find recycling information
            <br />
            <span className="text-green-600">for your area</span>
          </h1>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Search by suburb, postcode, or council name to see exactly what goes in each bin.
            Recycling rules vary — get the right information for your council.
          </p>

          <div className="flex justify-center">
            <SearchBar />
          </div>

          <p className="mt-4 text-sm text-gray-400">
            Covering 500+ councils across Australia
          </p>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-4 bg-white">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-10">How it works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {HOW_IT_WORKS.map(({ icon: Icon, step, title, description }) => (
              <div key={step} className="flex flex-col items-center text-center gap-4">
                <div className="relative">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-green-100">
                    <Icon className="h-7 w-7 text-green-600" />
                  </div>
                  <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-green-600 text-xs font-bold text-white">
                    {step}
                  </span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
                  <p className="text-sm text-gray-500 leading-relaxed">{description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Browse by state */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-3">
            Browse by state
          </h2>
          <p className="text-center text-gray-500 mb-8 text-sm">
            Select your state to browse councils in your area
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {STATES.map((state) => (
              <Link
                key={state.code}
                href={`/councils?state=${state.code}`}
                className="group flex flex-col items-center justify-center rounded-xl border-2 border-gray-200 bg-white p-4 text-center hover:border-green-400 hover:bg-green-50 transition-all"
              >
                <span className="text-2xl font-bold text-green-600 group-hover:scale-110 transition-transform">
                  {state.code}
                </span>
                <span className="mt-1 text-xs text-gray-500 leading-tight">{state.name}</span>
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
      <section className="py-12 px-4 bg-white border-t">
        <div className="container mx-auto max-w-2xl text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Not sure about a specific item?
          </h2>
          <p className="text-gray-500 text-sm mb-6">
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
