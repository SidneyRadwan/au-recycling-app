# Scraper

Python 3.12 scripts for seeding and maintaining council and recycling URL data.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/seed_councils.py` | Seed council names, slugs, states, and website URLs |
| `scripts/seed_recycling_urls.py` | Discover each council's recycling/waste page URL |
| `scripts/seed_materials.py` | Scrape recycling material data for each council |
| `scripts/seed_suburbs.py` | Seed suburb → council mapping |
| `scripts/councils_yaml.py` | Dump DB to YAML snapshot or load a snapshot into the DB |

---

## Seeding councils

### Full scrape (all sources live)

Scrapes state government directories, applies overrides from `council_overrides.yaml`, and upserts into the database:

```bash
uv run python scripts/seed_councils.py --output db
```

### YAML snapshot utilities

Dump the current DB state to a timestamped YAML, or restore from a snapshot (including recycling URLs):

```bash
uv run python scripts/councils_yaml.py dump
uv run python scripts/councils_yaml.py dump --output councils_custom.yaml
uv run python scripts/councils_yaml.py load councils_20260319_032617.yaml
```

### Limit to specific states

```bash
uv run python scripts/seed_councils.py --output db --states NSW VIC
```

### Reset before seeding

Truncates the `councils` table (cascades to `suburbs` and `council_materials`) before inserting:

```bash
uv run python scripts/seed_councils.py --output db --reset
```

---

## Discovering recycling URLs

Renders each council homepage with Playwright, scores nav links, and writes the best match.

### Discover and write to database

```bash
uv run python scripts/seed_recycling_urls.py --output db --workers 2
```

### Also update a YAML snapshot

Pass `--yaml` to populate the `recycling_url` field in an existing councils YAML alongside
the database write:

```bash
uv run python scripts/seed_recycling_urls.py --output db --workers 2 --yaml councils_20260319_143022.yaml
```

### Re-discover (clear existing URLs first)

```bash
uv run python scripts/seed_recycling_urls.py --output db --workers 2 --reset
```

---

## Seeding suburbs

Seeds the `suburbs` table from Matthew Proctor's Australian Postcodes dataset (URL configured via `SEED_POSTCODES_URL` in `.env`). Requires councils to already be seeded — suburb rows are matched to councils by LGA name.

### Seed into database

```bash
uv run python scripts/seed_suburbs.py --output db
```

### Preview SQL without writing

```bash
uv run python scripts/seed_suburbs.py --output stdout
```

### Reset before seeding

Truncates the `suburbs` table before inserting (does not cascade):

```bash
uv run python scripts/seed_suburbs.py --output db --reset
```

> **Note:** If you ran `seed_councils.py --reset`, suburbs are also wiped (cascade). Always re-run `seed_suburbs.py --output db` after a council reset.

---

## Scraping materials

Scrapes recycling material data for each council via Playwright + LLM extraction.

```bash
uv run python scripts/seed_materials.py --councils all --output db
uv run python scripts/seed_materials.py --councils all --output db --resume
uv run python scripts/seed_materials.py --councils city-of-sydney,city-of-melbourne --output db
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
cd scraper/

# 1. Scrape councils
uv run python scripts/seed_councils.py --output db

# 2. Seed suburbs (suburb/postcode → council mapping)
uv run python scripts/seed_suburbs.py --output db

# 3. Discover recycling URLs → populates recycling_url in the database
uv run python scripts/seed_recycling_urls.py --output db --workers 2

# 4. Snapshot DB state to YAML
uv run python scripts/councils_yaml.py dump

# 5. Scrape recycling materials for each council
uv run python scripts/seed_materials.py --councils all --output db --workers 2
```
