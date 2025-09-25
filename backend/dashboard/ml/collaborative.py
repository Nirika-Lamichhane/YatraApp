import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# STEP 1: Build interaction dataframe

def build_interactions(user_favorites, user_ratings, user_comments, destination_links, place_links):
    """
    Build user interactions based on favorites, ratings, and comments.
    Propagates scores from destinations -> places -> activities/foods/hotels.
    """
    interactions = []

    # ------------------------
    # FAVORITES
    # ------------------------
    for fav in user_favorites:
        user_id = fav['user_id']
        item_id = fav['item_id']
        item_type = fav['item_type']

        # Favorite itself
        interactions.append({
            "user_id": user_id,
            "item_id": item_id,
            "item_type": item_type,
            "score": 5.0
        })

        # If destination, propagate to related places, then their hotels/activities/foods
        if item_type == "destination" and item_id in destination_links:
            related_places = destination_links[item_id].get("places", [])
            for place_id in related_places:
                interactions.append({
                    "user_id": user_id,
                    "item_id": place_id,
                    "item_type": "place",
                    "score": 3.0
                })

                # Propagate hotels/activities/foods from place_links
                place_related = place_links.get(place_id, {})
                for hotel_id in place_related.get("hotels", []):
                    interactions.append({
                        "user_id": user_id,
                        "item_id": hotel_id,
                        "item_type": "hotel",
                        "score": 2.5
                    })
                for activity_id in place_related.get("activities", []):
                    interactions.append({
                        "user_id": user_id,
                        "item_id": activity_id,
                        "item_type": "activity",
                        "score": 2.5
                    })
                for food_id in place_related.get("foods", []):
                    interactions.append({
                        "user_id": user_id,
                        "item_id": food_id,
                        "item_type": "food",
                        "score": 2.5
                    })

        # If place, propagate to its activities and foods
        elif item_type == "place" and item_id in place_links:
            place_related = place_links[item_id]
            for hotel_id in place_related.get("hotels", []):
                interactions.append({
                    "user_id": user_id,
                    "item_id": hotel_id,
                    "item_type": "hotel",
                    "score": 2.5
                })
            for activity_id in place_related.get("activities", []):
                interactions.append({
                    "user_id": user_id,
                    "item_id": activity_id,
                    "item_type": "activity",
                    "score": 2.5
                })
            for food_id in place_related.get("foods", []):
                interactions.append({
                    "user_id": user_id,
                    "item_id": food_id,
                    "item_type": "food",
                    "score": 2.5
                })

    # RATINGS

    for rate in user_ratings:
        interactions.append({
            "user_id": rate['user_id'],
            "item_id": rate['item_id'],
            "item_type": rate['item_type'],
            "score": float(rate['rating'])
        })

    # COMMENTS

    for comment in user_comments:
        interactions.append({
            "user_id": comment['user_id'],
            "item_id": comment['item_id'],
            "item_type": comment['item_type'],
            "score": 3.0
        })

    return pd.DataFrame(interactions)

# STEP 2: Create user-item matrix

def create_user_item_matrix(interactions_df):
    return interactions_df.pivot_table(
        index="user_id",
        columns="item_id",
        values="score",
        fill_value=0
    )

# STEP 3: Calculate user similarity

def calculate_user_similarity(user_item_matrix):
    mat = user_item_matrix.values.astype(float)
    norms = np.linalg.norm(mat, axis=1)
    norms[norms == 0] = 1.0
    sim = (mat @ mat.T) / (norms[:, None] * norms[None, :])
    return pd.DataFrame(sim, index=user_item_matrix.index, columns=user_item_matrix.index)

# STEP 4: Get recommendations


def get_recommendations(user_id, user_item_matrix, user_similarity, top_n=5, category=None):
    if user_id not in user_item_matrix.index:
        return []

    sims = user_similarity.loc[user_id]
    weighted_scores = user_item_matrix.T.dot(sims)
    already_seen = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index)
    recommendations = weighted_scores.drop(labels=list(already_seen), errors="ignore")

    if category:
        recommendations = recommendations[[item for item in recommendations.index if item.startswith(category)]]

    return recommendations.sort_values(ascending=False).head(top_n).index.tolist()
