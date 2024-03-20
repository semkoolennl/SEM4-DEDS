import matplotlib.pyplot as plt
from exportutils import *

def actual_expected_plot():
    order_df    = execute_get_table("order_table")
    forecast_df    = execute_get_table("product_forecast_table")

    # Convert 'DATE_ORDER_DATE' column to datetime
    order_df['DATE_ORDER_DATE'] = pd.to_datetime(order_df['DATE_ORDER_DATE'])

    # Group by month and sum the order quantities
    order_df['Month'] = order_df['DATE_ORDER_DATE'].dt.to_period('M')
    orders_per_month = order_df.groupby('Month')['ORDER_DETAILS_QUANTITY'].sum()
    orders_per_month.index = orders_per_month.index.strftime('%Y-%m')

    # Assuming you have already calculated expected orders per month
    expected_orders_per_month = forecast_df.groupby(['YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH'])['PRODUCT_FORECAST_EXPECTED_VOLUME'].sum()
    expected_orders_per_month.index = expected_orders_per_month.index.map(lambda x: f"{x[0]}-{x[1]:02d}")

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(expected_orders_per_month, label='Expected Orders')
    plt.plot(orders_per_month, label='Actual Orders')
    plt.title('Expected vs. Actual Orders per Month')
    plt.xlabel('Month')
    plt.ylabel('Orders')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def actual_expected_per_product_plot():
    order_df = execute_get_table("order_table")
    forecast_df = execute_get_table("product_forecast_table")

    # Convert 'DATE_ORDER_DATE' column to datetime
    order_df['DATE_ORDER_DATE'] = pd.to_datetime(order_df['DATE_ORDER_DATE'])

    # Group by product and sum the order quantities
    orders_per_product = order_df.groupby('PRODUCT_PRODUCT_NUMBER')['ORDER_DETAILS_QUANTITY'].sum()

    # Group by product and sum the expected order volumes
    expected_orders_per_product = forecast_df.groupby('PRODUCT_PRODUCT_NUMBER')['PRODUCT_FORECAST_EXPECTED_VOLUME'].sum()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(orders_per_product.index, orders_per_product, label='Actual Orders')
    plt.bar(expected_orders_per_product.index, expected_orders_per_product, alpha=0.5, label='Expected Orders')
    plt.title('Expected vs. Actual Orders per Product')
    plt.xlabel('Product')
    plt.ylabel('Orders')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def actual_orders_per_method_plot():
    order_df = execute_get_table("order_table")

    # Group by sales method and sum the order quantities
    actual_orders_per_method = order_df.groupby('ORDER_METHOD_CODE')['ORDER_DETAILS_QUANTITY'].sum()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(actual_orders_per_method.index, actual_orders_per_method, label='Total orders')
    plt.title('Actual Orders per Sales Method')
    plt.xlabel('Sales Method')
    plt.ylabel('Number of Orders')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def inventory_turnover_rate_plot():
    inv_levels_df = execute_get_table("inventory_levels_table")

    # Group by product and get the mean inventory turnover rate
    turnover_rate_per_product = inv_levels_df.groupby('PRODUCT_PRODUCT_NUMBER')['INVENTORY_LEVELS_TURNOVER_RATE'].mean()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(turnover_rate_per_product.index, turnover_rate_per_product)
    plt.title('Inventory Turnover Rate per Product')
    plt.xlabel('Product')
    plt.ylabel('Turnover Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def inventory_vs_orders_over_time_plot():
    order_df = execute_get_table("order_table")
    inv_levels_df = execute_get_table("inventory_levels_table")

    # Convert 'DATE_ORDER_DATE' column to datetime and extract month
    order_df['Month'] = pd.to_datetime(order_df['DATE_ORDER_DATE']).dt.to_period('M')

    # Group by month and sum the order quantities
    orders_per_month = order_df.groupby('Month')['ORDER_DETAILS_QUANTITY'].sum()

    orders_per_month.index = orders_per_month.index.strftime('%Y-%m')

    # Group by month and calculate the total inventory count
    inventory_per_month = inv_levels_df.groupby(['YEAR_MONTH_YEAR', 'YEAR_MONTH_MONTH'])['INVENTORY_LEVELS_INVENTORY_COUNT'].sum()
    inventory_per_month.index = inventory_per_month.index.map(lambda x: f"{int(x[0])}-{int(x[1]):02d}")  # Convert to integers before formatting

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(orders_per_month.index, orders_per_month, label='Actual Orders', color='blue')
    plt.plot(inventory_per_month.index, inventory_per_month, label='Inventory Levels', color='green')

    plt.title('Comparison of Inventory Levels and Actual Orders over Time')
    plt.xlabel('Month')
    plt.ylabel('Quantity')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def inventory_order_correlation_per_product():
    order_df = execute_get_table("order_table")
    inv_levels_df = execute_get_table("inventory_levels_table")

    # Group by product and sum the order quantities
    orders_per_product = order_df.groupby('PRODUCT_PRODUCT_NUMBER')['ORDER_DETAILS_QUANTITY'].sum()

    # Group by product and calculate the total inventory count
    inventory_per_product = inv_levels_df.groupby('PRODUCT_PRODUCT_NUMBER')['INVENTORY_LEVELS_INVENTORY_COUNT'].sum()

    # Merge orders and inventory data
    merged_df = pd.merge(orders_per_product, inventory_per_product, left_index=True, right_index=True, suffixes=('_orders', '_inventory'))

    # Plot the correlation
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_df['ORDER_DETAILS_QUANTITY'], merged_df['INVENTORY_LEVELS_INVENTORY_COUNT'])
    plt.title('Correlation between Inventory Levels and Order Quantity per Product')
    plt.xlabel('Order Quantity')
    plt.ylabel('Inventory Levels')
    plt.tight_layout()
    plt.show()

def main():
    inventory_order_correlation_per_product()

if __name__ == '__main__':
    main()