#!/usr/bin/env python3
"""
Dump all councils from the database to a timestamped YAML snapshot.

Usage:
    uv run python scripts/dump_councils.py
    uv run python scripts/dump_councils.py --output councils_custom.yaml
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

_SCRAPER_DIR = Path(__file__).parent.parent
load_dotenv(_SCRAPER_DIR.parent / ".env")
time.tzset()


def _db_conn():
    db_url = os.environ.get("DATABASE_URL", "")
    m = re.match(r"jdbc:postgresql://([^:/]+)(?::(\d+))?/(\w+)", db_url)
    if m:
        host, port, dbname = m.group(1), m.group(2) or "5432", m.group(3)
    else:
        host, port, dbname = "localhost", "5432", "recycling"
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=os.environ.get("DATABASE_USERNAME", "recycling"),
        password=os.environ.get("DATABASE_PASSWORD", "recycling_dev"),
    )


def dump(path: Path | None = None) -> Path:
    import yaml

    if path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = _SCRAPER_DIR / f"councils_{ts}.yaml"

    conn = _db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name, slug, state, website, recycling_info_url"
                " FROM councils ORDER BY state, name"
            )
            rows = cur.fetchall()
    conn.close()

    councils = [
        {
            "name": name,
            "slug": slug,
            "state": state,
            "website": website,
            "recycling_url": recycling_url,
        }
        for name, slug, state, website, recycling_url in rows
    ]
    path.write_text(yaml.dump(councils, allow_unicode=True, sort_keys=False))
    print(f"Wrote {len(councils)} councils to {path}", file=sys.stderr)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump councils DB to YAML snapshot")
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="Output path (default: scraper/councils_YYYYMMDD_HHMMSS.yaml)",
    )
    args = parser.parse_args()
    dump(Path(args.output) if args.output else None)


if __name__ == "__main__":
    main()
