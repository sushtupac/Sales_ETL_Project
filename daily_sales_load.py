# daily_sales_load.py
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST") or "localhost"
DB_PORT = os.getenv("POSTGRES_PORT") or "5432"

DB_URL_SQLALCHEMY = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not os.path.exists('daily_sales.csv'):
    raise SystemExit("daily_sales.csv not found. Run data_generator.py first or provide that file.")

df = pd.read_csv('daily_sales.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df.dropna(subset=['customer_id', 'amount'], inplace=True)

engine = create_engine(DB_URL_SQLALCHEMY)
df.to_sql('landing_daily_sales', engine, if_exists='replace', index=False)
print("Wrote landing_daily_sales to DB.")
