
import pandas as pd
import numpy as np
from utils import *


# Doeltabel year_month   * = primary key

# YEAR_YEAR*

def get_table():
    go_staff = load_db('source/go_staff.sqlite')

    training = load_table(go_staff, 'training')[['YEAR']]
    satisfaction = load_table(go_staff, 'satisfaction')[['YEAR']]

    # Union the two tables
    year = pd.concat([training, satisfaction], ignore_index=True).drop_duplicates()

    # Convert to int
    year['YEAR'] = year['YEAR'].astype(int) 

    return year

print(get_table())