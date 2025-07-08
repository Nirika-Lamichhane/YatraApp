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
    
    user_item_matrix = df.pivot_table(index='user_id', columns='item_id', values='score',aggfunc='sum', fill_value=0)
    return user_item_matrix

def calculate_user_similarities(matrix):
    if matrix.empty:
        return pd.DataFrame()
    
    # calculates the similatities between users
    user_similarity = cosine_similarity(matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=matrix.index, columns=matrix.index) # this matrix.index creates the table/ matrix with the names os users on the both rows and columns as the id
    return user_similarity_df

def recommend_items(user_id, user_similarities, user_item_matix, top_n=5):
    """
    Recommend items for a given user based on user similarities.
    
    Args:
        user_id (int): User ID for whom to recommend items.
        user_similarities (pd.DataFrame): DataFrame containing user similarities.
        user_item_matrix (pd.DataFrame): User-item interaction matrix.
        top_n (int): Number of top recommendations to return.
        
    Returns:
        list: List of recommended item IDs.
    """
    try:
        similar_users= user_similarities[user_id].drop(user_id).sort_values(ascending=False) # this is the pandas series which gives the similar users
        scores= user_item_matix.loc[similar_users.index].T.dot(similar_users) # this .dot treates the similar users i.e. pandas serials as the column matrix as users*1

        # remove already interacted items by the user we want to recommend for
        scores=scores.drop(user_item_matix.loc[user_id][user_item_matix.loc[user_id]>0].index, errors='ignore')

        return scores.sort_values(ascending=False).head(top_n).index.tolist()  # return the top N list of items
    
    except Exception as e:
        print(f"Error recommending items for user {user_id} : {e}")
        return pd.Series()