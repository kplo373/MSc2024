# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:39:24 2024

Script to load in the RBR data for temperature, pressure, and salinity.
This data will be used to compare against the thermocouple readings for 
the same experimental run (cold pure water from the fridge warming to 
room temperature), to check accuracy.

@author: kplo373
"""
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

# filepath should be a string, including the path and filename at the end
def read_RBR_excel(filepath): # reading from an excel RBR
    xls = pd.ExcelFile(filepath)
    df = pd.read_excel(xls, 'Data', header = 1)  # skipping the first row as it doesn't contain much, and want df.columns to represent the actual headers

    print(df.columns)  # this is a list of headers

    # Select the temperature and time columns, will use these to plot
    time = np.array(df['Time'])  # datetime.datetime type - need to convert to floats
    temp = np.array(df['Temperature'])
    
    # It doesn't plot correctly below, let's link this function to extract time and temp into plot_RBR_thermocouples!
    #plt.plot(time, temp)  # not sure what format the time is - looks like datetimes...
    #plt.show()
    
    
    return time, temp


r'''
#file_path = r"D:\MSc Results\060728_20240926_1416_KateRBR.xlsx"
file_path = r"D:\MSc Results\RBR_Test\RBRtest3\060728_20241009_1124KateRBR3.xlsx"
df = read_RBR_excel(file_path)  # there is stuff in here, YAY!!
# gives a warning about no default style, but this isn't an issue - can just ignore it
'''