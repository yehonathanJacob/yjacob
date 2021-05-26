import abc
import os
from abc import ABC


class BasicSource(ABC):
    def __init__(self, source_path):
        self.source_path = source_path
        if os.path.isdir(source_path):
            raise IsADirectoryError("Expected having a file, got a directory.")
        elif not os.path.isfile(source_path):
            raise FileNotFoundError(f"There is no file in this directory: {source_path}")

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError("Expected to implement iteration to read the source.")
