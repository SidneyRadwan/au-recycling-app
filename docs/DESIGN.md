# Design Specification
## Australia Recycling — australiarecycling.com.au

| Field | Value |
|-------|-------|
| **Author** | Designer (AI Agent) |
| **Version** | 1.0 |
| **Date** | March 2026 |
| **Status** | ✅ Complete — ready for Figma |
| **Depends on** | `docs/PRD.md` v1.1 (approved) |
| **Figma file** | _(link to be added once created)_ |

---

## 1. Design Principles

Derived directly from PRD personas and goals.

### 1.1 Speed over decoration
Maya is standing next to her bin. She needs the answer in two taps. Every design decision must serve fast information retrieval — not brand expression. No hero animations, no full-bleed imagery, no splash screens.

### 1.2 Trust through clarity
Sarah shares the page with her family because it looks authoritative and up-to-date. Design signals trust via: clean typography, real council names, official links, a "last verified" date, and honest ad labelling. No dark patterns.

### 1.3 Bin colours are the UX
The yellow/red/green bin lid system is the mental model every Australian already has. The UI reinforces it — colour is not decorative, it is functional. Each bin section **must** use the lid colour as its dominant visual signal.

### 1.4 Mobile-first, thumb-friendly
Primary user is on mobile next to a bin. Search bar reachable with one thumb. Tap targets ≥ 44px. No horizontal scroll. Content readable at arm's length (minimum 16px body text).

### 1.5 Quiet ads, loud content
Ads exist to fund hosting. They are placed below the fold, never in the content flow, and clearly labelled. The word "Advertisement" appears above every ad unit. No popups, no interstitials, no autoplay.

---

## 2. Colour System

### 2.1 Brand palette

| Token | Hex | Usage |
|-------|-----|-------|
| `brand-primary` | `#16a34a` | CTAs, active nav, links, focus rings |
| `brand-primary-hover` | `#15803d` | Hover state on primary elements |
| `brand-light` | `#f0fdf4` | Hero background, hover fills on cards |
| `brand-subtle` | `#dcfce7` | Badges, chips, inline highlights |
| `brand-text` | `#166534` | Text on light green backgrounds |

### 2.2 Bin colours
These are the core visual language of the product. Chosen to match Australian standard bin lid colours.

| Bin type | Lid colour | Background | Border | Text | Emoji |
|----------|-----------|-----------|--------|------|-------|
| Recycling | Yellow | `#fefce8` | `#fde047` | `#713f12` | ♻️ |
| General waste | Red | `#fef2f2` | `#fca5a5` | `#7f1d1d` | 🗑️ |
| Green waste / FOGO | Green | `#f0fdf4` | `#86efac` | `#14532d` | 🌿 |
| Soft plastics | Purple | `#faf5ff` | `#d8b4fe` | `#581c87` | 🛍️ |
| Special drop-off | Blue | `#eff6ff` | `#93c5fd` | `#1e3a5f` | 📍 |
| Not accepted | Grey | `#f9fafb` | `#d1d5db` | `#374151` | 🚫 |

### 2.3 Neutral palette

| Token | Hex | Usage |
|-------|-----|-------|
| `gray-900` | `#111827` | Primary headings |
| `gray-700` | `#374151` | Body text |
| `gray-500` | `#6b7280` | Secondary text, placeholders |
| `gray-400` | `#9ca3af` | Disabled, meta info |
| `gray-200` | `#e5e7eb` | Borders, dividers |
| `gray-100` | `#f3f4f6` | Card backgrounds, tag pills |
| `white` | `#ffffff` | Page background, card fill |

### 2.4 Semantic colours

| Token | Hex | Usage |
|-------|-----|-------|
| `success` | `#16a34a` | Same as brand-primary |
| `warning` | `#d97706` | Data freshness warnings |
| `error` | `#dc2626` | Form errors, API failures |
| `info` | `#2563eb` | Informational banners |

---

## 3. Typography

**Font family:** Inter (Google Fonts). Fallback: `system-ui, -apple-system, sans-serif`.

Load weights 400, 500, 600, 700 only.

