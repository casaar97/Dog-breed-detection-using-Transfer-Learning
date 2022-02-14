import os
import shutil
import tarfile

from configuration_reader import ConfigurationFileReader
from dataset_operations.dataset_splitter import DatasetSplitter

config_reader = ConfigurationFileReader("config/dataset", "=")

config = config_reader.config

DATASET_DIRECTORY_NAME = config['DATASET_DIRECTORY_NAME']
DATASET_TAR_NAME = config['DATASET_TAR_NAME']
IMAGES_DIRECTORY_NAME = config['IMAGES_DIRECTORY_NAME']
TAR_PATH = os.path.join(DATASET_DIRECTORY_NAME, DATASET_TAR_NAME)
IMAGES_DIRECTORY_PATH = os.path.join(DATASET_DIRECTORY_NAME, IMAGES_DIRECTORY_NAME)


class DatasetExtractor:

    @classmethod
    def action(cls):
        print("Extracting " + TAR_PATH + " into: " + IMAGES_DIRECTORY_PATH)

        if os.path.isdir(IMAGES_DIRECTORY_PATH):
            print("Removing previous dataset directory: ", IMAGES_DIRECTORY_PATH)
            shutil.rmtree(IMAGES_DIRECTORY_PATH)

        my_tar = tarfile.open(TAR_PATH)
        my_tar.extractall(DATASET_DIRECTORY_NAME)  # specify which folder to extract to
        my_tar.close()

        print("Extraction completed.")

        cls.next()

    @classmethod
    def next(cls):
        DatasetSplitter().action()
