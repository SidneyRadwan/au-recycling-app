'use client'

import { useState, useRef } from 'react'
import { Sparkles, Send, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface AskAIProps {
  /** Pre-filled context, e.g. council name. Shown in the placeholder. */
  councilName?: string
  className?: string
}

/**
 * AI chat component — Phase 2 feature stub.
 * Shows the full chat UI. Backend endpoint /api/v1/ai/chat wired up in Phase 2.
 */
export default function AskAI({ councilName, className }: AskAIProps) {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const placeholder = councilName
    ? `Ask about ${councilName} recycling — e.g. "Can I recycle a pizza box?"`
    : `Ask anything — e.g. "Can I recycle a pizza box in Sydney?"`

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const q = query.trim()
    if (!q || loading) return

    setMessages((prev) => [...prev, { role: 'user', content: q }])
    setQuery('')
    setLoading(true)

    // Phase 2: replace with POST /api/v1/ai/chat
    await new Promise((r) => setTimeout(r, 900))
    setMessages((prev) => [
      ...prev,
      {
        role: 'assistant',
        content: councilName
          ? `Great question about ${councilName}! AI-powered answers are launching in Phase 2. In the meantime, scroll up to see the full bin guide for ${councilName}, or use the search bar to find another council.`
          : `AI search is coming soon! In the meantime, use the search bar above to find your council's specific recycling rules — every Australian council is different.`,
      },
    ])
    setLoading(false)
    inputRef.current?.focus()
  }

  return (
    <div className={cn('w-full', className)}>
      {/* Chat history */}
      {messages.length > 0 && (
        <div className="mb-3 space-y-3 max-h-64 overflow-y-auto">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={cn(
                'flex gap-2.5',
                msg.role === 'user' ? 'justify-end' : 'justify-start',
              )}
            >
              {msg.role === 'assistant' && (
                <div className="shrink-0 h-7 w-7 rounded-full bg-purple-100 flex items-center justify-center mt-0.5">
                  <Sparkles className="h-3.5 w-3.5 text-purple-600" aria-hidden="true" />
                </div>
              )}
              <div
                className={cn(
                  'rounded-2xl px-4 py-2.5 text-sm max-w-[85%] leading-relaxed',
                  msg.role === 'user'
                    ? 'bg-purple-600 text-white rounded-tr-sm'
                    : 'bg-purple-50 text-purple-900 border border-purple-100 rounded-tl-sm',
                )}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-2.5 justify-start">
              <div className="shrink-0 h-7 w-7 rounded-full bg-purple-100 flex items-center justify-center">
                <Sparkles className="h-3.5 w-3.5 text-purple-600" aria-hidden="true" />
              </div>
              <div className="rounded-2xl rounded-tl-sm px-4 py-3 bg-purple-50 border border-purple-100">
                <Loader2 className="h-4 w-4 text-purple-400 animate-spin" />
              </div>
            </div>
          )}
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="relative">
        <Sparkles className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-purple-400 pointer-events-none" aria-hidden="true" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className="w-full pl-10 pr-12 h-12 text-sm rounded-xl border-2 border-purple-200 bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 placeholder:text-muted-foreground disabled:opacity-60 dark:border-purple-800 dark:focus:ring-purple-600"
          aria-label="Ask AI a recycling question"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 rounded-lg bg-purple-600 text-white hover:bg-purple-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          aria-label="Send question"
        >
          <Send className="h-3.5 w-3.5" />
        </button>
      </form>
    </div>
  )
}
