# Sales ETL Pipeline

An end-to-end ETL pipeline that generates synthetic sales data, loads it into PostgreSQL, and produces an analytics aggregation layer — packaged with Docker for easy local setup.

## What This Does

- Generates realistic daily and weekly CSV sales data
- Loads bulk and incremental data into PostgreSQL
- Computes a sales analytics table for downstream reporting
- Runs entirely in Docker — no manual database setup needed

## Tech Stack

- Python (pandas, SQLAlchemy, psycopg2)
- PostgreSQL
- Docker / Docker Compose

## Project Structure

```
Sales_ETL_Project/
├── data_generator.py      # Generates sample CSV sales files
├── bulk_data_load.py      # Loads all CSVs, creates analytics table
├── weekly_data_load.py    # Incremental load, recomputes analytics
├── daily_sales_load.py    # Loads single daily CSV
├── docker-compose.yml     # Launches PostgreSQL container
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

## Setup

1. Clone the repo:
   ```
   git clone https://github.com/sushtupac/Sales_ETL_Project.git
   cd Sales_ETL_Project
   ```

2. Copy the env file and fill in your values:
   ```
   cp .env.example .env
   ```

3. Start PostgreSQL:
   ```
   docker-compose up -d
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the pipeline:
   ```
   python data_generator.py
   python bulk_data_load.py
   ```

## Key Concepts Demonstrated

- Incremental vs bulk data loading
- Upsert patterns to avoid duplicate records
- Analytics aggregation layer on top of raw data
- Environment variable management for credentials
- Dockerized database setup for reproducibility
