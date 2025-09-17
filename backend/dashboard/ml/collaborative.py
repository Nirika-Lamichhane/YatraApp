# dashboard/ml/collaborative.py
import pandas as pd

def build_user_item_matrix(user_favorites_df):
    """
    Build a user-item matrix for collaborative filtering.
    Args:
        user_favorites_df (pd.DataFrame): columns = ['user_id', 'item_id', 'score']
    Returns:
        pd.DataFrame: user-item matrix
    """
    user_item_matrix = user_favorites_df.pivot_table(
        index='user_id',
        columns='item_id',
        values='score',
        fill_value=0
    )
    return user_item_matrix

def calculate_user_similarity(user_item_matrix):
    """
    Placeholder for computing user similarity using cosine similarity
    """
    from sklearn.metrics.pairwise import cosine_similarity
    sim_matrix = cosine_similarity(user_item_matrix)
    return pd.DataFrame(sim_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)

def recommend_items_for_user(user_id, user_similarity, user_item_matrix, top_n=5):
    """
    Placeholder: return recommended item IDs for a user.
    """
    # Currently returns top-n popular items (replace with real CF logic later)
    item_scores = user_item_matrix.sum(axis=0)
    return item_scores.sort_values(ascending=False).head(top_n).index.tolist()
