import { Skeleton } from '@/components/ui/skeleton'

export default function Loading() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <Skeleton className="h-4 w-48 mb-6" />
      <Skeleton className="h-6 w-24 rounded mb-3" />
      <Skeleton className="h-9 w-64 mb-3" />
      <Skeleton className="h-4 w-full mb-1" />
      <Skeleton className="h-4 w-3/4 mb-8" />
      <Skeleton className="h-20 w-full rounded-xl mb-8" />
      <Skeleton className="h-11 w-44 rounded-lg" />
    </div>
  )
}
