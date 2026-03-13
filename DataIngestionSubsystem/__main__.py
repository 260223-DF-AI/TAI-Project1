from DataIngestionSubsystem.src import *
from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import Date, Integer, Numeric, String, create_engine
#from psycopg2 import *
import subprocess
import sys

def run_tests():
    print("Running tests...")

    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd="DataIngestionSubsystem"
    )

    if result.returncode != 0:
        print("Tests failed. Aborting program.")
        sys.exit(1)

    print("All tests passed.\n")

def main():
    logger = setup_logger(__name__)
    logger.info("Starting main()")

    # grab all files from data folder, keep only the ones with .csv or .json, and exit if error or no files found
    try:
        data_folder = Path("DataIngestionSubsystem/data")
        files = [f for f in data_folder.iterdir() if f.is_file() and (f.name.endswith(".csv") or f.name.endswith(".json"))]
        if len(files) == 0:
            raise FileNotFoundError
    except:
        logger.error("No valid files found in the data folder. Please upload a file with .csv or .json extension")
        exit()

    # loop until user chooses a file or quits
    while True:
        try:
            for i, file in enumerate(files):
                print(f"{i + 1}. - {file.name}")
        
            print()
            choice = int(input("Please enter the number of the file you would like to process or enter 0 to quit: "))
            
            # quit if choice = 0
            if choice == 0:
                exit()
        
            logger.info(f"{files[choice - 1].name} chosen, please wait while the program attempts to read file and create dataframe")
            
            # create dataframe from given file
            filepath = files[choice - 1].name
            df = load_data(f"DataIngestionSubsystem/data/{filepath}")
            df = clean_data(df)
            print()
            logger.info("Successful file upload and dataframe creation")
            print()
            
            # attempt to connect to database
            logger.info("Attempting to connect to database")
            logger.info("Connection created")

            logger.info("load dotenv successful")
            #CS = os.getenv('CS')    
            #engine = create_engine(CS, echo=True)
            db = Database()
            logger.info("creating and loading businesses table")
            businessDF = create_businesses_df(df)
            db.insert_into_businesses(businessDF)
            # businessDf = df[["ACCOUNT NUMBER", "LEGAL NAME", "DOING BUSINESS AS NAME"]]
            # businessDf.to_sql(name="businesses", con=engine, index=False, if_exists = "replace", dtype={
            #     "ACCOUNT NUMBER": Integer(),
            #     "LEGAL NAME": String(500),
            #     "DOING BUSINESS AS NAME": String(500)})
            logger.info("created and loaded business table")

            logger.info("creating and loading locations table")
            locationDF = create_locations_df(df)
            db.insert_into_locations(locationDF)
            # locationDf = df[["SITE NUMBER", "LATITUDE", "LONGITUDE", "ADDRESS NUMBER", "STREET DIRECTION", "STREET", "STREET TYPE", "ZIP CODE"]]
            # locationDf.to_sql(name="locations", con=engine, index=False, if_exists = "replace", dtype={
            #     "SITE NUMBER": Integer(),
            #     "LATITUDE": Numeric(14,11),
            #     "LONGITUDE": Numeric(14,11),
            #     "ADDRESS NUMBER": String(30),
            #     "STREET DIRECTION": String(1),
            #     "STREET": String(100),
            #     "STREET TYPE": String(30),
            #     "ZIP CODE": String(30)})
            logger.info("created and loaded locations table")

            logger.info("creating and loading permits table")
            permitDF = create_permits_df(df)
            db.insert_into_permits(permitDF)
            # permitDf = df[["PERMIT NUMBER", "ACCOUNT NUMBER", "SITE NUMBER", "ISSUED DATE", "EXPIRATION DATE", "PAYMENT DATE"]]
            # permitDf.to_sql(name="permits", con=engine, index=False, if_exists = "replace", dtype={
            #     "PERMIT NUMBER": Integer(),
            #     "ACCOUNT NUM": Integer(),
            #     "SITE NUMBER": Integer(),
            #     "ISSUED DATE": Date(),
            #     "EXPIRATION DATE": Date(),
            #     "PAYMENT DATE": Date()})
            logger.info("created and loaded permits table")

            db.commit_changes()
            
            logger.info("Successfully created and populated 3 tables")
            logger.info("Exiting")
            exit()

        # except if user enters invalid choice
        except Exception as e:
            print(e)
            print(type(e).__name__)
    # df = load_data("DataIngestionSubsystem/data/small-chunk.csv")
    # logger.info("data successfully loaded")
    # print(df)

    

if __name__ == "__main__":
    run_tests()
    main()
