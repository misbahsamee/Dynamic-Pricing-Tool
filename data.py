from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

# Load csv table
data = pd.read_csv('retail_data.csv')

print("Generating Clean_Data...")


# Quick data cleaning
# Set date column as datetime object
data.Date = pd.to_datetime(data.Date, format="%d/%m/%Y")

# Calculate price of each item from Sales and Quantity
data['item_price'] = data.Sales_Amount / data.Quantity
# Drop unused columns
data = data.drop('Unnamed: 0', axis=1)

product_grain = 'SKU_Category'

# Here we group and aggregate the transactions such that for each date and
# product (or category) we have:
#     - Total Quantity sold
#     - Total Sales Amount
#     - Average Discount in percentage
#     - Average item price
sales_by_date_and_category = data.groupby(['Date', product_grain]).agg(
    {
        'Quantity': 'sum',
        'item_price': np.average,
    }
).reset_index()

# Let's bring the day and month into separate columns
sales_by_date_and_category['day'] = sales_by_date_and_category.Date.dt.day
sales_by_date_and_category['month'] = sales_by_date_and_category.Date.dt.month

encoder = LabelEncoder().fit(sales_by_date_and_category[product_grain].values)
sales_by_date_and_category[product_grain] = encoder.transform(sales_by_date_and_category[product_grain])

sales_by_date_and_category.to_csv('clean_data.csv', index=False)

print("Clean_Data created!")
