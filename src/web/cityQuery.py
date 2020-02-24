import os
from dataclasses import dataclass
from src.cities.levenshtein import calculate_distance_score
from src.cities.trie import GeoCityInterface, Trie


@dataclass
class CityQuery:
    query: str
    latitude: float
    longitude: float

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")

    def _convert_to_json(self, city: GeoCityInterface):
        return {
            "name": city.name,
            "longitude": city.longitude,
            "latitude": city.latitude,
            "score": calculate_distance_score(self.query, city)
        }

    @staticmethod
    def _sort_by_score(cities):
        return sorted(cities, key=lambda x: x['score'], reverse=True)

    def get(self):
        trie = Trie(self.DATA_FILEPATH)
        city_data = trie.search(self.query)
        return {
            "suggestions": self._sort_by_score([self._convert_to_json(city) for city in city_data]) if city_data else []
        }
