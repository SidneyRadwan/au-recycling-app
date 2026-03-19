#!/usr/bin/env python3
"""
Australia Recycling Scraper — CLI entry point.

Usage:
    python scripts/seed_materials.py --councils all --output json
    python scripts/seed_materials.py --councils all --output json --resume   # skip already-scraped
    python scripts/seed_materials.py --councils city-of-sydney,city-of-melbourne --output db
"""

import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings
from councils.registry import get_all_slugs, get_scraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Australian council recycling data"
    )
    parser.add_argument(
        "--councils",
        default="all",
        help='Comma-separated council slugs, or "all". Default: all',
    )
    parser.add_argument(
        "--output",
        choices=["json", "db"],
        default="json",
        help="Output mode: json (write files) or db (upsert to PostgreSQL). Default: json",
    )
    parser.add_argument(
        "--output-dir",
        default=str(settings.scraper_output_dir),
        help="Directory for JSON output files",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip councils that already have output (json: existing file, db: scraped today)",
    )
    parser.add_argument(
        "--crawl-only",
        action="store_true",
        help="Crawl pages and save raw text to output/<slug>.crawl.txt without calling the LLM",
    )
    return parser.parse_args()


def already_scraped(slug: str, output: str, output_dir: Path) -> bool:
    """Return True if this council already has output from a previous run."""
    if output == "json":
        return (output_dir / f"{slug}.json").exists()
    if output == "db":
        try:
            from db import get_connection

            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM councils WHERE slug = %s "
                    "AND updated_at >= CURRENT_DATE",
                    (slug,),
                )
                return cur.fetchone() is not None
        except Exception:
            return False
    return False


def run_crawl_only(slug: str, output_dir: Path) -> bool:
    """Crawl pages and save combined text without calling the LLM."""
    logger.info("Crawling (no LLM): %s", slug)
    try:
        scraper = get_scraper(slug)
        url = scraper._config["recycling_url"]
        combined, visited = scraper._crawl_pages(url)
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / f"{slug}.crawl.txt"
        out_path.write_text(combined)
        logger.info("  Crawled %d page(s) → %s", len(visited), out_path)
        return True
    except Exception as e:
        logger.error("  Failed: %s", e)
        return False


def run_scraper(slug: str, output: str, output_dir: Path) -> bool:
    logger.info("Scraping: %s", slug)
    try:
        scraper = get_scraper(slug)
        data = scraper.scrape()

        if output == "json":
            output_dir.mkdir(parents=True, exist_ok=True)
            out_path = output_dir / f"{slug}.json"
            with open(out_path, "w") as f:
                json.dump(asdict(data), f, indent=2, default=str)
            logger.info("  Written to %s", out_path)
        elif output == "db":
            from db import save_council_data

            save_council_data(data)

        return True
    except Exception as e:
        logger.error("  Failed: %s", e)
        return False


def main() -> None:
    args = parse_args()

    slugs = (
        get_all_slugs()
        if args.councils == "all"
        else [s.strip() for s in args.councils.split(",") if s.strip()]
    )

    if not slugs:
        logger.error("No councils specified")
        sys.exit(1)

    output_dir = Path(args.output_dir)

    if args.resume:
        pending = [s for s in slugs if not already_scraped(s, args.output, output_dir)]
        skipped = len(slugs) - len(pending)
        if skipped:
            logger.info("Resuming — skipping %d already-scraped council(s)", skipped)
        slugs = pending

    if not slugs:
        logger.info("All councils already scraped. Use without --resume to re-scrape.")
        return

    logger.info("Running scraper for %d council(s): %s", len(slugs), ", ".join(slugs))

    if args.crawl_only:
        results = {slug: run_crawl_only(slug, output_dir) for slug in slugs}
    else:
        results = {slug: run_scraper(slug, args.output, output_dir) for slug in slugs}

    passed = sum(results.values())
    failed = len(results) - passed

    logger.info("Done — %d succeeded, %d failed", passed, failed)
    if failed:
        for slug, ok in results.items():
            if not ok:
                logger.error("  FAILED: %s", slug)
        sys.exit(1)


if __name__ == "__main__":
    main()
