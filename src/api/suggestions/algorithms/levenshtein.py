"""
Module calculating levenshtein distance measuring difference between 2 string sequences
"""

from Levenshtein import ratio

from src.api.models.city_models import CityInterface
from src.utils.format_helper import normalize_input


def _ratio(word1: str, word2: str):
    """Returns levenshtein distance between 2 normalized string parameters"""
    return ratio(normalize_input(word1), word2)


def calculate_levenshtein_score(key: str, city: CityInterface):
    """Returns maximum levenshtein distance between a city's possible names and search key"""
    names = [city.name] + city.alt_names
    return max(_ratio(name, key) for name in names)
