import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import psycopg2

# ------------------------ DATABASE SETTINGS ------------------------
DB_NAME = "recommendation_system"
DB_USER = "postgres"
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

# ------------------------ CLUSTERING FUNCTIONS ------------------------
def cluster_items(df, features, n_clusters=5, random_state=42):
    selected_features = df[features].fillna(df[features].mean())
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(selected_features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(scaled_features)
    df['cluster'] = clusters
    return df, kmeans

def add_cluster_badges(df, cluster_mapping):
    df['cluster_badge'] = df['cluster'].map(cluster_mapping)
    return df

# ------------------------ DB INSERT FUNCTION ------------------------
def insert_clustered_items_to_db(df, category):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO items (category, item_id, name, price, rating, popularity, cluster, cluster_badge)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                category,
                int(row['id']),
                row['name'],
                float(row.get('price', 0)),
                float(row.get('rating', 0)),
                float(row.get('popularity', 0)),
                int(row['cluster']),
                row['cluster_badge']
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Inserted clustered data for '{category}' into database.")
    except Exception as e:
        print(f"❌ Error inserting {category}: {e}")

# ------------------------ MAIN LOGIC ------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # -------- Destinations --------
    destinations = pd.read_csv(os.path.join(BASE_DIR, 'destinations.csv'))
    dest_features = ['rating', 'price', 'popularity']
    destinations, _ = cluster_items(destinations, dest_features)
    dest_cluster_map = { 0: 'Budget-friendly', 1: 'Luxury', 2: 'Hidden Gem' }
    destinations = add_cluster_badges(destinations, dest_cluster_map)
    insert_clustered_items_to_db(destinations, 'destinations')

    # -------- Foods --------
    foods = pd.read_csv(os.path.join(BASE_DIR, 'foods.csv'))
    food_features = ['taste_rating', 'price', 'popularity']
    foods = foods.rename(columns={'taste_rating': 'rating'})  # Match column name
    foods, _ = cluster_items(foods, ['rating', 'price', 'popularity'])
    food_cluster_map = { 1: 'Affordable', 0: 'Premium Dish', 2: 'Local Favorite' }
    foods = add_cluster_badges(foods, food_cluster_map)
    insert_clustered_items_to_db(foods, 'foods')

    # -------- Activities --------
    activities = pd.read_csv(os.path.join(BASE_DIR, 'activities.csv'))
    activity_features = ['thrill_level', 'duration', 'popularity']
    # Replace thrill_level with rating to match db schema
    activities = activities.rename(columns={'thrill_level': 'rating', 'duration': 'price'})  # symbolic mapping
    activities, _ = cluster_items(activities, ['rating', 'price', 'popularity'])
    act_cluster_map = { 0: 'Chill Vibes', 1: 'Adventure Packed', 2: 'Family Friendly' }
    activities = add_cluster_badges(activities, act_cluster_map)
    insert_clustered_items_to_db(activities, 'activities')

    # -------- Hotels --------
    hotels = pd.read_csv(os.path.join(BASE_DIR, 'hotels.csv'))
    hotels = hotels.rename(columns={'luxury_level': 'popularity'})  # symbolic mapping
    hotels_features = ['price', 'rating', 'popularity']
    hotels, _ = cluster_items(hotels, hotels_features)
    hotels_cluster_map = { 0: 'Affordable Stay', 1: 'Luxury Experience', 2: 'Boutique Hotel' }
    hotels = add_cluster_badges(hotels, hotels_cluster_map)
    insert_clustered_items_to_db(hotels, 'hotels')

    print("🎉 Clustering and DB insertion complete!")
