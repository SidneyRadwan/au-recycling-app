# Australia Recycling Website - Initial Plan

## Context

Build a public-facing website at australiarecycling.com.au that helps Australians find recycling information for their local council area. The project has a dual purpose: (1) solve a real problem — recycling rules are fragmented across hundreds of council websites, and (2) serve as a senior engineer portfolio piece demonstrating AI coding, architecture, and best practices.

---

## Notes on the Prompt

**Strengths of the concept:**
- Clear problem statement with genuine user value — recycling info in Australia really is fragmented across ~537 local government areas
- Good balance of features: basic utility (search), modern AI (text query agent), and advanced (image recognition)
- The portfolio framing is smart — it naturally motivates production-quality code, documentation, and clean architecture

**Considerations & tensions:**
- **Scope is ambitious.** AI text agent + image recognition + web scraping + cost tracking + mobile support is a lot. A phased approach is essential to avoid a half-finished project that doesn't demonstrate anything well.
- **Data scraping is the hardest part**, not the code. Council websites vary wildly in structure, many are PDFs, and some info is buried in downloadable guides. Starting with well-structured councils and augmenting with LLM-assisted extraction is the pragmatic path.
- **LangChain4j** is less documented than Python LangChain but has matured significantly. Spring AI is the fallback if we hit blockers.
- **Pre-scraped DB over live scraping.** Pre-scraped + periodic refresh is simpler, more reliable, and demonstrates data pipeline skills. Live scraping is fragile and adds latency.
- **"Document build process from PM to Figma to Code"** — excellent for a portfolio. Shows full product lifecycle thinking, not just code. Budget time for this as a first-class deliverable.

---

## Confirmed Decisions

- **Backend**: Java 21 + Spring Boot 3
- **AI Framework**: LangChain4j
- **Database**: Cloud SQL PostgreSQL (+ pgvector)
- **Frontend**: React 19 + TypeScript + Next.js (for SSR/SEO — see SEO section)
- **Approach**: Deliver features quickly in priority order, iterate. Image recognition last.

---

## SEO Strategy

The website targets Australians searching for recycling info — SEO is critical for organic traffic.

### Frontend: Next.js over Vite

**Vite produces a client-side SPA** — search engines see an empty `<div id="root">` on first load. This kills SEO for content-heavy pages. **Next.js** provides:
- **Server-side rendering (SSR)** and **static site generation (SSG)** — search engines see full HTML
- Built-in `<Head>` management for meta tags, Open Graph
- File-based routing that naturally creates clean, indexable URLs
- Image optimization (next/image) for Core Web Vitals
- Still React + TypeScript — same skills, better SEO output

This is the single most impactful architectural decision for SEO.

### SEO requirements to build into Phase 1:
- **Council-specific URLs**: `/councils/city-of-sydney`, `/councils/city-of-melbourne` — each indexable
- **Material-specific pages**: `/materials/styrofoam`, `/materials/soft-plastics` — target "can I recycle X" searches
- **Structured data (JSON-LD)**: `FAQPage`, `HowTo`, and `LocalBusiness` schemas for rich snippets
- **Meta tags + Open Graph**: per-page titles, descriptions, social sharing cards
- **sitemap.xml** and **robots.txt**: auto-generated from council/material data
- **Fast load times**: static generation where possible, CDN delivery
- **Mobile-first design**: Google uses mobile-first indexing

### Repo naming — avoid SEO conflict

**Recommended repo name: `au-recycling-app`** (or `recycle-mate`, `binwise`, etc.)

If the GitHub repo is named `australiarecycling`, it will compete with australiarecycling.com.au in search results — GitHub repos rank well in Google. You'd cannibalise your own SEO. The repo should be findable by portfolio reviewers (who'll have a direct link), not compete for organic "australia recycling" searches.

---

## Answers to Questions

### 1. Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Backend** | **Java 21 + Spring Boot 3** | Enterprise-grade, virtual threads (Loom), strong for senior-level portfolio. |
| **AI/LLM** | **LangChain4j** | Java-native LLM framework with agent, RAG, and tool-calling support. Distinctive choice vs. Python default. |
| **Frontend** | **React 19 + TypeScript + Next.js** | SSR/SSG for SEO. Still React + TS. Replaces Vite for production SEO needs. |
| **UI** | **Tailwind CSS + shadcn/ui** | Clean, accessible, mobile-first. Professional look without custom design overhead. |
| **Database** | **PostgreSQL + pgvector** | Relational for council data. pgvector enables semantic search for RAG pipeline. |
| **Image Recognition** | **Claude Vision API** | Identify items from photos and recycling symbols. No custom model training needed. |
| **Web Scraping** | **Python + BeautifulSoup/Scrapy** | Pragmatic choice even in Java project. Separate data pipeline, outputs to PostgreSQL. |
| **Containerization** | **Docker + Docker Compose** | Local dev and deployment. |
| **Infrastructure** | **Terraform** | IaC for GCP resources. |

### 2. Repository Design

**Mono-repo** — single project, single developer, shared CI/CD, atomic commits, one repo tells the portfolio story.

**Repo name: `au-recycling-app`** (to avoid SEO conflict with the domain)

