import pyodbc
import sqlalchemy
from .config import ConnectionConfig

def intialize_engine(config: ConnectionConfig) -> sqlalchemy.Engine:
    master_conn = pyodbc.connect(config.get_pyodbc_conn_string())
    # Set AUTOCOMMIT to True to avoid multi-statement transactions
    master_conn.autocommit = True

    exists_query = f"SELECT COUNT(*) FROM sys.databases WHERE name = '{config.database}'"
    result = master_conn.execute(exists_query).fetchone()

    # Create the 'greatwarehouse' database if it doesn't exist
    if result is not None and result[0] == 0:
        create_database_query = f"CREATE DATABASE {config.database}"
        master_conn.execute(create_database_query)
        print(f"Database '{config.database}' created successfully.\n\n")
    else:
        print(f"Database '{config.database}' already exists.\n\n")

    # Close the connection
    master_conn.close()

    return sqlalchemy.create_engine(config.get_sqlalchemy_conn_string(), echo=False)

def recreate_db(config: ConnectionConfig):
    master_conn = pyodbc.connect(config.get_pyodbc_conn_string())
    # Set AUTOCOMMIT to True to avoid multi-statement transactions
    master_conn.autocommit = True

    exists_query = f"SELECT COUNT(*) FROM sys.databases WHERE name = '{config.database}'"
    result = master_conn.execute(exists_query).fetchone()

    # Create the database if it doesn't exist
    if result is not None and result[0] == 0:
        create_database_query = f"CREATE DATABASE {config.database}"
        master_conn.execute(create_database_query)
        print(f"Database '{config.database}' created successfully.")
    else:
        # Drop the database if it already exists
        drop_database_query = f"DROP DATABASE {config.database}"
        master_conn.execute(drop_database_query)
        print(f"Database '{config.database}' dropped successfully.")

        # Recreate the database
        create_database_query = f"CREATE DATABASE {config.database}"
        master_conn.execute(create_database_query)
        print(f"Database '{config.database}' created successfully.")

    # Close the connection
    master_conn.close()