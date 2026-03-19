"""Unit tests for seed_recycling_urls scoring logic."""

from scripts.seed_recycling_urls import _score_link, _select_best


BASE_URL = "https://www.council.nsw.gov.au"
BASE_NETLOC = "www.council.nsw.gov.au"


def score(path: str, text: str) -> int:
    href = f"{BASE_URL}{path}"
    s, _ = _score_link(href, text, BASE_URL, BASE_NETLOC)
    return s


def best(links: list[tuple[str, str]]) -> str | None:
    full_links = [(f"{BASE_URL}{path}", text) for path, text in links]
    return _select_best(full_links, BASE_URL)


# ---------------------------------------------------------------------------
# Scoring tiers
# ---------------------------------------------------------------------------


class TestScoring:
    def test_primary_waste_and_recycling(self):
        assert score("/services/waste-and-recycling", "Waste & Recycling") == 2

    def test_primary_recycling_and_waste(self):
        assert score("/residents/recycling-and-waste", "Recycling and Waste") == 2

    def test_primary_waste_recycling_no_and(self):
        assert score("/services/waste-recycling", "Waste & Recycling") == 2

    def test_primary_via_text_only(self):
        """Primary keyword detected from link text even if slug is generic."""
        assert score("/environment/our-services", "Waste and Recycling") == 2

    def test_primary_waste(self):
        assert score("/residents/waste", "Waste") == 2

    def test_primary_recycling(self):
        assert score("/residents/recycling", "Recycling") == 2

    def test_primary_rubbish(self):
        assert score("/residents/rubbish-collection", "Rubbish") == 2

    def test_secondary_only_bin_collection_days(self):
        """Multiple secondary keyword hits do not accumulate."""
        assert score("/services/bin-collection-days", "Bin Collection Days") == 1

    def test_secondary_only_kerbside(self):
        assert score("/services/kerbside-collection", "Kerbside Collection") == 1

    def test_secondary_only_fogo(self):
        assert score("/services/food-and-garden-organics", "FOGO") == 1

    def test_secondary_only_bins(self):
        assert score("/residents/bins", "Bins") == 1

    def test_no_match(self):
        assert score("/about/contact", "Contact Us") == 0

    def test_no_match_roads(self):
        assert score("/services/roads-and-transport", "Roads") == 0

    def test_different_domain_skipped(self):
        s, _ = _score_link(
            "https://www.other.gov.au/waste", "Waste", BASE_URL, BASE_NETLOC
        )
        assert s == 0

    def test_skip_path_login(self):
        assert score("/login/waste", "Waste") == 0


# ---------------------------------------------------------------------------
# Section root wins over deep operational page (real-world examples)
# ---------------------------------------------------------------------------


class TestSectionRootPreferred:
    def test_canterbury_bankstown(self):
        """waste-and-recycling section root beats bin-collection-days."""
        result = best(
            [
                ("/residents/waste-and-recycling", "Waste and Recycling"),
                ("/residents/bin-collection-days", "Bin Collection Days"),
                ("/residents/bins", "Bins"),
            ]
        )
        assert result == f"{BASE_URL}/residents/waste-and-recycling"

    def test_albury(self):
        """waste-and-recycling section root beats collection-days-and-bins subpage (depth 3, filtered)."""
        result = best(
            [
                ("/services/waste-and-recycling", "Waste and Recycling"),
                (
                    "/services/waste-and-recycling/collection-days-and-bins",
                    "Collection Days",
                ),
            ]
        )
        assert result == f"{BASE_URL}/services/waste-and-recycling"

    def test_maitland(self):
        """waste-recycling section root beats food-and-garden-organics subpage (depth 3, filtered)."""
        result = best(
            [
                ("/services/waste-recycling", "Waste & Recycling"),
                ("/services/waste-recycling/food-and-garden-organics", "FOGO"),
                ("/services/waste-recycling/bulky-waste-service", "Book Bulky Waste"),
                ("/residents/bins", "Bins"),
            ]
        )
        assert result == f"{BASE_URL}/services/waste-recycling"

    def test_single_primary_beats_multiple_secondary(self):
        """waste alone (score 2) beats bin + collection + kerbside (score 1)."""
        result = best(
            [
                ("/residents/waste", "Waste"),
                ("/services/bin-kerbside-collection", "Bin Kerbside Collection Days"),
            ]
        )
        assert result == f"{BASE_URL}/residents/waste"

    def test_no_recycling_links(self):
        result = best(
            [
                ("/about/contact", "Contact Us"),
                ("/about/news", "News"),
            ]
        )
        assert result is None
