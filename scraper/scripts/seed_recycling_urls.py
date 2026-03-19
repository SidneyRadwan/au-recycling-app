#!/usr/bin/env python3
"""
Discover each council's recycling/waste page URL by scoring homepage links.

Uses a pool of Playwright (headless Chromium) instances run in parallel so that
JS-rendered navigation links are included in the candidate set.

Usage:
    uv run python seed_recycling_urls.py --output stdout             # print discovered URLs
    uv run python seed_recycling_urls.py --output db                 # write to database
    uv run python seed_recycling_urls.py --output db --states NSW VIC
    uv run python seed_recycling_urls.py --output db --workers 8     # parallel workers
    uv run python seed_recycling_urls.py --output db --reset         # re-discover all
"""

import argparse
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright

sys.path.insert(0, str(Path(__file__).parent.parent))
from councils.base import DEFAULT_HEADERS, _SKIP_PATH_SEGMENTS
from db import get_connection

# Thread-local storage: each worker thread owns one Browser instance.
_local = threading.local()
_playwright_instances: list[Playwright] = []
_playwright_lock = threading.Lock()


def _init_worker() -> None:
    pw = sync_playwright().start()
    _local.browser = pw.chromium.launch(headless=True)
    with _playwright_lock:
        _playwright_instances.append(pw)


def _stop_all_workers() -> None:
    for pw in _playwright_instances:
        try:
            pw.stop()
        except Exception:
            pass
    _playwright_instances.clear()


# Scoring tiers for identifying the recycling section root:
#   2 — primary keyword matched (recycling/waste/rubbish words)
#   1 — secondary keyword matched (bin types, collection services, etc.)
_PRIMARY_WORDS = frozenset(
    [
        "recycling",
        "recycle",
        "recyclable",
        "recyclables",
        "recycled",
        "waste",
        "rubbish",
    ]
)
_SECONDARY_WORDS = frozenset(
    [
        "bin",
        "bins",
        "compost",
        "composting",
        "organics",
        "drop-off",
        "disposal",
        "kerbside",
        "fogo",
        "hazardous",
        "chemical",
        "chemicals",
        "household",
        "litter",
        "e-waste",
        "ewaste",
        "battery",
        "batteries",
    ]
)


def _compile_pattern(words: frozenset[str]) -> re.Pattern:
    alts = "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))
    return re.compile(r"\b(?:" + alts + r")\b")


_PRIMARY_RE = _compile_pattern(_PRIMARY_WORDS)
_SECONDARY_RE = _compile_pattern(_SECONDARY_WORDS)

_SCORE_THRESHOLD = 1  # minimum score to be a candidate


