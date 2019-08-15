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
from singleDataPipeline import *

import warnings


def main(data_files):
    for i in range(len(data_files)):
        createOutputFolder("output")
        parameters = {"csv":data_files[i], "output": "output/graphs_" + str(i + 1), "graph_shape":(200,10), "skip":2, "iter":i + 1, "size":2}
        pipeline(parameters)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # test3 not included because too sparse, does not work with current algo
    data_files = ["data/test6.txt"]
    main(data_files)
