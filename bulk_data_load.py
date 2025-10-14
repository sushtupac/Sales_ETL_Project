import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

data_dir = 'data/'
all_files = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.endswith('.csv')
]

df_list = [pd.read_csv(file) for file in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

combined_df['order_date'] = pd.to_datetime(combined_df['order_date'])
combined_df.dropna(subset=['customer_id', 'amount'], inplace=True)

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/salesdb')
combined_df.to_sql('landing_bulk_sales', engine, if_exists='replace', index=False)

conn = psycopg2.connect(
    dbname='salesdb',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
cur = conn.cursor()
cur.execute("""
    DROP TABLE IF EXISTS sales_analytics;
    CREATE TABLE sales_analytics AS
    SELECT
        customer_id,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(amount)::numeric, 2) AS total_spent
    FROM landing_bulk_sales
    WHERE amount > 0
    GROUP BY customer_id;
""")
conn.commit()
cur.close()
conn.close()
