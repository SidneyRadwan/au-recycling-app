'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { Search, Loader2 } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { search } from '@/lib/api'
import type { SearchResult } from '@/types'

type FlatResult =
  | { type: 'council'; id: number; label: string; sublabel: string; href: string }
  | { type: 'suburb'; label: string; sublabel: string; href: string }
  | { type: 'material'; id: number; label: string; sublabel: string; href: string }

function flattenResults(results: SearchResult): FlatResult[] {
  const flat: FlatResult[] = []

  for (const c of results.councils) {
    flat.push({
      type: 'council',
      id: c.id,
      label: c.name,
      sublabel: c.state,
      href: `/councils/${c.slug}`,
    })
  }

  for (const s of results.suburbs) {
    flat.push({
      type: 'suburb',
      label: `${s.name} ${s.postcode}`,
      sublabel: s.councilName,
      href: `/councils/${s.councilSlug}`,
    })
  }

  for (const m of results.materials) {
    flat.push({
      type: 'material',
      id: m.id,
      label: m.name,
      sublabel: m.category ?? 'Material',
      href: `/materials/${m.slug}`,
    })
  }

  return flat
}

function groupLabel(type: FlatResult['type']): string {
  switch (type) {
    case 'council':
      return 'Councils'
    case 'suburb':
      return 'Suburbs'
    case 'material':
      return 'Materials'
  }
}

export default function SearchBar() {
  const router = useRouter()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<FlatResult[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const doSearch = useCallback(async (q: string) => {
    if (q.trim().length < 2) {
      setResults([])
      setOpen(false)
      return
    }
    setLoading(true)
    try {
      const data = await search(q.trim())
      const flat = flattenResults(data)
      setResults(flat)
      setOpen(flat.length > 0)
      setActiveIndex(-1)
    } catch {
      setResults([])
      setOpen(false)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      void doSearch(query)
    }, 300)
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [query, doSearch])

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(e.target as Node)
      ) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleSelect(result: FlatResult) {
    setOpen(false)
    setQuery('')
    router.push(result.href)
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!open) return

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setActiveIndex((prev) => Math.min(prev + 1, results.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setActiveIndex((prev) => Math.max(prev - 1, -1))
        break
      case 'Enter':
        e.preventDefault()
        if (activeIndex >= 0 && results[activeIndex]) {
          handleSelect(results[activeIndex])
        }
        break
      case 'Escape':
        setOpen(false)
        setActiveIndex(-1)
        inputRef.current?.blur()
        break
    }
  }

  // Group results for display
  const groups: { groupLabel: string; items: FlatResult[] }[] = []
  const seenTypes = new Set<FlatResult['type']>()

  for (const result of results) {
    if (!seenTypes.has(result.type)) {
      seenTypes.add(result.type)
      groups.push({ groupLabel: groupLabel(result.type), items: [] })
    }
    groups[groups.length - 1].items.push(result)
  }

  // Compute flat indices per group for keyboard nav
  let flatIndex = 0

  return (
    <div className="relative w-full max-w-2xl">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground pointer-events-none" />
        <Input
          ref={inputRef}
          type="search"
          placeholder="Search by suburb, postcode, or council name"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => results.length > 0 && setOpen(true)}
          className="pl-10 pr-10 h-12 text-base rounded-xl border-2 border-green-200 focus-visible:ring-green-500 focus-visible:border-green-500"
          aria-label="Search suburbs, postcodes, or councils"
          aria-autocomplete="list"
          aria-expanded={open}
          role="combobox"
        />
        {loading && (
          <span className="absolute right-3 top-0 bottom-0 flex items-center pointer-events-none">
            <Loader2 className="h-5 w-5 text-muted-foreground animate-spin" />
          </span>
        )}
      </div>

      {open && results.length > 0 && (
        <div
          ref={dropdownRef}
          className="absolute top-full left-0 right-0 z-50 mt-1 rounded-xl border bg-background shadow-lg overflow-hidden"
          role="listbox"
        >
          {groups.map((group) => (
            <div key={group.groupLabel}>
              <div className="px-3 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wide bg-muted border-b">
                {group.groupLabel}
              </div>
              {group.items.map((item) => {
                const currentIndex = flatIndex++
                return (
                  <button
                    key={`${item.type}-${item.label}`}
                    role="option"
                    aria-selected={activeIndex === currentIndex}
                    className={`w-full flex items-start gap-3 px-4 py-3 text-left hover:bg-green-50 dark:hover:bg-green-950 transition-colors ${
                      activeIndex === currentIndex ? 'bg-green-50 dark:bg-green-950' : ''
                    }`}
                    onMouseDown={(e) => {
                      e.preventDefault()
                      handleSelect(item)
                    }}
                    onMouseEnter={() => setActiveIndex(currentIndex)}
                  >
                    <span className="text-sm font-medium text-foreground leading-tight">
                      {item.label}
                    </span>
                    <span className="text-xs text-muted-foreground mt-0.5 ml-auto shrink-0">
                      {item.sublabel}
                    </span>
                  </button>
                )
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
