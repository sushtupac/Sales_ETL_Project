import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('daily_sales.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df.dropna(subset=['customer_id', 'amount'], inplace=True)

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/salesdb')
df.to_sql('landing_daily_sales', engine, if_exists='replace', index=False)
