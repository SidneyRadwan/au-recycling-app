"""Static-data scraper for Brisbane City Council (QLD)."""

from councils.base import BaseCouncilScraper
from models import BinType, CouncilData, CouncilMaterial


class BrisbaneCityScraper(BaseCouncilScraper):
    """Returns hardcoded recycling data for Brisbane City Council LGA.

    Source: https://www.brisbane.qld.gov.au/clean-and-green/rubbish-and-recycling
    Brisbane operates a three-bin system. There is no kerbside food-organics
    collection — food waste goes in general waste.
    Note: REDcycle collapsed in November 2022; soft plastics are now directed to
    supermarket-based programs (Coles, Woolworths) where available.
    """

    council_slug = "brisbane-city"

    def scrape(self) -> CouncilData:
        materials: list[CouncilMaterial] = [
            # --- Yellow-lid recycling bin ---
            CouncilMaterial(
                material_slug="cardboard",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Flatten boxes and place in the yellow-lid bin. "
                    "Remove polystyrene inserts and place them in general waste."
                ),
                notes="Large quantities of cardboard can be taken to a Brisbane City Council recycling drop-off.",
            ),
            CouncilMaterial(
                material_slug="paper",
                bin_type=BinType.RECYCLING,
                instructions="Newspapers, magazines, catalogues, office paper and envelopes are all accepted.",
            ),
            CouncilMaterial(
                material_slug="glass-bottles-and-jars",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Lids should be replaced on glass jars before placing "
                    "in the bin, or recycled separately. Labels do not need to be removed."
                ),
                notes=(
                    "Pyrex, ovenware, drinking glasses and window glass are NOT accepted. "
                    "These contaminate the glass recycling stream."
                ),
            ),
            CouncilMaterial(
                material_slug="plastic-bottles-and-containers",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Accepted: bottles and containers with a recycling triangle on the base. "
                    "Rinse clean and replace lids. Items must be larger than a credit card."
                ),
                notes="Soft and flexible plastics are NOT accepted kerbside.",
            ),
            CouncilMaterial(
                material_slug="steel-cans",
                bin_type=BinType.RECYCLING,
                instructions="Rinse food residue. Steel aerosol cans are also accepted when empty.",
            ),
            CouncilMaterial(
                material_slug="aluminium-cans",
                bin_type=BinType.RECYCLING,
                instructions=(
                    "Rinse clean. Aluminium foil is also accepted — scrunch into a ball. "
                    "Consider the 10c Container Deposit Scheme (Containers for Change) "
                    "for eligible drink containers to earn a refund."
                ),
                notes=(
                    "Queensland's Containers for Change scheme pays 10c per eligible "
                    "container. Most drink bottles and cans 150 mL–3 L qualify."
                ),
            ),
            CouncilMaterial(
                material_slug="milk-and-juice-cartons",
                bin_type=BinType.RECYCLING,
                instructions="Rinse and flatten cartons (Tetra Pak, milk cartons) before placing in bin.",
            ),
            # --- Green-lid garden organics bin ---
            CouncilMaterial(
                material_slug="garden-organics",
                bin_type=BinType.GREEN_WASTE,
                instructions=(
                    "Grass clippings, leaves, weeds, prunings and branches up to 15 cm "
                    "diameter are accepted. Collected fortnightly."
                ),
                notes=(
                    "Brisbane does NOT have a kerbside food-organics service. "
                    "Food scraps must go in general waste or be home composted."
                ),
            ),
            # --- Red-lid general waste bin ---
            CouncilMaterial(
                material_slug="food-waste",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "All food scraps go in the red-lid general waste bin. "
                    "Consider home composting or a worm farm to divert food waste from landfill."
                ),
                notes="Brisbane City Council offers subsidised compost bins — check brisbane.qld.gov.au/compost.",
            ),
            CouncilMaterial(
                material_slug="soft-plastics",
                bin_type=BinType.GENERAL_WASTE,
                instructions=(
                    "Plastic bags, cling wrap, bread bags, chip packets and other soft "
                    "plastics must go in general waste."
                ),
                notes=(
                    "Some Coles and Woolworths stores have in-store soft-plastics "
                    "collection points — check store availability before visiting."
                ),
            ),
            CouncilMaterial(
                material_slug="polystyrene",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Polystyrene foam packaging must go in general waste.",
            ),
            CouncilMaterial(
                material_slug="nappies",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap and seal soiled nappies before placing in general waste.",
            ),
            CouncilMaterial(
                material_slug="broken-glass",
                bin_type=BinType.GENERAL_WASTE,
                instructions="Wrap carefully in thick newspaper and place in general waste.",
            ),
            # --- Special drop-off ---
            CouncilMaterial(
                material_slug="batteries",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Do NOT place batteries in any kerbside bin — serious fire risk. "
                    "Drop off at B-cycle points at Coles, Woolworths, Officeworks, "
                    "Bunnings and Brisbane City Council facilities."
                ),
            ),
            CouncilMaterial(
                material_slug="e-waste",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Computers, TVs, phones and accessories can be dropped off at "
                    "Brisbane City Council's Recycling Drop-off Centres at no cost. "
                    "TechCollect also has drop-off points across Brisbane."
                ),
            ),
            CouncilMaterial(
                material_slug="paint",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Drop off unwanted paint at a Paintback collection site. "
                    "Never pour paint down the drain or place in kerbside bins."
                ),
            ),
            CouncilMaterial(
                material_slug="motor-oil",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Used motor oil can be dropped off at Brisbane City Council "
                    "Recycling Drop-off Centres. Many service stations also accept it."
                ),
            ),
            CouncilMaterial(
                material_slug="clothing-and-textiles",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Donate wearable clothing to charity bins (Salvos, Vinnies, "
                    "Red Cross). Damaged textiles can go to council collection points."
                ),
            ),
            # --- Container Deposit Scheme ---
            CouncilMaterial(
                material_slug="eligible-drink-containers",
                bin_type=BinType.SPECIAL_DROP_OFF,
                instructions=(
                    "Under Queensland's Containers for Change scheme, eligible drink "
                    "containers (most 150 mL–3 L bottles, cans, cartons) earn 10c each. "
                    "Find your nearest refund point at containersforchange.com.au."
                ),
                notes="Containers can also be put in the yellow-lid recycling bin if you don't want the refund.",
            ),
            # --- Not accepted in kerbside recycling ---
            CouncilMaterial(
                material_slug="plastic-bags",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Never put plastic bags in the yellow-lid recycling bin — "
                    "they tangle in sorting machinery. Place in general waste."
                ),
            ),
            CouncilMaterial(
                material_slug="drinking-glasses-and-pyrex",
                bin_type=BinType.NOT_ACCEPTED,
                instructions=(
                    "Drinking glasses, Pyrex and ovenware are not accepted in any "
                    "kerbside bin. Wrap and place in general waste."
                ),
            ),
            CouncilMaterial(
                material_slug="ceramics-and-crockery",
                bin_type=BinType.NOT_ACCEPTED,
                instructions="Wrap carefully and place in general waste.",
            ),
        ]

        return CouncilData(
            name="Brisbane City Council",
            slug=self.council_slug,
            state="QLD",
            website="https://www.brisbane.qld.gov.au",
            recycling_info_url="https://www.brisbane.qld.gov.au/clean-and-green/rubbish-and-recycling",
            description=(
                "Brisbane City Council operates a three-bin kerbside system: "
                "red-lid general waste (weekly), yellow-lid recycling (fortnightly) "
                "and green-lid garden organics (fortnightly). Brisbane does not "
                "currently offer kerbside food-organics collection. Queensland's "
                "Containers for Change scheme provides 10c refunds on eligible containers."
            ),
            suburbs=[
                "Brisbane CBD",
                "Fortitude Valley",
                "New Farm",
                "Teneriffe",
                "Paddington",
                "Red Hill",
                "Ashgrove",
                "Toowong",
                "West End",
                "South Brisbane",
                "Spring Hill",
                "Kelvin Grove",
                "Auchenflower",
                "Milton",
                "Petrie Terrace",
            ],
            materials=materials,
        )
