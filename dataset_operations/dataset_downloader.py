import os
import urllib.request
from configuration_reader import ConfigurationFileReader
from dataset_operations.dataset_extractor import DatasetExtractor

config_reader = ConfigurationFileReader("config/dataset", "=")
config = config_reader.config
url = config['DATASET_FILE_URL']
DATASET_DIRECTORY_NAME = config['DATASET_DIRECTORY_NAME']
DATASET_TAR_NAME = config['DATASET_TAR_NAME']
DOWNLOAD_PATH = os.path.join(".", DATASET_DIRECTORY_NAME, DATASET_TAR_NAME)


class DatasetDownloader:

    @classmethod
    def action(cls):

        print("Downloading dataset .tar file into: " + DOWNLOAD_PATH)

        if os.path.isfile(DOWNLOAD_PATH):
            print("Removing previous .tar dataset file: ", DOWNLOAD_PATH)
            os.remove(DOWNLOAD_PATH)


        print('Download started...')

        urllib.request.urlretrieve(url, DOWNLOAD_PATH)

        print("File downloaded successfully.")


        cls.next()

    @classmethod
    def next(cls):
        DatasetExtractor.action()