| Role | Size (desktop) | Size (mobile) | Weight | Line height | Usage |
|------|---------------|---------------|--------|-------------|-------|
| `display` | 48px | 36px | 700 | 1.1 | Hero heading only |
| `h1` | 30px | 26px | 700 | 1.2 | Page titles |
| `h2` | 24px | 20px | 600 | 1.3 | Section headings, bin type headers |
| `h3` | 20px | 18px | 600 | 1.4 | Card titles, sub-section headings |
| `body-lg` | 18px | 17px | 400 | 1.6 | Intro text, descriptions |
| `body` | 16px | 16px | 400 | 1.6 | Main content |
| `body-sm` | 14px | 14px | 400 | 1.5 | Secondary content, metadata |
| `label` | 13px | 13px | 500 | 1.4 | Badges, chips, nav items |
| `caption` | 12px | 12px | 400 | 1.4 | Legal text, ad labels, timestamps |

---

## 4. Spacing & Layout

**Base unit:** 4px (Tailwind default)

| Scale | px | Tailwind | Usage |
|-------|----|----------|-------|
| `xs` | 4px | `p-1` | Icon padding |
| `sm` | 8px | `p-2` | Tight spacing |
| `md` | 16px | `p-4` | Component padding |
| `lg` | 24px | `p-6` | Card padding |
| `xl` | 32px | `p-8` | Section internal padding |
| `2xl` | 48px | `py-12` | Section vertical gaps (mobile) |
| `3xl` | 64px | `py-16` | Section vertical gaps (desktop) |

**Max content widths:**
- Narrow (forms, single column): `max-w-2xl` (672px)
- Standard (most pages): `max-w-4xl` (896px)
- Wide (councils grid, lists): `max-w-7xl` (1280px)

**Grid:**
- Mobile: 1 column
- Tablet (≥ 640px): 2 columns
- Desktop (≥ 1024px): 3 columns (councils/materials grids)

---

## 5. Component Inventory

### 5.1 Header / Navigation

**Desktop:**
```
┌─────────────────────────────────────────────────────────────┐
│  ♻️ Australia Recycling        Home   Councils   Materials   │
└─────────────────────────────────────────────────────────────┘
```
- Logo: ♻️ icon + "Australia Recycling" in `font-semibold gray-900`
- Nav links: `body-sm`, `gray-600`, hover `green-600`
- Active link: `green-600`, `font-medium`
- Background: `white`, bottom border `gray-200`
- Sticky on scroll (position: sticky, top: 0, z-index: 50)

**Mobile:**
```
┌─────────────────────────────────┐
│  ♻️ Australia Recycling    ☰    │
└─────────────────────────────────┘
```
- Hamburger opens a slide-down menu with full-width nav links
- Menu links are `h3` sized, `py-4` padding for thumb targets

**States:** Default, scrolled (add `shadow-sm`), mobile-open

---

### 5.2 Search Bar

The most critical component. Must feel fast and reliable.

**Closed (default):**
```
┌─────────────────────────────────────────────────────────┐
│ 🔍  Search by suburb, postcode, or council name...      │
└─────────────────────────────────────────────────────────┘
```
- Full-width, max-w-2xl centred on home page
- Height: 52px (desktop), 48px (mobile)
- Border: `gray-300`, rounded-xl
- Focus: `ring-2 ring-green-500 border-green-500`
- Placeholder: `gray-400`
- Search icon: `gray-400`, left side, 20px

**Open with results:**
```
┌─────────────────────────────────────────────────────────┐
│ 🔍  bondi                                          ✕    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│  COUNCILS                                                │
│  ○  Waverley Council                        NSW  →      │
│                                                          │
│  SUBURBS                                                 │
│  ○  Bondi — Waverley Council                2026  →     │
│  ○  Bondi Beach — Waverley Council          2026  →     │
│  ○  Bondi Junction — Waverley Council       2022  →     │
│                                                          │
│  MATERIALS                                               │
│  — No matching materials                                 │
└─────────────────────────────────────────────────────────┘
```
- Dropdown: `white`, `rounded-xl`, `shadow-lg`, `border border-gray-200`
- Section headers: `caption`, `gray-400`, `uppercase`, `tracking-wide`, `px-4 py-2`
- Result rows: `py-3 px-4`, hover `bg-green-50`
- Active/keyboard-selected row: `bg-green-50`, left border `2px solid green-600`
- Postcode badge: `label`, `gray-500`, right-aligned
- Arrow: `gray-400`, right side
- No results section: italicised `gray-400` text
- Loading: spinner replaces search icon, rows replaced by 3 skeleton lines

