
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

'''  
cosine similairty computes the similarity between users based on interactions
how aligned are the preferences of 2 users

'''

# building the interaction datafrane

def build_interactions(user_favorites, user_ratings, destination_links):

    ''' 
    the destination links is a dict mapping destination ids to lists of related item ids
    using this all the items related to a favorited destination are also added with a lower score
    user_favorites is the list of dict with user_id, item_id, type (destination, place, hotel, activity, food)
    user_ratings is the list of dict representing explicit ratings given by users

    '''
    interactions = []  # empty list to append all user item ineteractions 

    for fav in user_favorites:
        score = 2  

        # for the favorited destination, add related items with lower score
        if fav["type"] == "destination":
            interactions.append({
                "user_id": fav["user_id"],
                "item_id": f"dest_{fav['item_id']}",  #  to know this is a destination
                "score": score
            })

            # appending related items with a lower score
            for related in destination_links.get(fav["item_id"], []):
                interactions.append({
                    "user_id": fav["user_id"],
                    "item_id": related,
                    "score": 1
                })

        # append other types of favroites 
        else:
            interactions.append({
                "user_id": fav["user_id"],
                "item_id": f"{fav['type']}_{fav['item_id']}",
                "score": score
            })

    # for the rating of the places 

    for rate in user_ratings:
        interactions.append({
            "user_id": rate["user_id"],
            "item_id": f"{rate['type']}_{rate['item_id']}",
            "score": rate["rating"]
        })

    return pd.DataFrame(interactions)


def build_user_item_matrix(interactions_df):
    return interactions_df.pivot_table(index="user_id", columns="item_id", values="score", fill_value=0)


def calculate_user_similarity(user_item_matrix):
    # cosine similarity with numpy
    mat = user_item_matrix.values.astype(float)
    norms = np.linalg.norm(mat, axis=1)
    # avoid division by zero
    norms[norms == 0] = 1.0
    sim = (mat @ mat.T) / (norms[:, None] * norms[None, :])
    return pd.DataFrame(sim, index=user_item_matrix.index, columns=user_item_matrix.index)


def recommend_items_for_user(user_id, user_similarity, user_item_matrix, top_n=5):
    if user_id not in user_item_matrix.index:
        return []
    sims = user_similarity.loc[user_id]
    weighted_scores = user_item_matrix.T.dot(sims)
    already = set(user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index)
    recommendations = weighted_scores.drop(labels=list(already), errors="ignore")
    return recommendations.sort_values(ascending=False).head(top_n).index.tolist()

# Example usage (from your script)
user_favorites = [
    {"user_id": 1, "item_id": 1, "type": "destination"},
    {"user_id": 1, "item_id": 10, "type": "place"},
    {"user_id": 2, "item_id": 2, "type": "destination"},
]

user_ratings = [
    {"user_id": 1, "item_id": 10, "rating": 5},
    {"user_id": 2, "item_id": 11, "rating": 4},
]

destination_links = {
    1: ["place_10", "hotel_2", "activity_3"],
    2: ["place_11", "food_5"]
}

df = build_interactions(user_favorites, user_ratings, destination_links)
uim = build_user_item_matrix(df)
sim = calculate_user_similarity(uim)
recs = recommend_items_for_user(1, sim, uim, top_n=3)

import caas_jupyter_tools as tools
tools.display_dataframe_to_user("Interactions", df)
tools.display_dataframe_to_user("User-Item Matrix", uim)
tools.display_dataframe_to_user("User Similarity", sim)

print("Recommendations for User 1:", recs)
