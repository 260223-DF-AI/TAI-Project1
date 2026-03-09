import pytest 
import DataIngestionSubsystem.src.file_reader as file_reader

class TestFileReader:

    #Arrange/Act 
    file = file_reader.load_data("/Users/andrewziets/Documents/Revature/TAI-Project1/DataIngestionSubsystem/data/sidewalk-cafe-permits.csv")

    def test_load_data():
        with pytest.raises(FileNotFoundError):
            file_reader.load_data("")

        #Assert 
        assert file != None

    def test_clean_data():
        # Arrange 
        data = {
            'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
            'Age': [25, 30, 25, 35, 30],
            'City': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Los Angeles']
        }
        df = pd.DataFrame(data)
        new_df = file_reader.clean_data(df)
        #Act 
        alice_count = (new_df['Name'] == 'Alice').sum()
        #Assert 
        assert alice_count == 1

        #Assert 
        assert (file["LOCATIONS"] == 0).all()
        assert (file["ADDRESS NUMBER START"] == 0).all()



    