# Sales ETL Project

Simple ETL demo — generates CSV sales files, loads into PostgreSQL, and computes a small analytics table.

# Files
- `data_generator.py` — produce sample CSV files (in `data/`) and `daily_sales.csv`.
- `bulk_data_load.py` — load all CSVs into `landing_bulk_sales` and create `sales_analytics`.
- `weekly_data_load.py` — append new records only; recompute analytics.
- `daily_sales_load.py` — load single `daily_sales.csv` into `landing_daily_sales`.
- `docker-compose.yml` — launches PostgreSQL container.
- `.env.example` — example env file (copy to `.env` and fill values).
- `.gitignore` — ignore `.env`, data, etc.

# Setup (local dev)

1. Clone repo:
```bash
git clone https://github.com/YOUR_USERNAME/Sales_ETL_Project.git
cd Sales_ETL_Project
