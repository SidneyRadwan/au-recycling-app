"""Static-data scraper for Inner West Council (NSW)."""

from councils.base import BaseCouncilScraper
from models import BinType, CouncilData, CouncilMaterial


class InnerWestCouncilScraper(BaseCouncilScraper):
    """Returns hardcoded recycling data for Inner West Council LGA (NSW).

    Source: https://www.innerwest.nsw.gov.au/live/waste-and-recycling
    Inner West Council was formed in 2016 from the former Ashfield, Leichhardt
    and Marrickville councils. It offers a four-bin system including FOGO in
    most streets.
    """

    council_slug = "inner-west-council"

    def scrape(self) -> CouncilData:
        materials: list[CouncilMaterial] = [
            # --- Yellow-lid recycling bin ---
            CouncilMaterial(
                material_slug="cardboard",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Flatten boxes. Remove polystyrene inserts and place in general waste. "
                    "Greasy pizza boxes go in the FOGO bin or general waste."
                ),
            ),
            CouncilMaterial(
                material_slug="paper",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Newspapers, magazines, office paper, envelopes, junk mail "
                    "and paper bags are all accepted."
                ),
            ),
            CouncilMaterial(
                material_slug="glass-bottles-and-jars",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Replace lids (metal or plastic lids are fine).",
                notes="Pyrex, ceramics, drinking glasses and window glass are NOT accepted.",
            ),
            CouncilMaterial(
                material_slug="plastic-bottles-and-containers",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Accepted: rigid plastic bottles and containers (any resin code). "
                    "Rinse clean and replace lids. Larger than a credit card."
                ),
                notes="Flexible/soft plastics including bags and cling wrap are not accepted kerbside.",
            ),
            CouncilMaterial(
                material_slug="steel-cans",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Empty aerosol cans also accepted.",
            ),
            CouncilMaterial(
                material_slug="aluminium-cans",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Aluminium foil trays and foil sheets are accepted "
                    "when scrunched into a ball larger than a golf ball."
                ),
                notes=(
                    "Eligible containers can alternatively be returned for 10c via "
                    "NSW Return and Earn reverse vending machines."
                ),
            ),
            CouncilMaterial(
                material_slug="milk-and-juice-cartons",
                bin_type=BinType.RECYCLING,
                instructions="Rinse and flatten cartons before placing in the yellow-lid bin.",
            ),
            # --- Lime-lid FOGO bin ---
            CouncilMaterial(
                material_slug="food-waste",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "All food scraps go in the lime-green FOGO bin: fruit and veg, "
                    "meat, fish, dairy, bread, cooked food, coffee grounds and tea bags. "
                    "Use a kitchen caddy lined with a compostable bag."
                ),
                notes=(
                    "Inner West Council provides free compostable liners to residents. "
                    "Collect from council offices or libraries."
                ),
            ),
            CouncilMaterial(
                material_slug="garden-organics",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Grass clippings, leaves, weeds and prunings up to 15 cm diameter "
                    "go in the FOGO bin. Collected weekly alongside general waste."
                ),
            ),
            CouncilMaterial(
                material_slug="compostable-packaging",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Certified compostable items (AS 4736 / AS 5810 seedling logo) "
                    "are accepted in the FOGO bin."
                ),
                notes="Conventional plastics marketed as 'biodegradable' are NOT accepted.",
            ),
            # --- Red-lid general waste bin ---
            CouncilMaterial(
                material_slug="soft-plastics",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Soft plastics (plastic bags, cling wrap, chip packets) go in general waste. "
                    "Some supermarkets accept them in-store."
                ),
            ),
            CouncilMaterial(
                material_slug="polystyrene",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Polystyrene foam goes in general waste.",
            ),
            CouncilMaterial(
                material_slug="nappies",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="broken-glass",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap in several layers of newspaper and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="ceramics-and-crockery",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap carefully and place in general waste.",
            ),
            # --- Special drop-off ---
            CouncilMaterial(
                material_slug="batteries",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Drop off at B-cycle points at supermarkets, Officeworks, "
                    "Bunnings or Inner West Council facilities."
                ),
            ),
            CouncilMaterial(
                material_slug="e-waste",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Free e-waste drop-off at Inner West Council depots in "
                    "Marrickville and Leichhardt. Also via TechCollect and MobileMuster."
                ),
            ),
            CouncilMaterial(
                material_slug="paint",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions="Drop at Paintback collection points — hardware stores and council depots.",
            ),
            CouncilMaterial(
                material_slug="clothing-and-textiles",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Donate wearable items to charity bins. "
                    "Damaged textiles to council recycling points."
                ),
            ),
            CouncilMaterial(
                material_slug="motor-oil",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions="Take to OilStewardship Australia drop-off sites — many service stations.",
            ),
            # --- Container Deposit Scheme ---
            CouncilMaterial(
                material_slug="eligible-drink-containers",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "NSW Return and Earn: 10c refund on eligible drink containers "
                    "at reverse vending machines across the Inner West."
                ),
            ),
            # --- Not accepted ---
            CouncilMaterial(
                material_slug="plastic-bags",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Never place plastic bags in the yellow-lid recycling bin.",
                notes="Place in general waste or return to supermarket collection.",
            ),
            CouncilMaterial(
                material_slug="drinking-glasses-and-pyrex",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Wrap and place in general waste.",
            ),
        ]

        return CouncilData(
            name="Inner West Council",
            slug=self.council_slug,
            state="NSW",
            website="https://www.innerwest.nsw.gov.au",
            recycling_info_url="https://www.innerwest.nsw.gov.au/live/waste-and-recycling",
            description=(
                "Inner West Council operates a four-bin system across the former "
                "Ashfield, Leichhardt and Marrickville LGAs. The FOGO lime-green bin "
                "accepts all food scraps and garden organics. General waste and FOGO "
                "are collected weekly; recycling and bulk waste are collected fortnightly."
            ),
            suburbs=[
                "Newtown",
                "Marrickville",
                "Leichhardt",
                "Balmain",
                "Rozelle",
                "Annandale",
                "Glebe",
                "Ashfield",
                "Summer Hill",
                "Petersham",
                "Enmore",
                "St Peters",
                "Sydenham",
                "Tempe",
                "Dulwich Hill",
            ],
            materials=materials,
        )
