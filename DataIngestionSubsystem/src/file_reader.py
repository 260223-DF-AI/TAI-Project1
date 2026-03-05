import pandas as pd

def load_data(filepath):
    """
    Creates a DataFrame object from the given file, cleans it, then returns it
    """
    df = pd.read_csv(filepath)
    clean_data(df)
    return df

def clean_data(df):
    pass

#df = load_data("/../data/sidewalk-cafe-permits.csv")
#print(df)