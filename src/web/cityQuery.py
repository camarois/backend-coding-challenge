from dataclasses import dataclass

from src.cities.haversine import calculate_haversine_score
from src.cities.levenshtein import calculate_levenshtein_score
from src.cities.trie import GeoCityInterface, SuffixTree


@dataclass
class CityQuery:
    query: str
    latitude: float
    longitude: float
    suffix_tree: SuffixTree

    ROUNDING = 2

    def _calculate_score(self, city: GeoCityInterface):
        if self.longitude and self.latitude:
            return calculate_levenshtein_score(self.query, city) - \
                   calculate_haversine_score(self.longitude, self.latitude, float(city.longitude), float(city.latitude))
        else:
            return calculate_levenshtein_score(self.query, city)

    def _convert_to_list(self, city: str, cities):
        geo_cities = cities.get(city)
        return [GeoCityInterface(
            id=geo_city["id"],
            name=geo_city["name"],
            alt_names=geo_city["alt_name"].split(',') if geo_city["alt_name"] else [],
            country=geo_city["admin1"] +
                    ", " + geo_city["country"] if geo_city["country"] == "US" else geo_city["country"],
            longitude=geo_city["long"],
            latitude=geo_city["lat"]
        ) for geo_city in geo_cities]

    def _convert_to_json(self, city: GeoCityInterface):
        return {
            "name": city.name + ", " + city.country,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "score": round(self._calculate_score(city), self.ROUNDING)
        }

    @staticmethod
    def _sort_by_score(cities):
        return sorted(cities, key=lambda x: x['score'], reverse=True)

    def get(self):
        cities, selected_cities = self.suffix_tree.search(self.query)
        geo_cities = [self._convert_to_list(city, cities) for city in selected_cities]
        geo_cities = [item for sublist in geo_cities for item in sublist]
        return {
            "suggestions": self._sort_by_score(
                [self._convert_to_json(geo_city) for geo_city in geo_cities]
            ) if geo_cities else []
        }
