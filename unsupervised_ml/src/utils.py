import os
import pandas as pd
import sqlite3

def get_source_path(path):
    # get current file path
    current = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current, '..', path)

def assertFileExists(path):
    try:
        open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' not found.")
    
def load_db(path):
    path = get_source_path(path)
    assertFileExists(path)
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

def load_csv(filename, usecols=None):
    filename = get_source_path(filename)
    assertFileExists(filename)
    data = pd.read_csv(filename, usecols=usecols)
    return data

def load_csv_table(data, table_name):
    if table_name in data:
        return data[table_name]
    else:
        print(f"Table '{table_name}' not found in the DataFrame.")
        return None
