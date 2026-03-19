#!/usr/bin/env python3
"""
Seed the suburbs table from Matthew Proctor's Australian Postcodes dataset.

The dataset already includes lgaregion (LGA name) for each suburb, so no
secondary ABS correspondence file is needed.

Data source URL is configured via SEED_POSTCODES_URL env var (see .env.example).

Usage:
    uv run python seed_suburbs.py                    # print SQL to stdout
    uv run python seed_suburbs.py --output db         # insert directly into the database
"""

import argparse
import io
import re
import sys
from pathlib import Path

import psycopg2
import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; au-recycling-seed/1.0)"}

_STATE_NORMALISE = {
    "NSW": "NSW",
    "VIC": "VIC",
    "QLD": "QLD",
    "SA": "SA",
    "WA": "WA",
    "TAS": "TAS",
    "NT": "NT",
    "ACT": "ACT",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[''`]", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def _strip_suffixes(name: str) -> str:
    """Remove common LGA suffixes to get a bare name for slug matching."""
    suffixes = [
        " rural city council",
        " city council",
        " shire council",
        " regional council",
        " town council",
        " community government council",
        " municipality",
        " council",
        " city",
        " shire",
    ]
    lower = name.lower().strip()
    for suffix in suffixes:
        if lower.endswith(suffix):
            return lower[: -len(suffix)].strip()
    return lower


def _db_connect():
    import os

    load_dotenv(Path(__file__).parent.parent.parent / ".env")
    db_url = os.environ.get("DATABASE_URL", "")
    m = re.match(r"jdbc:postgresql://([^:/]+)(?::(\d+))?/(\w+)", db_url)
    if m:
        host, port, dbname = m.group(1), m.group(2) or "5432", m.group(3)
    else:
        host, port, dbname = "localhost", "5432", "recycling"
    user = os.environ.get("DATABASE_USERNAME", "recycling")
    password = os.environ.get("DATABASE_PASSWORD", "recycling_dev")
    return psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password
    )


# ---------------------------------------------------------------------------
# Load councils from DB: { state -> { bare_slug -> council_id, full_slug -> council_id } }
# ---------------------------------------------------------------------------


def load_councils() -> dict[str, dict[str, int]]:
    conn = _db_connect()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, slug, state FROM councils")
        rows = cur.fetchall()
    conn.close()

    by_state: dict[str, dict[str, int]] = {}
    for council_id, name, slug, state in rows:
        bare = slugify(_strip_suffixes(name))
        by_state.setdefault(state, {})[slug] = council_id
        by_state.setdefault(state, {})[bare] = council_id

    return by_state


def _match_council(
    lga_name: str, state: str, by_state: dict[str, dict[str, int]]
) -> int | None:
    state_map = by_state.get(state, {})
    if not state_map:
        return None
    full = slugify(lga_name)
    bare = slugify(_strip_suffixes(lga_name))
    if full in state_map:
        return state_map[full]
    if bare in state_map:
        return state_map[bare]
    for slug, cid in state_map.items():
        if slug.startswith(bare + "-") or bare in slug:
            return cid
    return None


# Postcode dataset uses disambiguation suffixes, wrong states, or outdated names.
# Map (lga_name, state) → (canonical_name, canonical_state) matching the councils table.
_LGA_OVERRIDES: dict[tuple[str, str], tuple[str, str]] = {
    # Disambiguation suffixes — same bare name exists in multiple states
    ("Bayside (NSW)", "NSW"): ("Bayside Council", "NSW"),
    ("Bayside (Vic.)", "VIC"): ("Bayside City Council", "VIC"),
    ("Campbelltown (NSW)", "NSW"): ("Campbelltown City Council", "NSW"),
    ("Campbelltown (SA)", "SA"): ("City of Campbelltown", "SA"),
    ("Central Coast (NSW)", "NSW"): ("Central Coast Council", "NSW"),
    ("Central Highlands (Qld)", "QLD"): ("Central Highlands Regional Council", "QLD"),
    ("Central Highlands (Tas.)", "TAS"): ("Central Highlands", "TAS"),
    ("Flinders (Qld)", "QLD"): ("Flinders Shire Council", "QLD"),
    ("Flinders (Tas.)", "TAS"): ("Flinders", "TAS"),
    ("Kingston (SA)", "SA"): ("Kingston District Council", "SA"),
    ("Kingston (Vic.)", "VIC"): ("Kingston City Council", "VIC"),
    ("Latrobe (Tas.)", "TAS"): ("Latrobe", "TAS"),
    ("Latrobe (Vic.)", "VIC"): ("Latrobe City Council", "VIC"),
    # Punctuation differences
    ("Norwood Payneham and St Peters", "SA"): (
        "City of Norwood Payneham & St Peters",
        "SA",
    ),
    ("Glamorgan-Spring Bay", "TAS"): (
        "Glamorgan\u2013Spring Bay",
        "TAS",
    ),  # en-dash in DB
    ("Waratah-Wynyard", "TAS"): ("Waratah\u2013Wynyard", "TAS"),  # en-dash in DB
    ("Flinders Ranges", "SA"): ("Flinders Range Council", "SA"),  # singular in DB
    # Renamed council
    ("Moreland", "VIC"): ("Merri-bek City Council", "VIC"),
    # Wrong state in source data — council exists in a different state
    ("Laverton", "NT"): ("Laverton", "WA"),
    ("Laverton", "SA"): ("Laverton", "WA"),
    ("Carpentaria", "NT"): ("Carpentaria Shire Council", "QLD"),
    ("Snowy Monaro", "ACT"): ("Snowy Monaro Regional Council", "NSW"),
    ("Snowy Valleys", "ACT"): ("Snowy Valleys Council", "NSW"),
    # Border postcodes — suburb filed under wrong state in source data
    ("East Gippsland", "NSW"): ("East Gippsland Shire Council", "VIC"),
    ("Goondiwindi", "NSW"): ("Goondiwindi Regional Council", "QLD"),
    ("Mildura", "NSW"): ("Mildura Rural City Council", "VIC"),
    ("Swan Hill", "NSW"): ("Swan Hill Rural City Council", "VIC"),
    ("Inverell", "QLD"): ("Inverell Shire Council", "NSW"),
    ("Tenterfield", "QLD"): ("Tenterfield Shire Council", "NSW"),
    ("Albury", "VIC"): ("Albury City Council", "NSW"),
    ("Berrigan", "VIC"): ("Berrigan Shire Council", "NSW"),
    ("Snowy Valleys", "VIC"): ("Snowy Valleys Council", "NSW"),
}


# ---------------------------------------------------------------------------
# Fetch postcode CSV and build suburb rows
# ---------------------------------------------------------------------------


def fetch_and_build(
    postcodes_url: str, by_state: dict[str, dict[str, int]]
) -> list[tuple[str, str | None, str, int]]:
    import csv

    print(f"  Downloading postcode data from {postcodes_url}...", file=sys.stderr)
    resp = requests.get(postcodes_url, timeout=60, headers=_HEADERS)
    resp.raise_for_status()
    print(f"    {len(resp.content) // 1024} KB downloaded", file=sys.stderr)

    reader = csv.DictReader(io.StringIO(resp.text))

    seen: set[tuple[str, str, int]] = set()
    unmatched: set[str] = set()
    rows: list[tuple[str, str | None, str, int]] = []

    for row in reader:
        suburb = (row.get("locality") or "").strip().title()
        postcode = (row.get("postcode") or "").strip() or None
        state = _STATE_NORMALISE.get((row.get("state") or "").strip().upper())
        lga_name = (row.get("lgaregion") or "").strip()

        if not suburb or not state or not lga_name:
            continue

        # Skip Australia Post delivery centres — not real suburbs
        if suburb.endswith(" Dc") or suburb.endswith(" Bc") or suburb.endswith(" Mc"):
            continue

        lga_name, state = _LGA_OVERRIDES.get((lga_name, state), (lga_name, state))
        council_id = _match_council(lga_name, state, by_state)
        if council_id is None:
            unmatched.add(f"{state}: {lga_name}")
            continue

        key = (suburb.lower(), state, council_id)
        if key in seen:
            continue
        seen.add(key)

        rows.append((suburb, postcode, state, council_id))

    if unmatched:
        print(f"    WARNING: {len(unmatched)} LGA names unmatched:", file=sys.stderr)
        for lga in sorted(unmatched)[:20]:
            print(f"      {lga}", file=sys.stderr)
        if len(unmatched) > 20:
            print(f"      ... and {len(unmatched) - 20} more", file=sys.stderr)

    print(f"    {len(rows)} suburb rows built", file=sys.stderr)
    return rows


# ---------------------------------------------------------------------------
# SQL generation
# ---------------------------------------------------------------------------

_ESC = lambda v: "NULL" if v is None else "'" + v.replace("'", "''") + "'"  # noqa: E731


def generate_sql(rows: list[tuple[str, str | None, str, int]]) -> str:
    value_rows = ",\n".join(
        f"  ({_ESC(name)}, {_ESC(postcode)}, {_ESC(state)}, {council_id})"
        for name, postcode, state, council_id in rows
    )
    return f"""\
-- Auto-generated by scraper/seed_suburbs.py
-- {len(rows)} suburb→council mappings from Matthew Proctor's Australian Postcodes dataset
INSERT INTO suburbs (name, postcode, state, council_id) VALUES
{value_rows}
ON CONFLICT DO NOTHING;
"""


# ---------------------------------------------------------------------------
# Output modes
# ---------------------------------------------------------------------------


def write_to_db(
    rows: list[tuple[str, str | None, str, int]], reset: bool = False
) -> None:
    print("  Inserting into database...", file=sys.stderr)
    conn = _db_connect()
    with conn:
        with conn.cursor() as cur:
            if reset:
                cur.execute("TRUNCATE suburbs")
                print("  Reset: truncated suburbs", file=sys.stderr)
            cur.executemany(
                "INSERT INTO suburbs (name, postcode, state, council_id) "
                "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                rows,
            )
    conn.close()
    print(f"  Inserted {len(rows)} rows.", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed suburbs from postcode data")
    parser.add_argument(
        "--output",
        choices=["stdout", "db"],
        default="stdout",
        help="stdout: print SQL | db: insert directly",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Truncate suburbs before seeding. Only valid with --output db.",
    )
    args = parser.parse_args()

    if args.reset and args.output != "db":
        parser.error("--reset is only valid with --output db")

    postcodes_url = settings.seed_postcodes_url

    print("Loading councils from database...", file=sys.stderr)
    by_state = load_councils()
    total = sum(len(v) for v in by_state.values())
    print(f"  {total} council lookup entries", file=sys.stderr)

    rows = fetch_and_build(postcodes_url, by_state)
    print(f"\nTotal suburb rows: {len(rows)}", file=sys.stderr)

    if args.output == "stdout":
        print(generate_sql(rows))
    elif args.output == "db":
        write_to_db(rows, reset=args.reset)


if __name__ == "__main__":
    main()
