
import pandas as pd
from utils import *


# -- SALES_BRANCH doeltabel --

# SALES_BRANCH_CODE
# SALES_BRANCH_REGION
# SALES_BRANCH_CITY
# SALES_BRANCH_POSTAL_CODE
# SALES_BRANCH_ADDRESS1
# SALES_BRANCH_ADDRESS2
# SALES_STAFF_SALES_STAFF_CODE
# SALES_STAFF_MANAGER_CODE
# SALES_STAFF_FIRST_NAME
# SALES_STAFF_LAST_NAME
# SALES_STAFF_POSITION_EN
# SALES_STAFF_WORK_PHONE
# SALES_STAFF_FAX
# SALES_STAFF_EXTENSION
# SALES_STAFF_EMAIL
# SALES_STAFF_DATE_HIRED
# COUNTRY_COUNTRY_CODE
# COUNTRY_COUNTRY
# COUNTRY_LANGUAGE
# COUNTRY_CURRENCY_NAME


go_sales = load_db('source/go_sales.sqlite')


sales_branch = load_table(go_sales, 'SALES_BRANCH').add_prefix('SALES_BRANCH_')
sales_staff = load_table(go_sales, 'SALES_STAFF').add_prefix('SALES_STAFF_')
sales_country = load_table(go_sales, 'COUNTRY').add_prefix('COUNTRY_')

# JOIN
# sales_branch.sales_branch_code = sales_staff_sales_branch_code
# sales_branch.country_code = country_country_code
# sales_staff.manager_code = sales_staff.sales_staff_code

result = sales_branch.merge(sales_staff, left_on='SALES_BRANCH_SALES_BRANCH_CODE', right_on='SALES_STAFF_SALES_BRANCH_CODE', how='inner')
result = result.merge(sales_country, left_on='SALES_BRANCH_COUNTRY_CODE', right_on='COUNTRY_COUNTRY_CODE', how='left')

# Remove redundant columns
result = result.drop(columns=['SALES_BRANCH_COUNTRY_CODE', 'SALES_STAFF_SALES_BRANCH_CODE'])

# Rename foreign key columns
result = result.rename(columns={
    'SALES_BRANCH_SALES_BRANCH_CODE': 'SALES_BRANCH_CODE',
    'SALES_STAFF_SALES_STAFF_CODE': 'SALES_STAFF_CODE',
})

# SALES_BRANCH_CODE           object
# SALES_BRANCH_ADDRESS1       object
# SALES_BRANCH_ADDRESS2       object
# SALES_BRANCH_CITY           object
# SALES_BRANCH_REGION         object
# SALES_BRANCH_POSTAL_ZONE    object
# SALES_STAFF_CODE            object
# SALES_STAFF_FIRST_NAME      object
# SALES_STAFF_LAST_NAME       object
# SALES_STAFF_POSITION_EN     object
# SALES_STAFF_WORK_PHONE      object
# SALES_STAFF_EXTENSION       object
# SALES_STAFF_FAX             object
# SALES_STAFF_EMAIL           object
# SALES_STAFF_DATE_HIRED      object
# COUNTRY_COUNTRY_CODE        object
# COUNTRY_COUNTRY             object
# COUNTRY_LANGUAGE            object
# COUNTRY_CURRENCY_NAME       object

result['SALES_BRANCH_CODE'] = result['SALES_BRANCH_CODE'].astype('int')
result['SALES_BRANCH_ADDRESS1'] = result['SALES_BRANCH_ADDRESS1'].astype('string')
result['SALES_BRANCH_ADDRESS2'] = result['SALES_BRANCH_ADDRESS2'].astype('string')
result['SALES_BRANCH_CITY'] = result['SALES_BRANCH_CITY'].astype('string')
result['SALES_BRANCH_REGION'] = result['SALES_BRANCH_REGION'].astype('string')
result['SALES_BRANCH_POSTAL_ZONE'] = result['SALES_BRANCH_POSTAL_ZONE'].astype('string')
result['SALES_STAFF_CODE'] = result['SALES_STAFF_CODE'].astype('int')
result['SALES_STAFF_FIRST_NAME'] = result['SALES_STAFF_FIRST_NAME'].astype('string')
result['SALES_STAFF_LAST_NAME'] = result['SALES_STAFF_LAST_NAME'].astype('string')
result['SALES_STAFF_POSITION_EN'] = result['SALES_STAFF_POSITION_EN'].astype('string')
result['SALES_STAFF_WORK_PHONE'] = result['SALES_STAFF_WORK_PHONE'].astype('string')
result['SALES_STAFF_EXTENSION'] = result['SALES_STAFF_EXTENSION'].astype('string')
result['SALES_STAFF_FAX'] = result['SALES_STAFF_FAX'].astype('string')
result['SALES_STAFF_EMAIL'] = result['SALES_STAFF_EMAIL'].astype('string')
result['SALES_STAFF_DATE_HIRED'] = pd.to_datetime(result['SALES_STAFF_DATE_HIRED'], format='%d-%m-%Y')
result['COUNTRY_COUNTRY_CODE'] = result['COUNTRY_COUNTRY_CODE'].astype('int')
result['COUNTRY_COUNTRY'] = result['COUNTRY_COUNTRY'].astype('string')
result['COUNTRY_LANGUAGE'] = result['COUNTRY_LANGUAGE'].astype('string')
result['COUNTRY_CURRENCY_NAME'] = result['COUNTRY_CURRENCY_NAME'].astype('string')


