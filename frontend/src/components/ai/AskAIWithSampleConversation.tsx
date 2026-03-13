'use client'

import { Sparkles, Send } from 'lucide-react'

/**
 * Static design preview of the AI chat experience with a sample conversation.
 * Used for Figma design capture only — not used in production.
 */
export default function AskAIWithSampleConversation() {
  return (
    <div className="w-full space-y-6">
      {/* Conversation */}
      <div className="space-y-4">
        {/* User message */}
        <div className="flex gap-2.5 justify-end">
          <div className="rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm bg-purple-600 text-white max-w-[85%] leading-relaxed">
            Can I put a greasy pizza box in my recycling bin in the City of Sydney?
          </div>
        </div>

        {/* AI response — completed */}
        <div className="flex gap-2.5 justify-start">
          <div className="shrink-0 h-7 w-7 rounded-full bg-purple-100 flex items-center justify-center mt-0.5">
            <Sparkles className="h-3.5 w-3.5 text-purple-600" aria-hidden="true" />
          </div>
          <div className="rounded-2xl rounded-tl-sm px-4 py-3 bg-purple-50 border border-purple-100 text-sm text-purple-900 max-w-[85%] leading-relaxed space-y-2">
            <p>
              For <strong>City of Sydney</strong>, a greasy pizza box should go in the{' '}
              <span className="inline-flex items-center gap-1 font-medium text-green-800 bg-green-100 px-1.5 py-0.5 rounded text-xs">
                🟢 Green Lid (FOGO)
              </span>{' '}
              bin — not recycling.
            </p>
            <p>
              City of Sydney runs a Food Organics &amp; Garden Organics (FOGO) service, which means
              food-soiled cardboard like pizza boxes can go in the green bin for composting.
              The clean, unsoiled parts of the box can be flattened and placed in the yellow lid recycling bin.
            </p>
            <p className="text-xs text-purple-500">
              Source: City of Sydney recycling guidelines · Verified March 2026
            </p>
          </div>
        </div>

        {/* User follow-up */}
        <div className="flex gap-2.5 justify-end">
          <div className="rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm bg-purple-600 text-white max-w-[85%] leading-relaxed">
            What about aluminium foil?
          </div>
        </div>

        {/* AI streaming response */}
        <div className="flex gap-2.5 justify-start">
          <div className="shrink-0 h-7 w-7 rounded-full bg-purple-100 flex items-center justify-center mt-0.5">
            <Sparkles className="h-3.5 w-3.5 text-purple-600" aria-hidden="true" />
          </div>
          <div className="rounded-2xl rounded-tl-sm px-4 py-3 bg-purple-50 border border-purple-100 text-sm text-purple-900 max-w-[85%] leading-relaxed">
            <p>
              Yes! Aluminium foil is accepted in the{' '}
              <span className="inline-flex items-center gap-1 font-medium text-yellow-800 bg-yellow-100 px-1.5 py-0.5 rounded text-xs">
                🟡 Yellow Lid (Recycling)
              </span>{' '}
              bin in City of Sydney. Scrunch it into a ball at least the size of your fist so it doesn&apos;t fall through sorting machinery
              <span className="inline-block w-0.5 h-4 bg-purple-400 animate-pulse ml-0.5 align-middle" aria-hidden="true" />
            </p>
          </div>
        </div>
      </div>

      {/* Input */}
      <div className="relative">
        <Sparkles className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-purple-400 pointer-events-none" aria-hidden="true" />
        <input
          type="text"
          readOnly
          value=""
          placeholder="Ask a follow-up question…"
          className="w-full pl-10 pr-12 h-12 text-sm rounded-xl border-2 border-purple-200 bg-background focus:outline-none placeholder:text-muted-foreground dark:border-purple-800"
        />
        <div className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 rounded-lg bg-purple-600 text-white flex items-center justify-center opacity-40">
          <Send className="h-3.5 w-3.5" />
        </div>
      </div>

      <p className="text-xs text-muted-foreground text-center">
        AI answers are based on council recycling data and may vary. Always confirm with your council for the latest rules.
      </p>
    </div>
  )
}
