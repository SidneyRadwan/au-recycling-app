# Product Requirements Document
## Australia Recycling — australiarecycling.com.au

| Field | Value |
|-------|-------|
| **Author** | Product Manager (AI Agent) |
| **Version** | 1.1 |
| **Date** | March 2026 |
| **Status** | Approved — Phase 1 in development |
| **Next review** | After Phase 1 launch |

---

## 1. Executive Summary

Australia has ~537 local government areas (LGAs), each with their own recycling rules. What goes in the yellow bin in Sydney differs from Melbourne, which differs from Brisbane. There is no single authoritative source a resident can go to. This causes contamination (wrong items in wrong bins), which costs councils millions annually and reduces the value of recycled material.

**australiarecycling.com.au** solves this by aggregating recycling information from all Australian councils into a single, fast, searchable website. Users search by suburb, postcode, or council name and immediately see what goes in each bin — colour-coded to match the physical bins in their street.

**Dual purpose:** The site solves a genuine user problem AND demonstrates a senior engineer's ability to own the full product lifecycle: from problem definition to design, architecture, data pipeline, AI integration, and production deployment.

---

## 2. Problem Statement

### The problem
- A resident wants to know: *"Can I put my pizza box in the recycling bin?"* The answer depends entirely on their council. Many councils accept clean pizza boxes; some don't. There is no easy way to find out without navigating to the correct council's website — if the information exists online at all.
- Many Australians recycle by guessing. This leads to **wishcycling** — putting items in the recycling bin in hope, which contaminates entire loads and results in them going to landfill.
- Council websites are not designed for quick lookups. Information is buried, outdated, or formatted as downloadable PDFs.

### The scale
- ~537 LGAs across Australia
- Approx. 10.6 million households
- Recycling contamination costs Australia an estimated $300M+ per year
- Most common contaminated items: soft plastics, food waste, glass

### The opportunity
- High-intent search traffic: "recycling [suburb]", "can I recycle [item]", "[council] bin rules" — these are underserved keyword clusters
- No incumbent with good SEO and structured data
- LLM + vision AI can extract and standardise council data at scale

---

## 3. Goals and Non-Goals

### Goals
| # | Goal | Type |
|---|------|------|
| G1 | Users can find their council's bin rules in < 30 seconds | User |
| G2 | Every council page is indexable and ranks for its council name + "recycling" | Business (SEO) |
| G3 | Cover 100+ councils within 3 months of launch | Data |
| G4 | Cover all 537 LGAs within 12 months | Data |
| G5 | Site is self-sustaining (ad revenue ≥ hosting costs) within 6 months | Revenue |
| G6 | Demonstrate PM → Design → Code lifecycle for portfolio | Portfolio |

### Non-Goals (Phase 1)
- Real-time bin collection day schedules
- User accounts, saved preferences, or personalisation
- Council data submission portal for council staff
- Mobile app (PWA-ready responsive web is sufficient for now)
- AI features (Phase 2+)
- Image recognition (Phase 4)

---

## 4. User Personas

### Persona 1 — The Confused Recycler (primary)
**Name:** Maya, 34, Sydney
**Context:** Renting in a flat. Just finished a box of wine, has some bottle tops and a greasy pizza box.
**Goal:** Quickly find out what goes where without reading a PDF.
**Pain point:** Her council's website hasn't been updated since 2019.
**Device:** Mobile, usually while standing next to the bin.
**Success:** Finds her answer in two taps and bins it correctly.

### Persona 2 — The Recent Mover (primary)
**Name:** Tom, 28, just moved from Melbourne to Brisbane
**Context:** Used to a different bin system. Not sure if the rules are the same.
**Goal:** Get up to speed on his new council's rules quickly.
**Pain point:** Brisbane's website is hard to navigate on mobile.
**Success:** Searches his suburb, sees a clean colour-coded breakdown, bookmarks the page.

### Persona 3 — The Environmentally Conscious Parent (secondary)
**Name:** Sarah, 42, Canberra
**Context:** Wants to teach her kids to recycle correctly.
**Goal:** Find clear, trustworthy information to share with family.
**Pain point:** Conflicting advice online; unsure what's current.
**Success:** Shares the council page link with her household group chat.

