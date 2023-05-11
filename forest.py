from sklearn.ensemble import RandomForestRegressor
import joblib
import pandas as pd


sales_by_date_and_category = pd.read_csv('clean_data.csv')

print("Training RandomForestRegressor Model...")

rf = RandomForestRegressor(n_estimators=150)

sales_by_date_and_category = sales_by_date_and_category.sample(frac=1)
X = sales_by_date_and_category[['SKU_Category', 'item_price', 'day', 'month']]
Y = sales_by_date_and_category['Quantity']

rf = rf.fit(X, Y)

sales_by_date_and_category['predicted_quantity'] = rf.predict(X)
# Compute mean absolute error on predictions
sales_by_date_and_category['error'] = abs(
    sales_by_date_and_category.Quantity - sales_by_date_and_category.predicted_quantity)
print(f"Mean Absolute Error: {sales_by_date_and_category['error'].mean()}")

joblib.dump(rf, 'random_forest_model.joblib')

print("RF model created!")
