from DataIngestionSubsystem.src import *
from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import Date, Integer, Numeric, String, create_engine
#from psycopg2 import *

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
            load_dotenv()
            CS = os.getenv('CS')
            logger.info("Connection created")
            engine = create_engine(CS, echo=False)

            logger.info("Creating and populating 'businesses' table")
            businessDf = df[["ACCOUNT NUMBER", "LEGAL NAME", "DOING BUSINESS AS NAME"]]
            businessDf.to_sql(name="businesses", con=engine, index=False, if_exists = "replace", dtype={
                "ACCOUNT NUMBER": Integer,
                "LEGAL NAME": String,
                "DOING BUSINESS AS NAME": String})
            logger.info("Successful table creation and population for 'businesses'")
            
            logger.info("Creating and populating 'locations' table")
            locationDf = df[["SITE NUMBER", "LATITUDE", "LONGITUDE", "ADDRESS NUMBER", "STREET DIRECTION", "STREET", "STREET TYPE", "ZIP CODE"]]
            locationDf.to_sql(name="locations", con=engine, index=False, if_exists = "replace", dtype={
                "SITE NUMBER": Integer,
                "LATITUDE": Numeric,
                "LONGITUDE": Numeric,
                "ADDRESS NUMBER": String,
                "STREET DIRECTION": String,
                "STREET": String,
                "STREET TYPE": String,
                "ZIP CODE": String})
            logger.info("Successful table creation and population for 'locations'")
            
            logger.info("Creating and populating 'permits' table")
            permitDf = df[["PERMIT NUMBER", "ACCOUNT NUMBER", "SITE NUMBER", "ISSUED DATE", "EXPIRATION DATE", "PAYMENT DATE"]]
            permitDf.to_sql(name="permits", con=engine, index=False, if_exists = "replace", dtype={
                "PERMIT NUMBER": Integer,
                "ACCOUNT NUMBER": Integer,
                "SITE NUMBER": Integer,
                "ISSUED DATE": Date,
                "EXPIRATION DATE": Date,
                "PAYMENT DATE": Date})
            logger.info("Successful table creation and population for 'permits'")

            Base.metadata.create_all(engine)
            
            logger.info("Successfully created and populated 3 tables")
            logger.info("Exiting")
            exit()

        # except if user enters invalid choice
        except Exception as e:
            print(e)
            print(f"Please enter an integer between 1 and {len(files)}")
    

if __name__ == "__main__":
    main()
