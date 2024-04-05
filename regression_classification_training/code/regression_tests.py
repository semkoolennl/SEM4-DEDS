import pandas as pd
from utils import *

from sklearn.model_selection import train_test_split
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

# Define different sets of columns
column_sets = [
    ['UNIT_COST', 'UNIT_PRICE', 'UNIT_SALE_PRICE', 'PRODUCTION_COST'],
    ['UNIT_COST', 'UNIT_PRICE', 'UNIT_SALE_PRICE', 'MARGIN'],
    ['UNIT_PRICE', 'UNIT_SALE_PRICE', 'MARGIN', 'RETAILER_CODE'],
    ['UNIT_COST', 'PRODUCTION_COST', 'MARGIN', 'RETAILER_CODE'],
    merged_data.columns.tolist()  # All columns
]

for i, columns in enumerate(column_sets, 1):
    print(f"Columns Set {i}: {columns}")

    x = merged_data[columns]
    y = merged_data['QUANTITY']

    X_train, X_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.15,
        random_state=42
    )

    reg_model = LinearRegression().fit(X_train, y_train)
    y_pred = reg_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred)
    plt.xlabel('Actual Quantity')
    plt.ylabel('Predicted Quantity')
    plt.title(f'Columns Set {i}')
    plt.show()