**States:** Default, focused-empty, focused-loading, focused-with-results, focused-no-results, result-hover, result-keyboard-active

---

### 5.3 Bin Section Card

The core information unit. One card per bin type on council detail pages.

```
┌─────────────────────────────────────────────────────────┐  ← yellow border
│  ♻️  Recycling Bin (Yellow Lid)                          │  ← yellow bg
│─────────────────────────────────────────────────────────│
│  • Cardboard          Flatten boxes. Remove tape.        │
│  • Paper              Loose paper, newspapers.           │
│  • Glass bottles      Rinse clean. Lids can stay on.    │
│  • Plastic bottles    Check the number — 1,2,3,5 only.  │
│  • Steel cans         Rinse clean.                       │
│  • Aluminium cans     Eligible for 10c Return & Earn.   │
└─────────────────────────────────────────────────────────┘
```
- Card: `rounded-xl`, `border-2` (bin colour), background (bin colour light)
- Header: `h2`, bin emoji + label, text in bin dark colour
- Header padding: `px-6 py-4`, bottom border `1px` (bin colour border)
- List items: `px-6 py-3`, bullet `•` in bin colour, material name `font-medium`
- Instruction text: `body-sm gray-600`, same line, em-dash separator
- Notes (if any): `caption gray-400`, indented below instruction
- Material name is a link → `/materials/{slug}`, hover underline
- Alternating rows: every other row has subtle `bg-black/[0.02]` tint

**States:** Default, material-name-hover

---

### 5.4 Council Card (list page)

```
┌─────────────────────────────────┐
│  City of Sydney           NSW   │
│  Sydney CBD and inner suburbs   │
│                      View →     │
└─────────────────────────────────┘
```
- Card: `white`, `rounded-lg`, `border border-gray-200`
- Hover: `border-green-300`, `bg-green-50`, subtle `shadow-sm`
- Council name: `h3 gray-900`
- State badge: `label`, `green-100 text-green-800`, `rounded-full px-2`
- Description: `body-sm gray-500`, 2-line clamp
- "View →": `body-sm green-600`, bottom right
- Full card is clickable (not just the link)

**States:** Default, hover, focus

---

### 5.5 Search Result / Material Item (materials list)

```
┌─────────────────────────────────┐
│  📄 Cardboard                   │
│  Paper & Cardboard              │
│  Flatten and place in recycling │
└─────────────────────────────────┘
```
- Same card style as Council Card
- Category shown as `label` chip below name

---

### 5.6 State Pill / Filter

```
[ All states ]  [ NSW ]  [ VIC ]  [ QLD ]  [ SA ]  [ WA ]  [ TAS ]  [ ACT ]  [ NT ]
```
- Inactive: `bg-gray-100 text-gray-700`, `rounded-full px-4 py-2`, `label`
- Active: `bg-green-600 text-white`
- Hover (inactive): `bg-gray-200`
- Overflow on mobile: horizontal scroll, `scrollbar-hide`

---

### 5.7 Primary Button

```
[ View all councils → ]
```
- Background: `green-600`, hover `green-700`
- Text: `white`, `label` or `body-sm`, `font-medium`
- Padding: `px-5 py-2.5`
- Border radius: `rounded-lg`
- Focus: `ring-2 ring-green-500 ring-offset-2`
- Disabled: `opacity-50 cursor-not-allowed`

**Variants:** Primary (green), Secondary (white + border), Ghost (no bg, green text)

---

### 5.8 Breadcrumb

```
Home / Councils / City of Sydney
```
- `body-sm gray-500`
- Separator: ` / ` in `gray-400`
- Current page: `gray-900`, not a link
- Links: hover `green-600`

---

### 5.9 Ad Unit

