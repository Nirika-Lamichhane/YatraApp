import pandas as pd
import psycopg2
import os
from sklearn.metrics.pairwise import cosine_similarity

# connection details
DB_NAME = "recommendation_system"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

# action scores for user actions
ACTION_SCORES = {
    'view': 1,
    'click': 2,
    'save': 3,
    'book': 4
}

def fetch_user_logs():
    """
    Fetch user logs from PostgreSQL database.
    
    Returns:
        pd.DataFrame: DataFrame containing user logs.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
       # query = "SELECT * FROM user_logs" # gives everything from the table
        query = "SELECT user_id, item_id, action_type FROM user_logs"

        df = pd.read_sql(query, conn)
        conn.close()
        df['score']=df['action_type'].map(ACTION_SCORES)  # Map action types to scores i.e. words to numbers machine friednly numbers
        
        return df
    except Exception as e:
        print(f"Error fetching user logs: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    
def build_user_item_matrix(df):
    """
    Build a user-item interaction matrix from user logs.
    
    Args:
        df (pd.DataFrame): DataFrame containing user logs.
        
    Returns:
        pd.DataFrame: User-item interaction matrix.
    """
    if df.empty:
        return pd.DataFrame()  # Return empty DataFrame if input is empty
    
    user_item_matrix = df.pivot_table(index='user_id', columns='item_id', values='score', fill_value=0)
    return user_item_matrix