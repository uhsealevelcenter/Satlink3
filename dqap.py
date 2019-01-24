
from sl3 import *
import time
from math import sqrt

raw_vals = []
dqap_vals = []

mean = 0
stdev = 0
dqap = 0
nsamp = 0
num_dqap_samples = 0
dqap_quality = 0
is_started = 0

@MEASUREMENT
def get_data(val):
    """
    get new data and store to array.
    """
    global raw_vals, dqap_vals, mean, stdev, dqap, nsamp, num_dqap_samples, dqap_quality, is_started

    if utime.localtime()[5] == 30:
        is_started = 1
    print("sec = " + str(utime.localtime()[5]))
    print("nsamp = " + str(len(raw_vals)))
    #print(is_started)

    if is_started:
        raw_vals.append(val)

    return val

@MEASUREMENT
def create_dqap(val):
    """
    compute Mean, Standard Deviation, and DQAP.
    """
    global raw_vals, dqap_vals, mean, stdev, dqap, nsamp, num_dqap_samples, dqap_quality, is_started

    dqap_raw_vals = raw_vals
    # This should be here but it takes too long to copy, so clear is at end of routine.
    #raw_vals.clear()

    nsamp = len(dqap_raw_vals)

    # compute mean
    mean = sum(dqap_raw_vals) / len(dqap_raw_vals)
    print("mean = " + str(mean))

    # compute standard deviation
    variance = sum([(e-mean)**2 for e in dqap_raw_vals]) / len(dqap_raw_vals)
    stdev = sqrt(variance)
    print("stdev = " + str(stdev))

    # compute DQAP value
    if stdev == 0:
        dqap = mean
        num_dqap_samples = 0
        #dqap_quality = 2
    else:
        for meas in dqap_raw_vals:
            if ((meas <  mean + 3*stdev) and (meas >  mean - 3*stdev)):
                 dqap_vals.append(meas)
        if dqap_vals:
            dqap = sum(dqap_vals) / len(dqap_vals)
        print("dqap = " + str(dqap))
        num_dqap_samples = len(dqap_vals)
        print("num_dqap_samples = " + str(num_dqap_samples))
        #print("dqap_vals = " + str(dqap_vals))

    if (num_dqap_samples < nsamp/2):
        dqap_quality = 0
    else:
        dqap_quality = 1

    # reset the stuff every time
    raw_vals.clear()
    dqap_vals.clear()

    return val


@MEASUREMENT
def get_mean(val):
    time.sleep(.1)
    print("mean = " + str(mean))
    return mean

@MEASUREMENT
def get_stdev(val):
    time.sleep(.1)
    print("standard deviation = " + str(stdev))
    return stdev

@MEASUREMENT
def get_dqap(val):
    time.sleep(.1)
    print("DQAP value = " + str(dqap))
    return dqap

@MEASUREMENT
def get_num_dqap_samples(val):
    time.sleep(.3)
    print("num_dqap_samples = " + str(num_dqap_samples))
    return float(num_dqap_samples)

@MEASUREMENT
def get_dqap_quality(val):
    time.sleep(.1)
    print("dqap_quality = " + str(dqap_quality))
    return float(dqap_quality)
    
