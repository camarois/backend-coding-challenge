import suffixtree as st
from collections import defaultdict
from typing import List
from dataclasses import dataclass
from src.cities.utils import clean_input_line, normalize_input


@dataclass
class GeoCityInterface:
    id: str
    name: str
    alt_names: List[str]
    country: str
    longitude: float
    latitude: float


class SuffixTree:
    def __init__(self, file_path: str):
        self.tree = st.SuffixTree(True, [])
        self.cities = defaultdict(list)

        with open(file_path, 'r', encoding='utf8') as file:
            column_names = clean_input_line(next(file))
            raw_inputs = [dict(zip(column_names, clean_input_line(line))) for line in file]

        for city in raw_inputs:
            self.tree.addStrings([normalize_input(city["name"])])
            self.cities[normalize_input(city["name"])].append(city)
        self.tree = self.tree.createQueryTree()
        self.tree.cacheNodes()

    def search(self, key):
        return self.cities, set(self.tree.findString(key))
