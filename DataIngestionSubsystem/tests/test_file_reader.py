import pandas as pd
import pytest as pyt
from src.file_reader import load_data, clean_data, is_unique_column, find_empty_columns, compare_two_colums, validate_normalize_data
from pathlib import Path
#Arrange
# file = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/small-chunk.csv")
# df_validation = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/testing_files/validation_testing.csv")
# unclean_file = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/testing_files/test_clean.csv")
# json_test = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/testing_files/file.json")

# file_path = Path(__file__).resolve().parent.parent / "data" / "testing_files" / "small-chunk.csv"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "testing_files"
SMALL_DIR = BASE_DIR / "data"

file = load_data(str(SMALL_DIR / "small-chunk.csv"))
df_validation = load_data(str(DATA_DIR / "validation_testing.csv"))
unclean_file = load_data(str(DATA_DIR / "test_clean.csv"))
json_test = load_data(str(DATA_DIR / "file.json"))

class TestFileReader:
    
    def test_load_data(self):

        # Act + Assert 
        assert not file.empty

        # Arrange
        columns = [
            "PERMIT NUMBER", "ACCOUNT NUMBER", "SITE NUMBER", "LEGAL NAME", "DOING BUSINESS AS NAME", "ISSUED DATE", "EXPIRATION DATE",
            "PAYMENT DATE", "ADDRESS", "ADDRESS NUMBER START", "ADDRESS NUMBER", "STREET DIRECTION", "STREET", "STREET TYPE", "CITY",
            "STATE", "ZIP CODE", "WARD", "PRECINCT", "WARD PRECINCT", "POLICE DISTRICT", "LATITUDE", "LONGITUDE", "LOCATION",
            "Community Areas", "Zip Codes","Boundaries - ZIP Codes", "Census Tracts", "Wards"
        ]

        # Act + Assert correct file
        assert list(file.columns) == columns
        assert list(json_test.columns) == columns
    
    def test_validation(self): 

        df_valid, df_invalid = validate_normalize_data(df_validation)

        expected_valid = load_data(str(DATA_DIR  / "valid.csv"))
        expected_invalid = load_data(str(DATA_DIR / "invalid.csv"))

        pd.testing.assert_frame_equal(expected_valid, df_valid)
        pd.testing.assert_frame_equal(expected_invalid, df_invalid)

        df_valid_full, df_invalid_empty = validate_normalize_data(df_valid)
        pd.testing.assert_frame_equal(df_valid_full, df_valid)
        # Create an empty DataFrame with the same columns and dtypes
        empty_invalid = pd.DataFrame({col: pd.Series(dtype=df_invalid_empty[col].dtype) 
                                    for col in df_invalid_empty.columns})
        # Now the dtypes match
        pd.testing.assert_frame_equal(df_invalid_empty, empty_invalid)

    def test_clean_data(self):

        # Act + Assert drop null
        new_file = clean_data(file)
        assert new_file.isnull().sum().sum() == 0

        # Act + Assert drop duplicates
        duplicate_count = (file['legal_name'] == "KITTY O'SHEA'S CHICAGO, LLC").sum()
        assert duplicate_count == 1

        # Act + Assert - dropped columns
        cols_dropped = ["ADDRESS NUMBER START", "ADDRESS NUMBER","STREET DIRECTION", "WARD PRECINCT","LOCATION", "Zip Codes","Boundaries - ZIP Codes", "Census Tracts","Wards"]
        for col in cols_dropped:
            assert col not in new_file.columns

        # Act + Assert to_datetime worked
        new_file["issued_date"].dtype == "datetime64[ns]"
        new_file["expiration_date"].dtype  == "datetime64[ns]"
        new_file["payment_date"].dtype == "datetime64[ns]"

        # Act + Assert Chicago Illinois
        for index, row in new_file.iterrows():
            if row["CITY"] == "CHICAGO":
                assert row["STATE"] == "IL"

        # Testing loc_id was created correctly
        # assert not new_file["loc_id"].empty

    def test_is_unique_column(self):

        #Act and Assert - True
        assert is_unique_column(file, "permit_num") == True

        #Act and Assert - False
        assert is_unique_column(file, "legal_name") == False

    def test_find_empty_columns(self):

        # Arrange for multiple empty field
        data_empty = {
            "ID": [1,2,3,4,5],
            "Name": [None,None,None,None,None],
            "Email": [None,None,None,None,None],
            "Age": [None,None,None,None,None],
            "City": [None,None,None,None,None]
        }
        empty_df = pd.DataFrame(data_empty)

        # Arrange for multiple one empty field
        data = {
            "ID": [1,2,3,4,5],
            "Name": ["Alice", None, None, None, None],
            "Email": [None,"The", None, None, None],
            "Age": [None,None,"The",None,None],
            "City": [None,None,None,None,None]
        }
        df_one_empty = pd.DataFrame(data)

        # Act + Assert for multiple empty fields
        assert find_empty_columns(empty_df) == ["Name", "Email", "Age", "City"]

        #Act + Assert for one empty fields
        assert find_empty_columns(df_one_empty) == ["City"]

        # Act + Assert for no empty field
        assert find_empty_columns(file) == []

    def test_compare_two_colums(self):

        # Act + Assert case of non-similar columns
        assert compare_two_colums(file, "zipcode", "legal_name") == False

        # Arrange for identical columns
        data_truth = {
            "ID": [1,2,3,4,5],
            "Name": ["John", "Emma", "Liam", "Olivia", "Noah"],
            "First_Name": ["John", "Emma", "Liam", "Olivia", "Noah"],  # same as Name
            "Email": [
                "john@example.com",
                "emma@example.com",
                "liam@example.com",
                "olivia@example.com",
                "noah@example.com"
            ],
            "Age": [28, 34, 25, 31, 29],
            "City": ["Chicago", "New York", "San Francisco", "Austin", "Seattle"]
        }

        # Act + Assert case of identical columns 
        df_truth= pd.DataFrame(data_truth)
        assert compare_two_colums(df_truth, "Name", "First_Name") == True



    