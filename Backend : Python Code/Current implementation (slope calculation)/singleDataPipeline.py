import os
import pandas as pd

from scipy.optimize import leastsq
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

# Helper function files
from filter import *
from generalUtil import *
from plots import *
from cleaning import *
from anomalyClassifier import *

def pipeline(parameters):
    # get parameters
    csvFileName = parameters["csv"]
    outputFolderName = parameters["output"]
    graphShapeGeneral = parameters["graph_shape"]
    skipFactorForCalculatingSlopes = parameters["skip"]
    testDataIter = parameters["iter"]
    size = parameters["size"]

    # Read the csvFileName
    data = dataToDf(csvFileName, delimiter = ",")
    data.columns = data.iloc[0]
    data = data.drop([0])
    # Create general output folder
    createOutputFolder("output")
    createOutputFolder(outputFolderName)

    # Get the useful data starting point
    data = data.astype(float)
    beginningOfUsefulData = getIrrelevantData(data["resistance"])
    # Initial cleaning of the data
    removeSimilarValues(data, beginningOfUsefulData)
    removeNullValues(data, beginningOfUsefulData)

    # Edit interesting points list through top down approach
    interest = calculateSlopes(data, skipFactorForCalculatingSlopes, size)["interest"]
    print(interest.size)
    interest = removeLocalMaxMin(data, interest)["pois"]
    print(interest.size)
    interest = removeTopValues(data, interest)["pois"]
    print(interest.size)
    interest = removeVeryCloseInterestingPoints(interest)



    # Plot the overall data
    dataToImg(data[["ms"]].values, data[["resistance"]].values, outputFolderName + "\\general", "overall_iter_" + str(testDataIter), interest, graphShapeGeneral)

    # Get the segments and plot them
    segments = splitDataIntoSegments(data, interest)
    plotAndSaveSegments(segments, outputFolderName + "\\segments", (10, 5), testDataIter)

    xx = anomalyDetector(segments)
    overall = xx["overall"]
    all = xx["all"]
    return {"overall_anomaly":overall, "all_anomalies":all, "segments":segments, "interestingPoints":interest}
