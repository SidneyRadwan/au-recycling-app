"""Tests for scraper data models."""
import pytest
from models import BinType, CouncilData, CouncilMaterial, Material


def test_bin_type_values():
    assert BinType.RECYCLING == "RECYCLING"
    assert BinType.GENERAL_WASTE == "GENERAL_WASTE"
    assert BinType.GREEN_WASTE == "GREEN_WASTE"
    assert BinType.SOFT_PLASTICS == "SOFT_PLASTICS"
    assert BinType.SPECIAL_DROP_OFF == "SPECIAL_DROP_OFF"
    assert BinType.NOT_ACCEPTED == "NOT_ACCEPTED"


def test_council_material_defaults():
    cm = CouncilMaterial(material_slug="cardboard", bin_type=BinType.RECYCLING)
    assert cm.instructions is None
    assert cm.notes is None


def test_council_data_defaults():
    cd = CouncilData(name="Test Council", slug="test-council", state="NSW")
    assert cd.suburbs == []
    assert cd.materials == []
    assert cd.website is None
    assert cd.recycling_info_url is None
    assert cd.description is None


def test_council_data_with_materials():
    materials = [
        CouncilMaterial("cardboard", BinType.RECYCLING, instructions="Flatten boxes"),
        CouncilMaterial("food-waste", BinType.GENERAL_WASTE),
    ]
    cd = CouncilData(
        name="City of Sydney",
        slug="city-of-sydney",
        state="NSW",
        website="https://www.cityofsydney.nsw.gov.au",
        materials=materials,
    )
    assert len(cd.materials) == 2
    assert cd.materials[0].bin_type == BinType.RECYCLING
    assert cd.materials[0].instructions == "Flatten boxes"


def test_material_dataclass():
    m = Material(name="Cardboard", slug="cardboard", category="Paper & Cardboard")
    assert m.description is None


def test_bin_type_is_str():
    """BinType values must be plain strings for JSON serialisation."""
    assert isinstance(BinType.RECYCLING.value, str)
