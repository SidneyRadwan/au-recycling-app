# Australia Recycling App

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
