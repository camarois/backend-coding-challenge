from dataclasses import dataclass
from typing import List


@dataclass
class CityInterface:
    id: str
    name: str
    alt_names: List[str]
    country: str
    longitude: float
    latitude: float
