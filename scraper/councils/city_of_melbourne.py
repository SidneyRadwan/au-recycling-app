"""Static-data scraper for City of Melbourne Council (VIC)."""

from councils.base import BaseCouncilScraper
from models import BinType, CouncilData, CouncilMaterial


class CityOfMelbourneScraper(BaseCouncilScraper):
    """Returns hardcoded recycling data for the City of Melbourne LGA.

    Source: https://www.melbourne.vic.gov.au/residents/waste-recycling
    Melbourne operates a four-bin system including a dedicated FOGO bin.
    """

    council_slug = "city-of-melbourne"

    def scrape(self) -> CouncilData:
        materials: list[CouncilMaterial] = [
            # --- Yellow-lid recycling bin ---
            CouncilMaterial(
                material_slug="cardboard",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Flatten all boxes to save space. "
                    "Remove and dispose of any polystyrene packaging separately."
                ),
                notes="Wet or heavily soiled cardboard should go in general waste.",
            ),
            CouncilMaterial(
                material_slug="paper",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Newspapers, magazines, office paper, envelopes (including with "
                    "windows) and junk mail are all accepted."
                ),
            ),
            CouncilMaterial(
                material_slug="glass-bottles-and-jars",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Lids can go in recycling. No need to remove labels.",
                notes=(
                    "Pyrex, ovenware, drinking glasses and window glass are NOT accepted "
                    "— they have a different melting point and contaminate the glass stream."
                ),
            ),
            CouncilMaterial(
                material_slug="plastic-bottles-and-containers",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Melbourne accepts a wide range of rigid plastics numbered 1–7. "
                    "Rinse clean and replace lids. Containers must be larger than a credit card."
                ),
                notes=(
                    "Soft/flexible plastics (bags, wrap, sachets) are NOT accepted. "
                    "Return these to supermarket collection points."
                ),
            ),
            CouncilMaterial(
                material_slug="steel-cans",
                bin_type=BinType.RECYCLING,
                instructions="Rinse clean. Steel lids from glass jars can also go in the recycling bin.",
            ),
            CouncilMaterial(
                material_slug="aluminium-cans",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Aluminium foil and foil trays are accepted — "
                    "scrunch foil into a ball the size of a golf ball or larger."
                ),
            ),
            CouncilMaterial(
                material_slug="aerosol-cans",
                bin_type=BinType.RECYCLING,
                instructions="Ensure the can is completely empty before placing in the recycling bin.",
            ),
            CouncilMaterial(
                material_slug="milk-and-juice-cartons",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Cartons (Tetra Pak, milk cartons, juice cartons) are accepted. "
                    "Rinse and flatten where possible."
                ),
            ),
            # --- Lime/green-lid FOGO bin (Food Organics & Garden Organics) ---
            CouncilMaterial(
                material_slug="food-waste",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "All food scraps go in the lime-green FOGO bin: fruit and vegetable "
                    "peelings, meat, fish, dairy, bread, cooked food and leftovers. "
                    "Use the small kitchen caddy with compostable liners."
                ),
                notes=(
                    "City of Melbourne provides compostable caddy liners free of charge. "
                    "Collect from the Melbourne Town Hall or local council offices."
                ),
            ),
            CouncilMaterial(
                material_slug="garden-organics",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Grass clippings, leaves, weeds, prunings and small branches "
                    "(up to 10 cm diameter) go in the FOGO bin along with food scraps."
                ),
            ),
            CouncilMaterial(
                material_slug="compostable-packaging",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Certified compostable packaging (look for the seedling logo or "
                    "AS 4736 / AS 5810 certification) can go in the FOGO bin."
                ),
                notes="Conventional plastics labelled 'biodegradable' are NOT compostable — check the cert.",
            ),
            # --- Red-lid general waste bin ---
            CouncilMaterial(
                material_slug="soft-plastics",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Plastic bags, cling wrap, bubble wrap and chip packets cannot be "
                    "recycled kerbside. Place in general waste or return to supermarket collection."
                ),
            ),
            CouncilMaterial(
                material_slug="polystyrene",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Polystyrene foam goes in general waste. Do not place in recycling.",
            ),
            CouncilMaterial(
                material_slug="nappies",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="broken-glass",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Wrap in several layers of newspaper, tape securely and mark "
                    "'BROKEN GLASS' before placing in general waste."
                ),
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
                    "Do NOT place batteries in any kerbside bin. Drop off at B-cycle "
                    "points at Coles, Woolworths, Officeworks, Bunnings and council facilities."
                ),
            ),
            CouncilMaterial(
                material_slug="e-waste",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Victorian e-waste landfill ban has been in effect since 2019. "
                    "Take to a free e-waste drop-off site — search ecocentres.melbourne.vic.gov.au."
                ),
            ),
            CouncilMaterial(
                material_slug="clothing-and-textiles",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Donate wearable clothing to charity bins. "
                    "Damaged textiles can go to H&M, Zara or council clothing recycling points."
                ),
            ),
            CouncilMaterial(
                material_slug="paint",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Drop unwanted paint at a Paintback collection point — "
                    "many hardware stores participate."
                ),
            ),
            CouncilMaterial(
                material_slug="motor-oil",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions="Take used oil to an OilStewardship Australia drop-off site.",
            ),
            # --- Not accepted in kerbside recycling ---
            CouncilMaterial(
                material_slug="plastic-bags",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Never put plastic bags in the recycling bin — they tangle in sorting "
                    "machinery and cause costly shutdowns."
                ),
                notes="Return to supermarket soft-plastics drop-off.",
            ),
            CouncilMaterial(
                material_slug="drinking-glasses-and-pyrex",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Borosilicate glass (Pyrex), ovenware, drinking glasses and ceramics "
                    "are not accepted in the recycling bin."
                ),
                notes="Wrap and place in general waste.",
            ),
            CouncilMaterial(
                material_slug="medical-sharps",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Needles, syringes and lancets must be placed in an approved sharps "
                    "container and taken to a pharmacy or hospital for safe disposal."
                ),
            ),
        ]

        return CouncilData(
            name="City of Melbourne",
            slug=self.council_slug,
            state="VIC",
            website="https://www.melbourne.vic.gov.au",
            recycling_info_url="https://www.melbourne.vic.gov.au/residents/waste-recycling",
            description=(
                "City of Melbourne operates a four-bin system: red-lid general waste, "
                "yellow-lid recycling, lime-green FOGO (food and garden organics), and "
                "a purple-lid glass-only bin in some precincts. The FOGO service accepts "
                "all food scraps including meat and dairy."
            ),
            suburbs=[
                "Melbourne CBD",
                "Carlton",
                "Fitzroy",
                "Richmond",
                "South Yarra",
                "St Kilda Road Precinct",
                "Port Melbourne",
                "Docklands",
                "Southbank",
                "East Melbourne",
                "North Melbourne",
                "Parkville",
                "West Melbourne",
                "Kensington",
            ],
            materials=materials,
        )
