from dataclasses import dataclass

from src.api.suggestions.algorithms.haversine import calculate_haversine_score
from src.api.suggestions.algorithms.levenshtein import calculate_levenshtein_score
from src.api.suggestions.cityInterface import CityInterface
from src.utils.suffixTree import SuffixTree


@dataclass
class CityQuery:
    query: str
    latitude: float
    longitude: float
    suffix_tree: SuffixTree

    ROUNDING = 2

    def _calculate_score(self, city: CityInterface):
        if self.longitude and self.latitude:
            return calculate_levenshtein_score(self.query, city) - \
                   calculate_haversine_score(self.longitude, self.latitude, float(city.longitude), float(city.latitude))
        else:
            return calculate_levenshtein_score(self.query, city)

    def _convert_to_json(self, city: CityInterface):
        return {
            "name": city.name + ", " + city.country,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "score": round(self._calculate_score(city), self.ROUNDING)
        }

    @staticmethod
    def _convert_to_list(self, cities: list):
        return [CityInterface(
            id=city["id"],
            name=city["name"],
            alt_names=city["alt_name"].split(',') if city["alt_name"] else [],
            country=city["admin1"] + ", " + city["country"]
            if city["country"] == "US" else city["country"],
            longitude=city["long"],
            latitude=city["lat"]
        ) for city in cities]

    @staticmethod
    def _sort_by_score(cities):
        return sorted(cities, key=lambda x: x['score'], reverse=True)

    def get(self):
        cities, selected_cities = self.suffix_tree.search(self.query)
        selected_cities = [self._convert_to_list(cities.get(city)) for city in selected_cities]
        selected_cities = [item for sublist in selected_cities for item in sublist]

        return {
            "suggestions": self._sort_by_score(
                [self._convert_to_json(city) for city in selected_cities]
            ) if selected_cities else []
        }
