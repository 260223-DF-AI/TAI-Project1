import pandas as pd
import pytest as py
from src.file_reader import load_data, clean_data, is_unique_column, find_empty_columns, compare_two_colums

#Arrange
file = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/small-chunk.csv")

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

    def test_clean_data(self):

        # Act + Assert drop null
        new_file = clean_data(file)
        assert new_file.isnull().sum().sum() == 0

        # Act + Assert drop duplicates
        duplicate_count = (new_file['LEGAL NAME'] == "KITTY O'SHEA'S CHICAGO, LLC").sum()
        assert duplicate_count == 1

        # Act + Assert - dropped columns
        cols_dropped = ["ADDRESS NUMBER START", "ADDRESS NUMBER","STREET DIRECTION", "WARD PRECINCT","LOCATION", "Zip Codes","Boundaries - ZIP Codes", "Census Tracts","Wards"]
        for col in cols_dropped:
            assert col not in new_file.columns

        # Act + Assert to_datetime worked
        new_file["ISSUED DATE"].dtype == "datetime64[ns]"
        new_file["EXPIRATION DATE"].dtype  == "datetime64[ns]"
        new_file["PAYMENT DATE"].dtype == "datetime64[ns]"

    def test_is_unique_column(self):

        #Act and Assert - True
        assert is_unique_column(file, "PERMIT NUMBER") == True

        #Act and Assert - False
        assert is_unique_column(file, "LEGAL NAME") == False

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
        assert compare_two_colums(file, "ZIP CODE", "LEGAL NAME") == False

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



    