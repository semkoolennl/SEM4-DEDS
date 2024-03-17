
import pandas as pd
from utils import *


# -- SATISFACTION_TYPE doeltabel --

# SATISFACTION_TYPE_CODE
# SATISFACTION_TYPE_DESCRIPTION


go_staff = load_db('source/go_staff.sqlite')


satisfaction_type = load_table(go_staff, 'SATISFACTION_TYPE')
result = satisfaction_type
print(result)