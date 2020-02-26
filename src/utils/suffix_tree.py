from collections import defaultdict
import suffixtree as st
from src.utils.string_format import clean_input_line, normalize_input


class SuffixTree:
    COLUMN_ID = "name"

    def __init__(self, file_path: str):
        self.tree = st.SuffixTree(True, [])
        self.children = defaultdict(list)

        with open(file_path, 'r', encoding='utf8') as file:
            column_names = clean_input_line(next(file))
            raw_inputs = [dict(zip(column_names, clean_input_line(line))) for line in file]

        for child in raw_inputs:
            self.tree.addStrings([normalize_input(child[self.COLUMN_ID])])
            self.children[normalize_input(child[self.COLUMN_ID])].append(child)
        self.tree = self.tree.createQueryTree()
        self.tree.cacheNodes()

    def search(self, key):
        selected_cities = set(self.tree.findString(key)) if len(key) > 0 else []
        return self.children, selected_cities
