from dataclasses import dataclass
from src.cities.parser import load_data
from src.cities.trie import GeoCityInterface


@dataclass
class CityQuery:
    query: str
    latitude: float
    longitude: float

    DATA_FILEPATH = "../data/cities_canada-usa.tsv"

    def _convert_city_to_json(self, city: GeoCityInterface):
        return {
            "name": city.name,
            "longitude": city.longitude,
            "latitude": city.latitude,
        }

    def get(self):
        trie = load_data(self.DATA_FILEPATH)
        city_data = trie.search(self.query)
        return {
            "suggestions": [self._convert_city_to_json(city) for city in city_data] if city_data else []
        }