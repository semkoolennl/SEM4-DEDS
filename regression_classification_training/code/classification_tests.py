import pandas as pd
from utils import *

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics
import matplotlib.pyplot as plt



# Load databases
go_sales = load_db('source/go_sales.sqlite')
go_crm = load_db('source/go_crm.sqlite')
go_staff = load_db('source/go_staff.sqlite')

# Load tables
order_details = load_table(go_sales, 'ORDER_DETAILS')
returned_item = load_table(go_sales, 'RETURNED_ITEM')
order_header = load_table(go_sales, 'ORDER_HEADER')
product = load_table(go_sales, 'PRODUCT')


# Joins based on column names
merged_data = pd.merge(order_details, order_header, on='ORDER_NUMBER')
merged_data = pd.merge(merged_data, product, on='PRODUCT_NUMBER')
merged_data = pd.merge(merged_data, returned_item, on='ORDER_DETAIL_CODE')


merged_data.drop(columns=['UNIT_COST', 'UNIT_PRICE', 'RETAILER_NAME', 'RETAILER_CONTACT_CODE', 
                          'SALES_STAFF_CODE', 'PRODUCTION_COST', 'MARGIN', 'PRODUCT_IMAGE', 
                          'LANGUAGE', 'PRODUCT_NAME', 'DESCRIPTION'], inplace=True)

# Convert dates to float representation
merged_data['ORDER_DATE'] = pd.to_datetime(merged_data['ORDER_DATE'], format='%Y-%m-%d').astype('int64') / 10**9
merged_data['INTRODUCTION_DATE'] = pd.to_datetime(merged_data['INTRODUCTION_DATE'], format='%d-%m-%Y').astype('int64') / 10**9
merged_data['RETURN_DATE'] = pd.to_datetime(merged_data['RETURN_DATE'], format='%d-%m-%Y %H:%M:%S').astype('int64') / 10**9

print_columns(merged_data)

merged_data['RETURN_REASON_CODE'] = merged_data['RETURN_REASON_CODE'].astype('int64')
# merged_data = pd.get_dummies(merged_data, columns=['ORDER_DATE', 'INTRODUCTION_DATE', 'RETURN_DATE'])


x = merged_data.drop('RETURN_REASON_CODE', axis = 1)
y = merged_data.loc[:, ['RETURN_REASON_CODE']]

X_train, X_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.15,
    random_state=42
)

dtree = DecisionTreeClassifier(max_depth=2)
dtree = dtree.fit(X_train, y_train)
tree.plot_tree(dtree, feature_names= x.columns)
plt.show()

pred_df = pd.DataFrame(dtree.predict(X_test))
pred_df = pred_df.rename(columns= {0 : 'Predicted_returned_reason'})
model_results_frame = pd.concat([y_test.reset_index()['RETURN_REASON_CODE'], pred_df], axis = 1)
print(model_results_frame)

confusion_matrix = metrics.confusion_matrix(model_results_frame['RETURN_REASON_CODE'], model_results_frame['Predicted_returned_reason'], labels=[1, 2, 3, 4, 5])
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels = [1, 2, 3, 4, 5])
cm_display.plot()
plt.show()


print(metrics.accuracy_score(model_results_frame['RETURN_REASON_CODE'], model_results_frame['Predicted_returned_reason']))