import string
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

DEFAULT_LANGUAGE = 'english'
DEFAULT_TO_IGNORE = ['']


def text_to_words(text: str) -> list:
    return re.split(r'\W+', text)


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_stop_words(words: list, language=None) -> list:
    language = language or DEFAULT_LANGUAGE
    stop_word_options = stopwords.words(language)
    without_stop_words = [
        word for word in words
        if word not in stop_word_options
    ]

    return without_stop_words


def parse_lemmatize_words(words: list) -> list:
    lemmatizer = WordNetLemmatizer()
    lemmatize_words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]
    return lemmatize_words


def ignore_words(words: list, to_exclude=None) -> list:
    to_exclude = to_exclude or []
    to_exclude = set(to_exclude)
    to_exclude = to_exclude | set(DEFAULT_TO_IGNORE)
    return [
        word for word in words
        if word not in to_exclude
    ]


def preprocces_text_to_words(text: str, words_to_get_ignored=None, language=None) -> list:
    cleaned_punctuation = remove_punctuation(text)
    words = text_to_words(cleaned_punctuation)
    without_stop_words = remove_stop_words(words, language)
    lemmatize_words = parse_lemmatize_words(without_stop_words)
    excluded = ignore_words(lemmatize_words, words_to_get_ignored)
    return excluded
