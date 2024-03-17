
import pandas as pd
from utils import *


# -- RETAILER_CONTACT doeltabel --

# RETAILER_CONTACT_RETAILER_contact_code
# RETAILER_CONTACT_RETAILER_site_code
# RETAILER_CONTACT_FIRST_NAME
# RETAILER_CONTACT_LAST_NAME
# RETAILER_CONTACT_JOB_POSITION_EN
# RETAILER_CONTACT_EXTENSION
# RETAILER_CONTACT_FAX
# RETAILER_CONTACT_E_MAIL
# RETAILER_CONTACT_GENDER


go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')


retailer_contact = load_table(go_crm, 'RETAILER_CONTACT').add_prefix('RETAILER_CONTACT_')

# Transform types
retailer_contact['RETAILER_CONTACT_RETAILER_CONTACT_CODE'] = retailer_contact['RETAILER_CONTACT_RETAILER_CONTACT_CODE'].astype('int64')
retailer_contact['RETAILER_CONTACT_RETAILER_SITE_CODE'] = retailer_contact['RETAILER_CONTACT_RETAILER_SITE_CODE'].astype('int64')
retailer_contact['RETAILER_CONTACT_FIRST_NAME'] = retailer_contact['RETAILER_CONTACT_FIRST_NAME'].astype('string')
retailer_contact['RETAILER_CONTACT_LAST_NAME'] = retailer_contact['RETAILER_CONTACT_LAST_NAME'].astype('string')
retailer_contact['RETAILER_CONTACT_JOB_POSITION_EN'] = retailer_contact['RETAILER_CONTACT_JOB_POSITION_EN'].astype('string')
retailer_contact['RETAILER_CONTACT_EXTENSION'] = retailer_contact['RETAILER_CONTACT_EXTENSION'].astype('string') # has to be string as, NoneType cast to int is not allowed
retailer_contact['RETAILER_CONTACT_FAX'] = retailer_contact['RETAILER_CONTACT_FAX'].astype('string')
retailer_contact['RETAILER_CONTACT_E_MAIL'] = retailer_contact['RETAILER_CONTACT_E_MAIL'].astype('string')
retailer_contact['RETAILER_CONTACT_GENDER'] = retailer_contact['RETAILER_CONTACT_GENDER'].astype('string')

result = retailer_contact