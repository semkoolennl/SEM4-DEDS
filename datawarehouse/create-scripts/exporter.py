import os
import pyodbc
import pandas as pd
import importlib

DB = {
    'servername': 'localhost,1433',
    'database': 'master',  # Use 'master' as default system database
    'username': 'sa',
    'password': 'SuperPassword123!'
}

# Create the connection string to the master database
master_conn_str = (
    'DRIVER={SQL Server};'
    'SERVER=' + DB['servername'] + ';'
    'DATABASE=' + DB['database'] + ';'
    'UID=' + DB['username'] + ';'
    'PWD=' + DB['password'] + ';'
)

# Create the connection to the master database
master_conn = pyodbc.connect(master_conn_str)

# Set AUTOCOMMIT to True to avoid multi-statement transactions
master_conn.autocommit = True

# Check if the 'greatwarehouse' database exists
database_name = 'greatwarehouse'
exists_query = f"SELECT COUNT(*) FROM sys.databases WHERE name = '{database_name}'"
result = master_conn.execute(exists_query).fetchone()

if result[0] == 0:
    # Create the 'greatwarehouse' database if it doesn't exist
    create_database_query = f"CREATE DATABASE {database_name}"
    master_conn.execute(create_database_query)
    print(f"Database '{database_name}' created successfully.")
else:
    print(f"Database '{database_name}' already exists.")

# Close the connection to the master database
master_conn.close()

# Create the connection string to the 'greatwarehouse' database
warehouse_conn_str = (
    'DRIVER={SQL Server};'
    'SERVER=' + DB['servername'] + ';'
    'DATABASE=' + database_name + ';'
    'UID=' + DB['username'] + ';'
    'PWD=' + DB['password'] + ';'
)

# Create the connection to the 'greatwarehouse' database
warehouse_conn = pyodbc.connect(warehouse_conn_str)
print(warehouse_conn)


warehouse_conn.close()

modulleeee = 'test'
module = importlib.import_module(modulleeee)
print(module)


module_folder = 'datawarehouse/create-scripts/table_scripts'

# List all Python files in the folder
module_names = [file_name[:-3] for file_name in os.listdir(module_folder) if file_name.endswith('.py')]
print(module_names)

for module_name in module_names:
    try:
        print(f"{module_folder}.{module_name}")
        # module = importlib.import_module(f"{module_folder}.{module_name}")
    except ImportError:
        print('couldnt import')