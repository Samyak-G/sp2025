import os
import psycopg2
from psycopg2 import sql, extras
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install it with 'pip install python-dotenv' if you want to load .env files.")

# Parse DATABASE_URL if present
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    result = urlparse(DATABASE_URL)
    DB_NAME = result.path.lstrip('/')
    DB_USER = result.username
    DB_PASSWORD = result.password
    DB_HOST = result.hostname
    DB_PORT = result.port or '5432'
else:
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')

REQUIRED_VARS = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing = [var for var in REQUIRED_VARS if not locals().get(var)]
if missing:
    print(f"Warning: Missing required database parameters: {', '.join(missing)}")

SCHEMA_SQL = """
-- 1. Create a custom schema for organization (optional, but recommended)
CREATE SCHEMA IF NOT EXISTS walmart;

-- 2. Warehouses table
CREATE TABLE IF NOT EXISTS walmart.warehouse (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    capacity INTEGER NOT NULL
);

-- 3. Dock Scheduling table
CREATE TABLE IF NOT EXISTS walmart.dock_schedule (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER NOT NULL REFERENCES walmart.warehouse(id) ON DELETE CASCADE,
    truck_id VARCHAR(50) NOT NULL,
    dock_number INTEGER NOT NULL,
    scheduled_time TIMESTAMP NOT NULL,
    estimated_duration INTEGER, -- in minutes
    actual_duration INTEGER,
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, in_progress, completed
    cargo_type VARCHAR(50),
    truck_size VARCHAR(20)
);

-- 4. Inventory table
CREATE TABLE IF NOT EXISTS walmart.inventory_item (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER NOT NULL REFERENCES walmart.warehouse(id) ON DELETE CASCADE,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL,
    zone VARCHAR(10),
    shelf_number INTEGER,
    turnover_rate FLOAT,
    last_moved TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Delivery Route table
CREATE TABLE IF NOT EXISTS walmart.delivery_route (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    source_warehouse_id INTEGER REFERENCES walmart.warehouse(id) ON DELETE SET NULL,
    destination_address TEXT NOT NULL,
    destination_lat DOUBLE PRECISION,
    destination_lng DOUBLE PRECISION,
    vehicle_type VARCHAR(50) NOT NULL,
    distance_km FLOAT,
    estimated_duration INTEGER, -- in minutes
    carbon_emissions FLOAT, -- kg CO2
    delivery_status VARCHAR(20) DEFAULT 'pending'
);

-- 6. Customer Profile table
CREATE TABLE IF NOT EXISTS walmart.customer_profile (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100),
    location VARCHAR(100),
    age INTEGER,
    income_level VARCHAR(20),
    preferences JSONB,
    sentiment_history JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. (Optional) Weather Data table for external API results caching
CREATE TABLE IF NOT EXISTS walmart.weather_data (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    temperature FLOAT,
    humidity FLOAT,
    weather_condition VARCHAR(50),
    wind_speed FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(SCHEMA_SQL)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_db() 