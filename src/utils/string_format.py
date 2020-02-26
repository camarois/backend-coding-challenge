from unicodedata import normalize


def normalize_input(word: str):
    return normalize("NFD", word).lower()


def clean_input_line(line: str):
    return line.rstrip("\n").split("\t")
