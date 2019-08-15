import qrcode
import pyrebase

import os
import time

import pandas as pd
import numpy as np
import shutil
from generalUtil import createOutputFolder
from singleDataPipeline import pipeline

""" configuration """
config = {
  "apiKey": "AIzaSyBA2HdYTxzeXvIJedXm2Cx2MKpPv_2-pB0",
  "authDomain": "com.cvenkatramani.AsthmaAid",
  "databaseURL": "https://asthmatracker-4cbe1.firebaseio.com",
  "storageBucket": "asthmatracker-4cbe1.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

""" loop itself"""
# db.child("medicine").child(Hash).set(data)

# Check for when the database changes

# Pyrebase to get a child listener
# From the child, from the 1, download all the data
# For each data point, remove the \r\n then we gucci

# Ignore default
vvvv = db.child("info").get()
results = dict(vvvv.val())
keys = results.keys()

userResults = dict(db.child("patients").get().val())
userStuff = userResults.pop(list(userResults.keys())[0])

# How far we've gone
numKeys = 0
# How long we wait between loops
waitTime = 10
# How long the program takes to run on avg, in seconds
offsetTime = 0
# Our "exit" condition - currently continuous
sentinel = True
isAdmin = False

while(sentinel):
    if (isAdmin):
        shutil.rmtree('output', ignore_errors=True)
        shutil.rmtree('inputsFromDatabase', ignore_errors=True)
    all_data_for_all_keys =  {}
    for key in keys:
        if not key=='default':
            amps = [] # y
            mss = [] # x
            numKeys += 1
            uid = results[key][0]
            last = results[key][1][0]
            first_ms = results[key][1][0]
            first_ms = float(first_ms[:first_ms.index(",")])
            for elem in (results[key][1]):
                if len(elem) > len(last) + 2:
                    continue

                last = elem

                ms = (float(elem[:elem.index(",")]) - first_ms + 1)
                amp = float(elem[elem.index(",") + 1:]) - 400
                #
                # try:
                #
                # except:
                #     continue

                amps.append(amp)
                mss.append(ms)
            # Convert those lists into numpy arrays
            amps = np.array(amps)
            mss = np.array(mss)
            # concatenate them into a dataframe
            df = pd.DataFrame({"ms":mss, "resistance":amps})
            df.set_index("ms", inplace=True, drop=True)


            # save the dataframe as a csv
            createOutputFolder("inputsFromDatabase")
            df.to_csv("inputsFromDatabase/" + str(numKeys) + ".csv")

            # Removing the current data to save space in the database
            # db.child("requests").child(key).remove()

            # Run pipeline on the data
            name = "inputsFromDatabase/" + str(numKeys)
            parameters = {"csv": name + ".csv", "output": "output/graphs_" + str(numKeys), "graph_shape":(200,10), "skip":2, "iter":numKeys, "size":2}
            output = pipeline(parameters)

            # Getting the user wanted data and pushing it to them
            total_breaths = len(output["segments"])

            if (total_breaths == 0):
                continue

            is_attack = output["overall_anomaly"]
            print({"is_attack":is_attack, "total_breaths":total_breaths})

            data_for_this_key = {"is_attack":is_attack, "total_breaths":total_breaths}

            # Saving the segmentation data
            all_starts = []
            all_anomalies = []
            for i in range(len(output["all_anomalies"])):
                start = output["segments"][i]
                all_starts.append(start["ms"].iloc[0])
                all_anomalies.append(output["all_anomalies"][i])
                print("Starts at " + str(start["ms"].iloc[0]) + ", the anomalies are : " + str(output["all_anomalies"][i]))

            points_are_starts = []
            for i in range (len(all_starts)):
                # Check all poi
                if (all_starts[i] < 2):
                    points_are_starts.append(False)
                # else if (all_starts[i] == 1):
                #     points_are_starts.append()
                else:
                    if (i == 0):
                        points_are_starts.append(all_anomalies[0])
                    else :
                        if (all_anomalies[i] == True and all_anomalies[i - 1] == True):
                            points_are_starts.append(True)
                        else:
                            points_are_starts.append(False)

            data_for_this_key["all_starts"] = all_starts
            data_for_this_key["all_anomalies"] = all_anomalies
            data_for_this_key["points_which_are_anomalies"] = points_are_starts
            # Since set overwrites all data, we need to:
            # Make a huge list of data and send it all at once
            # get the current hash value for the DATA
            all_data_for_all_keys[key] = data_for_this_key

    all_data_for_all_keys["info"] = userStuff
    print()
    print("Pushing data...")
    print()
    db.child("patients").child(uid).set(all_data_for_all_keys)
    print("Pushed data to the database via Pyrebase!")
    # Remove this line later, just for testing to limit downloading
    sentinel = False

    # Sleep approximately enough to wait for phone
    # to receive data, then repeat process until user cancels
    # time.sleep(waitTime - offsetTime)
