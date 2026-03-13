import { cn } from '@/lib/utils'

interface AdUnitProps {
  /** 'banner' = 728×90, 'rectangle' = 300×250, 'leaderboard' mirrors banner */
  size?: 'banner' | 'rectangle'
  className?: string
}

/**
 * Ad placeholder unit — per DESIGN.md §5.9.
 * Always labelled "ADVERTISEMENT". Never injected into content flow.
 * Replace the inner div with the actual AdSense / Carbon Ads script in production.
 */
export default function AdUnit({ size = 'rectangle', className }: AdUnitProps) {
  return (
    <div className={cn('py-6', className)}>
      <p className="text-xs text-gray-400 uppercase tracking-widest mb-2">Advertisement</p>
      <div
        className={cn(
          'w-full rounded-lg border border-dashed border-gray-200 bg-gray-50 flex items-center justify-center text-xs text-gray-300',
          size === 'banner' ? 'h-[90px]' : 'h-[250px] max-w-[300px]',
        )}
        aria-hidden="true"
      >
        {size === 'banner' ? '728 × 90' : '300 × 250'}
      </div>
    </div>
  )
}