def _parse_links(html: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    return [
        (a.get("href", ""), a.get_text(strip=True))
        for a in soup.find_all("a", href=True)
    ]


def _normalise_netloc(netloc: str) -> str:
    """Strip www. prefix and redundant default ports for domain comparison."""
    host = netloc.lower()
    host = host.removesuffix(":80").removesuffix(":443")
    host = host.removeprefix("www.")
    return host


def _score_link(
    href: str, text: str, base_url: str, base_netloc: str
) -> tuple[int, str | None]:
    """Return (score, resolved_url). Score=0 means skip."""
    try:
        resolved = urljoin(base_url, href).split("#")[0]
        parsed = urlparse(resolved)
    except Exception:
        return 0, None

    if _normalise_netloc(parsed.netloc) != _normalise_netloc(base_netloc):
        return 0, None

    path_lower = parsed.path.lower()
    if any(skip in path_lower for skip in _SKIP_PATH_SEGMENTS):
        return 0, None
    if path_lower.endswith(".pdf"):
        return 0, None

    # Score only the leaf path segment + link text — not the full URL.
    leaf = urlparse(resolved).path.rstrip("/").rsplit("/", 1)[-1].lower()
    combined = (leaf + " " + text).lower()

    if _PRIMARY_RE.search(combined):
        score = 2
    elif _SECONDARY_RE.search(combined):
        score = 1
    else:
        score = 0

    return score, resolved


def _select_best(links: list[tuple[str, str]], final_url: str) -> str | None:
    """Given a list of (href, text) links from a page, return the best recycling section URL."""
    base_netloc = urlparse(final_url).netloc
    candidates: list[tuple[int, int, str]] = []  # (score, path_depth, url)

    for href, text in links:
        score, resolved = _score_link(href, text, final_url, base_netloc)
        if score >= _SCORE_THRESHOLD and resolved:
            depth = len([s for s in urlparse(resolved).path.split("/") if s])
            candidates.append((score, depth, resolved))

    if not candidates:
        return None

    candidates.sort(key=lambda c: (-c[0], c[1]))
    return candidates[0][2]


def _same_origin(netloc_a: str, netloc_b: str) -> bool:
    """True if two normalised netlocs belong to the same organisation.

    Allows subdomain changes (www ↔ my ↔ council) but rejects genuinely
    different domains: melville.wa.gov.au vs wasteauthority.wa.gov.au.
    """
    if netloc_a == netloc_b:
        return True
    return netloc_a.endswith("." + netloc_b) or netloc_b.endswith("." + netloc_a)


def _score_url(url: str) -> int:
    """Score a URL by its path alone (no link text). Used for cross-domain redirect targets."""
    leaf = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1].lower()
    if _PRIMARY_RE.search(leaf):
        return 2
    if _SECONDARY_RE.search(leaf):
        return 1
    return 0


def _get_links(website: str) -> tuple[list[tuple[str, str]], str]:
    """Render *website* in the calling thread's browser and return (links, final_url)."""
    ctx = _local.browser.new_context(
        user_agent=DEFAULT_HEADERS["User-Agent"],
        extra_http_headers={"Accept-Language": "en-AU,en;q=0.9"},
    )
    page = ctx.new_page()
    try:
        page.goto(website, wait_until="domcontentloaded", timeout=30_000)
        return _parse_links(page.content()), page.url
    except Exception as e:
        print(f"    ERROR {website}: {e}", flush=True)
        return [], website
    finally:
        ctx.close()


def discover_recycling_url(website: str) -> str | None:
    """Render council homepage and return the best-scoring recycling section URL, or None.

    Uses *council_overrides.yaml* for councils whose recycling page can't be
    auto-discovered (JS-only navigation with no recycling keywords, etc.).
    """
    original_netloc = _normalise_netloc(urlparse(website).netloc)
    links, final_url = _get_links(website)

    if not links:
        return None

    final_netloc = _normalise_netloc(urlparse(final_url).netloc)

    # Cross-domain redirect: don't harvest links from a foreign site.
    # Score the redirect target URL itself — if it looks like a recycling page
    # (e.g. council.wa.gov.au → wasteauthority.wa.gov.au/recycling) return it
    # directly; otherwise give up.
    if not _same_origin(original_netloc, final_netloc):
        return final_url if _score_url(final_url) >= _SCORE_THRESHOLD else None

    return _select_best(links, final_url)


def _load_overrides() -> dict:
    path = Path(__file__).parent.parent / "council_overrides.yaml"
    if not path.exists():
        return {}
    import yaml

    return yaml.safe_load(path.read_text()) or {}


def load_councils(states: list[str] | None, reset: bool) -> list[dict]:
    conn = get_connection()
    with conn.cursor() as cur:
        if reset:
            if states:
                cur.execute(
                    "UPDATE councils SET recycling_info_url = NULL WHERE state = ANY(%s)",
                    (states,),
                )
            else:
                cur.execute("UPDATE councils SET recycling_info_url = NULL")
            conn.commit()
            print("  Reset: cleared recycling_info_url", file=sys.stderr)

        query = (
            "SELECT slug, name, state, website FROM councils "
            "WHERE website IS NOT NULL AND recycling_info_url IS NULL"
        )
        params: list = []
        if states:
            query += " AND state = ANY(%s)"
            params.append(states)
        query += " ORDER BY state, slug"
        cur.execute(query, params)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    conn.close()
    return rows


