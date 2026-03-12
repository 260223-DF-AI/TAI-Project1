from DataIngestionSubsystem.src import *
from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, create_engine

def main():
    logger = setup_logger(__name__)
    logger.info("Starting main()")

    try:
        data_folder = Path("DataIngestionSubsystem/data")
        files = [f for f in data_folder.iterdir() if f.is_file() and (f.name.endswith(".csv") or f.name.endswith(".json"))]
        
    except:
        logger.error("No valid files found in the data folder. Please upload a file with .csv or .json extension")
        exit()
    while True:
        try:
            for i, file in enumerate(files):
                print(f"{i + 1}. - {file.name}")
            print()
            choice = int(input("Please enter the number of the file you would like to process or enter 0 to quit: "))
            if choice == 0:
                exit()
            print(files[choice - 1].name)
            filepath = files[choice - 1].name
            df = load_data(f"DataIngestionSubsystem/data/{filepath}")
            df = clean_data(df)
            print()
            logger.info("Successful file upload and dataframe creation")
            print()
            logger.info("Attempting to make tables")
            load_dotenv()
            logger.info("load dotenv successful")
            CS = os.getenv('CS')    
            engine = create_engine(CS, echo=True)
            logger.info("creating and loading businesses table")
            businessDf = df[["ACCOUNT NUMBER", "LEGAL NAME", "DOING BUSINESS AS NAME"]]
            businessDf.to_sql(name="businesses", con=engine, index=False, if_exists = "replace", dtype={
                "ACCOUNT NUMBER": Integer(),
                "LEGAL NAME": String(500),
                "DOING BUSINESS AS NAME": String(500)})
            logger.info("created and loaded business table")

            logger.info("creating and loading locations table")
            locationDf = df[["SITE NUMBER", "LATITUDE", "LONGITUDE", "ADDRESS NUMBER", "STREET DIRECTION", "STREET", "STREET TYPE", "ZIP CODE"]]
            locationDf.to_sql(name="locations", con=engine, index=False, if_exists = "replace", dtype={
                "SITE NUMBER": Integer(),
                "LATITUDE": Numeric(14,11),
                "LONGITUDE": Numeric(14,11),
                "ADDRESS NUMBER": String(30),
                "STREET DIRECTION": String(1),
                "STREET": String(100),
                "STREET TYPE": String(30),
                "ZIP CODE": String(30)})
            logger.info("created and loaded locations table")

            logger.info("creating and loading permits table")
            permitDf = df[["PERMIT NUMBER", "ACCOUNT NUMBER", "SITE NUMBER", "ISSUED DATE", "EXPIRATION DATE", "PAYMENT DATE"]]
            permitDf.to_sql(name="permits", con=engine, index=False, if_exists = "replace", dtype={
                "PERMIT NUMBER": Integer(),
                "ACCOUNT NUM": Integer(),
                "SITE NUMBER": Integer(),
                "ISSUED DATE": Date(),
                "EXPIRATION DATE": Date(),
                "PAYMENT DATE": Date()})
            logger.info("created and loaded permits table")

            Base.metadata.create_all(engine)
            
            logger.info("Success! Tables created!")
            exit()
        except Exception as e:
            print(e)
            print(f"Please enter an integer between 1 and {len(files)}")
    # df = load_data("DataIngestionSubsystem/data/small-chunk.csv")
    # logger.info("data successfully loaded")
    # print(df)
    

if __name__ == "__main__":
    main()
