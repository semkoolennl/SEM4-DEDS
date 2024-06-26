import pandas as pd
from utils import *

# -- SALES_TARGET_DATA doeltabel --

# SALES_TARGET_DATA_ID
# SALES_TARGET_DATA_SALES-TARGET
# SALES_TARGET_DATA_PRODUCTIVITY_SCORE* (calculateSPS(): (UNIT_PRICE * QUANTITY) / SALES_TARGET)

# ORDER_DETAILS_UNIT_COST
# ORDER_DETAILS_UNIT_PRICE
# ORDER_DETAILS_UNIT_SALE_PRICE
# ORDER_DETAILS_QUANTITY

# SALES_STAFF_CODE
# SALES_BRANCH_CODE
# PRODUCT_NUMBER
# RETAILER_CODE

go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')
go_staff = load_db('source/go_staff.sqlite')

sales_target_data = load_table(go_sales, 'SALES_TARGETData').add_prefix('SALES_TARGET_DATA_')
order_header = load_table(go_sales, 'ORDER_HEADER').add_prefix('ORDER_HEADER_')
order_details = load_table(go_sales, 'ORDER_DETAILS').add_prefix('ORDER_DETAILS_')
sales_staff = load_table(go_staff, 'SALES_STAFF').add_prefix('SALES_STAFF_')
sales_branch = load_table(go_staff, 'SALES_BRANCH').add_prefix('SALES_BRANCH_')
product = load_table(go_sales, 'PRODUCT').add_prefix('PRODUCT_')

sales_target_data = sales_target_data.merge(sales_staff, left_on='SALES_TARGET_DATA_SALES_STAFF_CODE', right_on='SALES_STAFF_SALES_STAFF_CODE', how='left')

# Aggregate order
order = order_details.merge(order_header, left_on='ORDER_DETAILS_ORDER_NUMBER', right_on='ORDER_HEADER_ORDER_NUMBER')
order['ORDER_HEADER_ORDER_DATE'] = pd.to_datetime(order['ORDER_HEADER_ORDER_DATE'])
order['YEAR_MONTH_YEAR'] = order['ORDER_HEADER_ORDER_DATE'].dt.year.astype(int)
order['YEAR_MONTH_MONTH'] = order['ORDER_HEADER_ORDER_DATE'].dt.month.astype(int)
order['ORDER_DETAILS_PRODUCT_NUMBER'] = order['ORDER_DETAILS_PRODUCT_NUMBER'].astype(int)
order


