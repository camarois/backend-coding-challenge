"""
Module for data models based on data inputs from cities_canada-usa.tsv
"""

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


@dataclass
class CityResponse:
    name: str
    latitude: float
    longitude: float
    score: float



