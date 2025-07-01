import pandas as pd
import os

'''
os is used here to get the path of the current file
that means even though we are running the file from some other folder other than 
its actual location, it will still be able to find the files in the same folder as this file.
'''
BASE_DIR = os.path.dirname(__file__)  # refers to ml_recommender/

def load_data():
    destinations = pd.read_csv(os.path.join(BASE_DIR, "destination.csv"))
    destination_types = pd.read_csv(os.path.join(BASE_DIR, "destination_types.csv"))
    activities = pd.read_csv(os.path.join(BASE_DIR, "activities.csv"))
    foods = pd.read_csv(os.path.join(BASE_DIR, "foods.csv"))
    hotels = pd.read_csv(os.path.join(BASE_DIR, "hotels.csv"))
    interactions = pd.read_csv(os.path.join(BASE_DIR, "user_interactions.csv"))

    destinations = destinations.merge(destination_types, left_on='destination_type_id', right_on='id', suffixes=('', '_type'))

    return destinations, destination_types, activities, foods, hotels, interactions
