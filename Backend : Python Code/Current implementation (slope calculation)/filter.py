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


def newSinusoidalFitter(dx, dy, name, size):
    # Alpha (regularization strength) of LASSO regression
    lasso_eps = 0.0001
    lasso_nalpha=20
    lasso_iter=5000
    # Min and max degree of polynomials features to consider
    degree_min = 2
    degree_max = 8

    # Test/train split
    X_train, X_test, y_train, y_test = train_test_split(dx, dy,test_size= 0.05)
    # Make a pipeline model with polynomial transformation and LASSO regression with cross-validation, run it for increasing degree of polynomial (complexity of the model)

    model1 = LassoCV(cv=10,verbose=0,normalize=True,eps=0.001,n_alphas=100, tol=0.0001,max_iter=5000)
    model1.fit(X_train,y_train)
    y_pred1 = np.array(model1.predict(X_train))

    RMSE_1=np.sqrt(np.sum(np.square(y_pred1-y_train)))
    print("Root-mean-square error of Metamodel:",RMSE_1)


    py = model1.predict(dx)

    fig, ax = plt.subplots(figsize=(size))
    ax.scatter(dx, py, s = 15) # Thicker width for easy identification by model
    ax.axis('off')
    fig.savefig(name + "pred_")
    plt.close(fig)
