
import pandas as pd
from utils import *


# -- ORDER doeltabel --

# ORDER_HEADER_order_number
# ORDER_DETAILS_order_detail_code
# ORDER_DETAILS_unit_cost
# ORDER_DETAILS_unit_price
# ORDER_DETAILS_unit_sale_price
# ORDER_DETAILS_quantity
# PRODUCT_production_cost
# PRODUCT_margin
# ORDER_profitability_index*
# ORDER_cvp_ratio*
# ORDER_sales_efficiency*
# PRODUCT_number
# DATE_order_date
# RETAILER_SITE_code
# RETAILER_CONTACT_code
# SALES_STAFF_code
# SALES_BRANCH_code 
# ORDER_METHOD_code


go_sales = load_db('source/go_sales.sqlite')


# Load all required tables here
order_header = load_table(go_sales, 'ORDER_HEADER')
order_details = load_table(go_sales, 'ORDER_DETAILS')
product = load_table(go_sales, 'PRODUCT')


# Remove unwanted columns, and add prefixes to the column names
order_header = order_header[[
    'ORDER_NUMBER', 
    'RETAILER_SITE_CODE', 
    'ORDER_METHOD_CODE',
    'SALES_STAFF_CODE',
    'SALES_BRANCH_CODE',
]].add_prefix('ORDER_HEADER_')

order_details = order_details[[
    'ORDER_NUMBER',
    'ORDER_DETAIL_CODE',
    'PRODUCT_NUMBER',
    'UNIT_COST',
    'UNIT_PRICE',
    'UNIT_SALE_PRICE',
    'QUANTITY'
]].add_prefix('ORDER_DETAILS_')

product = product[[
    'PRODUCT_NUMBER', 
    'PRODUCTION_COST', 
    'MARGIN'
]].add_prefix('PRODUCT_')


# Merge the tables
# order_details.order_number = order_header.order_number
# order_details.order_number = product.product_number

order = pd.merge(order_details, order_header, left_on='ORDER_DETAILS_ORDER_NUMBER', right_on='ORDER_HEADER_ORDER_NUMBER').drop('ORDER_DETAILS_ORDER_NUMBER', axis=1)
order = pd.merge(order, product, left_on='ORDER_DETAILS_PRODUCT_NUMBER', right_on='PRODUCT_PRODUCT_NUMBER').drop('ORDER_DETAILS_PRODUCT_NUMBER', axis=1)

# Rename columns
# ORDER_HEADER_ORDER_METHOD_CODE -> ORDER_METHOD_CODE
# ORDER_HEADER_RETAILER_SITE_CODE -> RETAILER_SITE_CODE
# ORDER_HEADER_RETAILER_CONTACT_CODE -> RETAILER_CONTACT_CODE
order = order.rename(columns={
    'ORDER_HEADER_ORDER_METHOD_CODE': 'ORDER_METHOD_CODE',
    'ORDER_HEADER_RETAILER_SITE_CODE': 'RETAILER_SITE_CODE',
    'ORDER_HEADER_RETAILER_CONTACT_CODE': 'RETAILER_CONTACT_CODE',
    'ORDER_HEADER_SALES_STAFF_CODE': 'SALES_STAFF_CODE',
    'ORDER_HEADER_SALES_BRANCH_CODE': 'SALES_BRANCH_CODE',
})

# Transform colums to the right type
order['ORDER_DETAILS_UNIT_COST'] = order['ORDER_DETAILS_UNIT_COST'].astype(float)
order['ORDER_DETAILS_UNIT_PRICE'] = order['ORDER_DETAILS_UNIT_PRICE'].astype(float)
order['ORDER_DETAILS_UNIT_SALE_PRICE'] = order['ORDER_DETAILS_UNIT_SALE_PRICE'].astype(float)
order['ORDER_DETAILS_QUANTITY'] = order['ORDER_DETAILS_QUANTITY'].astype(int)
order['PRODUCT_PRODUCTION_COST'] = order['PRODUCT_PRODUCTION_COST'].astype(float)
order['PRODUCT_MARGIN'] = order['PRODUCT_MARGIN'].astype(float)

# Add new calculated columns
# ORDER_PROFITABILITY_INDEX = PRODUCT_MARGIN / PRODUCT_PRODUCTION_COST
# ORDER_CVP_RATIO = (ORDER_DETAILS_UNIT_SALE_PRICE - ORDER_DETAILS_UNIT_COST) / ORDER_DETAILS_UNIT_SALE_PRICE
# ORDER_SALES_EFFICIENCY = ORDER_DETAILS_UNIT_SALE_PRICE / PRODUCT_PRODUCION_COST

order['ORDER_PROFITABILITY_INDEX'] = order['PRODUCT_MARGIN'] / order['PRODUCT_PRODUCTION_COST']
order['ORDER_CVP_RATIO'] = (order['ORDER_DETAILS_UNIT_SALE_PRICE'] - order['ORDER_DETAILS_UNIT_COST']) / order['ORDER_DETAILS_UNIT_SALE_PRICE']
order['ORDER_SALES_EFFICIENCY'] = order['ORDER_DETAILS_UNIT_SALE_PRICE'] / order['PRODUCT_PRODUCTION_COST']

result = order