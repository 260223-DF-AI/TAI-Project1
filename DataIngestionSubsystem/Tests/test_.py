import pandas as pd
import pytest 
from src.file_reader import load_data, clean_data, is_unique_column, find_empty_columns, compare_two_colums

class TestFileReader:

    #Arrange/Act 
    file = load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/sidewalk-cafe-permits.csv")

    def test_load_data(self):
        with pytest.raises(FileNotFoundError):
            load_data("")

        #Assert 
        assert file != None

    def test_clean_data(self):
        # Duplicates Check

        # Arrange 
        data = {
            'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
            'Age': [25, 30, 25, 35, 30],
            'City': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles']
        }
        df = pd.DataFrame(data)
        new_df = clean_data(df)
        #Act 
        alice_count = (new_df['Name'] == 'Alice').sum()
        #Assert 
        assert alice_count == 1

        #Assert - drop LOCATIONS and ADDRESS NUMBER
        assert (file["LOCATIONS"] == 0).all()
        assert (file["ADDRESS NUMBER START"] == 0).all()

        #




    