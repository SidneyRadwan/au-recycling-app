/**
 * Design preview page — shows the AI chat experience with a pre-loaded conversation.
 * Used for Figma capture only. Not linked from the site navigation.
 */
import type { Metadata } from 'next'
import AskAIWithSampleConversation from '@/components/ai/AskAIWithSampleConversation'

export const metadata: Metadata = {
  robots: { index: false, follow: false },
}

export default function AIPreviewPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <h1 className="text-2xl font-bold text-foreground mb-2">
        AI Recycling Assistant
      </h1>
      <p className="text-muted-foreground text-sm mb-8">
        Ask natural language questions about recycling in your area.
      </p>
      <AskAIWithSampleConversation />
    </div>
  )
}
