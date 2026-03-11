import logging
import time
from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup

from models import CouncilData
from utils import retry

logger = logging.getLogger(__name__)

# Default headers that mimic a real browser visit
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AuRecyclingScraper/1.0; "
        "+https://github.com/au-recycling-app)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
}


class BaseCouncilScraper(ABC):
    """Abstract base class for all council scrapers.

    Subclasses must implement :meth:`scrape` and set :attr:`council_slug`.
    The :meth:`fetch` helper handles rate-limiting and automatic retries so
    individual scrapers can focus solely on parsing.
    """

    #: Unique slug identifying this council — must match the registry key.
    council_slug: str = ""

    #: Minimum seconds to wait between HTTP requests (may be overridden per scraper).
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
    def scrape(self) -> CouncilData:
        """Collect and return recycling data for the council.

        Static-data scrapers simply build and return a :class:`~models.CouncilData`
        instance with hardcoded values.  Live scrapers call :meth:`fetch` and
        parse the HTML.
        """
        ...

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    @retry(times=3, delay=2.0, exceptions=(requests.RequestException,))
    def fetch(self, url: str, **kwargs) -> BeautifulSoup:
        """Fetch *url* and return a parsed :class:`~bs4.BeautifulSoup` document.

        Automatically respects :attr:`rate_limit_seconds` between calls and
        retries up to 3 times on network errors.

        Args:
            url: The URL to fetch.
            **kwargs: Extra keyword arguments forwarded to :meth:`requests.Session.get`.

        Returns:
            Parsed HTML document.

        Raises:
            requests.HTTPError: If the server returns a 4xx/5xx status.
        """
        self._respect_rate_limit()
        logger.debug("GET %s", url)
        response = self._session.get(url, timeout=30, **kwargs)
        response.raise_for_status()
        self._last_request_at = time.monotonic()
        return self._parse_html(response.text)

    def fetch_text(self, url: str, **kwargs) -> str:
        """Like :meth:`fetch` but returns the raw response text instead of BeautifulSoup."""
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
        """Parse *html* with BeautifulSoup.  Falls back to html.parser if lxml is absent."""
        try:
            return BeautifulSoup(html, parser)
        except Exception:
            return BeautifulSoup(html, "html.parser")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} slug={self.council_slug!r}>"
