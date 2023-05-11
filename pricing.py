import joblib

import pandas as pd
import numpy as np

sales_by_date_and_category = pd.read_csv('clean_data.csv')

rf = joblib.load('random_forest_model.joblib')

product_grain = 'SKU_Category'

categories = sales_by_date_and_category.SKU_Category.unique()


def optimize_quantity_out(model, df, product_grain, product_grain_value, day, month, grain=50):
    item_price_mean = df[df[product_grain] == product_grain_value].item_price.mean()

    # get virtual prices
    potential_price = np.linspace(item_price_mean * 0.25, item_price_mean * 2, grain)

    # loop to create each combination of price and discount
    samples = []
    for p in potential_price:
        sample = {
            product_grain: product_grain_value,
            'item_price': p,
            'day': day,
            'month': month
        }
        samples.append(sample)

    # use trained model to predict on virtual samples
    samples = pd.DataFrame(samples)
    samples['q_out_pred'] = model.predict(samples)
    samples['q_out_pred'] = samples['q_out_pred'].apply(np.ceil)
    samples['item_price'] = samples['item_price'].round(decimals=2)
    samples['revenue'] = samples.q_out_pred * samples.item_price
    # tag optimal params
    samples['is_optimal'] = [True if s == max(samples.revenue) else False for s in samples.revenue]
    optimal_samples = samples.loc[samples['is_optimal'] == True]
    optimal_samples = optimal_samples.drop_duplicates()
    return optimal_samples


# Here we choose the time period of our optimization
def max_revenue(day, month):
    optimal = pd.DataFrame(columns=['SKU_Category','item_price','day','month','q_out_pred','revenue','is_optimal'])
    # Here we choose the product (or category) to optimize
    for sku in categories:
        optimal = pd.concat([optimal,optimize_quantity_out(rf, sales_by_date_and_category, product_grain, sku, day, month, grain=100)],ignore_index=True)

    rev = optimal.sort_values(by='revenue',ascending=False).reset_index().drop(columns=['index','day','month','is_optimal'],axis=1)
    return rev






