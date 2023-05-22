import re

import pandas as pd


df = pd.read_csv("example_file1.csv")
new_columns = df['Message'].str.extract(r".*doc_id=(?P<doc_id>\d+) request_id=(?P<request_id>\d+) (?P<event>.+)", expand=True)
df2 = pd.concat([df, new_columns], axis=1)

month_number=1
year_back=True
formula = "FY_month(Jan) + FY_year(2022) - FY_day(3)"
formula = re.sub(r"FY_(?P<f>\w+)\(\s*(?P<v>\[\w+\])\s*\)",
                 fr"FY_\g<f>(\g<v>,month_number={month_number},year_back={year_back})", formula)