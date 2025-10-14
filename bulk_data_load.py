# bulk_data_load.py
import os
import pandas as pd
from sqlalchemy import create_engine
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
all_files = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir) if f.endswith('.csv')
]

if not all_files:
    raise SystemExit("No CSV files found in the 'data/' directory. Run data_generator.py first.")

df_list = []
for file in all_files:
    print("Loading:", file)
    temp_df = pd.read_csv(file)
    df_list.append(temp_df)

combined_df = pd.concat(df_list, ignore_index=True)

combined_df['order_date'] = pd.to_datetime(combined_df['order_date'])
combined_df.dropna(subset=['customer_id', 'amount'], inplace=True)

engine = create_engine(DB_URL_SQLALCHEMY)
combined_df.to_sql('landing_bulk_sales', engine, if_exists='replace', index=False)
print("Wrote landing_bulk_sales to DB.")

# Create analytics table
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
print("Created/Updated sales_analytics table.")
