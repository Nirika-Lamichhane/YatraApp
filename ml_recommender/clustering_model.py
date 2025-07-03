import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_destinations(destinations_df, n_clusters=3):
    features=destinations_df[['rating', 'price', 'popularity']]
    features = features.fillna(features.mean())  # Fill NaN values with column means

    # scale features for better clustering performance
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # create and fit kmeans
    kmeans=KMeans(n_clusters=n_clusters, random_state=42)
    clusters=kmeans.fit_predict(scaled_features)

    # add cluster info back to the dataframe
    destinations_df['cluster'] = clusters

    return destinations_df, kmeans

if __name__=="__main__":
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    destinations = pd.read_csv(os.path.join(BASE_DIR, 'destinations.csv'))
    clustered_destinations, model = cluster_destinations(destinations)
    print(clustered_destinations.head())