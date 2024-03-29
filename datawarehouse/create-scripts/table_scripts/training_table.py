
import pandas as pd
from utils import *


# -- Training doeltabel --

# SALES_STAFF_CODE
# COURSE_CODE


go_staff = load_db('source/go_staff.sqlite')


training = load_table(go_staff, 'TRAINING')
result = training.drop(columns=['YEAR'])

result['SALES_STAFF_CODE'] = result['SALES_STAFF_CODE'].astype('int')
result['COURSE_CODE'] = result['COURSE_CODE'].astype('int')