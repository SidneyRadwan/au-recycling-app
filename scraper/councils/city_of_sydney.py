"""Static-data scraper for City of Sydney Council (NSW)."""

from councils.base import BaseCouncilScraper
from models import BinType, CouncilData, CouncilMaterial


class CityOfSydneyScraper(BaseCouncilScraper):
    """Returns hardcoded recycling data for the City of Sydney LGA.

    Source: https://www.cityofsydney.nsw.gov.au/recycling-and-rubbish
    """

    council_slug = "city-of-sydney"

    def scrape(self) -> CouncilData:
        materials: list[CouncilMaterial] = [
            # --- Yellow-lid recycling bin ---
            CouncilMaterial(
                material_slug="cardboard",
                bin_type=BinType.RECYCLING,
                instructions="Flatten boxes and place inside bin. Remove tape where possible.",
                notes="Cardboard must be dry. Pizza boxes with grease go in general waste.",
            ),
            CouncilMaterial(
                material_slug="paper",
                bin_type=BinType.RECYCLING,
                instructions="Loose paper, newspapers, magazines and envelopes are all accepted.",
            ),
            CouncilMaterial(
                material_slug="glass-bottles-and-jars",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Lids can go in the recycling bin separately.",
                notes=(
                    "Broken glass must go in general waste wrapped in newspaper. "
                    "Pyrex, ovenware and drinking glasses are NOT accepted."
                ),
            ),
            CouncilMaterial(
                material_slug="plastic-bottles-and-containers",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse containers. Accepted plastics: 1 (PET), 2 (HDPE), "
                    "3 (PVC), 5 (PP). Check the triangle number on the base."
                ),
                notes="Squeeze air out and replace lids before placing in bin.",
            ),
            CouncilMaterial(
                material_slug="steel-cans",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Labels can be left on.",
            ),
            CouncilMaterial(
                material_slug="aluminium-cans",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Aluminium foil and foil trays are also accepted — "
                    "scrunch foil into a ball at least the size of a fist."
                ),
            ),
            CouncilMaterial(
                material_slug="aerosol-cans",
                bin_type=BinType.RECYCLING,
                instructions="Ensure completely empty before placing in recycling bin.",
                notes="Do not puncture or crush aerosols.",
            ),
            # --- Red-lid general waste bin ---
            CouncilMaterial(
                material_slug="food-waste",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "All food scraps go in the red-lid general waste bin unless "
                    "your building has a FOGO service."
                ),
                notes=(
                    "City of Sydney is rolling out a food-organics and garden-organics "
                    "(FOGO) service — check cityofsydney.nsw.gov.au for your street."
                ),
            ),
            CouncilMaterial(
                material_slug="soft-plastics",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Plastic bags, bread bags, cling wrap and chip packets are soft "
                    "plastics and must go in general waste. Do not place in recycling."
                ),
                notes=(
                    "Many Coles and Woolworths supermarkets accept soft plastics via "
                    "their in-store collection programs — check store availability."
                ),
            ),
            CouncilMaterial(
                material_slug="polystyrene",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Polystyrene foam packaging must go in the general waste bin.",
                notes="Check resourceful.sydney for drop-off locations that accept polystyrene.",
            ),
            CouncilMaterial(
                material_slug="nappies",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap soiled nappies in a bag and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="broken-glass",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap in several layers of newspaper or place in a sealed box before putting in general waste.",
                notes="Never place broken glass loose in any bin.",
            ),
            CouncilMaterial(
                material_slug="ceramics-and-crockery",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap carefully and place in general waste.",
            ),
            # --- Green-lid garden organics bin ---
            CouncilMaterial(
                material_slug="garden-organics",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Grass clippings, leaves, prunings, branches (up to 15 cm diameter) "
                    "and weeds are all accepted. Collected fortnightly."
                ),
                notes="No food waste in the green bin unless you have a FOGO service.",
            ),
            # --- Special drop-off / HHW ---
            CouncilMaterial(
                material_slug="batteries",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Do NOT place batteries in any kerbside bin — they are a fire hazard. "
                    "Drop off at council libraries, community recycling centres or "
                    "B-cycle drop-off points at many retailers."
                ),
            ),
            CouncilMaterial(
                material_slug="e-waste",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Computers, phones, TVs, printers and cables must be taken to a "
                    "drop-off point. Use the TechCollect or MobileMuster programs."
                ),
                notes="City of Sydney Community Recycling Centres accept e-waste at no cost.",
            ),
            CouncilMaterial(
                material_slug="clothing-and-textiles",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Donate wearable items to charity bins (Salvos, Vinnies, Red Cross). "
                    "Damaged textiles can be dropped at council clothing recycling points."
                ),
            ),
            CouncilMaterial(
                material_slug="paint",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Unwanted paint must go to a Paintback drop-off point. "
                    "Never pour paint down the drain or place in any kerbside bin."
                ),
            ),
            CouncilMaterial(
                material_slug="motor-oil",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Take used motor oil to an OilStewardship Australia drop-off site "
                    "(many service stations and auto stores)."
                ),
            ),
            # --- Not accepted in kerbside recycling ---
            CouncilMaterial(
                material_slug="plastic-bags",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Never place plastic bags in the recycling bin — they jam sorting machinery.",
                notes="Return to supermarket soft-plastics collection instead.",
            ),
            CouncilMaterial(
                material_slug="bubble-wrap",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Bubble wrap is a soft plastic and is not accepted in kerbside recycling.",
                notes="Drop off at supermarket soft-plastics collection.",
            ),
            CouncilMaterial(
                material_slug="drinking-glasses-and-pyrex",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Drinking glasses, Pyrex and ovenware have a different melting point "
                    "to container glass and contaminate the glass recycling stream."
                ),
                notes="Place in general waste wrapped in newspaper.",
            ),
        ]

        return CouncilData(
            name="City of Sydney",
            slug=self.council_slug,
            state="NSW",
            website="https://www.cityofsydney.nsw.gov.au",
            recycling_info_url="https://www.cityofsydney.nsw.gov.au/recycling-and-rubbish",
            description=(
                "City of Sydney Council provides weekly general waste and recycling "
                "collections, fortnightly garden organics pickup, and community "
                "recycling centres for household hazardous waste and special items."
            ),
            suburbs=[
                "Sydney",
                "Pyrmont",
                "Glebe",
                "Surry Hills",
                "Newtown",
                "Redfern",
                "Chippendale",
                "Darlinghurst",
                "Paddington",
                "Waterloo",
                "Erskineville",
                "Alexandria",
                "Beaconsfield",
                "Rosebery",
                "Zetland",
            ],
            materials=materials,
        )
