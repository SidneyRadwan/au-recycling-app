import { Skeleton } from '@/components/ui/skeleton'

export default function Loading() {
  return (
    <div className="container mx-auto max-w-4xl px-4 py-10">
      <Skeleton className="h-4 w-56 mb-6" />
      <div className="mb-8">
        <Skeleton className="h-9 w-72 mb-3" />
        <Skeleton className="h-4 w-40 mb-4" />
        <Skeleton className="h-4 w-52" />
      </div>
      <Skeleton className="h-6 w-48 mb-4" />
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-border overflow-hidden">
            <Skeleton className="h-12 w-full rounded-none" />
            <div className="p-4 flex flex-wrap gap-2">
              {Array.from({ length: 6 }).map((_, j) => (
                <Skeleton key={j} className="h-7 w-24 rounded-full" />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
