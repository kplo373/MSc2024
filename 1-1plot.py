# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:42:13 2024

Script for plotting 1:1 plots of raw data from the thermocouples
and thermal camera dataframe.

@author: kplo373
"""

import numpy as np
import matplotlib.pyplot as plt

def plot1to1(df_merged_cold, df_merged_hot):
    T_Opcold = df_merged_cold['temperature_Op']
    T_CScold = df_merged_cold['temperature_CS']
    T_Ophot = df_merged_hot['temperature_Op']
    T_CShot = df_merged_hot['temperature_CS']
    
    # Using 5th Percentile Minimum Value (from ChatGPT) for Cold Array
    # 1. Calculate the 5th percentile value
    percentile_5_value = np.percentile(T_Opcold, 5)
    # 2. Find the index of the closest value in y_cold to the 95th percentile value
    index_5 = np.argmin(np.abs(T_Opcold - percentile_5_value))
    # Print the result
    print(f"5th percentile value: {percentile_5_value}")
    print(f"Index of 5th percentile value in y_cold: {index_5}")
    print(f"Corresponding x_cold value: {T_CScold[index_5]}")  # or else add .iloc[index_95] if tempC1_origcold is a pandas series
    print()

    # Likewise, using 95th Percentile Max Value for Hot Array
    percentile_95_value = np.percentile(T_CShot, 95)
    index_95 = np.argmin(np.abs(T_CShot - percentile_95_value))
    print(f"95th percentile value: {percentile_95_value}")
    print(f"Index of 95th percentile value in x_hot: {index_95}")
    print(f"Corresponding y_hot value: {T_Ophot[index_95]}")
    
    tempOphot = T_Ophot[index_95:]  # this needs to start and end at same indices as tempC1hot
    tempCShot = T_CShot[index_95:] 
    tempOpcold = T_Opcold[index_5:]
    tempCScold = T_CScold[index_5:]
    
    
    plt.plot(tempCScold, tempOpcold)
    plt.plot(tempCShot, tempOphot)
    plt.show()
    
    return  # shall I return the clipped temperature arrays? and what if I left the sensors running overnight? not sure if that has been dealt with yet...

plot = plot1to1(df_merged_cold, df_merged_hot)


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

#%%   
from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold)  # this line is giving the index error******

df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot)  # but this line is fine
# print(df_sand_avgCScold)
# The index here is actually just the numbers 0 to 5061, not the datetime objects! That is accessed by the 'datetimes' column
    
    
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


from create_CampbellSci_Optris_dataframe import create_CampbellSci_Optris_dataframe
df_merged_cold = create_CampbellSci_Optris_dataframe(avgOp_dfcold, df_sand_avgCScold)
df_merged_hot = create_CampbellSci_Optris_dataframe(avgOp_dfhot, df_sand_avgCShot)
#print(df_mergedcold) 

#%% Test this actual function
plot = plot1to1(df_merged_cold, df_merged_hot)


