from councils.city_of_sydney import CityOfSydneyScraper
from councils.city_of_melbourne import CityOfMelbourneScraper
from councils.brisbane_city import BrisbaneCityScraper
from councils.waverley_council import WaverleyCouncilScraper
from councils.inner_west_council import InnerWestCouncilScraper

REGISTRY: dict[str, type] = {
    "city-of-sydney": CityOfSydneyScraper,
    "city-of-melbourne": CityOfMelbourneScraper,
    "brisbane-city-council": BrisbaneCityScraper,
    "waverley-council": WaverleyCouncilScraper,
    "inner-west-council": InnerWestCouncilScraper,
}


def get_all_slugs() -> list[str]:
    return list(REGISTRY.keys())


def get_scraper(slug: str):
    cls = REGISTRY.get(slug)
    if cls is None:
        raise ValueError(f"No scraper registered for slug: {slug}")
    return cls()
