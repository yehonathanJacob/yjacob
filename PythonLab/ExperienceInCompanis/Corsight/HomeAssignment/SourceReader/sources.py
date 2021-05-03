import os
import pandas as pd
from SourceReader.basic_reader import BasicSource


class PandasReader(BasicSource):
    def __iter__(self):
        df = pd.read_csv(self.source_path).T
        for value in df[0]:
            yield value


# TODO: Implement a reader that with the use of open file and context manager,
#  read each value until next comma, to cancel need of reading all file to memory


class DirectoryReader(BasicSource):
    def __init__(self, source_path):
        if not os.path.isdir(source_path):
            raise NotADirectoryError(f"No directory in {source_path}")
        try:
            super().__init__(source_path)
        except IsADirectoryError:
            pass

    def __iter__(self):
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                path_to_file = os.path.join(root, file)
                yield path_to_file
