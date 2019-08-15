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

from generalUtil import createOutputFolder

def plotAndSaveSegments(segments, outputFolder, shapeDesired, iter):
    counter = 0
    createOutputFolder(outputFolder)

    for segment in segments:
        counter += 1
        name_ = "iter_" + str(iter) + "_" + "segment_" + str(counter)
        dataToImg(segment["ms"], segment["resistance"], outputFolder , name_, [], shapeDesired)


def dataToImg(dfx, dfy, outputFolderName, name, interests, shape):
    fig, ax = plt.subplots(figsize=shape)
    ax.scatter(dfx, dfy, s = 100)

    for i in interests:
        ax.scatter(i, dfy[i], s = 500, c = 'r')

    ax.axis('off')

    createOutputFolder(outputFolderName)
    name = outputFolderName + "/" + name

    fig.savefig(name)
    plt.close(fig)
