#!/usr/bin/env python3
"""
Dump councils from the database to a YAML snapshot, or load a YAML snapshot into the database.

Usage:
    uv run python scripts/councils_yaml.py dump
    uv run python scripts/councils_yaml.py dump --output councils_custom.yaml
    uv run python scripts/councils_yaml.py load councils_20260319_032617.yaml
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


def load(path: Path) -> None:
    import yaml

    councils = yaml.safe_load(path.read_text()) or []
    conn = _db_conn()
    with conn:
        with conn.cursor() as cur:
            for c in councils:
                cur.execute(
                    """
                    INSERT INTO councils (name, slug, state, website, recycling_info_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET
                        name = EXCLUDED.name,
                        state = EXCLUDED.state,
                        website = EXCLUDED.website,
                        recycling_info_url = EXCLUDED.recycling_info_url
                    """,
                    (
                        c["name"],
                        c["slug"],
                        c["state"],
                        c.get("website"),
                        c.get("recycling_url"),
                    ),
                )
    conn.close()
    print(f"Loaded {len(councils)} councils from {path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump or load councils YAML snapshot")
    sub = parser.add_subparsers(dest="command", required=True)

    dump_p = sub.add_parser("dump", help="Dump DB to YAML")
    dump_p.add_argument(
        "--output",
        metavar="PATH",
        help="Output path (default: scraper/councils_YYYYMMDD_HHMMSS.yaml)",
    )

    load_p = sub.add_parser("load", help="Load YAML into DB")
    load_p.add_argument("file", metavar="PATH", help="YAML file to load")

    args = parser.parse_args()

    if args.command == "dump":
        dump(Path(args.output) if args.output else None)
    elif args.command == "load":
        load(Path(args.file))


if __name__ == "__main__":
    main()
