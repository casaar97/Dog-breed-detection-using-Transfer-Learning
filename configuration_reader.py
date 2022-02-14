import os


class ConfigurationFileReader:

    def __init__(self, path="", separator="="):

        if not os.path.isfile(path):
            raise ValueError("The path does not exist.")
        else:
            self.path = path

            self.separator = separator
            self.config = {}

            with open(path) as f:

                for line in f:
                    if separator in line:
                        # Find the name and value by splitting the string
                        name, value = line.split(separator, 1)

                        # Assign key value pair to dict
                        # strip() removes white space from the ends of strings
                        self.config[name.strip()] = value.strip()

    def __str__(self):
        for key, value in self.config:
            print(key, value)
        return
