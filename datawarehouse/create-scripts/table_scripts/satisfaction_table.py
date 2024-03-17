
import pandas as pd
from utils import *


# -- SATISFACTION doeltabel --

# SATISFACTION_YEAR
# SALES_STAFF_CODE
# SATISFACTION_TYPE_CODE


go_staff = load_db('source/go_staff.sqlite')


satisfaction = load_table(go_staff, 'SATISFACTION')
result = satisfaction
print(result)