```
┌─────────────────────────────────┐
│  ADVERTISEMENT                  │  ← caption gray-400, left-aligned
│  ┌─────────────────────────┐    │
│  │   [Ad content here]     │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
```
- Always labelled "ADVERTISEMENT" in `caption gray-400` above
- Surrounded by `py-4` clear space
- Never injected into content flow
- Placed: below bin sections on council pages, sidebar on desktop (if wide enough), footer area

---

### 5.10 Footer

```
┌─────────────────────────────────────────────────────────────┐
│  ♻️ Australia Recycling                                      │
│  Helping Australians recycle right since 2026               │
│                                                             │
│  This site is free to use. Small ads help cover our         │
│  hosting and AI costs.                                      │
│                                                             │
│  About   Privacy   Contact   GitHub                         │
│  © 2026 Australia Recycling                                  │
└─────────────────────────────────────────────────────────────┘
```
- Background: `gray-900`
- Text: `gray-400`, links hover `white`
- Ad transparency note: `body-sm gray-500`, italicised

---

## 6. Page Wireframes

### 6.1 Home Page

**Mobile:**
```
┌─────────────────────────┐
│  ♻️ Australia Recycling ☰│  ← Header
├─────────────────────────┤
│                         │
│  Free recycling info    │  ← Eyebrow chip (green-100)
│  for all Australians    │
│                         │
│  Find recycling         │  ← Display heading
│  information            │
│  for your area          │
│                         │
│  Search by suburb,      │  ← body-lg gray-600
│  postcode or council    │
│                         │
│ ┌─────────────────────┐ │  ← SearchBar (full width)
│ │ 🔍 Search...        │ │
│ └─────────────────────┘ │
│                         │
│  Covering 500+ councils │  ← caption gray-400 centred
│─────────────────────────│
│                         │
│  How it works           │  ← h2 centred
│                         │
│  ┌───┐  ①              │
│  │ 🔍│  Search your    │  ← Step cards, stacked
│  └───┘  suburb         │
│                         │
│  ┌───┐  ②              │
│  │📍 │  See what goes  │
│  └───┘  in each bin    │
│                         │
│  ┌───┐  ③              │
│  │✓  │  Recycle right  │
│  └───┘                  │
│─────────────────────────│
│                         │
│  Browse by state        │  ← h2 centred
│  Select your state...   │  ← body-sm gray-500
│                         │
│  ┌─────┐ ┌─────┐        │
│  │ NSW │ │ VIC │        │  ← 2-col state grid on mobile
│  └─────┘ └─────┘        │
│  ┌─────┐ ┌─────┐        │
│  │ QLD │ │  SA │        │
│  └─────┘ └─────┘        │
│  ... etc                │
│                         │
│  [ View all councils ]  │  ← Secondary button, centred
│─────────────────────────│
│                         │
│  Not sure about an item?│  ← CTA section
│  Browse our materials   │
│  database               │
│  [ Browse materials ]   │  ← Primary button
│─────────────────────────│
│  [Footer]               │
└─────────────────────────┘
```

**Desktop:** Same sections but:
- Hero: 2-column — text left, subtle illustration/icon right (or centred with more breathing room)
- How it works: 3 cards side by side
- State grid: 4 columns (2 rows of 4)

**Key constraint (AC-001-1):** Search bar must be above the fold on mobile. Hero text is secondary to the search bar — if it must be cut, cut the text, not the search bar.

---

### 6.2 Council Detail Page

