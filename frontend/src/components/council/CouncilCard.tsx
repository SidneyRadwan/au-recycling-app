import Link from 'next/link'
import { MapPin, ExternalLink } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { Council } from '@/types'

interface CouncilCardProps {
  council: Council
}

export default function CouncilCard({ council }: CouncilCardProps) {
  return (
    <Link href={`/councils/${council.slug}`} className="group block">
      <Card className="h-full transition-shadow hover:shadow-md group-hover:border-green-300">
        <CardHeader className="pb-2">
          <CardTitle className="text-base font-semibold text-foreground group-hover:text-green-700 transition-colors line-clamp-2">
            {council.name}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
            <MapPin className="h-3.5 w-3.5 shrink-0" />
            <span>{council.state}</span>
          </div>
          {council.website && (
            <span
              className="flex items-center gap-1 text-xs text-green-600 opacity-0 group-hover:opacity-100 transition-opacity"
              aria-hidden="true"
            >
              <ExternalLink className="h-3 w-3" />
              Website
            </span>
          )}
        </CardContent>
      </Card>
    </Link>
  )
}

export function CouncilCardSkeleton() {
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <div className="h-5 bg-muted rounded animate-pulse w-3/4" />
      </CardHeader>
      <CardContent>
        <div className="h-4 bg-muted rounded animate-pulse w-1/4" />
      </CardContent>
    </Card>
  )
}
