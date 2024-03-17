
import pandas as pd
from utils import *


# ResultTable overview - Sales_demographic 

# SALES_DEMOGRAPHIC_DEMOGRAPHIC_CODE
# SALES_DEMOGRAPHIC_SALES_PERCENT
# RETAILER_HEADQUARTERS_RETAILER_CODEMR
# RETAILER_HEADQUARTERS_RETAILER_NAME
# RETAILER_HEADQUARTERS_ADDRESS1
# RETAILER_HEADQUARTERS_ADDRESS2
# RETAILER_HEADQUARTERS_CITY
# RETAILER_HEADQUARTERS_REGION
# RETAILER_HEADQUARTERS_POSTAL_ZONE
# RETAILER_HEADQUARTERS_PHONE
# RETAILER_HEADQUARTERS_FAX
# RETAILER_SEGMENT_SEGMENT_CODE
# RETAILER_SEGMENT_LANGUAGE
# RETAILER_SEGMENT_SEGMENT_NAME
# RETAILER_SEGMENT_SEGMENT_DESCRIPTION
# AGE_GROUP_AGE_GROUP_CODE
# AGE_GROUP_UPPER_AGE
# AGE_GROUP_LOWER_AGE
# RETAILER_COUNTRY_COUNTRY_CODE
# RETAILER_COUNTRY_COUNTRY_EN
# RETAILER_COUNTRY_FLAG_IMAGE
# SALES_TERRITORY_SALES_TERRITORY_CODE
# SALES_TERRITORY_TERRITORY_NAME_EN


go_crm = load_db('source/go_crm.sqlite')


retailer_heaquarters = load_table(go_crm, 'retailer_headquarters').add_prefix('RETAILER_HEADQUARTERS_')
retailer_site = load_table(go_crm, 'retailer_site').add_prefix('RETAILER_SITE_')
retailer_segment = load_table(go_crm, 'retailer_segment').add_prefix('RETAILER_SEGMENT_')
retailer_country = load_table(go_crm, 'country').add_prefix('RETAILER_COUNTRY_')
sales_demographic = load_table(go_crm, 'sales_demographic').add_prefix('SALES_DEMOGRAPHIC_')
sales_territory = load_table(go_crm, 'sales_territory').add_prefix('SALES_TERRITORY_')
age_group = load_table(go_crm, 'age_group').add_prefix('AGE_GROUP_')


result = pd.merge(
    sales_demographic, retailer_heaquarters, left_on="SALES_DEMOGRAPHIC_RETAILER_CODEMR", right_on="RETAILER_HEADQUARTERS_RETAILER_CODEMR"
    ).drop(columns='SALES_DEMOGRAPHIC_RETAILER_CODEMR')

result = pd.merge(
    result, retailer_segment, left_on='RETAILER_HEADQUARTERS_SEGMENT_CODE', right_on='RETAILER_SEGMENT_SEGMENT_CODE'
    ).drop(columns='RETAILER_HEADQUARTERS_SEGMENT_CODE')

result = pd.merge(
    result, age_group, left_on="SALES_DEMOGRAPHIC_AGE_GROUP_CODE", right_on="AGE_GROUP_AGE_GROUP_CODE"
    ).drop(columns='SALES_DEMOGRAPHIC_AGE_GROUP_CODE')

result = pd.merge(
    result, retailer_country, left_on='RETAILER_HEADQUARTERS_COUNTRY_CODE', right_on='RETAILER_COUNTRY_COUNTRY_CODE'
    ).drop(columns='RETAILER_HEADQUARTERS_COUNTRY_CODE')

result = pd.merge(
    result, sales_territory, left_on='RETAILER_COUNTRY_SALES_TERRITORY_CODE', right_on='SALES_TERRITORY_SALES_TERRITORY_CODE'
    ).drop(columns='RETAILER_COUNTRY_SALES_TERRITORY_CODE')

print(result)