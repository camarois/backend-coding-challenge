from Levenshtein import ratio
from src.cities.trie import GeoCityInterface
from src.cities.utils import normalize_input


def _ratio(word1: str, word2: str):
    return ratio(normalize_input(word1), word2)


def calculate_levenshtein_score(q: str, city: GeoCityInterface):
    names = [city.name] + city.alt_names
    return max(_ratio(name, q) for name in names)
