"""
Module for suggestions api route methods
"""

from dataclasses import dataclass

from src.api.suggestions.algorithms.haversine import calculate_haversine_score
from src.api.suggestions.algorithms.levenshtein import calculate_levenshtein_score
from src.api.models.city_models import CityInterface, CityResponse
from src.utils.suffix_tree import SuffixTree


@dataclass
class CityQuery:
    suffix_tree: SuffixTree

    ROUNDING_DECIMALS = 2
    MAX_CITY_RESULTS = 10

    @staticmethod
    def _calculate_score(city: CityInterface, query, latitude, longitude):
        """Return city score according to query parameters"""
        if longitude and latitude:
            return calculate_levenshtein_score(query, city) - \
                   calculate_haversine_score(
                       latitude,
                       longitude,
                       float(city.latitude),
                       float(city.longitude)
                   )
        return calculate_levenshtein_score(query, city)

    def _sort_by_score(self, cities):
        """Returns highest-scoring city list"""
        return sorted(cities, key=lambda x: x.score, reverse=True)[:self.MAX_CITY_RESULTS]

    def get(self, query, latitude, longitude):
        """Returns json city suggestions according to query search"""
        cities, selected_cities = self.suffix_tree.search(query)
        selected_cities = [_convert_to_city_interface_list(cities.get(city)) for city in selected_cities]
        selected_cities = [item for sublist in selected_cities for item in sublist]

        return {
            "suggestions": self._sort_by_score(
                [CityResponse(
                    city.name + ", " + city.country,
                    city.latitude,
                    city.longitude,
                    max(0, round(self._calculate_score(city, query, latitude, longitude), self.ROUNDING_DECIMALS))
                ) for city in selected_cities]
            ) if selected_cities else []
        }


def _convert_to_city_interface_list(cities: list):
    """Converts selected suffix tree cities to list of city interfaces"""
    return [CityInterface(
        id=city["id"],
        name=city["name"],
        alt_names=city["alt_name"].split(',') if city["alt_name"] else [],
        country=city["admin1"] + ", " + city["country"]
        if city["country"] == "US" else city["country"],
        longitude=city["long"],
        latitude=city["lat"]
    ) for city in cities]
