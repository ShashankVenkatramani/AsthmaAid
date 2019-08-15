
def anomalyDetector(segments):
    anomaly = []
    for segment in segments:
        anomaly.append(detectAnomaly(segment))

    ov = False
    l = 0 # longest bad streak
    x = 0 # Current counter
    for i in range(len(anomaly) - 1):
        if (anomaly[i] == anomaly[i +1] and anomaly[i+1] == True):
            x += 1
        else:
            if (x > l):
                l = x
        if l > 2:
            ov =  True
    if x > 2:
        ov = True

    return {"overall": ov, "all":anomaly}


def detectAnomaly(segment):
    rc = segment["resistance"]

    minValue = rc.min()
    maxValue = rc.max()
    # get min of segment
    rc = rc.tolist()
    minIndex = rc.index(minValue)
    maxIndex = rc.index(maxValue)
    totalDiff = segment["ms"].shape[0]

    if (maxIndex - minIndex) <= totalDiff * 2/5:
        return False

    return True