# Remove original date columns
order = order.drop(columns=['ORDER_HEADER_ORDER_DATE', 'ORDER_HEADER_ORDER_NUMBER', 'ORDER_DETAILS_ORDER_DETAIL_CODE'])
order = order[['ORDER_DETAILS_PRODUCT_NUMBER', 'ORDER_HEADER_SALES_STAFF_CODE', 'ORDER_DETAILS_QUANTITY', 'ORDER_DETAILS_UNIT_COST', 'ORDER_DETAILS_UNIT_PRICE', 'ORDER_DETAILS_UNIT_SALE_PRICE', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH']]

order['ORDER_DETAILS_QUANTITY'] = order['ORDER_DETAILS_QUANTITY'].astype(int)
order['ORDER_DETAILS_UNIT_COST'] = order['ORDER_DETAILS_UNIT_COST'].astype(float)
order['ORDER_DETAILS_UNIT_PRICE'] = order['ORDER_DETAILS_UNIT_PRICE'].astype(float)
order['ORDER_DETAILS_UNIT_SALE_PRICE'] = order['ORDER_DETAILS_UNIT_SALE_PRICE'].astype(float)

# Calculate total cost, price and sale price
order['ORDER_DETAILS_TOTAL_COST'] = order['ORDER_DETAILS_QUANTITY'] * order['ORDER_DETAILS_UNIT_COST']
order['ORDER_DETAILS_TOTAL_PRICE'] = order['ORDER_DETAILS_QUANTITY'] * order['ORDER_DETAILS_UNIT_PRICE']
order['ORDER_DETAILS_TOTAL_SALE_PRICE'] = order['ORDER_DETAILS_QUANTITY'] * order['ORDER_DETAILS_UNIT_SALE_PRICE']

# Remove original columns
order = order.drop(columns=['ORDER_DETAILS_UNIT_COST', 'ORDER_DETAILS_UNIT_PRICE', 'ORDER_DETAILS_UNIT_SALE_PRICE'])

# Aggregate order
order = order.groupby(['ORDER_HEADER_SALES_STAFF_CODE', 'ORDER_DETAILS_PRODUCT_NUMBER', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH']).agg(
    ORDER_DETAILS_TOTAL_COST=('ORDER_DETAILS_TOTAL_COST', 'sum'),
    ORDER_DETAILS_TOTAL_PRICE=('ORDER_DETAILS_TOTAL_PRICE', 'sum'),
    ORDER_DETAILS_TOTAL_SALE_PRICE=('ORDER_DETAILS_TOTAL_SALE_PRICE', 'sum'),
    ORDER_DETAILS_QUANTITY=('ORDER_DETAILS_QUANTITY', 'sum')
).reset_index()

order['ORDER_DETAILS_QUANTITY'] = order['ORDER_DETAILS_QUANTITY'].astype(int)
order['YEAR_MONTH_YEAR'] = order['YEAR_MONTH_YEAR'].astype(int)
order['YEAR_MONTH_MONTH'] = order['YEAR_MONTH_MONTH'].astype(int)
order


# Merge with sales_target_data
sales_target_data['SALES_TARGET_DATA_SALES_YEAR'] = sales_target_data['SALES_TARGET_DATA_SALES_YEAR'].astype(int)
sales_target_data['SALES_TARGET_DATA_SALES_PERIOD'] = sales_target_data['SALES_TARGET_DATA_SALES_PERIOD'].astype(int)
sales_target_data['SALES_TARGET_DATA_PRODUCT_NUMBER'] = sales_target_data['SALES_TARGET_DATA_PRODUCT_NUMBER'].astype(int)
sales_target_data['SALES_TARGET_DATA_SALES_TARGET'] = sales_target_data['SALES_TARGET_DATA_SALES_TARGET'].astype(int)


result = sales_target_data.merge(order, left_on=['SALES_TARGET_DATA_SALES_STAFF_CODE', 'SALES_TARGET_DATA_PRODUCT_NUMBER', 'SALES_TARGET_DATA_SALES_YEAR', 'SALES_TARGET_DATA_SALES_PERIOD'], right_on=['ORDER_HEADER_SALES_STAFF_CODE', 'ORDER_DETAILS_PRODUCT_NUMBER', 'YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH'], how='left')
result


# Cleanup duplicate columns
result = result[[
    'SALES_TARGET_DATA_Id',
    'SALES_TARGET_DATA_SALES_TARGET',
    'ORDER_DETAILS_TOTAL_COST',
    'ORDER_DETAILS_TOTAL_PRICE',
    'ORDER_DETAILS_TOTAL_SALE_PRICE',
    'ORDER_DETAILS_QUANTITY',
    'SALES_TARGET_DATA_SALES_YEAR',
    'SALES_TARGET_DATA_SALES_PERIOD',
    'SALES_TARGET_DATA_SALES_STAFF_CODE',
    'SALES_STAFF_SALES_BRANCH_CODE',
    'SALES_TARGET_DATA_PRODUCT_NUMBER',
    'SALES_TARGET_DATA_RETAILER_CODE',
]]

# Rename columns
result = result.rename(columns={
    'SALES_TARGET_DATA_Id': 'SALES_TARGET_DATA_ID',
    'ORDER_DETAILS_TOTAL_COST': 'ORDER_DETAILS_TOTAL_COST',
    'ORDER_DETAILS_TOTAL_PRICE': 'ORDER_DETAILS_TOTAL_PRICE',
    'ORDER_DETAILS_TOTAL_SALE_PRICE': 'ORDER_DETAILS_TOTAL_SALE_PRICE',
    'ORDER_DETAILS_QUANTITY': 'ORDER_DETAILS_QUANTITY',
    'SALES_TARGET_DATA_SALES_YEAR': 'YEAR_MONTH_YEAR',
    'SALES_TARGET_DATA_SALES_PERIOD': 'YEAR_MONTH_MONTH',
})

# Rename foreign key columns
result = result.rename(columns={
    'SALES_TARGET_DATA_SALES_STAFF_CODE': 'SALES_STAFF_CODE',
    'SALES_STAFF_SALES_BRANCH_CODE': 'SALES_BRANCH_CODE',
    'SALES_TARGET_DATA_PRODUCT_NUMBER': 'PRODUCT_PRODUCT_NUMBER',
})

result['YEAR_MONTH_YEAR'] = result['YEAR_MONTH_YEAR'].astype(int)
result['YEAR_MONTH_MONTH'] = result['YEAR_MONTH_MONTH'].astype(int)
result['SALES_STAFF_CODE'] = result['SALES_STAFF_CODE'].astype(int)
result['SALES_BRANCH_CODE'] = result['SALES_BRANCH_CODE'].astype(int)
result['SALES_TARGET_DATA_RETAILER_CODE'] = result['SALES_TARGET_DATA_RETAILER_CODE'].astype(int)
