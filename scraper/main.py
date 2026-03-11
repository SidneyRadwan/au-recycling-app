#!/usr/bin/env python3
"""
Australia Recycling Scraper — CLI entry point.

Usage:
    python main.py --councils all --output json
    python main.py --councils city-of-sydney,city-of-melbourne --output db
"""
import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

from config import settings
from councils.registry import get_all_slugs, get_scraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape Australian council recycling data")
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
    return parser.parse_args()


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

    slugs = get_all_slugs() if args.councils == "all" else [
        s.strip() for s in args.councils.split(",") if s.strip()
    ]

    if not slugs:
        logger.error("No councils specified")
        sys.exit(1)

    logger.info("Running scraper for %d council(s): %s", len(slugs), ", ".join(slugs))

    output_dir = Path(args.output_dir)
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
