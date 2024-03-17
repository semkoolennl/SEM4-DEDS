import pandas as pd
import sqlalchemy
from exportutils import *
from table_scripts.utils import *
from sqlalchemy import create_engine

import pandas as pd
import numpy as np

np.random.seed(0)
number_of_samples = 10
frame = pd.DataFrame({
    'feature1': np.random.random(number_of_samples),
    'feature2': np.random.random(number_of_samples),
    'class':    np.random.binomial(2, 0.1, size=number_of_samples),
    },columns=['feature1','feature2','class'])


database_username = 'sa'
database_password = 'SuperPassword123!'
database_ip       = 'localhost'
port              = '1433'
database_name     = 'datawarehouse'

database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
                                               format(database_username, database_password, 
                                                      database_ip, port ,database_name))

# dit werkt niet eens lol...
frame.to_sql(con=database_connection, name='table_name_for_df', if_exists='replace')

# scripts = get_scripts()
# for script in scripts:
#     print(f'Executing script {script}')
#     tablename = script.split('_table')[0]
#     result    = execute_get_table(script)

#     print(f'Pushing to table {tablename} in database')
#     result.to_sql(con=database_connection, name=tablename, if_exists='replace')
#     print(f'Successfully pushed {script} to database')