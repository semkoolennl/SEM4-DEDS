import os
import sys
import pandas as pd

TABLE_SCRIPTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'table_scripts')

def get_scripts():
    # scan all files in table_scripts folder
    scripts = os.listdir(TABLE_SCRIPTS_PATH)

    # remove __init__.py * utils.py
    scripts = [script for script in scripts if script != '__init__.py' and script != 'utils.py']
    return scripts

def get_script_content(script):
    with open(os.path.join(TABLE_SCRIPTS_PATH, script), 'r') as file:
        return file.read()
    
def execute_get_table(script) -> pd.DataFrame:
    # make sure import of utils works
    sys.path.append(TABLE_SCRIPTS_PATH)
    
    exec(get_script_content(script))
    # now call local get_table function
    return locals()['result']
