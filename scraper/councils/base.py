import hashlib
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import anthropic
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from config import settings
from models import BinType, CouncilData, CouncilMaterial
from utils import retry

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AuRecyclingScraper/1.0; "
        "+https://github.com/au-recycling-app)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
}

# Keywords used to identify recycling-relevant links during crawling
_RECYCLING_KEYWORDS = frozenset(
    [
        "recycl",
        "waste",
        "rubbish",
        "bin",
        "compost",
        "organics",
        "drop-off",
        "disposal",
        "kerbside",
        "collection",
        "fogo",
        "hazardous",
        "chemical",
        "garden",
        "household",
        "litter",
        "e-waste",
        "ewaste",
        "battery",
        "batteries",
    ]
)

# Path segments that indicate non-content functional pages — skip these
_SKIP_PATH_SEGMENTS = frozenset(
    [
        "signin",
        "sign-in",
        "login",
        "logout",
        "auth",
        "oidc",
        "report",
        "book-",
        "find-my",
        "contact",
        "subscribe",
        "feedback",
        "search",
        "sitemap",
        "privacy",
        "terms",
    ]
)


class BaseCouncilScraper(ABC):
    """Abstract base class for all council scrapers."""

    council_slug: str = ""
    rate_limit_seconds: float = 1.0

    def __init__(self, rate_limit_seconds: Optional[float] = None) -> None:
        if rate_limit_seconds is not None:
            self.rate_limit_seconds = rate_limit_seconds
        self._session = requests.Session()
        self._session.headers.update(DEFAULT_HEADERS)
        self._last_request_at: float = 0.0

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def scrape(self) -> CouncilData: ...

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    @retry(times=3, delay=2.0, exceptions=(requests.RequestException,))
    def fetch(self, url: str, **kwargs) -> BeautifulSoup:
        self._respect_rate_limit()
        logger.debug("GET %s", url)
        response = self._session.get(url, timeout=30, **kwargs)
        response.raise_for_status()
        self._last_request_at = time.monotonic()
        return self._parse_html(response.text)

    def fetch_text(self, url: str, **kwargs) -> str:
        self._respect_rate_limit()
        logger.debug("GET (text) %s", url)
        response = self._session.get(url, timeout=30, **kwargs)
        response.raise_for_status()
        self._last_request_at = time.monotonic()
        return response.text

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        wait = self.rate_limit_seconds - elapsed
        if wait > 0:
            logger.debug("Rate limiting: sleeping %.2fs", wait)
            time.sleep(wait)

    @staticmethod
    def _parse_html(html: str, parser: str = "lxml") -> BeautifulSoup:
        try:
            return BeautifulSoup(html, parser)
        except Exception:
            return BeautifulSoup(html, "html.parser")

    @staticmethod
    def _html_to_text(html: str) -> tuple[str, list[str]]:
        """Return (page_text, hrefs) from raw HTML."""
        soup = BaseCouncilScraper._parse_html(html)
        hrefs = [a["href"] for a in soup.find_all("a", href=True)]
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True), hrefs

    # ------------------------------------------------------------------
    # Crawler + LLM-assisted extraction
    # ------------------------------------------------------------------

    _EXTRACTION_PROMPT = """\
You are extracting Australian council recycling data from one or more council website pages.

Return ONLY a valid JSON array (no markdown, no prose) where each item has:
- "material_slug": lowercase-with-hyphens identifier for one specific material or item type (e.g. "cardboard-boxes", "egg-cartons", "pizza-boxes", "plastic-milk-bottles")
- "bin_type": one of RECYCLING, GENERAL_WASTE, GREEN_WASTE, SOFT_PLASTICS, SPECIAL_DROP_OFF, NOT_ACCEPTED
- "instructions": string describing what to do with this material (required)
- "notes": string with extra context or null

Rules:
- Create one entry per specific item or material type — do not group distinct items under a single slug.
  For example, "cardboard boxes including egg cartons and pizza boxes" should become three entries:
  "cardboard-boxes", "egg-cartons", "pizza-boxes" — each with the same bin_type and relevant instructions.
- If the same material appears on multiple pages, use the most detailed entry.
- If bin type is ambiguous, use the most specific match.

Page content:
{text}"""

    def _crawl_pages(self, start_url: str, max_pages: int = 6) -> tuple[str, set[str]]:
        """Crawl *start_url* and relevant linked pages. Returns (combined_text, visited_urls).

        Keeps a single Playwright browser open across all page fetches to avoid
        repeated launch overhead.
        """
        base = urlparse(start_url)
        visited: set[str] = set()
        pages_text: list[str] = []

        logger.info("Crawling %s (max %d pages)", start_url, max_pages)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=DEFAULT_HEADERS["User-Agent"],
                extra_http_headers={
                    "Accept-Language": DEFAULT_HEADERS["Accept-Language"]
                },
            )

            def render(url: str) -> tuple[str, list[str]]:
                self._respect_rate_limit()
                page = context.new_page()
                page.goto(url, wait_until="networkidle", timeout=30_000)
                html = page.content()
                page.close()
                self._last_request_at = time.monotonic()
                return self._html_to_text(html)

            # Fetch the start page
            text, raw_hrefs = render(start_url)
            visited.add(start_url)
            pages_text.append(text)

            # Resolve and filter links
            candidates: list[str] = []
            seen_candidates: set[str] = set()
            for href in raw_hrefs:
                url = urljoin(start_url, href).split("#")[0]
                parsed = urlparse(url)
                if parsed.netloc != base.netloc:
                    continue
                if url in visited or url in seen_candidates:
                    continue
                seen_candidates.add(url)
                url_lower = url.lower()
                path_lower = urlparse(url).path.lower()
                if any(skip in path_lower for skip in _SKIP_PATH_SEGMENTS):
                    continue
                if any(kw in url_lower for kw in _RECYCLING_KEYWORDS):
                    candidates.append(url)

            # Prioritise URLs with more recycling keywords in their path
            candidates.sort(
                key=lambda u: sum(
                    kw in urlparse(u).path.lower() for kw in _RECYCLING_KEYWORDS
                ),
                reverse=True,
            )
            logger.info("Found %d candidate link(s) to follow", len(candidates))

            # Follow candidates up to max_pages total
            for url in candidates:
                if len(pages_text) >= max_pages:
                    break
                if url in visited:
                    continue
                try:
                    logger.info("  Crawling: %s", url)
                    sub_text, _ = render(url)
                    visited.add(url)
                    pages_text.append(sub_text)
                except Exception as e:
                    logger.warning("  Skipping %s: %s", url, e)

            browser.close()

        logger.info("Crawled %d page(s), extracting materials", len(pages_text))

        # Budget 15k chars total, split evenly across pages
        chars_per_page = 15_000 // len(pages_text)
        combined = "\n\n---\n\n".join(t[:chars_per_page] for t in pages_text)

        return combined, visited

    def extract_materials(
        self, start_url: str, max_pages: int = 6
    ) -> list[CouncilMaterial]:
        """Crawl *start_url* and relevant linked pages, then extract materials via Claude."""
        combined, _ = self._crawl_pages(start_url, max_pages)
        return self._llm_extract(combined, start_url)

    _LLM_CACHE_DIR = Path(__file__).parent.parent / "output" / ".llm_cache"

    def _llm_extract(self, text: str, source_url: str) -> list[CouncilMaterial]:
        """Send *text* to Claude and parse the returned JSON into CouncilMaterial objects.

        Responses are cached on disk keyed by a hash of the prompt so re-runs
        don't consume API tokens during development.
        """
        prompt = self._EXTRACTION_PROMPT.format(text=text)
        cache_key = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        self._LLM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = self._LLM_CACHE_DIR / f"{cache_key}.txt"

        if cache_file.exists():
            logger.info("LLM cache hit for %s", source_url)
            raw = cache_file.read_text()
        else:
            client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            message = client.messages.create(
                model=settings.extraction_model,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = message.content[0].text.strip()
            cache_file.write_text(raw)
            logger.debug("LLM response cached at %s", cache_file)

        logger.debug("Raw LLM response: %s", raw[:500])

        fence_match = re.search(r"```(?:json)?\s*(\[.*?])\s*```", raw, re.DOTALL)
        if fence_match:
            raw = fence_match.group(1)
        else:
            start, end = raw.find("["), raw.rfind("]")
            if start != -1 and end != -1:
                raw = raw[start : end + 1]
            else:
                logger.warning("No JSON array found in LLM response for %s", source_url)
                return []

        items: list[dict] = json.loads(raw)
        valid_bin_types = {bt.value for bt in BinType}
        seen_slugs: dict[str, CouncilMaterial] = {}

        for item in items:
            bin_type_str = str(item.get("bin_type", "")).upper()
            if bin_type_str not in valid_bin_types:
                logger.warning("Skipping unknown bin_type %r", bin_type_str)
                continue
            slug = item.get("material_slug", "").strip()
            if not slug:
                continue
            material = CouncilMaterial(
                material_slug=slug,
                bin_type=BinType(bin_type_str),
                instructions=item.get("instructions") or None,
                notes=item.get("notes") or None,
            )
            # Deduplicate by slug — keep whichever has more detail
            existing = seen_slugs.get(slug)
            if existing is None or len(str(material.instructions or "")) > len(
                str(existing.instructions or "")
            ):
                seen_slugs[slug] = material

        materials = list(seen_slugs.values())
        logger.info("Extracted %d materials from %s", len(materials), source_url)
        return materials

    def __repr__(self) -> str:
        return f"<{type(self).__name__} slug={self.council_slug!r}>"


class GenericCouncilScraper(BaseCouncilScraper):
    """Config-driven scraper for councils that need no custom extraction logic."""

    def __init__(self, config: dict) -> None:
        super().__init__()
        self._config = config
        self.council_slug = config["slug"]

    def scrape(self) -> CouncilData:
        url = self._config["recycling_url"]
        return CouncilData(
            name=self._config["name"],
            slug=self._config["slug"],
            state=self._config["state"],
            website=self._config.get("website"),
            recycling_info_url=url,
            description=self._config.get("description"),
            suburbs=self._config.get("suburbs", []),
            materials=self.extract_materials(url),
        )
