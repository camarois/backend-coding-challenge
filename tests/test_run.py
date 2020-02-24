import os
from src.cities.trie import SuffixTree
from run import app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILEPATH = os.path.join(ROOT_DIR, "../data/cities_canada-usa.tsv")


def test_construct_app():
    app()


def test_construct_suffix_tree():
    SuffixTree(os.path.join(ROOT_DIR, DATA_FILEPATH))


# def test_simple_query():
#     query = CityQuery(
#         query="Toronto",
#         latitude=43.70011,
#         longitude=-79.4163,
#         suffix_tree=SuffixTree(os.path.join(ROOT_DIR, DATA_FILEPATH))
#     )
#     cities = query.get()
#     assert any(city["name"] == "Toronto, CA" for city in cities["suggestions"])
#     assert any(city["latitude"] == 43.70011 for city in cities["suggestions"])
#     assert any(city["longitude"] == -79.4163 for city in cities["suggestions"])
