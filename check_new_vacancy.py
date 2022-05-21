from os import path
import os.path
import pandas as pd


if path.exists("Previous_Parsed_Data.csv") and path.exists("Parsed_Data.csv"):
    cur = pd.read_csv("Parsed_Data.csv")
    prev = pd.read_csv("Previous_Parsed_Data.csv")
    if cur.equals(prev):
        print("There are not new vacancies")
    else:
        finish = pd.concat([cur, prev]).drop_duplicates(keep=False)
        finish.to_csv("New_Vacancy.csv")
else:
    print("Need to run a program at least 2 times")
    exit(0)