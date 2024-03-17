
import pandas as pd
from utils import *

# -- COURSE doeltabel --

# COURSE_COURSE_CODE
# COURSE_COURSE_DESCRIPTION

import os

# Get the path of the current file
current_file_path = os.path.abspath(__file__)

# Get the current working directory
current_directory = os.getcwd()

# Compute the relative path
relative_path = os.path.relpath(current_file_path, current_directory)
print(relative_path)

go_staff = load_db('source/go_staff.sqlite')

course = load_table(go_staff, 'COURSE')
result = course
print(result)


