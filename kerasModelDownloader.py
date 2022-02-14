import os

from tensorflow import keras

from configuration_reader import ConfigurationFileReader
from dataset_operations.dataset_downloader import DatasetDownloader
from tensorflow.keras.preprocessing.image import ImageDataGenerator

dataset_config_reader = ConfigurationFileReader("config/dataset", "=")
dataset_config = dataset_config_reader.config

DATASET_DIRECTORY_NAME = dataset_config['DATASET_DIRECTORY_NAME']
DATASET_SPLITTER_OUTPUT_DIRECTORY = dataset_config['DATASET_SPLITTER_OUTPUT_DIRECTORY']

models_config_reader = ConfigurationFileReader("config/models", "=")
model_config = models_config_reader.config

VGG16_MODEL_PATH = model_config['VGG16_MODEL_PATH']

if not os.path.isdir("dataset"):
    os.mkdir("dataset")

DatasetDownloader.action()

base_model = keras.applications.VGG16(
    weights='imagenet',
    input_shape=(224, 224, 3),
    include_top=False)

# Freeze base model
base_model.trainable = False

# Create inputs with correct shape
inputs = keras.Input(shape=(224, 224, 3))

x = base_model(inputs, training=False)

# Add pooling layer or flatten layer
x = keras.layers.GlobalAveragePooling2D()(x)

# Add final dense layer
outputs = keras.layers.Dense(120, activation='softmax')(x)

# Combine inputs and outputs to create model
model = keras.Model(inputs, outputs)

model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

datagen = ImageDataGenerator(samplewise_center=True,  # set each sample mean to 0
                             rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
                             zoom_range=0.1,  # Randomly zoom image
                             width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
                             height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
                             horizontal_flip=True,  # randomly flip images
                             vertical_flip=False)

# load and iterate training dataset
train_it = datagen.flow_from_directory(os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY, 'train'),
                                       target_size=(224, 224),
                                       color_mode='rgb',
                                       class_mode="categorical")
# load and iterate validation dataset
valid_it = datagen.flow_from_directory(os.path.join(DATASET_DIRECTORY_NAME, DATASET_SPLITTER_OUTPUT_DIRECTORY, 'test'),
                                       target_size=(224, 224),
                                       color_mode='rgb',
                                       class_mode="categorical")

model.fit(train_it,
          validation_data=valid_it,
          steps_per_epoch=train_it.samples / train_it.batch_size,
          validation_steps=valid_it.samples / valid_it.batch_size,
          epochs=10)

# Unfreeze the base model
base_model.trainable = True

# Compile the model with a low learning rate
model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=.00001),
              loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_it,
          validation_data=valid_it,
          steps_per_epoch=train_it.samples / train_it.batch_size,
          validation_steps=valid_it.samples / valid_it.batch_size,
          epochs=10)

model.evaluate(valid_it, steps=valid_it.samples / valid_it.batch_size)