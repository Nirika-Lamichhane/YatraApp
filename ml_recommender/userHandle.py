from clustering_model import data_storage
import pandas as pd

'''
here category is input to the function which can be foods activities hotels or destinations
selected badge is like affordable adventure packed luxury etc

'''
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
 
'''

# function testing
if __name__=="__main__":
    filtered_foods= get_filtered('foods','Affordable')
    print(filtered_foods)
    