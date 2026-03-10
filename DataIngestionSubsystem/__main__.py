from DataIngestionSubsystem.src import *

def main():
    print("starting")
    logger = setup_logger(__name__)
    logger.info("Main started")

    logger.info("Main completed successfully")
    print("ending")
if __name__ == "__main__":
    main()

# main()