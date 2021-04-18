import os
from typing import List

from jedi.api import file_name

from text_sources import WebPageSource
from get_k_count import generate_k_count_table
from models import WordCount

def bulk_run(texts:List[str], k:int, output_file_name:str):
    for plain_text in texts:
        table_count = generate_k_count_table(plain_text, k)
        path_to_file = os.path.join(os.getcwd(), output_file_name)
        table_count.to_csv(path_to_file)
        WordCount.insert_df(table_count)


if __name__ == '__main__':
    url = 'http://www.gutenberg.org/files/11/11-0.txt'
    k = 100
    output_file_name = f"{k}_word_count.csv"
    words_to_get_ignored = []
    language = None
    text_source = WebPageSource(url)
    plain_text = text_source.get_text_from_source()

    texts = [plain_text]
    bulk_run(texts, k, output_file_name)
