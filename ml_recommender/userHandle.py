from clustering_model import data_storage
import pandas as pd

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
user_logs=[]

ACTION_SCORES={
    'view': 1,
    'click': 2,
    'save':3,
    'book':4
}

def log_user_Action(user_id,category,selected_badge,action_type,item_id=None):
    """
    Logs user actions for tracking and analysis.
    
    Args:
        user_id (str): Unique identifier for the user.
        category (str): Category of the item (e.g., 'foods', 'activities').
        selected_badge (str): Badge selected by the user.
        action_type (str): Type of action performed (e.g., 'view', 'click').
        item_id (str, optional): Unique identifier for the item. Defaults to None.
    """
    score = ACTION_SCORES.get(action_type, 0) # if action type not found then returns 0 by default

    log_entry = {
        'user_id': user_id,
        'category': category,
        'selected_badge': selected_badge,
        'action_type': action_type,
        'item_id': item_id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    }
    user_logs.append(log_entry)