**Mobile:**
```
┌─────────────────────────┐
│  Header                 │
├─────────────────────────┤
│  Home / Councils /      │  ← Breadcrumb
│  City of Sydney         │
│                         │
│  City of Sydney    NSW  │  ← h1 + state badge
│                         │
│  The City of Sydney     │  ← body gray-600 description
│  covers the CBD...      │
│                         │
│  🔗 Official website    │  ← green link
│  🔗 Recycling info      │  ← green link
│─────────────────────────│
│                         │
│ ┌─────────────────────┐ │  ← Bin section: Recycling
│ │♻️ Recycling (Yellow) │ │     yellow bg + border
│ │─────────────────────│ │
│ │• Cardboard          │ │
│ │  Flatten boxes...   │ │
│ │• Paper              │ │
│ │• Glass bottles      │ │
│ │  Rinse clean...     │ │
│ │• Plastic bottles    │ │
│ │• Steel cans         │ │
│ │• Aluminium cans     │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │  ← Bin section: Green waste
│ │🌿 Green Waste        │ │     green bg + border
│ │─────────────────────│ │
│ │• Garden organics    │ │
│ │  Fortnightly...     │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │  ← Bin section: General waste
│ │🗑️ General Waste      │ │     red bg + border
│ │─────────────────────│ │
│ │• Food waste         │ │
│ │• Nappies            │ │
│ │• Polystyrene        │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │  ← Bin section: Soft plastics
│ │🛍️ Soft Plastics      │ │     purple bg + border
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │  ← Bin section: Special drop-off
│ │📍 Special Drop-off  │ │     blue bg + border
│ └─────────────────────┘ │
│                         │
│  ADVERTISEMENT          │  ← Ad unit, labelled
│  ┌─────────────────────┐│
│  │                     ││
│  └─────────────────────┘│
│                         │
│  ⚠️ Data last verified  │  ← caption gray-400 disclaimer
│  March 2026. Always     │
│  check with council.    │
├─────────────────────────┤
│  Footer                 │
└─────────────────────────┘
```

**Desktop:** Bin sections go full width (single column, max-w-4xl). Consider a sticky sidebar with a "jump to section" nav for long pages.

---

### 6.3 Search Autocomplete (overlay)

```
┌─────────────────────────────────────────────┐
│  Header                                     │
├─────────────────────────────────────────────┤
│             ┌───────────────────────────┐   │
│             │ 🔍  bondi beach      ✕    │   │  ← Input
│             └───────────────────────────┘   │
│             ┌───────────────────────────┐   │
│             │  COUNCILS                 │   │
│             │  Waverley Council  NSW  → │   │  ← Result rows
│             │───────────────────────────│   │
│             │  SUBURBS                  │   │
│             │  Bondi Beach       2026 → │   │
│             │  Bondi             2026 → │   │
│             └───────────────────────────┘   │
│                                             │
│  [rest of page dimmed/overlaid]             │
└─────────────────────────────────────────────┘
```
- Page behind search dims to `bg-black/20` when dropdown is open (mobile)
- Dropdown has max-height `360px`, scrollable if more results
- Tapping outside dismisses

---

### 6.4 Councils List Page

**Mobile:**
```
┌─────────────────────────┐
│  Header                 │
├─────────────────────────┤
│  Browse Councils        │  ← h1
│  Select your council    │  ← body-lg gray-600
│  to see local rules.    │
│                         │
│  ← scroll →            │  ← State filter pills, horizontal scroll
│  All  NSW  VIC  QLD ... │
│                         │
│  Showing 24 of 537      │  ← body-sm gray-500
│                         │
│ ┌─────────────────────┐ │
│ │ City of Sydney  NSW │ │  ← Council cards, 1-col mobile
│ │ The City of Sydney  │ │
│ │ covers the CBD...   │ │
│ │              View → │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ City of Melbourne   │ │
│ └─────────────────────┘ │
│                         │
│  [ Previous ]  1/22  [ Next ]  ← Pagination
├─────────────────────────┤
│  Footer                 │
└─────────────────────────┘
```
**Desktop:** 3-column grid for council cards.

---

### 6.5 Materials List Page

```
┌─────────────────────────┐
│  Header                 │
├─────────────────────────┤
│  What Can I Recycle?    │  ← h1
│  Browse common items    │  ← body-lg
│                         │
│  All  Paper  Plastics   │  ← Category filter pills
│  Glass  Metals ...      │
│                         │
│  Paper & Cardboard      │  ← h2 section heading
│  ────────────────────   │
│  ┌───────┐  ┌───────┐   │
│  │Cardbd │  │ Paper │   │  ← 2-col (mobile), 3-col (desktop)
│  └───────┘  └───────┘   │
│                         │
│  Plastics               │  ← h2
│  ────────────────────   │
│  ┌───────┐  ┌───────┐   │
│  │Bottles│  │Bags   │   │
│  └───────┘  └───────┘   │
└─────────────────────────┘
```

---

### 6.6 Material Detail Page