### Persona 4 — The Portfolio Reviewer (meta)
**Name:** Engineering hiring manager or technical recruiter
**Context:** Reviewing the GitHub repo as part of a job application.
**Goal:** Assess full-stack, AI, and product thinking capability.
**Success:** Sees clear PM → Design → Code documentation, live product, and production-quality code.

---

## 5. User Stories & Acceptance Criteria

### Phase 1 — Foundation + Council Search

---

**US-001 — Suburb/Council Search**
> *As an Australian resident, I want to search by suburb, postcode, or council name so I can quickly find my council's recycling information.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-001-1 | Search bar is prominently placed on the home page above the fold on mobile |
| AC-001-2 | Autocomplete activates after ≥ 2 characters |
| AC-001-3 | Suggestions are debounced (300ms) to avoid excessive API calls |
| AC-001-4 | Results are grouped into three sections: Councils, Suburbs, Materials |
| AC-001-5 | API responds in < 500ms for all search queries |
| AC-001-6 | Selecting a suburb result navigates to that suburb's council page |
| AC-001-7 | Selecting a council result navigates to the council's detail page |
| AC-001-8 | Keyboard navigation works (arrow keys, Enter, Escape) |
| AC-001-9 | "No results" state is shown clearly; does not show an empty dropdown |
| AC-001-10 | Search works on mobile and desktop |

---

**US-002 — Council Recycling Information Page**
> *As a user who found my council, I want to see a clear, colour-coded list of what goes in each bin.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-002-1 | Page URL follows pattern `/councils/{slug}` (e.g. `/councils/city-of-sydney`) |
| AC-002-2 | Materials are grouped by bin type |
| AC-002-3 | Each bin section is colour-coded to match physical bin lid colours: Yellow (recycling), Red (general waste), Green (garden/FOGO), Purple (soft plastics), Blue (special drop-off), Grey (not accepted) |
| AC-002-4 | Each material lists any specific instructions (e.g. "flatten cardboard", "rinse containers") |
| AC-002-5 | A link to the official council recycling page is displayed |
| AC-002-6 | Page renders full HTML server-side (SSR) — not a loading spinner |
| AC-002-7 | Page includes correct `<title>` and `<meta description>` |
| AC-002-8 | Page includes FAQPage JSON-LD structured data |
| AC-002-9 | Page shows council name, state, and brief description |
| AC-002-10 | If a council has no data yet, a helpful "no data" state is shown (not a broken page) |

---

**US-003 — Material Lookup**
> *As a user, I want to search for a specific item (e.g. "pizza box") and find out if and how I can recycle it.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-003-1 | Material pages exist at `/materials/{slug}` |
| AC-003-2 | Material page shows name, category, and description |
| AC-003-3 | A prominent call-to-action directs users to search for their council |
| AC-003-4 | Material pages are included in sitemap.xml |
| AC-003-5 | Material page has correct SEO metadata (title: "Can I recycle [Material]?") |
| AC-003-6 | Materials list page at `/materials` allows filtering by category |

---

**US-004 — Browse by State**
> *As a user, I want to browse councils by state to explore recycling information.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-004-1 | Home page includes a state grid with all 8 states/territories |
| AC-004-2 | Clicking a state navigates to `/councils?state=NSW` (or equivalent) |
| AC-004-3 | Councils list page filters correctly by state |
| AC-004-4 | Councils list page is paginated (24 per page) |
| AC-004-5 | State filter visually highlights the active state |

---

**US-005 — SEO Foundation**
> *As the site owner, I want every council page to be fully indexable so that Google ranks us for "[council name] recycling" searches.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-005-1 | `/sitemap.xml` is auto-generated and includes all council and material URLs |
| AC-005-2 | `/robots.txt` allows all crawlers and references the sitemap |
| AC-005-3 | All pages have unique `<title>` tags |
| AC-005-4 | All pages have unique `<meta name="description">` tags |
| AC-005-5 | Council and material pages include JSON-LD structured data |
| AC-005-6 | Lighthouse SEO score ≥ 95 on council detail pages |
| AC-005-7 | Lighthouse performance score ≥ 85 on council detail pages |
| AC-005-8 | Core Web Vitals: LCP < 2.5s, CLS < 0.1 |

