import pandas as pd
from utils import *

from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Load databases
go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')
go_staff = load_db('source/go_staff.sqlite')

# Load tables
order_details = load_table(go_sales, 'ORDER_DETAILS')
order_header = load_table(go_sales, 'ORDER_HEADER')
product = load_table(go_sales, 'PRODUCT')
order_method = load_table(go_sales, 'ORDER_METHOD')
sales_branch = load_table(go_staff, 'SALES_BRANCH')
sales_staff = load_table(go_staff, 'SALES_STAFF')
retailer_site = load_table(go_sales, 'RETAILER_SITE')

# Joins based on column names
merged_data = pd.merge(order_details, order_header, on='ORDER_NUMBER')
merged_data = pd.merge(merged_data, product, on='PRODUCT_NUMBER')
merged_data = pd.merge(merged_data, order_method, on='ORDER_METHOD_CODE')
merged_data = pd.merge(merged_data, sales_branch, on='SALES_BRANCH_CODE')
merged_data = pd.merge(merged_data, sales_staff, on='SALES_STAFF_CODE')
merged_data = pd.merge(merged_data, retailer_site, on='RETAILER_SITE_CODE')

# Drop columns that are irrelevant or not usable
merged_data.drop(columns=['RETAILER_NAME', 'PRODUCT_IMAGE', 'LANGUAGE', 'PRODUCT_NAME', 'DESCRIPTION',
                           'ADDRESS1_x', 'ADDRESS2_x', 'WORK_PHONE', 'CITY_x', 'CITY_y', 'REGION_y', 'REGION_x',
                           'FAX', 'EMAIL', 'POSTAL_ZONE_x', 'FIRST_NAME', 'LAST_NAME', 'ADDRESS1_y', 'ADDRESS2_y', 'POSTAL_ZONE_y', 'EXTENSION'], inplace=True)

# Convert dates to float representation
merged_data['ORDER_DATE'] = pd.to_datetime(merged_data['ORDER_DATE']).astype('int64') / 10**9
merged_data['INTRODUCTION_DATE'] = pd.to_datetime(merged_data['INTRODUCTION_DATE']).astype('int64') / 10**9
merged_data['DATE_HIRED'] = pd.to_datetime(merged_data['DATE_HIRED']).astype('int64') / 10**9


merged_data = pd.get_dummies(merged_data, columns=['ORDER_METHOD_EN', 'POSITION_EN'])

# Cast columns to float
merged_data['UNIT_COST'] = merged_data['UNIT_COST'].astype(float)
merged_data['UNIT_PRICE'] = merged_data['UNIT_PRICE'].astype(float)
merged_data['UNIT_SALE_PRICE'] = merged_data['UNIT_SALE_PRICE'].astype(float)
merged_data['PRODUCTION_COST'] = merged_data['PRODUCTION_COST'].astype(float)
merged_data['MARGIN'] = merged_data['MARGIN'].astype(float)

# Cast columns to int64
merged_data['RETAILER_CODE'] = merged_data['RETAILER_CODE'].astype('int64')
merged_data['MANAGER_CODE'] = merged_data['MANAGER_CODE'].astype('int64')
merged_data['COUNTRY_CODE_y'] = merged_data['COUNTRY_CODE_y'].astype('int64')
merged_data['ACTIVE_INDICATOR'] = merged_data['ACTIVE_INDICATOR'].astype('int64')
merged_data['RETAILER_SITE_CODE'] = merged_data['RETAILER_SITE_CODE'].astype('int64')
merged_data['RETAILER_CONTACT_CODE'] = merged_data['RETAILER_CONTACT_CODE'].astype('int64')
merged_data['SALES_STAFF_CODE'] = merged_data['SALES_STAFF_CODE'].astype('int64')
merged_data['SALES_BRANCH_CODE_x'] = merged_data['SALES_BRANCH_CODE_x'].astype('int64')
merged_data['ORDER_METHOD_CODE'] = merged_data['ORDER_METHOD_CODE'].astype('int64')
merged_data['PRODUCT_TYPE_CODE'] = merged_data['PRODUCT_TYPE_CODE'].astype('int64')
merged_data['COUNTRY_CODE_x'] = merged_data['COUNTRY_CODE_x'].astype('int64')
merged_data['ORDER_DETAIL_CODE'] = merged_data['ORDER_DETAIL_CODE'].astype('int64')
merged_data['ORDER_NUMBER'] = merged_data['ORDER_NUMBER'].astype('int64')
merged_data['PRODUCT_NUMBER'] = merged_data['PRODUCT_NUMBER'].astype('int64')
merged_data['SALES_BRANCH_CODE_y'] = merged_data['SALES_BRANCH_CODE_y'].astype('int64')



# print(merged_data)
# print_columns(merged_data)

x = merged_data.drop('QUANTITY', axis = 1)
y = merged_data.loc[:, ['QUANTITY']]


X_train, X_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size= 0.15,
    random_state= 42
)


reg_model = linear_model.LinearRegression()
reg_model = LinearRegression().fit(X_train, y_train)

y_pred = reg_model.predict(X_test)

pred_df = pd.DataFrame(y_pred)
pred_df= pred_df.rename(columns= {0 : 'Prediction_Quantity'})


y_test_pred_merge = pd.concat([y_test.reset_index()["QUANTITY"], pred_df], axis=1)
y_test_pred_merge.loc[y_test_pred_merge['Prediction_Quantity'].notna(), :]


plt.scatter(y_test_pred_merge['QUANTITY'], y_test_pred_merge['Prediction_Quantity'])
plt.xlabel('QUANTITY')
plt.ylabel('Prediction_Quantity')
plt.show()

print(mean_squared_error(y_test_pred_merge['QUANTITY'], y_test_pred_merge['Prediction_Quantity']))
print(mean_absolute_error(y_test_pred_merge['QUANTITY'], y_test_pred_merge['Prediction_Quantity']))