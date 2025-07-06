'''
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


standard scaling is used to normalize the features before clustering so as to make all the features standard
i.e. contributing equally to the clustering as this is without history.


def cluster_destinations(destinations_df, n_clusters=3):
    features=destinations_df[['rating', 'price', 'popularity']] #selecting features i.e. column from dataframe
    features = features.fillna(features.mean())  # Fill NaN values with column means

    # scale features for better clustering performance
    scaler = StandardScaler()  
    # changes data to have mean=0 and variance=1
    # this is important for kmeans as it is sensitive to the scale of the data
    scaled_features = scaler.fit_transform(features)

    # create and fit kmeans
    kmeans=KMeans(n_clusters=n_clusters, random_state=42)
    
    clusters=kmeans.fit_predict(scaled_features)
    
    fit learns the model from the data and returns the cluster labels for each data point like cluster 0,1 etc
    predict assigns each data point to a cluster based on the learned model
    

    # add cluster info back to the dataframe
    destinations_df['cluster'] = clusters

    return destinations_df, kmeans

if __name__=="__main__": # this means run this code only if the file is run directly without importing

    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    destinations = pd.read_csv(os.path.join(BASE_DIR, 'destinations.csv'))
    print(os.path.abspath('destinations.csv')) #gives the absolute path of the file
    print(destinations)
    clustered_destinations, model = cluster_destinations(destinations)
    #print(clustered_destinations.head()) # this only shows the first 5 rows no matter how many rows are there
    print(clustered_destinations)  # This will print the entire table with all clustered destinations
    print(model.cluster_centers_)  # This will print the cluster centers
'''

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

def cluster_items(df, features, n_clusters=3, random_state=42):
    """
    General clustering function for any item category.

    Args:
        df (pd.DataFrame): Data to cluster.
        features (list): Feature columns for clustering.
        n_clusters (int): Number of clusters.
        random_state (int): For reproducibility.

    Returns:
        pd.DataFrame: DataFrame with a new 'cluster' column.
        KMeans: The trained KMeans model.
    """
    # Select features and fill missing values
    selected_features = df[features].fillna(df[features].mean())

    # Scale features to have mean=0 and variance=1
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(selected_features)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(scaled_features)

    # Add cluster labels to DataFrame
    df['cluster'] = clusters
    return df, kmeans

def add_cluster_badges(df, cluster_mapping):
    """
    Map cluster numbers to friendly badge names.

    Args:
        df (pd.DataFrame): DataFrame with 'cluster' column.
        cluster_mapping (dict): Mapping from cluster number to badge name.

    Returns:
        pd.DataFrame: DataFrame with new 'cluster_badge' column.
    """
    df['cluster_badge'] = df['cluster'].map(cluster_mapping)
    return df

# Get the folder of this script to load CSVs correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load and cluster destinations
destinations = pd.read_csv(os.path.join(BASE_DIR, 'destinations.csv'))
dest_features = ['rating', 'price', 'popularity']
destinations, dest_model = cluster_items(destinations, dest_features)
dest_cluster_map = {
    0: 'Budget-friendly',
    1: 'Luxury',
    2: 'Hidden Gem'
}
destinations = add_cluster_badges(destinations, dest_cluster_map)

# Load and cluster foods
foods = pd.read_csv(os.path.join(BASE_DIR, 'foods.csv'))
food_features = ['taste_rating', 'price', 'popularity']
foods, food_model = cluster_items(foods, food_features)
food_cluster_map = {
    0: 'Affordable',
    1: 'Premium Dish',
    2: 'Local Favorite'
}
foods = add_cluster_badges(foods, food_cluster_map)

# Load and cluster activities
activities = pd.read_csv(os.path.join(BASE_DIR, 'activities.csv'))
activity_features = ['thrill_level', 'duration', 'popularity']
activities, act_model = cluster_items(activities, activity_features)
activity_cluster_map = {
    0: 'Chill Vibes',
    1: 'Adventure Packed',
    2: 'Family Friendly'
}
activities = add_cluster_badges(activities, activity_cluster_map)

# Load and cluster hotels
hotels = pd.read_csv(os.path.join(BASE_DIR, 'hotels.csv'))
hotels_features = ['price', 'rating', 'luxury_level']
hotels, hotels_model = cluster_items(hotels, hotels_features)
hotels_cluster_map = {
    0: 'Affordable Stay',
    1: 'Luxury Experience',
    2: 'Boutique Hotel'
}
hotels = add_cluster_badges(hotels, hotels_cluster_map)

# Store all clustered data in a dictionary for easy access
data_storage = {
    'destinations': destinations,
    'foods': foods,
    'activities': activities,
    'hotels': hotels
}
print(foods.groupby('cluster').mean())  # Print mean of each cluster for foods

if __name__ == "__main__":
    # Testing prints when running this file directly
    print("Destinations sample:\n", destinations.head(), "\n")
    print("Foods sample:\n", foods.head(), "\n")
    print("Activities sample:\n", activities.head(), "\n")
    print("Hotels sample:\n", hotels.head())


'''
data storage is needed as it will keep all clustered dataframes readily available for program
in app, a user might quickly switch between the categories then at that time i want to access the clustered data quickly without reading csv again
for performing further filtering, displaying or interaction without reloading from csv everytime

'''