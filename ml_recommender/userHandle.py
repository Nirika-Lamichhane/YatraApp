from clustering_model import data_storage
import pandas as pd
import os

'''
here category is input to the function which can be foods activities hotels or destinations
selected badge is like affordable adventure packed luxury etc

'''

# filtering logic
def get_filtered(Category, selected_badge):
    df= data_storage.get(Category) 
    if df is not None:
        filtered_df=df[df['cluster_badge']==selected_badge]
    # this only returns the dataframe of the matched badge in the clusterd dataframe. i.e. if Affordable is selected badge then only returns the df for that badge from the specific category
        return filtered_df
    else:
        return pd.DataFrame() # instead of crashing even if not found it returns an empty table.
    
'''
 data_storage is the dict of the clustered data from the data frames of the actual datas and tables
 this df line helps us to fetch the right dataframe based on the category user chooses


# function testing
if __name__=="__main__":
    filtered_foods= get_filtered('foods','Affordable')
    print(filtered_foods)
    
'''

# log system to store the history of the system

from datetime import datetime
import psycopg2 # helps python talk to postgresql database

# PostgreSQL connection details — update as per your setup
DB_NAME = "recommendation_system"  # Name of your PostgreSQL database i.e like house
DB_USER = "postgres"
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = "localhost"
DB_PORT = "5432"

ACTION_SCORES = {
    'view': 1,
    'click': 2,
    'save': 3,
    'book': 4
}

def log_user_Action(user_id, category, selected_badge, action_type, item_id=None):
    """
    Logs user actions for tracking and analysis in PostgreSQL.
    """
    score = ACTION_SCORES.get(action_type, 0)  # Not used here but useful later

    timestamp = datetime.now()

    log_entry = {
        'user_id': user_id,
        'category': category,
        'selected_badge': selected_badge,
        'action_type': action_type,
        'item_id': item_id,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert log entry into user_logs table 
        # here in insert we are not inserting the action score so to fetch the datas from the table we have to use the action score to provide numerical values to them
        
        cursor.execute('''
            INSERT INTO user_logs (user_id, category, selected_badge, action_type, item_id, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            log_entry['user_id'],
            log_entry['category'],
            log_entry['selected_badge'],
            log_entry['action_type'],
            log_entry['item_id'],
            log_entry['timestamp']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("User action logged to database successfully.")

    except Exception as e:
        print(f"Error logging user action: {e}")

''' 
this is to check if the table is created or not

log_user_Action(user_id=1, category='Foods', selected_badge='Affordable', action_type='click', item_id=101)
log_user_Action(user_id=5, category='Hotels', selected_badge='Affordable Stay', action_type='click', item_id=101)
log_user_Action(user_id=8, category='Destinations', selected_badge='Luxury', action_type='click', item_id=101)
'''