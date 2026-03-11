"""Static-data scraper for Waverley Council (NSW)."""

from councils.base import BaseCouncilScraper
from models import BinType, CouncilData, CouncilMaterial


class WaverleyCouncilScraper(BaseCouncilScraper):
    """Returns hardcoded recycling data for Waverley Council LGA (NSW).

    Source: https://www.waverley.nsw.gov.au/environment/waste-and-recycling
    Waverley covers Bondi Beach, Bondi Junction, Rose Bay, Vaucluse and surrounds.
    """

    council_slug = "waverley-council"

    def scrape(self) -> CouncilData:
        materials: list[CouncilMaterial] = [
            # --- Yellow-lid recycling bin ---
            CouncilMaterial(
                material_slug="cardboard",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Flatten all cardboard boxes. Pizza boxes with excessive grease "
                    "should go in general waste."
                ),
            ),
            CouncilMaterial(
                material_slug="paper",
                bin_type=BinType.RECYCLING,
                instructions="Newspapers, magazines, office paper and envelopes are accepted.",
            ),
            CouncilMaterial(
                material_slug="glass-bottles-and-jars",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Lids can be recycled separately.",
                notes="Pyrex, ovenware, ceramics and drinking glasses are NOT accepted.",
            ),
            CouncilMaterial(
                material_slug="plastic-bottles-and-containers",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Accepted plastics: 1 (PET), 2 (HDPE), 3 (PVC), 5 (PP). "
                    "Rinse clean and replace lids before placing in bin."
                ),
            ),
            CouncilMaterial(
                material_slug="steel-cans",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean.",
            ),
            CouncilMaterial(
                material_slug="aluminium-cans",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Aluminium foil is also accepted — "
                    "scrunch into a ball at least the size of a golf ball."
                ),
                notes=(
                    "NSW Container Deposit Scheme (Return and Earn) pays 10c per "
                    "eligible container. Many reverse vending machines in the LGA."
                ),
            ),
            CouncilMaterial(
                material_slug="milk-and-juice-cartons",
                bin_type=BinType.RECYCLING,
                instructions="Rinse and flatten Tetra Pak and milk cartons.",
            ),
            # --- Green-lid garden organics bin ---
            CouncilMaterial(
                material_slug="garden-organics",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Grass clippings, leaves, weeds and prunings (branches up to 10 cm "
                    "diameter) are accepted. Collected fortnightly."
                ),
                notes="Waverley Council is trialling a FOGO service — check waverley.nsw.gov.au for updates.",
            ),
            # --- Red-lid general waste bin ---
            CouncilMaterial(
                material_slug="food-waste",
                bin_type=BinType.GENERAL_WASTE,
                instructions="All food scraps go in general waste.",
            ),
            CouncilMaterial(
                material_slug="soft-plastics",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Soft plastics (plastic bags, cling wrap, chip packets) go in general waste."
                ),
                notes="Some supermarkets accept soft plastics in-store — check store availability.",
            ),
            CouncilMaterial(
                material_slug="polystyrene",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Polystyrene foam must go in general waste.",
            ),
            CouncilMaterial(
                material_slug="nappies",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="broken-glass",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap carefully in newspaper and place in general waste.",
            ),
            # --- Special drop-off ---
            CouncilMaterial(
                material_slug="batteries",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Drop off at B-cycle collection points at Woolworths Bondi Junction, "
                    "Coles Bondi Beach and the Waverley Council depot."
                ),
            ),
            CouncilMaterial(
                material_slug="e-waste",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Take e-waste to Waverley Council's Community Recycling Centre "
                    "or to a TechCollect drop-off site."
                ),
            ),
            CouncilMaterial(
                material_slug="paint",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions="Drop off at Paintback collection points — check paintback.com.au.",
            ),
            CouncilMaterial(
                material_slug="clothing-and-textiles",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions="Donate to charity bins or council clothing recycling drop-off points.",
            ),
            # --- Container Deposit Scheme ---
            CouncilMaterial(
                material_slug="eligible-drink-containers",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "NSW Return and Earn pays 10c per eligible container at reverse vending "
                    "machines. Bondi Junction Westfield and several local stores have machines."
                ),
            ),
            # --- Not accepted ---
            CouncilMaterial(
                material_slug="plastic-bags",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Never place plastic bags in the recycling bin.",
            ),
            CouncilMaterial(
                material_slug="drinking-glasses-and-pyrex",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Wrap carefully and place in general waste.",
            ),
        ]

        return CouncilData(
            name="Waverley Council",
            slug=self.council_slug,
            state="NSW",
            website="https://www.waverley.nsw.gov.au",
            recycling_info_url="https://www.waverley.nsw.gov.au/environment/waste-and-recycling",
            description=(
                "Waverley Council provides weekly general waste and recycling collections "
                "and fortnightly garden organics pickup. The LGA includes popular coastal "
                "suburbs Bondi Beach and Rose Bay. NSW Return and Earn container deposit "
                "machines are accessible throughout the area."
            ),
            suburbs=[
                "Bondi",
                "Bondi Beach",
                "Bondi Junction",
                "Rose Bay",
                "Vaucluse",
                "Tamarama",
                "Bronte",
                "Waverley",
                "Dover Heights",
                "Watson's Bay",
            ],
            materials=materials,
        )
