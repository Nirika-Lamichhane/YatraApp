# dashboard/ml/db_loader.py
import pandas as pd
import psycopg2
import os

# ------------------------ DATABASE SETTINGS ------------------------
DB_NAME = "your_db_name"  # replace with your DB name
DB_USER = "postgres"      # or your DB user
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    """Return a new connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def load_table(table_name):
    """Fetch a table from the database and return as a Pandas DataFrame."""
    try:
        conn = get_connection()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading table {table_name}: {e}")
        return pd.DataFrame()

def load_all_data():
    """
    Load all required tables from PostgreSQL.
    
    Returns:
        tuple: destinations, destination_types, places, activities, foods, hotels, user_interactions
    """
    destinations = load_table("destinations")
    destination_types = load_table("destination_types")
    places = load_table("places")
    activities = load_table("activities")
    foods = load_table("foods")
    hotels = load_table("hotels")
    user_interactions = load_table("user_interactions")  # or favorites/logs table

    # If needed, merge destinations with destination_types
    if not destinations.empty and not destination_types.empty:
        destinations = destinations.merge(
            destination_types,
            left_on="type_id",  # adjust according to your DB schema
            right_on="id",
            suffixes=('', '_type')
        )

    return destinations, destination_types, places, activities, foods, hotels, user_interactions
