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
