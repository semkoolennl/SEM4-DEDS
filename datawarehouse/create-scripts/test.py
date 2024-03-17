from exportutils import *
from table_scripts.utils import *

scripts = get_scripts()
for script in scripts:
    print(f"Executing {script}...")
    tablename = script.split('_table')[0]
    dataframe = execute_get_table(script)
    print_columns(dataframe)
    print()
