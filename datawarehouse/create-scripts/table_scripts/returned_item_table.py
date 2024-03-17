
import pandas as pd
from utils import *


# -- ORDER doeltabel --

# RETURNED_ITEM_return_code
# RETURNED_ITEM_return_quantity
# ORDER_DETAILS_unit_cost
# ORDER_DETAILS_unit_price
# ORDER_DETAILS_unit_sale_price
# ORDER_DETAILS_quantity
# DATE_returned_date
# ORDER_DETAILS_order_detail_code
# RETURN_REASON_return_reason_code


go_sales = load_db('source/go_sales.sqlite')


returned_item = load_table(go_sales, 'RETURNED_ITEM').add_prefix('RETURNED_ITEM_')
order_details = load_table(go_sales, 'ORDER_DETAILS').add_prefix('ORDER_DETAILS_')

# merge tables
result = returned_item.merge(order_details, left_on='RETURNED_ITEM_ORDER_DETAIL_CODE', right_on='ORDER_DETAILS_ORDER_DETAIL_CODE', how='left')

# Remove unwanted columns: RETURNED_ITEM_ORDER_DETAIL_CODE
result = result.drop(columns=['RETURNED_ITEM_ORDER_DETAIL_CODE'])

# Rename foreign key columns
result = result.rename(columns={
    'RETURNED_ITEM_RETURN_REASON_CODE': 'RETURN_REASON__RETURN_REASON_CODE',
    'RETURNED_ITEM_RETURN_DATE': 'DATE_RETURN_DATE',
    'ORDER_DETAILS_ORDER_NUMBER': 'ORDER_HEADER_ORDER_NUMBER',
    'ORDER_DETAILS_PRODUCT_NUMBER': 'PRODUCT_PRODUCT_NUMBER'
})

result['DATE_RETURN_DATE'] = pd.to_datetime(result['DATE_RETURN_DATE'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d')