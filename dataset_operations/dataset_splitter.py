import os
import shutil
from shutil import copyfile

from configuration_reader import ConfigurationFileReader

config_reader = ConfigurationFileReader("config/dataset", "=")

DATASET_DIRECTORY_NAME = config_reader.config['DATASET_DIRECTORY_NAME']
IMAGES_DIRECTORY_NAME = config_reader.config['IMAGES_DIRECTORY_NAME']
DATASET_SPLITTER_OUTPUT_DIRECTORY = config_reader.config['DATASET_SPLITTER_OUTPUT_DIRECTORY']


class DatasetSplitter:

    @classmethod
    def action(cls):

        if os.path.isdir(os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY)):
            print("Removing previous splitted dataset directory: ", os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY))
            shutil.rmtree(os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY))

        data_dir = os.path.join(DATASET_DIRECTORY_NAME, IMAGES_DIRECTORY_NAME)

        class_names = os.listdir(data_dir)

        output_dir = os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY)
        training_output_dir = output_dir + "\\train"
        training_output_dir = os.path.join(output_dir, "train")
        test_output_dir = output_dir + "\\test"
        test_output_dir = os.path.join(output_dir, "test")

        TRAINING_NUMBER = 0.95
        TEST_NUMBER = 0.05

        if os.path.isdir(output_dir):
            print("Removing previous dataset directory.")
            shutil.rmtree(output_dir)

        print("Creating new dataset directory.")
        os.mkdir(output_dir)
        print("Creating training dataset directory.")
        os.mkdir(training_output_dir)
        print("Creating test dataset directory.")
        os.mkdir(test_output_dir)

        print("Creating train and test classes directories.")
        for dog in class_names:
            os.mkdir(os.path.join(training_output_dir, dog))
            os.mkdir(os.path.join(test_output_dir, dog))

        for directory in os.listdir(data_dir):
            # print(directory)

            number_of_photos = len(os.listdir(data_dir + "\\" + directory))
            number_of_photos = len(os.listdir(os.path.join(data_dir, directory)))


            # print(number_of_photos)

            training_number_of_photos = int(number_of_photos * TRAINING_NUMBER)
            test_number_of_photos = int(number_of_photos * TEST_NUMBER)

            dog_breed = directory

            # print(os.listdir(data_dir + "/" + directory))

            photo_list = os.listdir(data_dir + "\\" + directory)
            photo_list = os.listdir(os.path.join(data_dir, directory))

            for photo in photo_list[:training_number_of_photos]:
                #copyfile(data_dir + "\\" + directory + "\\" + photo, training_output_dir + "\\" + dog_breed + "\\" + photo)
                copyfile(os.path.join(data_dir, directory, photo), os.path.join(training_output_dir, dog_breed, photo))

            for photo in photo_list[training_number_of_photos:]:
                #copyfile(data_dir + "\\" + directory + "\\" + photo, test_output_dir + "\\" + dog_breed + "\\" + photo)
                copyfile(os.path.join(data_dir, directory, photo), os.path.join(test_output_dir, dog_breed, photo))
        print("Done.")

    @classmethod
    def next(cls):
        pass
