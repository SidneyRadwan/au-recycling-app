# Australia Recycling

> Helping Australians find recycling information by council area.

Recycling rules are fragmented across ~537 local government areas in Australia. This site surfaces them in one place at [australiarecycling.com.au](https://australiarecycling.com.au).

## Quick Start

### Prerequisites
- Docker & Docker Compose
- **Or** Java 21, Node.js 20, Python 3.12, PostgreSQL 16

### Using Docker Compose (recommended)

```bash
cp .env.example .env
docker-compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Database: localhost:5432

### Using Dev Container

Open in VS Code with the Dev Containers extension, or launch in GitHub Codespaces. Everything is pre-configured.

### Manual Setup

```bash
# Backend
cd backend
./gradlew bootRun

# Frontend
cd frontend
npm install
npm run dev

# Scraper
cd scraper
pip install -r requirements.txt
python main.py
```

## Project Structure

```
au-recycling-app/
├── backend/           # Java Spring Boot API
├── frontend/          # Next.js (React + TypeScript)
├── scraper/           # Python data pipeline
├── infrastructure/    # Terraform + Docker Compose
├── docs/              # Documentation
├── .github/workflows/ # CI/CD
└── .devcontainer/     # Dev container config
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Java 21 + Spring Boot 3 |
| Frontend | React 19 + TypeScript + Next.js |
| UI | Tailwind CSS + shadcn/ui |
| Database | PostgreSQL + pgvector |
| AI/LLM | LangChain4j (Claude API) |
| Infrastructure | Docker, Terraform, GCP Cloud Run |

## License

MIT
