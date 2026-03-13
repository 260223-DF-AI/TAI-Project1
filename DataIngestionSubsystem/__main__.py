from DataIngestionSubsystem.src import *
from pathlib import Path
from dotenv import load_dotenv
import os
#from sqlalchemy import Date, Integer, Numeric, String, create_engine
#from psycopg2 import *

def main():
    logger = setup_logger(__name__)
    logger.info("Starting main()")
    print()

    # grab all files from data folder, keep only the ones with .csv or .json, and exit if error or no files found
    data_folder = Path("DataIngestionSubsystem/data")
    files = [f for f in data_folder.iterdir() if f.is_file() and (f.name.endswith(".csv") or f.name.endswith(".json"))]

    if len(files) == 0:
        logger.error("No valid files found in the data folder. Please upload a file with .csv or .json extension")
        exit()
        

    # loop until user chooses a file or quits
    while True:
        try:
            for i, file in enumerate(files):
                print(f"{i + 1}. - {file.name}")
        
            print()
            choice = int(input("Please enter the number of the file you would like to process or enter 0 to quit: "))
            print()
            # quit if choice = 0
            if choice == 0:
                exit()
        
            logger.info(f"{files[choice - 1].name} chosen, please wait while the program attempts to read file and create dataframe")
            
            # if user chose a file with incorrect format, it will be ignored on the next run through
            filepath = files[choice - 1].name

            # create dataframe from given file
            df = load_data(f"DataIngestionSubsystem/data/{filepath}")
            df = clean_data(df)
            print()
            logger.info("Successful file upload and dataframe creation")
            print()
            
            # attempt to connect to database
            logger.info("Attempting to connect to database")
            db = Database()
            logger.info("Connection created, tables created")

            logger.info("Attempting to create dataframe and load 'business' table")
            businessDF = create_businesses_df(df)
            db.insert_into_businesses(businessDF)
            logger.info("Loaded 'business' table with dataframe")

            logger.info("Attempting to create dataframe and load 'locations' table")
            locationDF = create_locations_df(df)
            db.insert_into_locations(locationDF)
            logger.info("Loaded 'locations' table with dataframe")

            logger.info("Attempting to create dataframe and load 'permits' table")
            permitDF = create_permits_df(df)
            db.insert_into_permits(permitDF)
            logger.info("Loaded 'permits' table with dataframe")

            #db.commit_changes()
            
            logger.info("Successfully created and populated 3 tables")
            logger.info("Exiting")
            exit()

        # except if user enters invalid choice
        except ValueError as e:
            logger.error(f"{filepath} is not in the correct format")
            print()
            files.remove(files[choice - 1])
            print("Choose a new file:")
        except Exception as e:
            print(e)
            print(type(e).__name__)

if __name__ == "__main__":
    main()
