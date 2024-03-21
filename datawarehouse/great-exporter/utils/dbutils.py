import os
import pandas as pd
import numpy as np
import pyodbc
import sqlite3
from .config import SourceSQLite3Database, SourceCSVDatabase

def get_source_path(path: str) -> str:
    # get current file path
    current = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current, '..', path)

def assertFileExists(path: str) -> None:
    try:
        open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{path}' not found.")
    
def load_db(path: str) -> sqlite3.Connection:
    path = get_source_path(path)
    assertFileExists(path)
    conn = sqlite3.connect(path)
    return conn

def load_mssql_db(conn_string: str) -> pyodbc.Connection:
    return pyodbc.connect(conn_string)

def get_tables(conn: str) -> pd.DataFrame:
    return pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn) # type: ignore

def drop_trial_column(table: pd.DataFrame) -> pd.DataFrame:
    # Search for Column Like %TRIAL%
    trial_columns = [col for col in table.columns if 'TRIAL' in col]
    # Drop Columns
    table = table.drop(columns=trial_columns) # type: ignore
    return table

def load_table(conn: sqlite3.Connection, table: str) -> pd.DataFrame:
    query = "SELECT * FROM {}".format(table)
    df = pd.read_sql_query(query, conn) # type: ignore
    return drop_trial_column(df)

def print_columns(frame: pd.DataFrame):
    for col in frame.columns:
        print(col)

def load_csv(filename: str, usecols: list[int]|None = None) -> pd.DataFrame:
    filename = get_source_path(filename)
    assertFileExists(filename)
    data = pd.read_csv(filename, usecols=usecols) # type: ignore
    return data

def load_csv_table(data: pd.DataFrame, table_name: str) -> pd.DataFrame:
    if table_name in data:
        return data[table_name] # type: ignore
    else:
        raise ValueError(f"Table '{table_name}' not found in the DataFrame.")
    
class DatabaseManager:
    database_configs: dict[str, SourceSQLite3Database|SourceCSVDatabase]
    database_conns:   dict[str, sqlite3.Connection | pd.DataFrame] = {}

    def __init__(self, database_configs: dict[str, SourceSQLite3Database|SourceCSVDatabase]):
        self.database_configs = database_configs


    def get_table(self, table_name: str, database_name: str) -> pd.DataFrame:
        if database_name in self.database_conns:
            database = self.database_conns[database_name]
            if isinstance(database, pd.DataFrame):
                return self.database_conns[database_name][table_name] # type: ignore
            else:
                return load_table(database, table_name)
        
        config = self.database_configs[database_name]
        if isinstance(config, SourceCSVDatabase):
            usecols = np.arange(0, config.colcount).tolist()
            conn    = load_csv(config.path, usecols)

            self.database_conns[database_name] = conn

            return load_csv_table(conn, table_name)
        else:
            conn = load_db(config.path)
            self.database_conns[database_name] = conn
            return load_table(conn, table_name)
        
    


