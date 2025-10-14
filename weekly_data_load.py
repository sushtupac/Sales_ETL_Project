# weekly_data_load.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST") or "localhost"
DB_PORT = os.getenv("POSTGRES_PORT") or "5432"

DB_URL_SQLALCHEMY = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

data_dir = 'data/'
all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

engine = create_engine(DB_URL_SQLALCHEMY)

# get latest date from landing table (if exists)
latest_date = None
with engine.connect() as conn:
    try:
        result = conn.execute(text("SELECT max(order_date) FROM landing_bulk_sales"))
        latest_date = result.scalar()
        print("Latest date in landing_bulk_sales:", latest_date)
    except Exception as e:
        print("landing_bulk_sales may not exist yet:", e)
        latest_date = None

df_list = []
for file in all_files:
    try:
        temp_df = pd.read_csv(file)
        temp_df['order_date'] = pd.to_datetime(temp_df['order_date'])
        if latest_date is not None:
            temp_df = temp_df[temp_df['order_date'] > pd.to_datetime(latest_date)]
        temp_df.dropna(subset=['customer_id', 'amount'], inplace=True)
        if not temp_df.empty:
            df_list.append(temp_df)
            print(f"New data found in {file}: {len(temp_df)} rows")
        else:
            print(f"No new rows in {file}")
    except Exception as e:
        print(f"Error loading {file}: {e}")

if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_sql('landing_bulk_sales', engine, if_exists='append', index=False)
    print("Appended new rows to landing_bulk_sales.")
else:
    print("No new data to load.")

# recreate analytics table
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
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
print("Recreated sales_analytics table.")
