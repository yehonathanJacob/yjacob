import os, sys

sys.path.append(os.getcwd())
import argparse, logging

from typing import Optional

import pandas as pd
import uvicorn
from starlette.responses import RedirectResponse
from fastapi import FastAPI, HTTPException
from assiment2.crawler import ZillowCrawler, ElementClickInterceptedException
from assiment2.database_manager import CrawlingResults

app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs/")


@app.get("/get_data")
def get_data(address: Optional[str]):
    zillow_crawler = ZillowCrawler()

    try:
        result = zillow_crawler.crawle_apartment_details(address)
    except ElementClickInterceptedException as e:
        raise HTTPException(status_code=502, detail="Can't pass the reCAPTCHA. Please pass it and try again.")

    result['great_schools'] = ",".join(result['great_schools'])
    df = pd.DataFrame([result])
    CrawlingResults.insert_df(df)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument('--mode', default="DEBUG")
    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.mode))

    uvicorn.run(app, host=args.host, port=args.port)
