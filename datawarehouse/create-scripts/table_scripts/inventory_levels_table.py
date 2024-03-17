
import pandas as pd
import numpy as np
from utils import *


# -- INVENTORY_LEVELS doeltabel --

# INVENTORY_LEVELS_ID (pk)
# INVENTORY_LEVELS_inventory_count
# PRODUCT_production_cost
# PRODUCT_margin
# ORDER_DETAILS_unit_cost
# ORDER_DETAILS_unit_price
# ORDER_DETAILS_unit_sale_price
# ORDER_DETAILS_quantity
# INVENTORY_LEVELS_turnover_rate* (calculateTurnoverRate(): turnover_rate = quantity / inventory_count)
# PRODUCT_product_number (fk uit ORDER_DETAILS)


go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')

inventory_levels = load_csv('source/GO_SALES_INVENTORY_LEVELSData.csv', np.arange(0,4)).add_prefix('INVENTORY_LEVELS_')
order_header = load_table(go_sales, 'ORDER_HEADER').add_prefix('ORDER_HEADER_')
order_details = load_table(go_sales, 'ORDER_DETAILS').add_prefix('ORDER_DETAILS_')
sales_staff = load_table(go_sales, 'SALES_STAFF').add_prefix('SALES_STAFF_')
sales_branch = load_table(go_sales, 'SALES_BRANCH').add_prefix('SALES_BRANCH_')
product = load_table(go_sales, 'PRODUCT').add_prefix('PRODUCT_')

# Merge columns
# sales_target_data.product = order_details.product_number
product = product[['PRODUCT_PRODUCT_NUMBER', 'PRODUCT_PRODUCTION_COST', 'PRODUCT_MARGIN']]
product['PRODUCT_PRODUCT_NUMBER'] = product['PRODUCT_PRODUCT_NUMBER'].astype(int)
product['PRODUCT_MARGIN'] = product['PRODUCT_MARGIN'].astype(float)
product['PRODUCT_PRODUCTION_COST'] = product['PRODUCT_PRODUCTION_COST'].astype(float)

result = inventory_levels.merge(product, left_on='INVENTORY_LEVELS_PRODUCT_NUMBER', right_on='PRODUCT_PRODUCT_NUMBER')

# Add year_month date to order_detail by first joining order_header 
order = order_details.merge(order_header, left_on='ORDER_DETAILS_ORDER_NUMBER', right_on='ORDER_HEADER_ORDER_NUMBER')
order['ORDER_HEADER_ORDER_DATE'] = pd.to_datetime(order['ORDER_HEADER_ORDER_DATE'])
order['YEAR_MONTH_YEAR'] = order['ORDER_HEADER_ORDER_DATE'].dt.year.astype(int)
order['YEAR_MONTH_MONTH'] = order['ORDER_HEADER_ORDER_DATE'].dt.month.astype(int)
order['ORDER_DETAILS_PRODUCT_NUMBER'] = order['ORDER_DETAILS_PRODUCT_NUMBER'].astype(int)
order = order[['ORDER_DETAILS_PRODUCT_NUMBER', 'ORDER_DETAILS_QUANTITY', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH']]
order = order.groupby(['ORDER_DETAILS_PRODUCT_NUMBER', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH']).sum().reset_index()

# Merge order with inventory_levels, year, month and product_number
result = result.merge(order, left_on=['INVENTORY_LEVELS_PRODUCT_NUMBER', 'INVENTORY_LEVELS_INVENTORY_YEAR', 'INVENTORY_LEVELS_INVENTORY_MONTH'], right_on=['ORDER_DETAILS_PRODUCT_NUMBER', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH'], how='left')

# Calculate turnover_rate
result['INVENTORY_LEVELS_TURNOVER_RATE'] = result['ORDER_DETAILS_QUANTITY'] / result['INVENTORY_LEVELS_INVENTORY_COUNT']

# Remove duplicate columns
result = result.drop(columns=['ORDER_DETAILS_PRODUCT_NUMBER', 'INVENTORY_LEVELS_INVENTORY_YEAR', 'INVENTORY_LEVELS_INVENTORY_MONTH', 'INVENTORY_LEVELS_PRODUCT_NUMBER', 'ORDER_DETAILS_QUANTITY'])
print(result)