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
- **"LangChain workflow"** is mentioned specifically — LangChain is Python-native. LangChain4j exists for Java and has matured significantly, but has a smaller community and less documentation. This is a key decision point (see below).
- **Live scraping (MCP) vs. pre-scraped DB** — for a portfolio piece, pre-scraped + periodic refresh is simpler, more reliable, and demonstrates data pipeline skills. Live scraping is fragile and adds latency. Recommend pre-scraped with a refresh pipeline.
- **"Document build process from PM to Figma to Code"** — this is excellent for a portfolio. Shows full product lifecycle thinking, not just code. Budget time for this documentation as a first-class deliverable.

---

## Answers to Questions

### 1. Tech Stack

**Recommended stack:**

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Backend** | **Java 21 + Spring Boot 3** | User's preference, enterprise-grade, excellent for demonstrating senior-level architecture. Spring Boot 3 with virtual threads (Project Loom) is modern and performant. |
| **AI/LLM Orchestration** | **LangChain4j** | Java-native LLM framework. Supports Claude, OpenAI, and others. Has tool-calling, RAG, and agent capabilities. Less mature than Python LangChain but viable and impressive for a portfolio — shows you can work outside the "just use Python" default. |
| **Frontend** | **React 19 + TypeScript + Vite** | User's existing skills, modern tooling, fast dev experience. |
| **UI Framework** | **Tailwind CSS + shadcn/ui** | Clean, accessible components. Good mobile support out of the box. Professional look without custom design overhead. |
| **Database** | **PostgreSQL + pgvector** | Relational for structured council data. pgvector extension enables semantic search over recycling rules (useful for the AI query feature — embed recycling rules, find relevant ones by similarity). |
| **Image Recognition** | **Claude Vision API (claude-sonnet-4-6)** | Identify items from photos and recycling symbols. No need to train custom models — multimodal LLM handles this well. |
| **Web Scraping** | **Python + BeautifulSoup/Scrapy** | Even in a Java-centric project, Python is the pragmatic choice for scraping. Run as a separate data pipeline, not part of the main app. Outputs structured data into PostgreSQL. |
| **Containerization** | **Docker + Docker Compose** | Local dev and deployment. |
| **Infrastructure** | **Terraform** | IaC for GCP resources. More portfolio-relevant than Helm for this project size (see deployment answer). |

**Decided:** Java 21 + LangChain4j. Java is distinctive in a portfolio full of Python AI projects, and LangChain4j's agent/RAG capabilities align well with the requirements.

### 2. Repository Design

**Recommendation: Mono-repo.**

Reasons:
- Single project, single team (one person), shared CI/CD
- Atomic commits across frontend + backend changes
- Easier to review as a portfolio piece — one repo tells the whole story
- Simpler dependency management

**Proposed structure:**
```
australiarecycling/
├── backend/                  # Java Spring Boot API
│   ├── src/main/java/
│   ├── src/test/java/
│   ├── Dockerfile
│   └── build.gradle          # or pom.xml
├── frontend/                 # React + TypeScript + Vite
│   ├── src/
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

**Recommendation: GCP with Cloud Run (not GKE/Kubernetes).**

| Component | GCP Service | Cost Estimate |
|-----------|------------|---------------|
| Backend API | **Cloud Run** | ~$0-5/mo (scales to zero, pay per request) |
| Frontend | **Firebase Hosting** | Free tier (static files + CDN) |
| Database | **Cloud SQL (PostgreSQL) micro** | ~$7-10/mo (smallest instance) |
| Secrets | **Secret Manager** | Free tier |
| DNS | **Cloud DNS** | ~$0.20/mo |
| CI/CD | **GitHub Actions** → Cloud Build | Free tier |

**Total estimated cost: ~$10-15/month** at low traffic.

**Why Cloud Run over GKE:**
- GKE minimum cost is ~$70-100/month (cluster management fee + nodes). Overkill for this project.
- Cloud Run is containerized (still uses Docker, still demonstrates container skills) but scales to zero.
- Helm charts for a single-service app don't demonstrate much. Cloud Run + Terraform demonstrates more relevant infrastructure skills.
- If the user specifically wants to show Kubernetes/Helm skills, could add a `k8s/` directory with Helm charts as an "alternative deployment" without actually running GKE.

**Even simpler alternative — Railway or Render:**
- One-click deploys from GitHub, ~$5-7/month total
- Less impressive for a portfolio but dramatically simpler to set up
- Could use this for staging/dev and GCP for "production"

**Cheaper database alternative:**
- **Supabase** free tier gives PostgreSQL + pgvector + auth + REST API for free
- Trade-off: less "build it yourself" demonstration, but very practical

---

## Confirmed Decisions

- **Backend**: Java 21 + Spring Boot 3
- **AI Framework**: LangChain4j
- **Database**: Cloud SQL PostgreSQL (+ pgvector)
- **Approach**: Deliver features quickly in priority order, iterate. Image recognition last.

## Phased Build Plan

### Phase 1: Foundation + Council Search (deliver fast, then iterate)
- Project scaffolding: mono-repo, Docker Compose, CI pipeline (GitHub Actions)
- Spring Boot API skeleton with health checks, OpenAPI docs
- React app with routing, layout, responsive mobile-first shell (Tailwind + shadcn/ui)
- PostgreSQL schema: councils, materials, bin types, rules
- **Scrape 10-20 major councils** (Sydney, Melbourne, Brisbane, Perth, Adelaide councils) as seed data
- Council/suburb search API with autocomplete
- Recycling info display per council (what goes in which bin)
- **Deploy to Cloud Run immediately** — get it live early
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

1. **Council data quality**: Many councils publish recycling info as PDFs or in inconsistent formats. LLM-assisted extraction helps but won't be 100% accurate. Need a strategy for data validation.
2. **LangChain4j maturity**: Fewer examples and community resources than Python LangChain. May hit undocumented edges. Mitigation: Spring AI as fallback.
3. **Scope creep**: The feature list is broad. Strict phasing and "good enough" acceptance criteria are essential. A polished Phase 1-3 is better than a rough Phase 1-5.
4. **LLM costs**: Without rate limiting, a public site with AI features could generate unexpected bills. Implement hard limits early.

---

## Verification / How to Test

- **Local dev**: `docker-compose up` should bring up the full stack (frontend, backend, database)
- **Backend**: Integration tests with Testcontainers (PostgreSQL), unit tests for service layer
- **Frontend**: Vitest + React Testing Library for component tests
- **AI features**: Test with recorded prompts/responses to avoid LLM costs in CI
- **Scraper**: Test against saved HTML snapshots of council pages
- **E2E**: Playwright for critical user flows (search council → view recycling info → ask AI question)
- **Deployment**: Terraform plan in CI, deploy to staging on PR merge, production on tag
