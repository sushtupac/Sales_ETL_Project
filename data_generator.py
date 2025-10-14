import pandas as pd
import numpy as np
from datetime import date, timedelta
import os

def generate_sales_data(sale_date, num_rows=500):
    np.random.seed(int(sale_date.strftime("%Y%m%d")))
    order_ids = np.arange(1, num_rows + 1)
    order_dates = [sale_date.isoformat()] * num_rows
    customer_ids = np.random.choice(np.arange(1000, 1100), size=num_rows)
    amounts = np.round(np.random.uniform(10, 1000, size=num_rows), 2)
    df = pd.DataFrame({
        'order_id': order_ids,
        'order_date': order_dates,
        'customer_id': customer_ids,
        'amount': amounts
    })
    mask_cust = np.random.rand(num_rows) < 0.05
    df.loc[mask_cust, 'customer_id'] = np.nan
    mask_amt = np.random.rand(num_rows) < 0.05
    df.loc[mask_amt, 'amount'] = np.nan
    return df

os.makedirs("data", exist_ok=True)
start_date = date(2025, 7, 10)

for i in range(7):
    d = start_date + timedelta(days=i)
    df_day = generate_sales_data(d, num_rows=500)
    df_day.to_csv(f"data/daily_sales_{d.isoformat()}.csv", index=False)

df_today = generate_sales_data(date(2025, 7, 16), num_rows=500)
df_today.to_csv("daily_sales.csv", index=False)
