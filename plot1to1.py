# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:42:13 2024

Script for plotting 1:1 plots of raw data from the thermocouples
and thermal camera dataframe.

@author: kplo373
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# str_expt parameter should be a string of the type of experiment done, e.g. '50% Pellet-Sand'
def plot1to1(df_merged_cold, df_merged_hot, str_expt):
    T_Opcold = df_merged_cold['temperature_Op']  # extracting the temperature arrays
    T_CScold = df_merged_cold['temperature_CS']
    T_Ophot = df_merged_hot['temperature_Op']
    T_CShot = df_merged_hot['temperature_CS']
    
    stdOpcold = df_merged_cold['stdev_Op']  # extracting the standard deviation arrays
    stdCScold = df_merged_cold['stdev_CS']
    stdOphot = df_merged_hot['stdev_Op']
    stdCShot = df_merged_hot['stdev_CS']
    
    sterrOpcold = df_merged_cold['sterr_Op']  # extracting the standard error arrays
    sterrCScold = df_merged_cold['sterr_CS']
    sterrOphot = df_merged_hot['sterr_Op']
    sterrCShot = df_merged_hot['sterr_CS']
    
    # Using 5th Percentile Minimum Value (from ChatGPT) for Cold Array
    # 1. Calculate the 5th percentile value
    percentile_5_value = np.percentile(T_Opcold, 5)
    # 2. Find the index of the closest value in y_cold to the 95th percentile value
    index_5 = np.argmin(np.abs(T_Opcold - percentile_5_value))
    # Print the result
    print(f"5th percentile value: {percentile_5_value}")
    print(f"Index of 5th percentile value in y_cold: {index_5}")
    print(f"Corresponding x_cold value: {T_CScold.iloc[index_5]}")  # or else add .iloc[index_95] if tempC1_origcold is a pandas series
    print()

    # Likewise, using 95th Percentile Max Value for Hot Array
    percentile_95_value = np.percentile(T_CShot, 95)
    index_95 = np.argmin(np.abs(T_CShot - percentile_95_value))
    print(f"95th percentile value: {percentile_95_value}")
    print(f"Index of 95th percentile value in x_hot: {index_95}")
    print(f"Corresponding y_hot value: {T_Ophot.iloc[index_95]}")
    
    tempOphot = T_Ophot.iloc[index_95:]  # this needs to start and end at same indices as tempC1hot
    tempCShot = T_CShot.iloc[index_95:] 
    tempOpcold = T_Opcold.iloc[index_5:]
    tempCScold = T_CScold.iloc[index_5:]
    
    sdOpcold = stdOpcold.iloc[index_5:]
    sdCScold = stdCScold.iloc[index_5:]
    sdOphot = stdOphot.iloc[index_95:]
    sdCShot = stdCShot.iloc[index_95:]
    
    seOpcold = sterrOpcold.iloc[index_5:]
    seCScold = sterrCScold.iloc[index_5:]
    seOphot = sterrOphot.iloc[index_95:]
    seCShot = sterrCShot.iloc[index_95:]
    
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(tempCScold.iloc[0], tempOpcold.iloc[0])
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max(tempCShot.iloc[0], tempOphot.iloc[0])
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below
    print('Limits:', lower_lim, upper_lim)
    
    plt.figure(figsize=(7, 7))  # make it into a square shape, same axes limits!
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)

    # To plot the 1:1 reference line
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    #plt.errorbar(tempCScold, tempOpcold, yerr=seOpcold, xerr=seCScold, color='k')  # just include one errorbar maybe? Is there a better way to show them separately?
    #plt.errorbar(tempCScold, tempOpcold, yerr=seOpcold, color='k')
    plt.plot(tempCScold, tempOpcold, 'bo', label='Cold Raw Data')  # listing this after errorbars and as dots allow it to show up over black errorbars

    #can add a plt.errorbar() here too for the hot data - assuming using standard error like Tom said
    plt.plot(tempCShot, tempOphot, 'r', label='Hot Raw Data')
    
    plt.title('Sensor Comparison For ' + str_expt + ' Experiment')  # have to manually add in what percentage of plastic etc.
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.grid()
    plt.legend()
    plt.show()

    
    # can I create new merged dfs here that only have the clipped data? Then won't need to do the percentile limits in any other functions...
    #need to clip the stdev and sterr arrays too.. then create new merged df and return them.
    df_clipped_cold = pd.DataFrame({'tempCS': tempCScold, 'stdCS': sdCScold, 'sterrCS': seCScold, 
                                    'tempOp': tempOpcold, 'stdOp': sdOpcold, 'sterrOp': seOpcold})
    df_clipped_hot = pd.DataFrame({'tempCS': tempCShot, 'stdCS': sdCShot, 'sterrCS': seCShot, 
                                    'tempOp': tempOphot, 'stdOp': sdOphot, 'sterrOp': seOphot})
    
    
    
    return df_clipped_cold, df_clipped_hot

#df_cold, df_hot = plot1to1(df_merged_cold, df_merged_hot, '50% Pellet-Sand')


#%% to test
# To get the filepath
from get_filepaths import get_filepaths
path_cold, files_cold = get_filepaths('12/08/2024', 'AM')  # for the cold 50% nurdle-sand experiment
# path gives a folder, and files are the files in that folder. Need to select specific file from files list
path_Opcold = path_cold + '\\' + files_cold[0]
path_CScold = path_cold + '\\' + files_cold[2]

path_hot, files_hot = get_filepaths('13/08/2024', 'AM')  # for the hot 50% nurdle-sand experiment
path_Ophot = path_hot + '\\' + files_hot[0]
path_CShot = path_hot + '\\' + files_hot[2]


# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(path_CScold)
dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(path_CShot)
 
from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
# print(df_sand_avgCScold)
    
    
# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOpcold, a1cold, a2cold, a3cold, a4cold = read_Optris(path_Opcold)
dt_objsOphot, a1hot, a2hot, a3hot, a4hot = read_Optris(path_Ophot)
    
from read_Optris import resample_Optris
resampled_df_a1cold = resample_Optris(dt_objsOpcold, a1cold)
resampled_df_a3cold = resample_Optris(dt_objsOpcold, a3cold)
resampled_df_a1hot = resample_Optris(dt_objsOphot, a1hot)
resampled_df_a3hot = resample_Optris(dt_objsOphot, a3hot)
    
from read_Optris import average_Optris
avgOp_dfcold = average_Optris(resampled_df_a1cold, resampled_df_a3cold)
avgOp_dfhot = average_Optris(resampled_df_a1hot, resampled_df_a3hot)
# print(avgOp_dfcold)


from create_merged_df import create_merged_df
df_merged_cold = create_merged_df(avgOp_dfcold, df_sand_avgCScold)
df_merged_hot = create_merged_df(avgOp_dfhot, df_sand_avgCShot)
#print(df_mergedcold)



#%% Test this actual function
df_cold, df_hot = plot1to1(df_merged_cold, df_merged_hot, '50% Pellet-Sand')


