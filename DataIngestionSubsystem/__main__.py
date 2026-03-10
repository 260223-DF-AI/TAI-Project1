from DataIngestionSubsystem.src import *

def main():
    logger = setup_logger(__name__)
    logger.info("Main started")
    df = load_data("DataIngestionSubsystem/data/small-chunk.csv")
    logger.info("data successfully loaded")
    print(df)
    logger.info("Main completed successfully")

if __name__ == "__main__":
    main()