def write_to_db(slug: str, recycling_url: str) -> None:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE councils SET recycling_info_url = %s WHERE slug = %s",
            (recycling_url, slug),
        )
    conn.commit()
    conn.close()


def _update_yaml(yaml_path: Path, results: dict[str, str | None]) -> None:
    """Write recycling_url values back into a councils YAML file."""
    import yaml

    data = yaml.safe_load(yaml_path.read_text()) or []
    for entry in data:
        slug = entry.get("slug")
        if slug in results:
            entry["recycling_url"] = results[slug]
    yaml_path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False))
    print(f"Updated recycling URLs in {yaml_path}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Discover recycling URLs for all councils"
    )
    parser.add_argument(
        "--output",
        choices=["stdout", "db"],
        default="stdout",
        help="stdout: print results | db: write recycling_info_url to database",
    )
    parser.add_argument(
        "--states",
        nargs="+",
        default=None,
        metavar="STATE",
        help="Limit to specific states (e.g. --states NSW VIC)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        metavar="N",
        help="Number of parallel Playwright workers (default: 4)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing recycling_info_url values before running. Only valid with --output db.",
    )
    parser.add_argument(
        "--yaml",
        metavar="PATH",
        help="Path to a councils YAML file to update with discovered recycling_url values.",
    )
    args = parser.parse_args()

    if args.reset and args.output != "db":
        parser.error("--reset is only valid with --output db")

    yaml_path = Path(args.yaml) if args.yaml else None

    councils = load_councils(args.states, args.reset)

    # slug → recycling_url for YAML back-write (overrides + discovered)
    yaml_results: dict[str, str | None] = {}

    overrides = _load_overrides()
    for slug, fields in overrides.items():
        if "recycling_info_url" in fields:
            url = fields["recycling_info_url"]
            if args.output == "db":
                write_to_db(slug, url)
            yaml_results[slug] = url
            print(f"  OVERRIDE {slug}: {url}", flush=True)

    total = len(councils)
    print(f"  {total} councils to process with {args.workers} workers", file=sys.stderr)

    resolved = 0
    unresolved: list[str] = []
    completed = 0

    try:
        with ThreadPoolExecutor(
            max_workers=args.workers, initializer=_init_worker
        ) as executor:
            future_to_council = {
                executor.submit(discover_recycling_url, c["website"]): c
                for c in councils
            }

            for future in as_completed(future_to_council):
                council = future_to_council[future]
                completed += 1
                slug = council["slug"]
                state = council["state"]
                website = council["website"]

                try:
                    recycling_url = future.result()
                except Exception as e:
                    print(
                        f"[{completed}/{total}] ERROR   {state} {slug}: {e}", flush=True
                    )
                    recycling_url = None

                if recycling_url:
                    resolved += 1
                    yaml_results[slug] = recycling_url
                    if args.output == "db":
                        write_to_db(slug, recycling_url)
                        print(
                            f"[{completed}/{total}] SEEDED  {state} {slug}: {recycling_url}",
                            flush=True,
                        )
                    else:
                        print(
                            f"[{completed}/{total}] FOUND   {state} {slug}: {recycling_url}",
                            flush=True,
                        )
                else:
                    unresolved.append(f"{state}/{slug} ({website})")
                    print(
                        f"[{completed}/{total}] SKIP    {state} {slug}: unresolved",
                        flush=True,
                    )
    finally:
        _stop_all_workers()

    if yaml_path:
        _update_yaml(yaml_path, yaml_results)

    print(
        f"\nSummary: {resolved} resolved, {len(unresolved)} unresolved", file=sys.stderr
    )
    if unresolved:
        print("\nUnresolved councils:", file=sys.stderr)
        for entry in unresolved:
            print(f"  {entry}", file=sys.stderr)


if __name__ == "__main__":
    main()