---

### Phase 2 — AI Text Agent *(future)*

**US-006 — Conversational Recycling Questions**
> *As a user, I want to ask natural language questions like "Can I recycle a pizza box in Sydney?" and get a helpful answer.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-006-1 | A chat interface is accessible from council pages |
| AC-006-2 | The agent uses RAG to retrieve council-specific data before answering |
| AC-006-3 | Answers cite the council they are based on |
| AC-006-4 | LiteLLM proxy routes requests; provider is configurable via env var |
| AC-006-5 | Each request logs token usage and estimated cost |
| AC-006-6 | Rate limiting: max 5 AI queries per IP per minute |
| AC-006-7 | Budget cap: AI queries halt if daily spend exceeds configurable limit |

---

### Phase 3 — Cost Dashboard *(future)*

**US-007 — LLM Cost Visibility**
> *As the site operator, I want to see how much AI queries are costing me so I can manage spend.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-007-1 | Dashboard shows daily/weekly/monthly AI spend |
| AC-007-2 | Per-query cost is visible |
| AC-007-3 | Budget alert fires when 80% of monthly limit is reached |
| AC-007-4 | Hard cap disables AI features when monthly limit is hit |

---

### Phase 4 — Image Recognition *(future)*

**US-008 — Photo Recycling Check**
> *As a user, I want to take a photo of an item to find out if and how it can be recycled in my area.*

| # | Acceptance Criterion |
|---|----------------------|
| AC-008-1 | Camera and file upload both supported |
| AC-008-2 | Claude Vision identifies the item |
| AC-008-3 | Result is cross-referenced with user's council rules |
| AC-008-4 | Works on mobile (camera API) |
| AC-008-5 | Recycling symbols/numbers identified if visible |

---

## 6. Information Architecture

```
australiarecycling.com.au/
├── /                           Home — search bar + state grid
├── /councils                   Councils list (paginated, filterable by state)
├── /councils/{slug}            Council detail — bin sections, materials
├── /materials                  Materials list (filterable by category)
├── /materials/{slug}           Material detail
├── /about                      About the site (Phase 5)
├── /sitemap.xml                Auto-generated
└── /robots.txt                 Auto-generated
```

---

## 7. Business Model

**Ad-supported, free to users.**

- Non-intrusive display ads (no popups, no autoplay, no interstitials)
- Ad networks: Google AdSense (Phase 1), Carbon Ads (Phase 3 — developer/eco audience fit)
- User-facing transparency note on every page: *"This site is free to use. Small ads help cover our hosting and AI costs."*
- Estimated break-even: ~5,000 monthly active users at typical RPM

**Revenue model does not compromise UX.** Ads are placed below the fold on detail pages and in the footer. Core content is always visible without scrolling past ads.

---

## 8. SEO Strategy

SEO is the primary growth channel. No paid acquisition budget.

| Signal | Approach |
|--------|----------|
| Technical SEO | Next.js SSR — full HTML on first load, no SPA shell |
| URL structure | `/councils/city-of-sydney` — clean, indexable, shareable |
| Structured data | FAQPage, HowTo JSON-LD on council/material pages |
| Content depth | Per-material instructions, not just yes/no |
| Internal linking | Council → suburbs → materials, materials → councils |
| Sitemap | Auto-generated from database, submitted to Google Search Console |
| Page speed | Static generation where possible, ISR with 1h revalidation |
| Target keywords | "[council name] recycling", "can I recycle [item]", "[suburb] bin rules" |

---