```
┌─────────────────────────┐
│  Header                 │
├─────────────────────────┤
│  Home / Materials /     │  ← Breadcrumb
│  Cardboard              │
│                         │
│  [Paper & Cardboard]    │  ← Category chip, green-100
│                         │
│  Cardboard              │  ← h1
│  Corrugated boxes,      │  ← body-lg gray-600
│  cereal boxes...        │
│                         │
│ ┌─────────────────────┐ │
│ │ ⚠️ Rules vary by     │ │  ← amber info box
│ │ council. Search your │ │
│ │ council above.       │ │
│ └─────────────────────┘ │
│                         │
│  [ Find your council →] │  ← Primary button
├─────────────────────────┤
│  Footer                 │
└─────────────────────────┘
```

---

## 7. User Flows

### Flow 1 — Find my council (primary)
```
Home
  → Type "bondi" in search bar
  → See dropdown: Suburbs → "Bondi Beach — Waverley Council"
  → Tap result
  → Council Detail: Waverley Council
  → Scan bin sections
  → Tap material link (e.g. "Cardboard")
  → Material Detail page
  → Tap "Find your council →" (returns to Waverley)
```

### Flow 2 — Browse by state
```
Home
  → Tap "NSW" in state grid
  → Councils list filtered to NSW
  → Tap "City of Sydney" card
  → Council Detail page
```

### Flow 3 — Material lookup
```
Home
  → Tap "Browse materials" CTA
  → Materials list
  → Filter by "Plastics"
  → Tap "Soft Plastics"
  → Material detail: "Take to supermarket drop-off"
  → Tap "Find your council →" to see council-specific instructions
```

---

## 8. Responsive Breakpoints

| Breakpoint | px | Layout changes |
|------------|-----|----------------|
| Mobile | 0–639px | 1-col, stacked sections, hamburger nav |
| Tablet | 640–1023px | 2-col grids, inline nav still condensed |
| Desktop | 1024px+ | 3-col grids, full nav, sidebar possible |

All layouts designed **mobile-first**. Desktop is an enhancement, not the base.

---

## 9. Accessibility Requirements

Derived from PRD: WCAG 2.1 AA.

- All interactive elements keyboard-accessible (Tab, Enter, Space, Escape, Arrow keys)
- Focus rings visible on all focusable elements (`ring-2 ring-green-500 ring-offset-2`)
- Colour is never the **only** indicator — bin sections use emoji + label + colour
- Minimum contrast: 4.5:1 for normal text, 3:1 for large text
- All images have alt text (or `aria-hidden` if decorative)
- Search results announced to screen readers via `aria-live="polite"`
- Bin section headers use `<h2>` — not `<div>` — for document outline
- Material links descriptive: "Cardboard recycling instructions", not "click here"

---

## 10. Empty & Error States

| State | Message | Action |
|-------|---------|--------|
| Search — no results | "No results for '[query]'. Try your council name or a suburb." | Clear button |
| Search — error | "Search unavailable. Try again." | Retry icon |
| Council — no data | "We don't have data for this council yet. Check their website directly." | Link to council website |
| Council — not found | 404 page | "Go home" + "Browse councils" |
| API down | Friendly error with retry | Retry button |
| Materials — empty | "No materials in this category yet." | "Browse all materials" |

---

## 11. Open Design Questions

These map to `OQ-4` and related items in `docs/PRD.md`:

| # | Question | Impact |
|---|----------|--------|
| DQ-1 | Should the council detail page show a "search this council" bar? (so user can quickly find a specific material without scrolling) | High — consider for Phase 1 if councils have many materials |
| DQ-2 | Should bin sections be collapsed by default on mobile? (accordion UX) | Medium — reduces scroll but adds interaction cost |
| DQ-3 | "Last verified" date — show on council header or bin section footer? | Low — footer preferred |
| DQ-4 | What does the AI chat widget look like on council pages? (Phase 2) | Design reserve space now |
| DQ-5 | Should the state grid use state outlines/maps instead of text tiles? | Low — text tiles are faster to build and accessible |

---

*Next: Create Figma file using this spec. All pages listed in Section 6 to be designed at 390px (iPhone 14) and 1440px (desktop). Link Figma file at top of this document once created.*
