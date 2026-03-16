from pathlib import Path

import yaml

from councils.base import BaseCouncilScraper, GenericCouncilScraper

# Path to the central council config file
_CONFIG_PATH = Path(__file__).parent.parent / "councils.yaml"


def _load_configs() -> dict[str, dict]:
    with open(_CONFIG_PATH) as f:
        entries = yaml.safe_load(f)
    return {entry["slug"]: entry for entry in entries}


# Custom scrapers for councils that need non-standard extraction logic.
# Any slug not listed here gets a GenericCouncilScraper from councils.yaml.
_CUSTOM_SCRAPERS: dict[str, type[BaseCouncilScraper]] = {}


def get_all_slugs() -> list[str]:
    return list(_load_configs().keys())


def get_scraper(slug: str) -> BaseCouncilScraper:
    configs = _load_configs()
    if slug not in configs:
        raise ValueError(f"No council configured for slug: {slug!r}")
    if slug in _CUSTOM_SCRAPERS:
        return _CUSTOM_SCRAPERS[slug]()
    return GenericCouncilScraper(configs[slug])
