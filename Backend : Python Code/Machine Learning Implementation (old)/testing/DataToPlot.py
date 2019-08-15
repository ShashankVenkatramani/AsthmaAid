"""
This file acts as a helper method, where it takes in a set of data,
arranged either as a text or csv file, then plots the data in matplotlib,
then saves that image to the user's computer
"""
import matplotlib.pyplot as plt
import pandas as pd

def getType(filename):
    x = filename.index(".")
    return (filename[x + 1:])

def dataToDf(filename, delimiter):
    if (getType(filename) == "csv"):
        return pd.read_csv(filename, header = None)
    else:
        return pd.read_csv(filename, sep = delimiter, header = None)

def dataToImg(dfx, dfy, name):
    plt.scatter(dfx, dfy)
    plt.axis('off')
    # plt.show()
    plt.savefig(name)


times = dataToDf("inputs/testMinutesInput.txt", " ")
breaths = dataToDf("inputs/testBreathInput.txt", " ")

dataToImg(times, breaths, "outputs/testPlot.png")