```
au-recycling-app/
├── backend/                  # Java Spring Boot API
│   ├── src/main/java/
│   ├── src/test/java/
│   ├── Dockerfile
│   └── build.gradle
├── frontend/                 # React + TypeScript + Next.js
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/
│   │   └── lib/
│   ├── Dockerfile
│   └── package.json
├── scraper/                  # Python data pipeline
│   ├── scrapers/             # Per-council scrapers
│   ├── processors/           # LLM-assisted data extraction
│   └── requirements.txt
├── infrastructure/           # Terraform + Docker Compose
│   ├── terraform/
│   ├── docker-compose.yml
│   └── docker-compose.dev.yml
├── docs/                     # Build process documentation
│   ├── 01-product-requirements.md
│   ├── 02-design-figma.md
│   ├── 03-architecture.md
│   └── 04-deployment.md
├── .github/workflows/        # CI/CD
├── CLAUDE.md                 # AI assistant context
└── README.md
```

### 3. Deployment

**GCP with Cloud Run (not GKE).**

| Component | GCP Service | Cost Estimate |
|-----------|------------|---------------|
| Backend API | **Cloud Run** | ~$0-5/mo (scales to zero) |
| Frontend | **Cloud Run** or **Vercel** | Free-$0/mo (Next.js on Vercel free tier is ideal; Cloud Run works too) |
| Database | **Cloud SQL PostgreSQL micro** | ~$7-10/mo |
| Secrets | **Secret Manager** | Free tier |
| DNS | **Cloud DNS** | ~$0.20/mo |
| CI/CD | **GitHub Actions** | Free tier |

**Total: ~$10-15/month** at low traffic.

Cloud Run over GKE: GKE minimum ~$70-100/month is overkill. Cloud Run still demonstrates containerization skills but scales to zero. Helm charts can be included in `k8s/` as an alternative deployment showcase without running GKE.

**Note on frontend hosting:** Next.js on Vercel's free tier is the simplest option with excellent performance. If the user wants everything on GCP, Cloud Run handles Next.js SSR fine.

---

## Phased Build Plan

### Phase 1: Foundation + Council Search (get it live fast)
- Project scaffolding: mono-repo, Docker Compose, CI pipeline (GitHub Actions)
- Spring Boot API skeleton with health checks, OpenAPI docs
- Next.js app with routing, layout, responsive mobile-first shell (Tailwind + shadcn/ui)
- PostgreSQL schema: councils, materials, bin types, rules
- **SEO foundation**: SSR pages, meta tags, structured data, sitemap, robots.txt
- **Scrape 10-20 major councils** (Sydney, Melbourne, Brisbane, Perth, Adelaide councils) as seed data
- Council/suburb search API with autocomplete
- Recycling info display per council (what goes in which bin)
- Council-specific URLs (`/councils/city-of-sydney`) and material pages (`/materials/styrofoam`)
- **Deploy immediately** — get it live and indexable early
- Material search ("can I recycle X?") — database-driven, no AI yet

### Phase 2: AI Text Agent
- LangChain4j integration with Claude API
- RAG pipeline: embed council recycling rules with pgvector, retrieve relevant context
- Conversational agent: "Is styrofoam recyclable in City of Sydney?"
- SOP/prompt templates for common question patterns
- LLM cost tracking: log token usage per request, store in DB

### Phase 3: LLM Cost Dashboard + Expand Data
- Cost management dashboard UI (usage graphs, budget alerts, per-query cost)
- Rate limiting and budget caps
- Expand council coverage — scrape more councils, refine data quality
- Data validation and correction workflow

### Phase 4: Image Recognition (last)
- Image upload UI (camera + file upload, mobile-optimized)
- Claude Vision integration: identify item from photo
- Recycling symbol/label recognition
- Cross-reference identified item with council rules

### Phase 5: Polish & Documentation
- Performance optimization, caching
- Full build process documentation (PM → Design → Code)
- Architecture diagrams, demo video
- Production hardening (error handling, monitoring, logging)
- README and contribution guide

---

## Key Risks

1. **Council data quality**: Many councils publish recycling info as PDFs or in inconsistent formats. LLM-assisted extraction helps but won't be 100% accurate. Need a data validation strategy.
2. **LangChain4j maturity**: Fewer examples and community resources than Python LangChain. May hit undocumented edges. Mitigation: Spring AI as fallback.
3. **Scope creep**: A polished Phase 1-3 is better than a rough Phase 1-5. Strict phasing and "good enough" criteria are essential.
4. **LLM costs**: Without rate limiting, a public site with AI features could generate unexpected bills. Implement hard limits early.

---

## Verification / How to Test

- **Local dev**: `docker-compose up` brings up the full stack (frontend, backend, database)
- **Backend**: Integration tests with Testcontainers (PostgreSQL), unit tests for service layer
- **Frontend**: Vitest + React Testing Library for component tests
- **SEO**: Lighthouse audits, structured data testing tool, mobile-friendly test
- **AI features**: Test with recorded prompts/responses to avoid LLM costs in CI
- **Scraper**: Test against saved HTML snapshots of council pages
- **E2E**: Playwright for critical user flows (search council → view recycling info → ask AI question)
- **Deployment**: Terraform plan in CI, deploy to staging on PR merge, production on tag
