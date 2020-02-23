from src.cities.trie import Trie


def clean_input_line(line):
    return line.rstrip("\n").split("\t")


def load_data(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        column_names = clean_input_line(next(file))
        raw_inputs = [dict(zip(column_names, clean_input_line(line))) for line in file]
        return Trie(raw_inputs)
