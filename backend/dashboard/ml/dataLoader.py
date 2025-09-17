# dashboard/ml/db_loader.py
import pandas as pd
import psycopg2  # to communicate with PostgreSQL
import os        # to read environment variables

# ------------------------ DATABASE SETTINGS -------------------
DB_NAME = "recommendation_system"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

# ------------------------ GLOBAL CACHE ------------------------
user_interaction_cache = None  # This will store merged favorites + comments in memory

# ------------------------ DATABASE CONNECTION ------------------------
def get_connection():
    """Return a new connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ------------------------ TABLE LOADER ------------------------
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

# MERGE USER INTERACTIONS  this returns a merged dataframe 
def load_user_interactions(force_refresh=False):
    """
    Load favorites + comments and merge into one DataFrame.
    Cache the result in memory to avoid re-merging every login.

    Args:
        force_refresh (bool): If True, reload data from DB even if cached.

    Returns:
        pd.DataFrame: Merged user interactions
    """
    global user_interaction_cache

    # Return cached version if available and not forced to refresh
    if user_interaction_cache is not None and not force_refresh:
        return user_interaction_cache

    # Load favorites and comments
    favorites = load_table("dashboard_favorite")
    comments = load_table("dashboard_comment")

    # Add a column to distinguish the type of interaction
    if not favorites.empty:
        favorites['interaction_type'] = 'favorite'
    if not comments.empty:
        comments['interaction_type'] = 'comment'

    # Merge both tables into a single DataFrame
    user_interaction_cache = pd.concat([favorites, comments], ignore_index=True)

    return user_interaction_cache

# ------------------------ LOAD ALL DATA ------------------------
def load_all_data():
    """
    Load all required tables from PostgreSQL.

    Returns:
        tuple: destinations, destination_types, places, activities, foods, hotels, user_interactions
    """
    destinations = load_table("accounts_destination")
    destination_types = load_table("accounts_destinationtype")
    places = load_table("dashboard_place")
    activities = load_table("dashboard_activity")
    foods = load_table("dashboard_food")
    hotels = load_table("dashboard_hotel")

    # Load merged user interactions from cache (or DB if first time)
    user_interactions = load_user_interactions()

    # Merge destinations with destination_types if available
    if not destinations.empty and not destination_types.empty:
        destinations = destinations.merge(
            destination_types,
            left_on="type_id",  # foreign key pointing to destination_type
            right_on="id",
            suffixes=('', '_type')
        )

    return destinations, destination_types, places, activities, foods, hotels, user_interactions
