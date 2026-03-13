import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center">
      <div className="text-6xl mb-4" aria-hidden="true">
        ♻️
      </div>
      <h1 className="text-3xl font-bold text-foreground mb-2">Page not found</h1>
      <p className="text-muted-foreground mb-8 max-w-md">
        Sorry, we couldn&apos;t find the page you were looking for. It may have been moved or doesn&apos;t exist.
      </p>
      <div className="flex gap-4">
        <Button asChild className="bg-green-600 hover:bg-green-700">
          <Link href="/">Back to home</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href="/councils">Browse councils</Link>
        </Button>
      </div>
    </div>
  )
}
