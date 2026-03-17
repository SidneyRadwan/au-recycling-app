from councils.base import BaseCouncilScraper, GenericCouncilScraper
from db import get_council_scraper_configs

# Custom scrapers for councils that need non-standard extraction logic.
# Any slug not in this dict gets a GenericCouncilScraper using DB config.
_CUSTOM_SCRAPERS: dict[str, type[BaseCouncilScraper]] = {}


def get_all_slugs() -> list[str]:
    return [c["slug"] for c in get_council_scraper_configs()]


def get_scraper(slug: str) -> BaseCouncilScraper:
    configs = {c["slug"]: c for c in get_council_scraper_configs()}
    if slug not in configs:
        raise ValueError(f"No council configured for slug: {slug!r}")
    if slug in _CUSTOM_SCRAPERS:
        return _CUSTOM_SCRAPERS[slug]()
    return GenericCouncilScraper(configs[slug])
