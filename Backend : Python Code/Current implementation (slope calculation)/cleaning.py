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

def removeNullValues(data, beginning):
    data["resistance"] = data["resistance"][beginning:]
    data["ms"] = data["ms"][beginning:]
    # removing null values
    data = data[pd.notnull(data['ms'])]

    return data

def removeSimilarValues(data, beginning):
    for i in range(beginning + 1, len(data["ms"]) - 2):
        # print(data.shape)
        # print(data["ms"])
        if (data["ms"][i] == data["ms"][i + 1] and not data[ms][i-1] == np.NaN):
            data["ms"][i] = np.NaN

    return data

def removeClusters(data):

    remove = []
    for i in range(len(data) - 1):
        if (data[i + 1] - data[i] < 5):
            remove.append(data[i])

    data = data.tolist()

    for x in remove:
        data.remove(x)

    return np.asarray(data)


def removeLocalMaxMin(data, interests):

    # we get the interesting data here
    interesting_data = []

    for x in interests:
        interesting_data.append(data["resistance"][x])

    # Typecast to numpy array
    interesting_data = np.asarray(interesting_data)

    # calculate the mean, then the minimum value, make a range
    avg_interest = np.mean(interesting_data)
    approx_amplitude = avg_interest - interesting_data.min()


    remove = []
    max = np.amax(interesting_data)

    for i in range(len(interesting_data) - 1):
        diff = abs(interesting_data[i+1] - interesting_data[i])
        if (diff < approx_amplitude/2 or max - interesting_data[i] < approx_amplitude/3 ):
            remove.append(interests[i]) # Append the INDEX to remove

    interests = interests.tolist()

    for x in remove:
        interests.remove(x)

    interests = np.asarray(interests)

    return {"approximate_amplitude" : approx_amplitude, "pois":interests, "avg_value":avg_interest}


def removeTopValues(data, interests):
    interesting_data = []

    for x in interests:
        if (not x == 0):
            interesting_data.append(data["resistance"][x])

    interesting_data = np.asarray(interesting_data)
    avg_interest = np.mean(interesting_data)
    approx_amplitude = avg_interest - min(interesting_data)

    remove = []

    for i in range(len(interesting_data) - 1):
        diff = interesting_data[i+1] - interesting_data[i]
        if (diff < 0 and diff > -1 * approx_amplitude / 2):
            remove.append(interests[i]) # Append the INDEX to remove

    # Necessary reshaping
    interests = interests.reshape(-1,1)
    interesting_data = interesting_data.reshape(-1,1)

    if (interesting_data[interesting_data.size - 1] > avg_interest):
        remove.append(interests[interesting_data.size - 1, :])

    interests = interests.tolist()

    for x in remove:
        interests.remove(x)

    interests = np.asarray(interests)

    return {"approximate_amplitude" : approx_amplitude, "pois":interests, "avg_value":avg_interest}

def removeVeryCloseInterestingPoints(interest):
    if (len(interest) >= 2):
        diffs = 0
        interest = interest.tolist()

        for i in range(len(interest) - 1):
            diffs = diffs + interest[i+1][0] - interest[i][0]

        print(len(interest) - 1)
        avg = diffs / ( len(interest) - 1)
        remove = []
        print(avg)

        for i in range(len(interest) - 1):
            if (interest[i+1][0] - interest[i][0]) < avg / 3:
                remove.append(interest[i])

        for x in remove:
            interest.remove(x)

        interest = np.asarray(interest)

    return interest
