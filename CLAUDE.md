# Australia Recycling App

## General Rules
- Only build what is required, what is no longer required should be removed
- Follow best practices ALWAYS unless explicitly instructed otherwise
- Self-review code after writing. After discovering a solution to a problem, evaluate if the approach is the cleanest approach to the goal
- Simplicity is key
- Improve dev experience, use dev containers that automate as much as possible, VS code tasks
- We are working in a repository with other contributors, all changes must be reproducible for others

## Project Overview
Website (australiarecycling.com.au) helping Australians find recycling information by council area. Mono-repo with Java backend, React frontend, and Python scraper.

## Architecture
- **Backend**: Java 21 + Spring Boot 3 + Gradle — `backend/`
- **Frontend**: Next.js 15 + React 19 + TypeScript + Tailwind + shadcn/ui — `frontend/`
- **Scraper**: Python 3.12 + BeautifulSoup/Scrapy — `scraper/`
- **Database**: PostgreSQL 16 + pgvector
- **Infrastructure**: Docker Compose (dev), Terraform + GCP Cloud Run (prod) — `infrastructure/`

## Key Commands
```bash
# Full stack
docker-compose up

# Backend
cd backend && ./gradlew bootRun        # Run
cd backend && ./gradlew test            # Test
cd backend && ./gradlew build           # Build

# Frontend
cd frontend && npm run dev              # Dev server
cd frontend && npm run build            # Build
cd frontend && npm run test             # Test
cd frontend && npm run lint             # Lint

# Scraper
cd scraper && python -m pytest          # Test
cd scraper && python main.py            # Run scraper
```

## Conventions
- Feature branches merged via PR to main
- Spring Boot profiles: dev, prod
- All config externalized via env vars (never hardcode secrets)
- API endpoints: `/api/v1/...`
- Council URL pattern: `/councils/{slug}` (e.g., `/councils/city-of-sydney`)
- Material URL pattern: `/materials/{slug}` (e.g., `/materials/styrofoam`)

## Environment Variables
See `.env.example` for all required variables. Key ones:
- `DATABASE_URL` — PostgreSQL connection string
- `ANTHROPIC_API_KEY` — Claude API key (never commit)
- `NEXT_PUBLIC_API_URL` — Backend API URL for frontend

---

## Figma MCP Integration Rules

These rules govern every Figma-to-code task. Follow them in order — do not skip steps.

### Required Workflow

1. Run `get_design_context` for the exact Figma node(s) being implemented
2. If the response is too large or truncated, run `get_metadata` to get the high-level node map, then re-fetch only the required nodes with `get_design_context`
3. Run `get_screenshot` for a visual reference of the node/variant being implemented
4. Only after you have both `get_design_context` and `get_screenshot`, download any assets and begin implementation
5. Translate the MCP output (React + Tailwind) into this project's conventions (see rules below)
6. Validate the final UI against the Figma screenshot for 1:1 visual parity before marking complete

### Component Organisation

- IMPORTANT: Check `frontend/src/components/ui/` for existing shadcn/ui primitives before creating new ones
- Primitive UI components (Button, Card, Badge, Input, Skeleton) → `frontend/src/components/ui/`
- Feature components (CouncilCard, BinSection, MaterialBadge, SearchBar) → `frontend/src/components/{feature}/`
- Layout components (Header, Footer) → `frontend/src/components/layout/`
- Page components → `frontend/src/app/{route}/page.tsx`
- All components use PascalCase filenames. Default exports for pages/layouts, named exports for UI primitives

### Styling Rules

- IMPORTANT: Use Tailwind CSS utility classes exclusively — no inline styles, no CSS Modules, no styled-components
- IMPORTANT: Never hardcode hex colours. Use Tailwind's colour palette (`green-600`, `yellow-50`, etc.) or CSS variables via the token system below
- IMPORTANT: Always use semantic token classes for text, background, and border colours — never hardcode `text-gray-*`, `bg-white`, `bg-gray-*`, or `border-gray-*`. Semantic tokens automatically handle dark mode; hardcoded palette classes require manual `dark:` overrides on every element.
- Use `cn()` from `@/lib/utils` (re-exports `clsx` + `tailwind-merge`) for conditional class merging
- Use `cva()` from `class-variance-authority` for components with multiple variants (see `Button`, `Badge`)
- All interactive elements need focus rings: `focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`
- Minimum tap target size: 44px height (`h-11` or larger) for mobile touch targets

### Design Tokens

Tokens are defined as CSS HSL variables in `frontend/src/app/globals.css` and mapped in `frontend/tailwind.config.ts`.

| Semantic token | Tailwind class | Usage |
|----------------|---------------|-------|
| `--primary` (green) | `bg-primary`, `text-primary` | CTAs, active nav, focus rings |
| `--background` | `bg-background` | Page/section backgrounds (replaces `bg-white`) |
| `--foreground` | `text-foreground` | Primary body text (replaces `text-gray-900`) |
| `--muted` | `bg-muted` | Subtle section backgrounds (replaces `bg-gray-50`) |
| `--muted-foreground` | `text-muted-foreground` | Secondary/placeholder text (replaces `text-gray-500/600`) |
| `--card` | `bg-card` | Card backgrounds |
| `--border` | `border-border` | Default borders (replaces `border-gray-200`) |
| `--ring` | `ring-ring` | Focus ring colour |

