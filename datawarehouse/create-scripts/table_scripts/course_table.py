
import pandas as pd
from utils import *

# -- COURSE doeltabel --

# COURSE_COURSE_CODE
# COURSE_COURSE_DESCRIPTION

go_staff = load_db('source/go_staff.sqlite')

course = load_table(go_staff, 'COURSE')
result = course
print(result)


