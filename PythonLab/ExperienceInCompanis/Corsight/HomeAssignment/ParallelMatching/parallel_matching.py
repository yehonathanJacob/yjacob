from shutil import copyfile
import multiprocessing as mp
import threading
import os.path
from dataclasses import dataclass

from SourceReader.sources import PandasReader, DirectoryReader

CSV_READER = PandasReader


@dataclass
class Match:
    source_of_file: str
    num_intersection: int

    def __str__(self):
        name_of_file = os.path.basename(self.source_of_file)
        return f"{name_of_file}\t{self.num_intersection}"

    def __hash__(self):
        return hash(str(self))


class ParallelMatching:
    def __init__(self, A: str, B: str, X: int):
        self.A_reader = DirectoryReader(A)
        self.B_reader = DirectoryReader(B)
        self.minimum_intersection = X

    @classmethod
    def run_parallel_matching(cls, A: str, B: str, C: str, X: int):
        os.makedirs(C, exist_ok=True)
        C_output_dir = C
        pm = cls(A, B, X)

        matches_results = pm.load_matches_results()
        pm.copy_files_from_A(matches_results, C_output_dir)
        pm.write_scores(matches_results, C_output_dir)

    def load_matches_results(self):
        result_for_A_dir = []
        with mp.Pool(processes=os.cpu_count() - 1) as pool:
            for A_file_directory in iter(self.A_reader):
                max_match_result = pool.apply_async(ParallelMatching._process_file_match,
                                                    (A_file_directory, self.B_reader, self.minimum_intersection))
                result_for_A_dir.append(max_match_result)

            matches_results = [max_match_result.get() for max_match_result in result_for_A_dir
                               if max_match_result.get() is not None]

        return matches_results

    def copy_files_from_A(self, matches_results, C_output_dir):
        thread_list = []
        for match in matches_results:
            C_output_file = os.path.join(C_output_dir, os.path.basename(match.source_of_file))
            t = threading.Thread(target=copyfile, args=(match.source_of_file, C_output_file))
            t.start()
            thread_list.append(t)
        [t.join() for t in thread_list]

    def write_scores(self, matches_results, C_output_dir):
        scores = [str(match) for match in matches_results]
        scores_file_path = os.path.join(C_output_dir, "scores.txt")
        with open(scores_file_path, "w") as f:
            f.write("\n".join(scores))

    @staticmethod
    def _process_file_match(A_file_directory, B_reader, minimum_intersection):
        match = None
        for B_file_directory in iter(B_reader):
            number_match = ParallelMatching._check_number_match(A_file_directory, B_file_directory)
            if number_match > minimum_intersection:
                match = match or Match(A_file_directory, number_match)

                if number_match > match.num_intersection:
                    match.num_intersection = number_match

        return match

    @staticmethod
    def _check_number_match(A_file_directory, B_file_directory):
        A_file_reader = iter(CSV_READER(A_file_directory))
        B_file_reader = iter(CSV_READER(B_file_directory))
        count_matches = 0
        try:
            B_value = next(B_file_reader)
            A_value = next(A_file_reader)
            while True:
                if A_value == B_value:
                    count_matches += 1
                    A_value = next(A_file_reader)
                    B_value = next(B_file_reader)
                elif A_value > B_value:
                    B_value = next(B_file_reader)
                else:
                    A_value = next(A_file_reader)

        except StopIteration:
            return count_matches