**Bin type colours** are defined in `frontend/src/components/council/MaterialBadge.tsx` as `BIN_TYPE_CONFIG`. Use this config — never create new bin colour classes ad-hoc:

```typescript
// Import and use this — do not duplicate
import { BIN_TYPE_CONFIG } from '@/components/council/MaterialBadge'
const config = BIN_TYPE_CONFIG[binType]
// config.containerClass, config.headerClass, config.badgeClass
```

Bin colour reference:
- Recycling → `yellow-*` classes
- General Waste → `red-*` classes
- Green Waste → `green-*` classes
- Soft Plastics → `purple-*` classes
- Special Drop-off → `blue-*` classes
- Not Accepted → `gray-*` classes

### Typography

Use Tailwind's text scale directly — do not add custom font sizes to `tailwind.config.ts`:

| Role | Classes |
|------|---------|
| Display/Hero | `text-4xl md:text-5xl font-bold` |
| Page title (h1) | `text-3xl font-bold` |
| Section heading (h2) | `text-xl md:text-2xl font-semibold` |
| Card title (h3) | `text-lg font-semibold` |
| Body | `text-base` (default) |
| Small/meta | `text-sm` |
| Caption/label | `text-xs` |

Font family is Inter (system-ui fallback) — loaded via `frontend/src/app/layout.tsx`. Do not import additional fonts.

### Spacing & Layout

- Base unit: 4px (Tailwind default scale — use `p-1`, `p-2`, `p-4`, `p-6`, `p-8`)
- Section vertical padding: `py-12` mobile, `py-16` desktop
- Max content widths: `max-w-2xl` (forms), `max-w-4xl` (detail pages), `max-w-7xl` (list/grid pages)
- Page wrapper: `mx-auto px-4 sm:px-6 lg:px-8` inside a `max-w-*` container
- Grid: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4` for card grids

### Icons

- IMPORTANT: Use `lucide-react` exclusively — do not install other icon packages
- Icons already in use: `Search`, `Loader2`, `Menu`, `X`, `ExternalLink`, `ChevronRight`, `MapPin`, `Recycle`, `CheckCircle2`
- Import pattern: `import { IconName } from 'lucide-react'`
- Standard size: `h-5 w-5` (inline), `h-4 w-4` (inside buttons via `[&_svg]:size-4` on Button)
- IMPORTANT: If the Figma MCP server returns a localhost source for an SVG/image asset, use that source directly — do not create placeholders

### Assets

- Static assets → `frontend/public/`
- No images are currently used in the project (text + emoji + lucide icons only)
- IMPORTANT: Do not add image packages or icon fonts. If Figma provides a localhost asset URL, use it directly

### Path Aliases

Always use the `@/` alias — no relative imports beyond one directory level:
```typescript
import { cn } from '@/lib/utils'           // ✓
import { Button } from '@/components/ui/button'  // ✓
import { search } from '@/lib/api'         // ✓
import { Council } from '@/types'          // ✓
import { cn } from '../../../lib/utils'    // ✗
```

### Server vs Client Components

- Pages in `src/app/` are **Server Components** by default — fetch data directly, no `useState`/`useEffect`
- Add `'use client'` only when the component needs interactivity (SearchBar, Header mobile menu)
- Data fetching uses `fetch` with Next.js cache options in `frontend/src/lib/api.ts`:
  - Detail pages: `next: { revalidate: 3600 }` (1 hour ISR)
  - Search: `cache: 'no-store'`
- `generateStaticParams` + `dynamicParams: true` for council/material detail pages

### SEO Requirements

Every page must have:
- Unique `<title>` and `<meta description>` via `generateMetadata` (server components) or `export const metadata`
- JSON-LD structured data on council pages (FAQPage schema) — see `frontend/src/app/councils/[slug]/page.tsx`
- Breadcrumb navigation using plain `<nav>` + `<Link>` (not a component)

### Accessibility

- All interactive elements keyboard-accessible (Tab, Enter, Space, Escape, Arrow keys)
- SearchBar uses full ARIA combobox pattern: `role="combobox"`, `aria-expanded`, `aria-autocomplete`, `role="listbox"`, `role="option"`, `aria-selected`
- Bin type sections use colour + emoji + text label (never colour alone)
- Minimum contrast: WCAG AA (4.5:1 normal text, 3:1 large text)
- Decorative emojis: `aria-hidden="true"`

### API Integration

All backend calls go through `frontend/src/lib/api.ts`. Do not call the backend API directly from components:
```typescript
import { getCouncil, getCouncils, getMaterials, getMaterial, search } from '@/lib/api'
```
Backend base URL: `process.env.NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8080`). Never hardcode this.
