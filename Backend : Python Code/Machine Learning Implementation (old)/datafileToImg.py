"""
This file acts as a helper method, where it takes in a set of data,
arranged either as a text or csv file, then plots the data in matplotlib,
then saves that image to the user's computer
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def getType(filename):
    x = filename.index(".")
    return (filename[x + 1:])

def dataToDf(filename, delimiter):
    if (getType(filename) == "csv"):
        return pd.read_csv(filename, header = None)
    else:
        return pd.read_csv(filename, sep = delimiter, header = None)

def dataToImg(dfx, dfy, name):
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.scatter(dfx, dfy, s = 150) # Thicker width for easy identification by model
    ax.axis('off')
    fig.savefig(name)
    plt.close(fig)

def getOutliers(X):
    """
    # Detecting outliers based on the Modified Z-score method
    threshold = 3.5

    median = np.median(X)
    median_absolute_deviation = np.median([np.abs(x - median) for x in X])
    modified_z_scores = [0.6745 * (x - median) / median_absolute_deviation for x in X]
    return np.asarray(np.where(np.abs(modified_z_scores) > threshold))
    """
    # Detecting outliers based on the IQR Method
    quartile_1, quartile_3 = np.percentile(X, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    # print(X)
    # print("Lower: " + str(lower_bound) + ", Upper: " + str(upper_bound))
    lowers = np.asarray(X[X < lower_bound])
    uppers = np.asarray(X[X > upper_bound])

    # Prevents error when using np.concatenate
    if (lowers.size == 0):
        # print("The outliers are : " + str(uppers))
        return uppers
    if (uppers.size == 0):
        # print("The outliers are : " + str(lowers))
        return lowers

    toRet = np.concatenate((lowers, uppers))
    # print("The outliers are : " + str(toRet))
    return toRet
