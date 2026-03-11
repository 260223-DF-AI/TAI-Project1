from DataIngestionSubsystem.src import *
from pathlib import Path

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
            filepath = files[choice - 1].name
            df = load_data(f"DataIngestionSubsystem/data/{filepath}")
            print()
            logger.info("Successful file upload and dataframe creation!")
            print()
            print(df)
            exit()
        except Exception as e:
            print()
            print(f"Please enter an integer between 1 and {len(files)}")
    # df = load_data("DataIngestionSubsystem/data/small-chunk.csv")
    # logger.info("data successfully loaded")
    # print(df)
    

if __name__ == "__main__":
    main()
