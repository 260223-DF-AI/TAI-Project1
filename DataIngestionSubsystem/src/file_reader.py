import pandas as pd

def load_data(filepath):
    """
    Creates a DataFrame object from the given file, cleans it, then returns it
    """
    dotIndex = filepath.rfind('.')
    try:
        if(filepath[dotIndex + 1].lower() == 'csv'):
            df = pd.read_csv(filepath,
                dtype={'ZIP CODE':'str'}, # Make ZIP CODE a str
                date_format="%Y-%m-%dT%H:%M:%S.%f",
                parse_dates=['ISSUED DATE', 'EXPIRATION DATE', 'PAYMENT DATE'],
                na_values=None # We can change this later
            )
        elif(filepath[dotIndex + 1].lower() == 'json'):
            df = pd.read_json(filepath,
                dtype={'ZIP CODE':'str'}, # Make ZIP CODE a str
                date_format="%Y-%m-%dT%H:%M:%S.%f",
                parse_dates=['ISSUED DATE', 'EXPIRATION DATE', 'PAYMENT DATE'],
                na_values=None # We can change this later
            )
    except FileNotFoundError:
        # Eventually we will probably also want to log this
        print(f"Given filepath ({filepath}) does not exist.")
    clean_data(df)
    return df

def clean_data(df: pd.DataFrame):
    # Handle rows with None values/missing data: Drop row
    df.dropna(inplace=True)

    # Handle duplicate data
    df.drop_duplicates(inplace=True)

    # drop LOCATION and ADDRESS NUMBER START columns
    df.drop(columns=["LOCATION", "ADDRESS NUMBER START"], inplace=True)

    # Standardize text columns
    strCols = [col for col in df.columns if df[col].dtype == 'str'] # not sure how necessary this line is
    df[strCols] = df[strCols].apply(lambda col: col.str.upper())

    return df

# To check what columns we can use for a primary key
def is_unique_column(df: pd.DataFrame, colName: str) -> bool:
    """
    Checks if all values in a column are unique
    Args:
        df: Pandas DataFrame
        colName: str of the name of the column to check
    Returns
        True if the column contains all unique values
        False otherwise
    """
    return len(df[colName].unique()) == df[colName].size

# This is because many of the rows in the beginning of our data set didn't have values in the STATE column
def find_empty_columns(df: pd.DataFrame) -> list:
    """Parse data and see which columns are empty"""
    emptyCols = []
    for col in df.columns:
        if(df[col].count() == 0):
            emptyCols.append(col)
    return emptyCols

def check_uniform_col_vals(df: pd.DataFrame, col: str) -> bool:
    return len(df[col].unique()) == 1

# This is because we had two similarly named columns ("ZIP CODE" and "Zip Codes")
def compare_two_colums(df: pd.DataFrame, colName1: str, colName2: str) -> bool:
    """
    Returns:
        True if all of the data in the columns are same
        False otherwise
    """
    redundantData = [val for val in df[colName1] == df[colName2] if val == True]
    return True if len(redundantData) == df[colName1].size else False

# The primary key for our main table will probably be PERMIT NUMBER
#df = load_data("/../data/sidewalk-cafe-permits.csv")
#print(df)