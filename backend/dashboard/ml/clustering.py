# dashboard/ml/clustering.py
print("this is clustering")
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def cluster_items(df, features, n_clusters=3, random_state=42):
    """
    Cluster items using KMeans.
    Args:
        df (pd.DataFrame): DataFrame with items
        features (list): list of column names to use for clustering
        n_clusters (int): number of clusters
    Returns:
        df (pd.DataFrame): original df with 'cluster' column
        kmeans (KMeans object): trained KMeans model
    """
    df_copy = df.copy()
    df_copy[features] = df_copy[features].fillna(0)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_copy[features])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    df_copy['cluster'] = kmeans.fit_predict(scaled_features)
    return df_copy, kmeans

def add_cluster_badges(df, cluster_mapping):
    """
    Map cluster numbers to human-readable badges.
    Args:
        df (pd.DataFrame): DataFrame with 'cluster' column
        cluster_mapping (dict): {cluster_number: badge_name}
    """
    df_copy = df.copy()
    df_copy['cluster_badge'] = df_copy['cluster'].map(cluster_mapping)
    return df_copy
