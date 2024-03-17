
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
# RETAILER_CONTACT_E_MAIL (EMAIL maken?)
# RETAILER_CONTACT_GENDER


go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')


retailer_contact = load_table(go_crm, 'RETAILER_CONTACT')
result = retailer_contact