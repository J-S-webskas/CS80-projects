import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Dense, Flatten

from sklearn.model_selection import train_test_split

# This version is accepted by the autograder

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images, labels = [], []

    # Get 0~NUM_CATEGORIES-1
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        for image in os.listdir(category_path):

            # Full path of image
            image_path = os.path.join(category_path, image)

            # imread reads an image using full path, resize to (IMG_WIDTH, IMG_HEIGHT)
            images.append(cv2.resize(cv2.imread(image_path), (IMG_WIDTH, IMG_HEIGHT)))

            # Read labels
            labels.append(category)

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolution layer. Learn 32 filters using a 3x3 kernel
        Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),

        # 2nd Convolution layer: learn 64 filters using 3x3 kernel
        Conv2D(64, (3, 3), activation="relu"),
        Conv2D(64, (3, 3), activation="relu"),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.3),

        # Flatten units
        Flatten(),

        # Add a hiddden laer with dropout
        Dense(256, activation ="relu"),
        BatchNormalization(),        
        Dropout(0.3),

        # Add an output layer with output units for NUM_CATEGORIES units
        Dense(NUM_CATEGORIES, activation="softmax")
    ])
    return model

if __name__ == "__main__":
    main()
