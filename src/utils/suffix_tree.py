"""
Suffix tree creation and usage methods
"""

from collections import defaultdict
import os
import suffixtree as st
from src.utils.format_helper import clean_input_line, normalize_input


class SuffixTree:
    COLUMN_ID = "name"
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILEPATH = os.path.join(ROOT_DIR, "../../data/cities_canada-usa.tsv")

    def __init__(self):
        """Creates suffix tree in O(n) for n number of string for constant-sized alphabets, O(1) for insertion in
        hashmap """
        self.tree = st.SuffixTree(True, [])
        self.children = defaultdict(list)

        with open(self.DATA_FILEPATH, 'r', encoding='utf8') as file:
            column_names = clean_input_line(next(file))
            raw_inputs = [dict(zip(column_names, clean_input_line(line))) for line in file]

        for child in raw_inputs:
            self.tree.addStrings([normalize_input(child[self.COLUMN_ID])])
            self.children[normalize_input(child[self.COLUMN_ID])].append(child)
        self.tree = self.tree.createQueryTree()
        self.tree.cacheNodes()

    def search(self, key):
        """Returns tree dictionary and list of selected cities according to key parameter. Search is O(m),
        for m length of key """
        selected_cities = set(self.tree.findString(key)) if len(key) > 0 else []
        return self.children, selected_cities
