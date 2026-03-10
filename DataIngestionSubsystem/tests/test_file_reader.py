import pandas as pd
import pytest as py
from src.file_reader import load_data, clean_data, is_unique_column, find_empty_columns, compare_two_colums

#Arrange
file = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/sidewalk-cafe-permits.csv")

class TestFileReader:
    
    def test_load_data(self):
        #Act + Assert 
        assert not file.empty

    def test_clean_data(self):
        # Act + Assert drop null
        assert file.isnull().sum().sum() == 0

        #Act + Assert duplicates
        duplicate_count = (file['LEGAL NAME'] == "KITTY O'SHEA'S CHICAGO, LLC").sum()
        assert duplicate_count == 1

        #Assert - drop LOCATIONS and ADDRESS NUMBER
        for col in ["LOCATION", "ADDRESS NUMBER START"]:
            assert col not in file.columns

    def test_is_unique_column(self):
        pass

    def test_find_empty_columns(self):
        pass

    def test_compare_two_colums(self):
        pass



    