import pandas as pd
import os

'''
os is used here to get the path of the current file
that means even though we are running the file from some other folder other than 
its actual location, it will still be able to find the files in the same folder as this file.
'''
try:
    BASE_DIR = os.path.dirname(__file__) # this 
except NameError:
    # __file__ is not defined in Jupyter notebooks so while using notebook use this
    BASE_DIR = os.getcwd()

def load_data():
    destinations = pd.read_csv("destination.csv")
    destination_types = pd.read_csv("destination_types.csv")
    activities = pd.read_csv("activities.csv")
    foods = pd.read_csv("foods.csv")
    hotels = pd.read_csv("hotels.csv")
    interactions = pd.read_csv("user_interactions.csv")

    destinations = destinations.merge(destination_types, left_on='destination_type_id', right_on='id', suffixes=('', '_type'))

    return destinations, destination_types, activities, foods, hotels, interactions