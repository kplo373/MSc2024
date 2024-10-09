# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 10:36:26 2024

Function to read in RBR files that are rsk format rather
than xlsx (Excel).

@author: kplo373
"""
import pyrsktools as pyrsk
import numpy as np

def read_RBR(filepath):
    rsk = pyrsk.RSK(filepath)
    # Open the RSK file. Metadata is read here
    rsk.open()
    
    t1 = np.datetime64("2024-10-01")  # choosing the rough day when I did the test (Tues 1st Oct 2024)
    t2 = np.datetime64("2024-10-02")
    rsk.readdata(t1, t2)
    print(len(rsk.data))
    print(rsk)
    print(rsk.channelNames)
    # ('conductivity', 'temperature', 'pressure')
    #print(rsk.data["timestamp"])  # must be the index maybe?
    # ['2024-10-01T09:06:44.000' ... '2024-10-01T10:03:54.000']
    #print(rsk.data["temperature"])
    
    timestamps = rsk.data["timestamp"]
    temps = rsk.data["temperature"]
    
    rsk.close()
    
    return timestamps, temps


#filepath = r"D:\MSc Results\RBR_Test\060728_20241001_1004KateRBR.rsk"  # this one works! the .print(rsk) says data is populated with 3431 elements
# RBR2 isn't plotting anything... seems empty?? .data is unpopulated
filepath = r"D:\MSc Results\RBR_Test\RBRtest3\060728_20241009_1124KateRBR3.rsk"  # same as RBR3... unpopulated data! The exported excel file is okay though, so use that...
timestamps, temps = read_RBR(filepath)


#%% Now, want to plot the RBR temperatures against the thermocouple temperatures for the same time period
import matplotlib.pyplot as plt

plt.plot(timestamps, temps)
plt.show()

# It works!! Will have to play around with what format time should be... datetimes to match the thermocouples?

