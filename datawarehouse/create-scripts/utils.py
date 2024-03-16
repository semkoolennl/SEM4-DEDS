import pandas as pd
import sqlite3

def load_db(path):
    conn = sqlite3.connect(path)
    return conn

def get_tables(conn):
    return pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

def drop_trial_column(table):
    # Search for Column Like %TRIAL%
    trial_columns = [col for col in table.columns if 'TRIAL' in col]
    # Drop Columns
    table = table.drop(columns=trial_columns)
    return table

def load_table(conn, table):
    query = "SELECT * FROM {}".format(table)
    df = pd.read_sql_query(query, conn)
    return drop_trial_column(df)

def print_columns(frame: pd.DataFrame):
    for col in frame.columns:
        print(col)