
import pandas as pd
import numpy as np
from utils import *


# Doeltabel year_month   * = primary key

# YEAR_MONTH_YEAR*
# YEAR_MONTH_QUARTER
# YEAR_MONTH_MONTH*


# Load databases and tables to retrieve all the distinct values
go_sales = load_db('source/go_sales.sqlite')

sales_target_data = load_table(go_sales, 'SALES_TARGETData')
product_forecast = load_csv('source/GO_SALES_PRODUCT_FORECASTData.csv')
inventory_levels = load_csv('source/GO_SALES_INVENTORY_LEVELSData.csv', np.arange(0,4))

# Remove all columns that are not date related
sales_target_data = sales_target_data[['SALES_YEAR', 'SALES_PERIOD']]
product_forecast = product_forecast[['YEAR', 'MONTH']]
inventory_levels = inventory_levels[['INVENTORY_YEAR', 'INVENTORY_MONTH']]


# Rename columns to match the target table
sales_target_data = sales_target_data.rename(columns={'SALES_YEAR': 'YEAR', 'SALES_PERIOD': 'MONTH'})
inventory_levels = inventory_levels.rename(columns={'INVENTORY_YEAR': 'YEAR', 'INVENTORY_MONTH': 'MONTH'})


# Merge all the dataframes to get all the distinct values
distinct_values = pd.concat([sales_target_data, product_forecast, inventory_levels], ignore_index=True)

# Transform the data to the correct format
distinct_values['YEAR'] = distinct_values['YEAR'].astype(int)
distinct_values['MONTH'] = distinct_values['MONTH'].astype(int)

# Add quarter column
distinct_values['QUARTER'] = (distinct_values['MONTH'] - 1) // 3 + 1
result = distinct_values