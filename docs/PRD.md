# Product Requirements Document
## Australia Recycling

**Version:** 1.0
**Date:** March 2026
**Status:** Phase 1 — Active Development

---

## Problem Statement

Australians want to recycle correctly but recycling rules vary significantly across ~537 local government areas. There is no single source of truth. The result: contamination, confusion, and recyclables ending up in landfill.

---

## Goals

1. **User goal:** Find out what goes in which bin for my council area in under 30 seconds.
2. **Business goal:** Build a high-quality, SEO-friendly site that demonstrates full-stack engineering capability.
3. **Revenue goal:** Cover hosting costs (~$15/mo) via non-intrusive ads.

---

## User Stories

### Phase 1: Foundation + Council Search

**US-001: Suburb/council search**
> As an Australian resident, I want to search by my suburb, postcode, or council name so I can quickly find my council's recycling information.

Acceptance criteria:
- Search bar with autocomplete (debounced, ≥2 characters)
- Results grouped by: Councils, Suburbs, Materials
- Selecting a suburb navigates to the relevant council page
- Response time < 500ms

**US-002: Council recycling info**
> As a user who found my council, I want to see a clear, colour-coded list of what goes in each bin.

Acceptance criteria:
- Materials grouped by bin type (yellow/recycling, red/general, green/garden, etc.)
- Colour-coded sections matching bin lid colours
- Instructions per material (e.g. "flatten cardboard", "rinse containers")
- Link to official council recycling page

**US-003: Material lookup**
> As a user, I want to search for a specific item (e.g. "pizza box") to find out if and how I can recycle it.

Acceptance criteria:
- Material pages at `/materials/{slug}`
- Shows which bin type it goes in
- Shows any special instructions

**US-004: Browse by state**
> As a user, I want to browse councils by state to explore recycling information.

Acceptance criteria:
- State filter on councils list page
- 8 Australian states/territories supported

---

## Phase 2: AI Text Agent (Future)

**US-005: Conversational recycling questions**
> As a user, I want to ask natural language questions like "Can I recycle a pizza box?" and get a helpful answer.

---

## Phase 4: Image Recognition (Future)

**US-006: Photo recycling check**
> As a user, I want to take a photo of an item and be told whether and how it can be recycled in my area.

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Page load (LCP) | < 2.5s |
| Lighthouse performance | > 85 |
| Lighthouse SEO | > 95 |
| Mobile responsive | Yes |
| Accessibility | WCAG 2.1 AA |
| Uptime | 99% |

---

## Out of Scope (Phase 1)

- User accounts / saved preferences
- Push notifications for bin collection days
- Real-time collection schedules
- Council admin portal
- AI chat agent (Phase 2)
- Image recognition (Phase 4)

---

## SEO Strategy

- SSR via Next.js for all council and material pages
- URL structure: `/councils/{slug}`, `/materials/{slug}`
- JSON-LD structured data (FAQPage, HowTo)
- Sitemap.xml auto-generated from database
- Target keywords: "recycling [suburb name]", "can I recycle [item]", "[council] recycling rules"

---

## Success Metrics

| Metric | 3-month target |
|--------|----------------|
| Organic search impressions | 10,000/mo |
| Councils indexed | 100+ |
| Monthly active users | 1,000+ |
| Avg. session duration | > 1 min |
