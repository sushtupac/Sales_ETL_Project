import os
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

DB_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/salesdb'
PG_RAW = {
    'dbname': 'salesdb',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

data_dir = 'data/'
all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]
engine = create_engine(DB_URL)

with engine.connect() as conn:
    result = conn.execute(text("select max(order_date) from landing_bulk_sales"))
    latest_date = result.scalar()

df_list = []
for file in all_files:
    try:
        temp_df = pd.read_csv(file)
        temp_df['order_date'] = pd.to_datetime(temp_df['order_date'])
        if latest_date:
            temp_df = temp_df[temp_df['order_date'] > latest_date]
        temp_df.dropna(subset=['customer_id', 'amount'], inplace=True)
        if not temp_df.empty:
            df_list.append(temp_df)
    except Exception as e:
        print(f"Error loading {file}: {e}")

if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_sql('landing_bulk_sales', engine, if_exists='append', index=False)
else:
    print("No new data to load.")

conn = psycopg2.connect(**PG_RAW)
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
