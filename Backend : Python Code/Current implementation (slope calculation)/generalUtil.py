import os
import pandas as pd

from scipy.optimize import leastsq
from scipy.signal import argrelextrema
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

def getType(filename):
    x = filename.index(".")
    return (filename[x + 1:])

def dataToDf(filename, delimiter):
    if (getType(filename) == "csv"):
        return pd.read_csv(filename, header = None)
    else:
        return pd.read_csv(filename, sep = delimiter, names = ["ms", "resistance"])

def slope(x1, x2, ydiff):
    return (x1 - x2) / ydiff

def createOutputFolder(outputFolderName):
    if not (os.path.exists(os.path.join(os.getcwd(), outputFolderName))):
        os.mkdir(os.path.join(os.getcwd(), outputFolderName))

def avgSlope(rc, beg, end):
    diff = 0
    for i in range (beg, end):
        diff += slope(rc[i], rc[i+1], 10)

    return diff / (end - beg)


def calculateSlopes(data, skipFactorForCalculatingSlopes, size):
    """
    Go from 0 to data.size - 1
    Calculate the slopes between points i and i + 1
    Check where the slopes turn negative, put a big red dot there on plot
    """

    diffs = []
    rc = data["resistance"].values
    for i in range(1, data["ms"].size - size):
        diff = avgSlope(rc, i, i + size)
        i += skipFactorForCalculatingSlopes
        diffs.append(diff)

    poi = []

    for i in range(0, len(diffs) - 1):
        if (diffs[i] < 0.04 and diffs[i] > -0.04):
            poi.append(i + 1)


    return {"slopes":diffs, "interest":np.asarray(poi)}




def getIrrelevantData(data):
    counter = 0
    while (data.size - counter) > 100:
        snapshot = data[counter: counter + 100]
        std = np.std(snapshot)
        if (std > 10):
            break

        # We only go up by 10 so we have a shifting window, most accurate
        counter += 10

    return counter # subset of data from current point on which is relevant

def splitDataIntoSegments(data, interests):
    segments = []
    interests = interests.tolist()
    for i in range(0, len(interests) - 1):
        # segment is from current interest at i to next point at i + 1
        # print(type(data))
        # print(type(interests))
        left = interests[i][0]
        right = interests[i + 1][0]

        xx = data["ms"][left:right]
        xy = data["resistance"][left:right]
        segment_1 = pd.DataFrame(data = {"ms":xx, "resistance":xy})
        if (segment_1["ms"].size > 10):
            segments.append(segment_1)

    return segments
