
import pandas as pd
import numpy as np
from utils import *


# -- PRODUCT_FORECAST doeltabel --

# PRODUCT_FORECAST_ID
# PRODUCT_FORECAST_EXPECTED_VOLUME
# INVENTORY_LEVELS_DATA_INVENTORY_COUNT
# PRODUCT_PRODUCTION_COST
# PRODUCT_MARGIN
# YEAR_MONTH_YEAR (komt uit product_forecast)
# YEAR_MONTH_MONTH (komt uit product_forecast)
# PRODUCT_PRODUCT_NUMBER


go_sales = load_db('../source/go_sales.sqlite')


product_forecast = load_csv('../source/GO_SALES_PRODUCT_FORECASTData.csv')
inventory_levels = load_csv('../source/GO_SALES_INVENTORY_LEVELSData.csv', np.arange(0,4))
product = load_table(go_sales, 'PRODUCT')


# Remove unnwanted columns
product = product[['PRODUCT_NUMBER', 'PRODUCTION_COST', 'MARGIN']]

# Transform product dtypes
product['PRODUCT_NUMBER'] = product['PRODUCT_NUMBER'].astype('int64')
product['PRODUCTION_COST'] = product['PRODUCTION_COST'].astype('float64')
product['MARGIN'] = product['MARGIN'].astype('float64')

# Add prefixes
product_forecast = product_forecast.add_prefix('PRODUCT_FORECAST_')
inventory_levels = inventory_levels.add_prefix('INVENTORY_LEVELS_')
product = product.add_prefix('PRODUCT_')



# Merge tables
# JOIN
# product_forecast_data.product_number = inventory_levels_data.product_number AND product_forecast_data.year = inventory_levels_data.inventory_year AND product_forecast_data.month = inventory_levels_data.inventory_month 

result = product_forecast.merge(inventory_levels, 
    left_on=['PRODUCT_FORECAST_PRODUCT_NUMBER', 'PRODUCT_FORECAST_YEAR', 'PRODUCT_FORECAST_MONTH'], 
    right_on=['INVENTORY_LEVELS_PRODUCT_NUMBER', 'INVENTORY_LEVELS_INVENTORY_YEAR', 'INVENTORY_LEVELS_INVENTORY_MONTH'])

result = result.merge(product, 
    left_on='PRODUCT_FORECAST_PRODUCT_NUMBER', 
    right_on='PRODUCT_PRODUCT_NUMBER')

# Remove duplicate columns
result = result.drop(columns=['PRODUCT_FORECAST_PRODUCT_NUMBER', 'INVENTORY_LEVELS_PRODUCT_NUMBER', 'INVENTORY_LEVELS_INVENTORY_YEAR', 'INVENTORY_LEVELS_INVENTORY_MONTH'])

# Rename foreign key columns
result = result.rename(columns={
    'PRODUCT_FORECAST_YEAR': 'YEAR_MONTH_YEAR',
    'PRODUCT_FORECAST_MONTH': 'YEAR_MONTH_MONTH'
})

print(result)