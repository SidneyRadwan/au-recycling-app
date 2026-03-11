from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class BinType(str, Enum):
    RECYCLING = "RECYCLING"
    GENERAL_WASTE = "GENERAL_WASTE"
    GREEN_WASTE = "GREEN_WASTE"
    SOFT_PLASTICS = "SOFT_PLASTICS"
    SPECIAL_DROP_OFF = "SPECIAL_DROP_OFF"
    NOT_ACCEPTED = "NOT_ACCEPTED"


@dataclass
class Material:
    name: str
    slug: str
    category: str
    description: Optional[str] = None


@dataclass
class CouncilMaterial:
    material_slug: str
    bin_type: BinType
    instructions: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class CouncilData:
    name: str
    slug: str
    state: str
    website: Optional[str] = None
    recycling_info_url: Optional[str] = None
    description: Optional[str] = None
    suburbs: list[str] = field(default_factory=list)
    materials: list[CouncilMaterial] = field(default_factory=list)
