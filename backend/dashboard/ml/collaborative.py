# dashboard/ml/collaborative.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# STEP 1: Build interaction dataframe
# --------------------------------------------------
def build_interactions(user_favorites, user_ratings, destination_links):
    """
    Build a unified dataframe of user interactions.

    Args:
        user_favorites (list of dict): [{'user_id': 1, 'item_id': 101, 'item_type': 'place'}, ...]
        user_ratings (list of dict):   [{'user_id': 1, 'item_id': 101, 'rating': 4.5, 'item_type': 'hotel'}, ...]
        destination_links (list of dict): [{'place_id': 101, 'hotel_id': 201, 'activity_id': 301, 'food_id': 401}, ...]

    Returns:
        pd.DataFrame: user-item interactions with scores
    """

    interactions = []

    # Favorites → implicit score
    for fav in user_favorites:
        interactions.append({
            "user_id": fav["user_id"],
            "item_id": f"{fav['item_type']}_{fav['item_id']}",
            "score": 1.0
        })

    # Ratings → explicit score
    for rating in user_ratings:
        interactions.append({
            "user_id": rating["user_id"],
            "item_id": f"{rating['item_type']}_{rating['item_id']}",
            "score": rating["rating"]
        })

    # Destination links → propagate place interactions to hotels/activities/foods
    for link in destination_links:
        place_id = f"place_{link['place_id']}"
        if "hotel_id" in link:
            interactions.append({
                "user_id": link.get("user_id", 0),  # optional, if linked by system
                "item_id": f"hotel_{link['hotel_id']}",
                "score": 0.5
            })
        if "activity_id" in link:
            interactions.append({
                "user_id": link.get("user_id", 0),
                "item_id": f"activity_{link['activity_id']}",
                "score": 0.5
            })
        if "food_id" in link:
            interactions.append({
                "user_id": link.get("user_id", 0),
                "item_id": f"food_{link['food_id']}",
                "score": 0.5
            })

    return pd.DataFrame(interactions)


# --------------------------------------------------
# STEP 2: Create user-item matrix
# --------------------------------------------------
def create_user_item_matrix(interactions):
    if interactions.empty:
        return pd.DataFrame()
    return interactions.pivot_table(
        index="user_id", columns="item_id", values="score", fill_value=0
    )


# --------------------------------------------------
# STEP 3: Generate recommendations
# --------------------------------------------------
def get_recommendations(user_id, user_item_matrix, top_n=5):
    """
    Recommend items for a given user.

    Args:
        user_id (int): Target user
        user_item_matrix (pd.DataFrame): User-item matrix
        top_n (int): Number of recommendations

    Returns:
        list of item_ids
    """
    if user_item_matrix.empty or user_id not in user_item_matrix.index:
        return []

    # Compute similarity
    similarity = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(
        similarity, index=user_item_matrix.index, columns=user_item_matrix.index
    )

    # Get top similar users
    similar_users = similarity_df[user_id].drop(user_id).sort_values(ascending=False)

    if similar_users.empty:
        return []

    # Weighted scores from similar users
    user_scores = user_item_matrix.loc[similar_users.index].T.dot(similar_users)

    # Remove already interacted items
    interacted_items = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index)
    recommendations = user_scores.drop(labels=interacted_items, errors="ignore")

    # Top N
    return recommendations.sort_values(ascending=False).head(top_n).index.tolist()
