from Levenshtein import ratio

from src.api.suggestions.cityInterface import CityInterface
from src.utils.stringFormat import normalize_input


def _ratio(word1: str, word2: str):
    return ratio(normalize_input(word1), word2)


def calculate_levenshtein_score(q: str, city: CityInterface):
    names = [city.name] + city.alt_names
    return max(_ratio(name, q) for name in names)
