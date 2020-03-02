"""
Helper methods for string format
"""

from unicodedata import normalize


def normalize_input(word: str):
    """Normalize according to NFD and lower string parameter"""
    return normalize("NFD", word).lower()


def clean_input_line(line: str):
    """Remove end and tab sequences in string parameter"""
    return line.rstrip("\n").split("\t")
