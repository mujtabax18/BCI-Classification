import tsfresh

# df is the dataset which will be in dataframe format
# Y is the independent variable
# id show epoch id name
# fdr_level on which selection is to be performed.
# Read the documentation of tsfreah at https://tsfresh.readthedocs.io/en/latest/api/tsfresh.feature_extraction.html
# sel_x gives the features as output of function

def tsfresh(df,y,column_id,fdr_level):
    extracted_features = tsfresh.extract_features(df,column_id=column_id)
    tsfresh.utilities.dataframe_functions.impute(extracted_features)
    sel_x=tsfresh.select_features(extracted_features,y,fdr_level=fdr_level)
    return sel_x
    
    