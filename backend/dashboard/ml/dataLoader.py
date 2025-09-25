# dashboard/ml/db_loader.py
import pandas as pd
import psycopg2
import os

# ------------------------ DATABASE SETTINGS -------------------
DB_NAME = "recommendation_system"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

# ------------------------ GLOBAL CACHE ------------------------
user_interaction_cache = None  # stores interactions in memory

# ------------------------ DATABASE CONNECTION ------------------------
def get_connection():
    """Return a new connection to PostgreSQL."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ------------------------ TABLE LOADER ------------------------
def load_table(table_name):
    """Load a table from DB as a Pandas DataFrame."""
    try:
        conn = get_connection()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading table {table_name}: {e}")
        return pd.DataFrame()

# ------------------------ MERGE USER INTERACTIONS ------------------------
def load_user_interactions(force_refresh=False):
    """
    Load favorites + comments + ratings and build links.
    Returns a dictionary matching recommend_view expectations.
    """
    global user_interaction_cache

    if user_interaction_cache is not None and not force_refresh:
        return user_interaction_cache

    # Load tables
    favorites = load_table("dashboard_favorite")
    comments = load_table("dashboard_comment")
    ratings = load_table("dashboard_rating")  # create this table if needed

    # Convert to lists of dicts
    favorites_list = favorites.to_dict(orient="records") if not favorites.empty else []
    comments_list = comments.to_dict(orient="records") if not comments.empty else []
    ratings_list = ratings.to_dict(orient="records") if not ratings.empty else []

    # Load items for links
    destinations = load_table("accounts_destination")
    places = load_table("dashboard_place")
    hotels = load_table("dashboard_hotel")
    activities = load_table("dashboard_activity")
    foods = load_table("dashboard_food")

    # Build destination_links dictionary
    destination_links_dict = {}
    for dest_id in destinations["id"].tolist():
        related_places = places[places["destination_id"] == dest_id]["id"].tolist()
        related_hotels = hotels[hotels["place_id"].isin(related_places)]["id"].tolist()
        related_activities = activities[activities["place_id"].isin(related_places)]["id"].tolist()
        related_foods = foods[foods["place_id"].isin(related_places)]["id"].tolist()
        destination_links_dict[dest_id] = (
            [f"place_{pid}" for pid in related_places] +
            [f"hotel_{hid}" for hid in related_hotels] +
            [f"activity_{aid}" for aid in related_activities] +
            [f"food_{fid}" for fid in related_foods]
        )

    # Build place_links dictionary
    place_links_dict = {}
    for place_id in places["id"].tolist():
        related_hotels = hotels[hotels["place_id"] == place_id]["id"].tolist()
        related_activities = activities[activities["place_id"] == place_id]["id"].tolist()
        related_foods = foods[foods["place_id"] == place_id]["id"].tolist()
        place_links_dict[place_id] = (
            [f"hotel_{hid}" for hid in related_hotels] +
            [f"activity_{aid}" for aid in related_activities] +
            [f"food_{fid}" for fid in related_foods]
        )

    # Combine into dictionary
    user_interaction_cache = {
        "favorites": favorites_list,
        "ratings": ratings_list,
        "comments": comments_list,
        "destination_links": destination_links_dict,
        "place_links": place_links_dict
    }

    return user_interaction_cache

# ------------------------ LOAD ALL DATA ------------------------
def load_all_data():
    """
    Load all required tables from PostgreSQL and user interactions.
    Returns:
        tuple: destinations, destination_types, places, activities, foods, hotels, user_interactions
    """
    destinations = load_table("accounts_destination")
    destination_types = load_table("accounts_destinationtype")
    places = load_table("dashboard_place")
    activities = load_table("dashboard_activity")
    foods = load_table("dashboard_food")
    hotels = load_table("dashboard_hotel")

    # Load user interactions
    user_interactions = load_user_interactions()

    # Merge destinations with destination_types if available
    if not destinations.empty and not destination_types.empty:
        destinations = destinations.merge(
            destination_types,
            left_on="type_id",
            right_on="id",
            suffixes=('', '_type')
        )

    return destinations, destination_types, places, activities, foods, hotels, user_interactions
