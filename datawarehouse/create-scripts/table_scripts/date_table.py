import pandas as pd
from utils import *


# Doeltabel date

# DATE_DATE
# DATE_MONTH
# DATE_QUARTER
# DATE_YEAR

# Load databases
go_staff = load_db('source/go_staff.sqlite')
go_sales = load_db('source/go_sales.sqlite')

# Load tables
sales_staff = load_table(go_staff, 'SALES_STAFF')[['DATE_HIRED']]
product = load_table(go_sales, 'PRODUCT')[['INTRODUCTION_DATE']]
order_header = load_table(go_sales, 'ORDER_HEADER')[['ORDER_DATE']]
returned_item = load_table(go_sales, 'RETURNED_ITEM')[['RETURN_DATE']]

# Rename all date columns to DATE
sales_staff_date = sales_staff.rename(columns={'DATE_HIRED': 'DATE_DATE'})
product_date = product.rename(columns={'INTRODUCTION_DATE': 'DATE_DATE'})
order_header_date = order_header.rename(columns={'ORDER_DATE': 'DATE_DATE'})
returned_item_date = returned_item.rename(columns={'RETURN_DATE': 'DATE_DATE'})

# Transform all date columns to a single format 'YYYY-MM-DD'
sales_staff_date['DATE_DATE'] = pd.to_datetime(sales_staff_date['DATE_DATE'], format='%d-%b-%Y %H:%M:%S %p').dt.strftime('%Y-%m-%d')
product_date['DATE_DATE'] = pd.to_datetime(product_date['DATE_DATE'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
order_header_date['DATE_DATE'] = pd.to_datetime(order_header_date['DATE_DATE'])
returned_item_date['DATE_DATE'] = pd.to_datetime(returned_item_date['DATE_DATE'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d')

# Union all date columns
date = pd.concat([sales_staff_date, product_date, order_header_date, returned_item_date], ignore_index=True).drop_duplicates()

# Add DATE_MONTH, DATE_QUARTER, DATE_YEAR
date['DATE_MONTH'] = pd.to_datetime(date['DATE_DATE']).dt.month.astype('int64')
date['DATE_QUARTER'] = pd.to_datetime(date['DATE_DATE']).dt.quarter.astype('int64')
date['DATE_YEAR'] = pd.to_datetime(date['DATE_DATE']).dt.year.astype('int64')

sales_staff_date['DATE_DATE'] = sales_staff_date['DATE_DATE'].astype('datetime64[ns]')
product_date['DATE_DATE'] = product_date['DATE_DATE'].astype('datetime64[ns]')
order_header_date['DATE_DATE'] = order_header_date['DATE_DATE'].astype('datetime64[ns]')
returned_item_date['DATE_DATE'] = returned_item_date['DATE_DATE'].astype('datetime64[ns]')


result = date