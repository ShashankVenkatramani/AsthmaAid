# Make a CNN
# Train this CNN on every image from a specifier folder
# Use the value at the end of the image name (0 or 1) to determine it's value
# Return this CNN

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
import numpy as np
import pandas as pd
import os
import cv2
from sklearn.model_selection import train_test_split
np.random.seed(7)

class CNN:
    def __init__(self, dataFolder):
        self.data = dataFolder

    def constructModel(self):
        # Getting all the images and corresponding values from the specified folder
        images = [] # X
        values = [] # Y
        for filename in os.listdir(self.data):
            img = cv2.imread(os.path.join(self.data,filename))
            if img is not None:
                images.append(img)
                values.append(int(filename.split("_")[1][:1]))


        self.model = Sequential()
        X_train, X_test, y_train, y_test =train_test_split(images, values, test_size = 0.2, random_state = 42)
        


    #def returnModel(self):
        # Return self.model

cnn = CNN("output")
cnn.constructModel()
