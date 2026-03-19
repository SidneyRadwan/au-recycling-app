# Scraper

Python 3.12 scripts for seeding and maintaining council and recycling URL data.

## Scripts

| Script | Purpose |
|--------|---------|
| `seed_councils.py` | Seed council names, slugs, states, and website URLs |
| `seed_recycling_urls.py` | Discover each council's recycling/waste page URL |

---

## Seeding councils

### Full scrape (all sources live)

Scrapes state government directories, applies overrides from `council_overrides.yaml`, writes
a timestamped `councils_YYYYMMDD_HHMMSS.yaml` snapshot, and upserts into the database:

```bash
uv run python seed_councils.py --output db
```

### Seed from a YAML snapshot (when sources are down)

Skip scraping entirely and reseed the database from a previously generated YAML file:

```bash
uv run python seed_councils.py --from-file councils_20260319_143022.yaml --output db
```

### Snapshot current database state

Read all councils from the database and write to a new timestamped YAML (includes any existing
`recycling_url` values):

```bash
uv run python seed_councils.py --dump-db
```

### Limit to specific states

```bash
uv run python seed_councils.py --output db --states NSW VIC
```

### Reset before seeding

Truncates the `councils` table (cascades to `suburbs` and `council_materials`) before inserting:

```bash
uv run python seed_councils.py --output db --reset
```

---

## Discovering recycling URLs

Renders each council homepage with Playwright, scores nav links, and writes the best match.

### Discover and write to database

```bash
uv run python seed_recycling_urls.py --output db --workers 2
```

### Also update a YAML snapshot

Pass `--yaml` to populate the `recycling_url` field in an existing councils YAML alongside
the database write:

```bash
uv run python seed_recycling_urls.py --output db --workers 2 --yaml councils_20260319_143022.yaml
```

### Re-discover (clear existing URLs first)

```bash
uv run python seed_recycling_urls.py --output db --workers 2 --reset
```

---

## Manual overrides

`council_overrides.yaml` supplies corrections that can't be auto-discovered:

- **`website`** — corrects a stale or wrong homepage URL (used as the discovery seed)
- **`recycling_info_url`** — directly sets the recycling page URL, skipping discovery

These are applied on every run of both scripts.

---

## Typical full workflow

```bash
# 1. Scrape councils → creates councils_YYYYMMDD_HHMMSS.yaml
uv run python seed_councils.py --output db

# 2. Discover recycling URLs → populates recycling_url in the YAML and the database
uv run python seed_recycling_urls.py --output db --workers 2 --yaml councils_<timestamp>.yaml
```
