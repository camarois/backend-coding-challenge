from Levenshtein import ratio

from src.cities.utils import normalize_input
from src.cities.trie import GeoCityInterface


def _ratio(word1: str, word2: str):
    return ratio(word1, word2)


def calculate_distance_score(q: str, city: GeoCityInterface):
    names = [city.name] + city.alt_names
    return max(_ratio(normalize_input(name), normalize_input(q)) for name in names)