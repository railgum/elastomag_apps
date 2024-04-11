import pandas as pd
import sqlite3


def convert_excel_to_db(file_name, db_name):
    db = sqlite3.connect(db_name)

    dfs = pd.read_excel(file_name, sheet_name=None)
    for table, df in dfs.items():
        df.to_sql(table, db, if_exists='replace')
