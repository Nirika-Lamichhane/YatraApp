# dashboard/ml/clustering.py

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
    if df.empty:
        return df, None
    
    df_copy = df.copy()

    # filling missing values with 0 as Kmeans cant handle NaNs
    df_copy[features] = df_copy[features].fillna(0)

    # scaling the features 
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_copy[features])

    # using KMeans to cluster
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

    # adds the column named cluster in the dataframe 
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
    if 'cluster' in df_copy.columns:
        df_copy['cluster_badge'] = df_copy['cluster'].map(cluster_mapping) # cluster mapping is the dictionary that maps the cluster numbers to human readable badges
    else:
        df_copy['cluster_badge'] = None
    return df_copy
   

def cluster_for_dashboard(df, features, n_clusters=3, badge_mapping=None):
    """
    Full pipeline for dashboard: clustering + optional badges. i.e. like the main function
    it assigns the process to the functions
    

    Args:
        df (pd.DataFrame): DataFrame to cluster.
        features (list): Features to use for clustering.
        n_clusters (int): Number of clusters.
        badge_mapping (dict, optional): {cluster_number: badge_name}

    Returns:
        pd.DataFrame: Clustered DataFrame (with badges if provided)
    """
    clustered_df, kmeans = cluster_items(df, features, n_clusters)
    if badge_mapping:
        clustered_df = add_cluster_badges(clustered_df, badge_mapping)
    return clustered_df
