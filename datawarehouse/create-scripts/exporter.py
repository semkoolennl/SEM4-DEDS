# import pyodbc
# DB = {'servername': 'localhost\SQLExpress',
#       'database': 'testDB'}# create the connection
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')
# df = pd.read_sql_query('SELECT * FROM TestTable',conn)