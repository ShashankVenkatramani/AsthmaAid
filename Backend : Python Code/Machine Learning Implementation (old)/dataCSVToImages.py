from datafileToImg import *
import pandas as pd
import numpy as np
import os
"""
times = dataToDf("inputs/testMinutesInput.txt", " ")
breaths = dataToDf("inputs/testBreathInput.txt", " ")
dataToImg(times, breaths, "outputs/testPlot.png")
"""

# Take in a csv file with a list of data text files
# We are going to split this into individual text files, send that to the functions
# we get form datafileToImg, then send all these images to a folder

def csvToImages(csvFileName, outputFolderName):
    # Making the output folder
    if not (os.path.exists(os.path.join(os.getcwd(), outputFolderName))):
        os.mkdir(os.path.join(os.getcwd(), outputFolderName))

    # Read the csvFileName
    csv = pd.read_csv(csvFileName, delimiter=',')
    num = csv.shape[0]
    # For every filename
    for i in range (0, num):
        # First, get the filename
        currFile = csv.iloc[i, 0]
        # Get the csv file associated with the file
        df = dataToDf(currFile, " ")
        # Generate an image, name it i_0or1forAsthma and put it in outputFolderName
        x = np.array([1,2,3,4,5,6,7,8,9,10, 11, 12])
        labels = pd.DataFrame(data = x)
        dataToImg(labels, df, outputFolderName + "/" + str(i) + "_" + str(csv.iloc[i,1]))
