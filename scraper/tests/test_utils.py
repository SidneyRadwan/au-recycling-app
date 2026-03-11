"""Tests for scraper utility functions."""
import time

import pytest
from utils import slugify, retry


def test_slugify_basic():
    assert slugify("City of Sydney") == "city-of-sydney"


def test_slugify_special_chars():
    assert slugify("Moreland City Council!") == "moreland-city-council"


def test_slugify_extra_spaces():
    assert slugify("  Inner   West  Council  ") == "inner-west-council"


def test_slugify_numbers():
    assert slugify("Region 2 Council") == "region-2-council"


def test_slugify_already_slug():
    assert slugify("city-of-melbourne") == "city-of-melbourne"


def test_slugify_ampersand():
    assert slugify("Arts & Culture Council") == "arts-culture-council"


def test_retry_success_first_try():
    calls = []

    @retry(times=3)
    def succeeds():
        calls.append(1)
        return "ok"

    result = succeeds()
    assert result == "ok"
    assert len(calls) == 1


def test_retry_succeeds_on_second_try():
    calls = []

    @retry(times=3)
    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise ValueError("not yet")
        return "ok"

    result = flaky()
    assert result == "ok"
    assert len(calls) == 2


def test_retry_exhausted():
    calls = []

    @retry(times=3)
    def always_fails():
        calls.append(1)
        raise RuntimeError("always bad")

    with pytest.raises(RuntimeError, match="always bad"):
        always_fails()

    assert len(calls) == 3
