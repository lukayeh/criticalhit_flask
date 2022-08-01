import pandas as pd
import sqlite3

conn = sqlite3.connect("database.db")
db_df = pd.read_sql_query("SELECT * FROM roster", conn)
db_df.to_csv("roster.csv", index=False)
