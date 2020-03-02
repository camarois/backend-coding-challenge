from src.api.models.city_models import CityInterface
from src.api.suggestions.algorithms import levenshtein
from Levenshtein import ratio

from src.utils.format_helper import normalize_input

TORONTO = CityInterface(
        id=6167865,
        name="Toronto",
        alt_names=["Gorad", "Taronta", "Torontas", "Torontu", "Torontum", "Torontó", "YTO", "duo lun duo", "roranro",
                   "taronto", "teareantea", "tho rxn to", "tolonto", "toramto", "toranto", "toronto", "twrntw",
                   "twrwntw", "Τορόντο", "Горад Таронта", "Торонто", "Տորոնտո", "टोराँटो", "तोरन्तो", "টরোন্টো", "ਟੋਰਾਂਟੋ",
                   "ரொறன்ரோ", "టొరంటో", "ಟೊರಾಂಟೋ", "ടോറോണ്ടോ", "โทรอนโต", "တိုရွန်တိုမြို့", "ტორონტო",
                   "トロント", "多伦多", "토론토"],
        country="CA",
        longitude=43.70011,
        latitude=-79.4163
    )
KEY = "tolonto"


def test_levenshtein_score():
    actual_score = levenshtein.calculate_levenshtein_score(KEY, TORONTO)

    assert actual_score == 1


def test_levenshtein_ratio():
    expected_ratio = ratio(normalize_input(TORONTO.name), KEY)
    actual_ratio = levenshtein._ratio(TORONTO.name, KEY)

    assert expected_ratio == actual_ratio
