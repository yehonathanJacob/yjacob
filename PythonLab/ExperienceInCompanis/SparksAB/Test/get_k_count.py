import logging
import argparse

import pandas as pd

from preprocess_text import preprocces_text_to_words
from models import WordCountColumnNames

logging.basicConfig(level=logging.DEBUG)


def generate_table_count_word(words: list) -> pd.DataFrame:
    table_of_words = pd.DataFrame(words)
    series_count = table_of_words[0].value_counts()
    table_count = pd.DataFrame(
        {WordCountColumnNames.word: series_count.index, WordCountColumnNames.count: series_count.values})
    logging.info(f"Mean: {table_count['Count'].mean()} Median: {table_count['Count'].median()}")
    return table_count


def generate_k_count_table(text: str, k: int, words_to_get_ignored=None, language=None) -> pd.DataFrame:
    words = preprocces_text_to_words(text, words_to_get_ignored, language)
    table_count = generate_table_count_word(words)
    sorted_table_count = table_count.sort_values(WordCountColumnNames.count, ascending=False)
    return sorted_table_count.head(k)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str)
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--path_to_file', type=str)
    parser.add_argument('--words_to_get_ignored', type=str, nargs='+', default=None)
    parser.add_argument('--language', type=str, default=None)

    args = parser.parse_args()

    text_to_process = args.text or open(args.path_to_file, "r").read()


