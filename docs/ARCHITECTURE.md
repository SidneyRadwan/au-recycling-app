# Architecture Documentation
## Australia Recycling

---

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                    User's Browser                    │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────┐
│               Next.js Frontend                       │
│         (Vercel / Cloud Run)                         │
│   - SSR for SEO                                      │
│   - React 19 + TypeScript                           │
│   - Tailwind + shadcn/ui                            │
└──────────────────────┬──────────────────────────────┘
                       │ REST /api/v1/
┌──────────────────────▼──────────────────────────────┐
│           Spring Boot Backend API                    │
│              (GCP Cloud Run)                         │
│   - Java 21                                          │
│   - Spring Boot 3.x                                 │
│   - JPA + Flyway                                    │
└──────────────────────┬──────────────────────────────┘
                       │ JDBC
┌──────────────────────▼──────────────────────────────┐
│           PostgreSQL + pgvector                      │
│              (GCP Cloud SQL)                         │
│   - councils, suburbs, materials tables             │
│   - Vector embeddings (Phase 2)                     │
└─────────────────────────────────────────────────────┘

Data Pipeline:
┌─────────────────────────────────────────────────────┐
│           Python Scraper                             │
│   - BeautifulSoup / Scrapy                          │
│   - Upserts → PostgreSQL directly                   │
└─────────────────────────────────────────────────────┘
```

---

## API Design

### Base URL
- Dev: `http://localhost:8080/api/v1`
- Prod: `https://api.australiarecycling.com.au/api/v1`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/councils` | List councils (paginated, filter by state) |
| GET | `/councils/{slug}` | Council detail with materials |
| GET | `/materials` | List materials (filter by category) |
| GET | `/materials/{slug}` | Material detail |
| GET | `/search?q={q}` | Search councils, suburbs, materials |

### Response Format (Council Detail)
```json
{
  "id": 1,
  "name": "City of Sydney",
  "slug": "city-of-sydney",
  "state": "NSW",
  "website": "https://www.cityofsydney.nsw.gov.au",
  "recyclingInfoUrl": "https://www.cityofsydney.nsw.gov.au/recycling",
  "materialsByBinType": {
    "RECYCLING": [
      {
        "materialName": "Cardboard",
        "binType": "RECYCLING",
        "instructions": "Flatten boxes. Remove food residue.",
        "notes": null
      }
    ],
    "GENERAL_WASTE": [...],
    "GREEN_WASTE": [...],
    "NOT_ACCEPTED": [...]
  }
}
```

---

## Database Schema

See `backend/src/main/resources/db/migration/V1__initial_schema.sql`

Key tables:
- `councils` — LGA data (name, slug, state, website)
- `suburbs` — Suburb → council mapping
- `materials` — Recyclable/waste items
- `council_materials` — Council-specific rules per material

---

## Frontend Architecture

### Page Types
- **Static pages**: Home, About, Materials list (ISR, revalidate 1hr)
- **Dynamic SSR**: Council detail (SSR with 1hr cache), Material detail (SSR)
- **Client components**: SearchBar (autocomplete), Navigation (mobile menu)

### Data Flow
```
Server Component (page.tsx)
  → fetch from Spring Boot API (server-side)
  → render full HTML (SSR for SEO)
  → hydrate client components (SearchBar)
    → fetch /api/v1/search?q= (client-side)
    → render dropdown results
```

---

## Infrastructure

### Development
- `docker-compose up` — starts db, backend, frontend
- pgvector/pgvector:pg16 Docker image for database

### Production (GCP)
- **Frontend**: Vercel (free tier) or Cloud Run
- **Backend**: Cloud Run (auto-scaling, min 0 instances)
- **Database**: Cloud SQL PostgreSQL micro (~$7/mo)
- **Secrets**: GCP Secret Manager for API keys
- **DNS**: Cloud DNS → australiarecycling.com.au

### CI/CD
- GitHub Actions on push to main / PRs
- Jobs: backend-test (with Postgres service), frontend-build, scraper-test
- Future: deploy to Cloud Run on main merge

---

## Phase 2: RAG + AI Agent (Planned)

```
User query → Spring Boot → LangChain4j
  → Embed query (Claude API)
  → pgvector similarity search (council_materials)
  → Claude API with RAG context
  → Structured recycling answer
```
