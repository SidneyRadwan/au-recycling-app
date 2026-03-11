# Design Specification
## Australia Recycling — australiarecycling.com.au

| Field | Value |
|-------|-------|
| **Author** | Designer (AI Agent) |
| **Version** | 0.1 — Placeholder |
| **Status** | ⏳ In progress — awaiting Claude → Figma integration |
| **Depends on** | `docs/PRD.md` v1.1 (approved) |

---

## Status

The PM document (`docs/PRD.md`) is complete and approved.

This document will contain:
- Wireframes for all pages (home, council detail, materials, search)
- Component inventory with states (default, hover, active, loading, error)
- Colour system, typography scale, spacing system
- Mobile and desktop layouts
- User flow diagrams
- Figma file link

**Blocked on:** Claude → Figma integration setup. Once resolved, this document and the linked Figma file will be completed before any frontend UI work is finalised.

---

## Design Tokens (preliminary)

These have been established in the code scaffold and will be formalised in Figma:

### Colours
| Token | Value | Usage |
|-------|-------|-------|
| `green-600` | `#16a34a` | Primary CTA, links, active states |
| `green-50` | `#f0fdf4` | Hero background, hover fills |
| `green-100` | `#dcfce7` | Badges, chips |
| `yellow-50` | `#fefce8` | Recycling bin section |
| `yellow-300` | `#fde047` | Recycling bin border |
| `red-50` | `#fef2f2` | General waste bin section |
| `green-50` (dark) | `#f0fdf4` | Green waste bin section |
| `purple-50` | `#faf5ff` | Soft plastics section |
| `blue-50` | `#eff6ff` | Special drop-off section |
| `gray-50` | `#f9fafb` | Not accepted section |

### Typography
| Role | Font | Size | Weight |
|------|------|------|--------|
| Display heading | Inter / system-ui | 48px (mobile: 36px) | 700 |
| Page title | Inter | 30px | 700 |
| Section heading | Inter | 24px | 600 |
| Body | Inter | 16px | 400 |
| Small / meta | Inter | 14px | 400 |
| Label / badge | Inter | 12px | 500 |

### Spacing
- Base unit: 4px
- Component padding: 16px / 24px
- Section gaps: 40px / 64px
- Max content width: 1280px (7xl)

---

## Pages to Design

| Page | Priority | Status |
|------|----------|--------|
| Home (hero + search) | P0 | ⏳ Pending Figma |
| Council detail | P0 | ⏳ Pending Figma |
| Search results / autocomplete | P0 | ⏳ Pending Figma |
| Councils list | P1 | ⏳ Pending Figma |
| Materials list | P1 | ⏳ Pending Figma |
| Material detail | P1 | ⏳ Pending Figma |
| 404 | P2 | ⏳ Pending Figma |
| About | P3 | ⏳ Pending Figma |

---

*This document will be updated once the Claude → Figma workflow is established. See `OQ-4` in `docs/PRD.md`.*
