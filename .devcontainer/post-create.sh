#!/usr/bin/env bash
set -euo pipefail

# Frontend dependencies
cd /workspace/frontend && bun install

# Scraper dependencies (uses cached packages from Dockerfile layer)
cd /workspace/scraper && uv sync && uv run playwright install chromium

# Git hooks
cd /workspace && pre-commit install && pre-commit install-hooks

# Wait for Postgres then run migrations
echo "Waiting for database..."
until bash -c "echo > /dev/tcp/db/5432" 2>/dev/null; do sleep 1; done
echo "Database ready — running migrations"
set -a && . /workspace/.env 2>/dev/null; set +a
cd /workspace/backend && ./gradlew flywayMigrate --quiet --no-daemon