## 9. Non-Functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Page load (LCP) | < 2.5s | Measured on council detail page, 4G mobile |
| Lighthouse Performance | ≥ 85 | |
| Lighthouse SEO | ≥ 95 | |
| Lighthouse Accessibility | ≥ 90 | WCAG 2.1 AA |
| Mobile responsive | Yes | Mobile-first design |
| Uptime | 99% | Cloud Run auto-scaling |
| API response time | < 500ms (p95) | Search endpoint |
| Data freshness | Council data reviewed quarterly | Manual + scraper refresh |

---

## 10. Data Strategy

**Phase 1 — Seed data (manual + static scrapers)**
- 10–20 major councils seeded via Python static data scrapers
- SQL migration seeds materials table with 26+ common items
- Councils prioritised by population: Sydney, Melbourne, Brisbane, Perth, Adelaide + inner suburbs

**Phase 2 — Scraper pipeline**
- Python BeautifulSoup/Scrapy scrapers per council
- LLM-assisted extraction for unstructured content (PDFs, tables)
- Upsert to PostgreSQL via `scraper/db.py`

**Phase 3 — Scale**
- Target all 537 LGAs
- Automated freshness checks — detect if council page has changed
- Data quality score per council

---

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Council data quality varies wildly (PDFs, inconsistent formats) | High | High | LLM-assisted extraction; manual validation for top 50 councils |
| LLM costs spike unexpectedly | Medium | High | Rate limiting + hard budget cap from day one |
| LangChain4j / LiteLLM integration complexity | Medium | Medium | LiteLLM proxy abstracts the model layer; Spring AI as Java fallback |
| Scope creep delays Phase 1 launch | High | Medium | Strict phasing; "good enough" acceptance criteria; deploy early |
| Council websites change structure, breaking scrapers | Medium | Medium | Scrapers are per-council; static data as fallback |
| Low organic traffic initially | High | Low | Expected — SEO is a 3–6 month play; launch early to start indexing |

---

## 12. Success Metrics

| Metric | 1-month | 3-month | 6-month |
|--------|---------|---------|---------|
| Councils covered | 20 | 100 | 300 |
| Organic impressions | 1,000 | 10,000 | 50,000 |
| Monthly active users | 200 | 1,000 | 5,000 |
| Avg. session duration | > 30s | > 60s | > 90s |
| Lighthouse SEO | ≥ 95 | ≥ 95 | ≥ 95 |
| Ad revenue vs. hosting cost | 0% | 20% | 80% |

---

## 13. Open Questions

| # | Question | Owner | Due |
|---|----------|-------|-----|
| OQ-1 | Which ad network to integrate first — AdSense or Carbon Ads? | PM | Phase 3 |
| OQ-2 | Do we need a "last verified" date on council data to maintain user trust? | PM | Phase 1 launch |
| OQ-3 | How to handle councils that actively restrict scraping? | Engineering | Phase 2 |
| OQ-4 | Claude-to-Figma integration workflow — how to generate design assets? | Design | Before Phase 1 UI build |
| OQ-5 | Should material pages show which councils accept/reject them? (cross-reference table) | PM | Phase 2 |

---

## 14. Phased Roadmap

```
Phase 1 — Foundation + Council Search
  ├── Project scaffold (done)
  ├── PM document (this document)
  ├── Design — Figma (in progress)
  ├── Backend: Spring Boot API + Flyway migrations
  ├── Frontend: Next.js SSR, search, council/material pages
  ├── Scraper: seed 10–20 councils
  ├── Infrastructure: Docker Compose, CI/CD, Cloud Run deploy
  └── LAUNCH

Phase 2 — AI Text Agent
  ├── LiteLLM proxy service (docker-compose sidecar)
  ├── RAG pipeline with pgvector
  ├── Conversational agent on council pages
  └── Cost tracking per query

Phase 3 — Cost Dashboard + Data Expansion
  ├── LLM cost dashboard UI
  ├── Budget caps + rate limiting
  └── Expand to 100+ councils

Phase 4 — Image Recognition
  └── Claude Vision — photo → recycling advice

Phase 5 — Polish + Documentation
  └── Architecture diagrams, demo video, production hardening
```

---

*This document was authored as part of the PM → Design → Code workflow. The next step is `docs/DESIGN.md` — wireframes and component specifications for handoff to Figma.*
