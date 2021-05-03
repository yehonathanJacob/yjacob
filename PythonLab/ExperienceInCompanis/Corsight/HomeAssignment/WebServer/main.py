import sys, os
sys.path.append(os.getcwd())

from tempfile import TemporaryDirectory
import argparse
import time
from typing import List, Optional
import logging

import pandas as pd
from starlette.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, Query, HTTPException

from WebServer.tags_metadata import tags_metadata
from ParallelMatching.parallel_matching import ParallelMatching
from SourceReader.sources import DirectoryReader

app = FastAPI(openapi_tags=tags_metadata)

class Directories:
    A = None
    B = None
    C = None

    @staticmethod
    def valid_side():
        return ['A', 'B']

    @classmethod
    def setup_directories(cls, base_dir):
        cls.A = os.path.join(base_dir, 'A')
        cls.B = os.path.join(base_dir, 'B')
        cls.C = os.path.join(base_dir, 'C')
        [os.makedirs(directory, exist_ok=True) for directory in [cls.A, cls.B, cls.C]]


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs/")


@app.get("/add_row/{side}", tags=["add_row"])
def add_row(side: str, values: Optional[List[int]] = Query(None), file_name: Optional[str] = Query(None)):
    if side not in Directories.valid_side():
        raise HTTPException(status_code=404, detail=f"Expected side to be one of: {Directories.valid_side()}")

    if values is None:
        raise HTTPException(status_code=404,
                            detail=f"Expected to have at least one values, we don't creat empty files.")

    values = sorted(values)
    file_name = file_name or f"{time.time()}.csv"
    dir_path = vars(Directories)[side]
    file_path = os.path.join(dir_path, file_name)
    df = pd.DataFrame(values)
    df.T.to_csv(file_path, index=False)
    return {"side": side, "number_of_values": len(values), "file_name": file_name}

@app.get("/match/{X}", tags=["match"])
def match(X: int):
    ParallelMatching.run_parallel_matching(Directories.A, Directories.B, Directories.C, X)
    scores_path = os.path.join(Directories.C, 'scores.txt')
    with open(scores_path, "r") as f:
        results = [line_result for line_result in f]
    return results

@app.get("/status/", tags=["status"])
def status():
    A_reader = iter(DirectoryReader(Directories.A))
    B_reader = iter(DirectoryReader(Directories.B))

    return {"A": len(list(A_reader)), "B": len(list(B_reader))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument('--mode', default="DEBUG")
    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.mode))

    with TemporaryDirectory() as tmpdir:
        logging.debug(f"Set files root directory: {tmpdir}")
        Directories.setup_directories(tmpdir)
        uvicorn.run(app, host=args.host, port=args.port)
