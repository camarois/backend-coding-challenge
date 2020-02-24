from typing import List
from dataclasses import dataclass
from src.cities.utils import clean_input_line, normalize_input


@dataclass
class GeoCityInterface:
    id: str
    name: str
    alt_names: List[str]
    longitude: float
    latitude: float


class WordNode:
    def __init__(self, val):
        self.val = val
        self.children = {}
        self.isWord = False
        self.data = None


class Trie:
    def __init__(self, file_path: str):
        """
        Initialize your data structure here.
        """
        self.root = WordNode("")
        self.cities = []

        with open(file_path, 'r', encoding='utf8') as file:
            column_names = clean_input_line(next(file))
            raw_inputs = [dict(zip(column_names, clean_input_line(line))) for line in file]

        for city in raw_inputs:
            self.insert(city["name"], city)

    def insert(self, word: str, city: {}) -> None:
        """
        Inserts a word into the trie.
        """
        curr = self.root
        for letter in normalize_input(word):
            if letter not in curr.children:
                curr.children[letter] = WordNode(letter)

            curr = curr.children[letter]

        curr.isWord = True
        curr.data = GeoCityInterface(
            id=city["id"],
            name=city["name"],
            alt_names=city["alt_name"].split(',') if city['alt_name'] else [],
            longitude=float(city["long"]),
            latitude=float(city["lat"])
        )

    def suggestionsRec(self, node, word):
        if node.isWord:
            self.cities.append(node.data)

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def search(self, key):
        if not key:
            return []

        node = self.root
        not_found = False
        temp_word = ''

        for a in list(normalize_input(key)):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]

        if not_found:
            return None
        elif node.isWord and not node.children:
            return [node.data]

        self.suggestionsRec(node, temp_word)

        return self.cities
