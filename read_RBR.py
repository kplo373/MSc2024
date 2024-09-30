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
import matplotlib.pyplot as plt

# filepath should be a string, including the path and filename at the end
def read_RBR(filepath):
    # create dictionary of dataframes (one df per excel sheet)
    xl_file = pd.ExcelFile(filepath)
    dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}
    # this gives a dictionary with df.keys() == Metadata, Events, Data.
    data = dfs['Data']  # this is a dataframe of the raw data collected
    headers = data.iloc[0]
    data.columns = headers  # setting the column names as the headers, otherwise they are mostly all unnamed
    
    # Select the temperature and time columns, will use these to plot
    time = np.array(data['Time'])  # datetime.datetime type - need to convert to floats
    #timestamp = time.timestamp()  # this way isn't working... need to find a better way to convert into float for plotting
    
    temp = np.array(data['Temperature'])
    
    plt.plot(time, temp)  # not sure what format the time is - looks like datetimes...
    plt.show()
    
    
    return data


file_path = r"D:\MSc Results\060728_20240926_1416_KateRBR.xlsx"
df = read_RBR(file_path)
# gives a warning about no default style, but this isn't an issue - can just ignore it
