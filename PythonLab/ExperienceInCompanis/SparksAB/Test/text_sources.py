from abc import ABC, abstractmethod

from requests import get


class TextSource(ABC):
    @abstractmethod
    def get_text_from_source(self) -> str:
        ...


class WebPageSource(TextSource):
    def __init__(self, url):
        self.url = url

    def get_text_from_source(self) -> str:
        response = get(url=self.url)
        return response.text
