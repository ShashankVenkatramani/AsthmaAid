from datafileToImg import dataToDf, getOutliers
import os

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

class NN:
    def __init__(self):
        np.set_printoptions(threshold=np.nan)
        print("New Neural Network")

    def setInputDirectory(self, input):
        self.input = os.path.join(os.getcwd(), input)
        print("Set input directory to " + str(self.input))

    def collectData(self):
        print("Collecting data, saving")
        # Get all the inputs
        X = []
        Y = []
        csv = pd.read_csv(self.input)
        num = csv.shape[0]
        # For every input csv file in the input file
        for i in range (0, num):
            currFile = csv.iloc[i, 0]
            hasAsthma = csv.iloc[i,1]
            # Get the csv file associated with the file
            df = dataToDf(currFile, " ")
            x = df.iloc[0,:].values
            x = getOutliers(x)
            if x.size == 0: # Making sure no empty inputs for training
                x = np.asarray([])#.reshape(x.shape[1]))

            X.append(x)
            Y.append(hasAsthma)

        self.x = np.asarray(X)
        self.y = np.asarray(Y)

    def constructMLP(self, hidden = (14, 10, 6), iters = 1000):
        print("Constructing a Multi-Layer Perceptron")
        # CHANGE THE RATIO FOR TEST_SIZE TO SOMETHING IF TRAINING PLUS OPTIMIZATION
        X_train, X_test, y_train, y_test =train_test_split(self.x, self.y, test_size = 0, random_state = 42)
        self.y_test = y_test # Only saving the variable we need - y_test for evaluations
        mlp = MLPClassifier(hidden_layer_sizes = hidden, max_iter=iters)
        # 3 layers, one of 14 nodes, one of 10 nodes, one of 6 nodes
        mlp.fit(X_train, y_train)
        self.model = mlp

    def constructDTC(self):
        print("Constructing a Decision-Tree classifier")
        # CHANGE THE RATIO FOR TEST_SIZE TO SOMETHING IF TRAINING PLUS OPTIMIZATION
        X_train, X_test, y_train, y_test =train_test_split(self.x, self.y, test_size = 0, random_state = 42)
        self.y_test = y_test # Only saving the variable we need - y_test for evaluations
        DTC = DecisionTreeClassifier()

        DTC.fit(X_train, y_train)
        self.model = DTC

    def constructKNN(self):
        print("Constructing a K-Neighbors Classifier")
        # CHANGE THE RATIO FOR TEST_SIZE TO SOMETHING IF TRAINING PLUS OPTIMIZATION
        X_train, X_test, y_train, y_test =train_test_split(self.x, self.y, test_size = 0, random_state = 42)
        self.y_test = y_test
        classifier = KNeighborsClassifier(n_neighbors=5)

        X_train = X_train.reshape((-1,1))
        y_train = y_train.reshape((-1,1))

        print("X_train shape : " + str(X_train.reshape((-1,1)).shape))
        print("y_train shape : " + str(y_train.shape))
        
        classifier.fit(X_train, y_train)
        self.model = classifier


    # INSANELY BUGGY, SVC'S HAVE SOME GARBAGE ARCHITECTURE TO USE AND PLAY with
    # SCREW IT DTC's AND KNN's ARE BETTER ANYWAY
    def constructSVC(self, kernel = 'rbf', degree = 3): # Default value is the best kernel
        # Kernels = 'linear', 'poly', 'rbf','sigmoid'
        print("Constructing a Support Vector Machine")
        # CHANGE THE RATIO FOR TEST_SIZE TO SOMETHING IF TRAINING PLUS OPTIMIZATION
        X_train, X_test, y_train, y_test =train_test_split(self.x, self.y, test_size = 0, random_state = 42)
        self.y_test = y_test # Only saving the variable we need - y_test for evaluations

        max(X_train, key=lambda coll: len(coll))
        largest = max(X_train, key=len)
        print(largest.shape[0])

        self.largest = largest

        new_X_train = []
        for te in X_train:
            arr = np.asarray(te)
            if not arr.shape[0] == largest.shape[0]:
                print(arr)
                if (arr.shape[0] == 0):
                    arr = np.zeros((3))
                else:
                    arr = np.pad(arr, (0, largest - arr.shape[0]), 'constant', constant_values = (0,0))
            new_X_train.append(arr)

        if (kernel == 'poly'):
            SVM = SVC(kernel = 'poly', degree = degree)
        else:
            SVM = SVC(kernel = kernel)

        new_X_train = np.asarray(new_X_train)
        SVM.fit(new_X_train, y_train)
        self.model = SVM

    def makePredictions(self, data):
        print("Predicting")
        data = getOutliers(data)
        np.trim_zeros(data)
        #print("The data post trimming is: " + str(data))

        """ Include bottom section if using SVC's cuz they're STUPID """
        #
        # if data.size == 0: # No outliers? No asthma attack
        #     self.predictions = 0
        # else:
        #     if (data.shape[0] == 0):
        #         data = np.zeros((3))
        #     else:
        #         data = np.pad(data, (0, self.largest.shape[0] - data.shape[0]), 'constant', constant_values = (0,0))
        #
        #     data = np.reshape(data, (data.size, 1))
        #     predictionsnew = self.model.predict(data)
        #     self.predictions = predictionsnew

        """ Remove this bottom section if using SVC's cuz they're STUPID """
        if data.size == 0:
             self.predictions = 0
        else:
            data = np.reshape(data, (data.size, 1))
            predictionsnew = self.model.predict(data)
            self.predictions = predictionsnew

    # Only used for optimization of model
    def evaluatePredictions(self):
        print("Evaluating")
        print("Test: " + str(self.y_test))
        print("Predictions: " + str(self.predictions))
        print(confusion_matrix(self.y_test, self.predictions))
        print(classification_report(self.y_test, self.predictions))

    def getPredictions(self):
        return self.predictions

    def returnModel(self):
        return self.model

def main():
    nn = NN()
    nn.setInputDirectory("data\\allInputs.txt")
    nn.collectData()
    nn.constructKNN() # linear, poly, rbf, sigmoid
    testInput = np.array([6, 10, 13, 15, 18, 37, 21, 13, 14, 11, 9, 12]).reshape(1,-1)
    nn.makePredictions(testInput)
    print("Predictions for the data are: " + str(nn.getPredictions()))

if __name__ == "__main__":
    main()
