import pandas as pd
#from .logger import *

def load_data(filepath):
    """
    Creates a DataFrame object from the given file, cleans it, then returns it
    """
    df = pd.DataFrame()
    dotIndex = filepath.rfind('.')
    try:
        if(filepath[dotIndex + 1:].lower() == 'csv'):
            df = pd.read_csv(
                filepath,
                dtype={
                    "ZIP CODE": "string",
                    "ADDRESS NUMBER": "string"
                },
                date_format = "%Y-%m-%dT%H:%M:%S.%f",
                parse_dates=['ISSUED DATE', 'EXPIRATION DATE', 'PAYMENT DATE']
            )
        elif(filepath[dotIndex + 1:].lower() == 'json'):
            # Read JSON file
            df = pd.read_json(
                filepath,
                dtype={
                    "ZIP CODE": "string",
                    "ADDRESS NUMBER": "string"
                }
            )
            # Parse dates after reading
            date_cols = ['ISSUED DATE', 'EXPIRATION DATE', 'PAYMENT DATE']
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], format="%Y-%m-%dT%H:%M:%S.%f", errors='coerce')
    except FileNotFoundError:
        # Eventually we will probably also want to log this
        print(f"Given filepath ({filepath}) does not exist.")
    # df_validated, df_invalid = validate_normalize_data(df)
    return df

def validate_normalize_data(df):

    # Ensure numeric columns
    number_cols = ['PERMIT NUMBER', 'ACCOUNT NUMBER', 'SITE NUMBER',
                   'LATITUDE', 'LONGITUDE']

    df[number_cols] = df[number_cols].apply(pd.to_numeric, errors='coerce')

    # a Series of booleans which states whether all of the following statements are True
    valid_mask = (
        (df['PERMIT NUMBER'] > 0) &
        (df['ACCOUNT NUMBER'] > 0) &
        (df['SITE NUMBER'] > 0)
    )

    df_validated = df[valid_mask].copy().reset_index(drop=True)
    df_invalid = df[~valid_mask].copy().reset_index(drop=True)
    return df_validated, df_invalid

def clean_data(df: pd.DataFrame):
   
    # if city is chicago but no state is present, fill in with IL
    df.loc[df["CITY"] == "CHICAGO", "STATE"] = "IL"

    # Handle rows with None values/missing data: Drop row
    df.dropna(inplace=True)

    # Handle duplicate data
    df.drop_duplicates(inplace=True)

    # drop LOCATION and ADDRESS NUMBER START columns
    df.drop(columns=["ADDRESS NUMBER START", "WARD PRECINCT","LOCATION", "Zip Codes","Boundaries - ZIP Codes", "Census Tracts","Wards"], inplace=True)

    # remove time part from date (example: 2019-11-25T00:00:00.000 becomes just 2019-11-25)
    df["ISSUED DATE"] = pd.to_datetime(df["ISSUED DATE"]).dt.date
    df["EXPIRATION DATE"] = pd.to_datetime(df["EXPIRATION DATE"]).dt.date
    df["PAYMENT DATE"] = pd.to_datetime(df["PAYMENT DATE"]).dt.date

    # Standardize text columns
    strCols = [col for col in df.columns if df[col].dtype == 'str'] # not sure how necessary this line is
    df[strCols] = df[strCols].apply(lambda col: col.str.upper())

    # Renaming columns for the database
    df.rename(columns={
        'PERMIT NUMBER': 'permit_num',
        'ACCOUNT NUMBER': 'account_num',
        'SITE NUMBER': 'site_num',
        'LEGAL NAME': 'legal_name',
        'DOING BUSINESS AS NAME': 'opper_name',
        'ISSUED DATE': 'issued_date',
        'EXPIRATION DATE': 'expiration_date',
        'PAYMENT DATE': 'payment_date',
        'ADDRESS NUMBER': 'address_num',
        'STREET DIRECTION': 'street_dir',
        'STREET': 'street',
        'STREET TYPE': 'street_type',
        'ZIP CODE': 'zipcode',
        'LATITUDE': 'latitude',
        'LONGITUDE': 'longitude'
    }, inplace=True)

    return df

def create_businesses_df(df: pd.DataFrame):
    busDF = df.copy()
    return busDF[['account_num','legal_name']].drop_duplicates()

def create_locations_df(df: pd.DataFrame):
    locDf = df.copy()
    locDf = locDf[['site_num', 'address_num', 'street_dir', 'street', 'street_type', 'zipcode', 'latitude', 'longitude']].drop_duplicates()
    locDf['loc_id'] = [indx for indx, row in locDf.iterrows()]
    return locDf

def create_permits_df(df: pd.DataFrame, locDf: pd.DataFrame):
    location_cols = [
        'site_num',
        'address_num',
        'street_dir',
        'street',
        'street_type',
        'zipcode',
        'latitude',
        'longitude'
    ]
    df = df.merge(
        locDf,
        on=location_cols,
        how="left"
    )
    permDf = df.copy()
    return permDf[['permit_num', 'account_num', 'loc_id', 'opper_name', 'issued_date', 'expiration_date', 'payment_date']]

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
#df = load_data("../data/small-chunk.csv")
#print(df["EXPIRATION DATE"])