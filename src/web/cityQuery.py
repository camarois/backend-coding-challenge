import os
from dataclasses import dataclass
from src.cities.levenshtein import calculate_distance_score
from src.cities.trie import GeoCityInterface, SuffixTree


@dataclass
class CityQuery:
    query: str
    latitude: float
    longitude: float

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")

    def _convert_to_list(self, city: str, cities):
        geo_cities = cities.get(city)
        return [GeoCityInterface(
            id=geo_city["id"],
            name=geo_city["name"],
            alt_names=geo_city["alt_name"].split(',') if geo_city["alt_name"] else [],
            longitude=float(geo_city["long"]),
            latitude=float(geo_city["lat"]),
        ) for geo_city in geo_cities]

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
        suffix_tree = SuffixTree(self.DATA_FILEPATH)

        cities, selected_cities = suffix_tree.search(self.query)
        geo_cities = [self._convert_to_list(city, cities) for city in selected_cities]
        geo_cities = [item for sublist in geo_cities for item in sublist]
        return {
            "suggestions": self._sort_by_score(
                [self._convert_to_json(geo_city) for geo_city in geo_cities]
            ) if geo_cities else []
        }
