# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:53:48 2024

This is a function following on from the averaging Optris and CampbellSci 
functions, putting both the Campbell Scientific thermocouple data and the 
Optris thermal camera temperature data into one dataframe, with datetime 
as the index. Only the common time data should be included in the dataframe.

@author: kplo373
"""
# Just in case it can't find the right data folder, use these two lines below
#import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions in the second cell

import pandas as pd
import numpy as np

def create_merged_df(Optris_df, CampbellSci_df):    
    mean_Op = Optris_df['Op_temp']
    datetime_Op = Optris_df['datetimes']
    T_Op = mean_Op.to_numpy()  # creating a numpy array for the Optris average temperatures
    stdevOp = Optris_df['stdevs'].values  # adding .values converts it from pd.series to np.ndarray and prevents NaNs in final dataframe
    sterrOp = Optris_df['sterrs'].values
    
    dt_objCS = CampbellSci_df['datetimes']
    T_CS = CampbellSci_df['mean_temperatures'].values
    stdevCS = CampbellSci_df['stdev'].values
    sterrCS = CampbellSci_df['sterr'].values
    
    # Compare the lengths of the mean temperature arrays, after resampling Optris in a previous function
    #print(f"Length of T_Op: {len(T_Op)}")
    #print(f"Length of T_CS: {len(T_CS)}")  # they don't actually match, but are on the same scale now!
    
    # Setting up dataframes for Optris and Campbell Scientific cold temperature arrays
    df_Op = pd.DataFrame({'temperature_Op': T_Op, 'stdev_Op': stdevOp, 'sterr_Op': sterrOp}, index = datetime_Op)
    df_CS = pd.DataFrame({'temperature_CS': T_CS, 'stdev_CS': stdevCS, 'sterr_CS': sterrCS}, index = dt_objCS)
    
    # Merge the resampled Optris data with the C1 data
    df_merged = df_CS.join(df_Op, how='inner', lsuffix='_CS', rsuffix='_Op')  # this only includes values from both arrays

    #T_CS = df_merged['temperature_CS'].values  # these didn't really give clear temperatures like Optris does below
    T_CS = df_merged['temperature_Op'].values  # named it T_CS to not change everything below but it is actually T_Op data!

    # Trimming parameters
    window_size = 360  # 10-second intervals in a 1-hour rolling window
    threshold = 0.07  # for "approximately constant" temperature - can increase/decrease if needed!
    stabil_len = 2000  # require stabilisation for at least 300 consecutive pts

    # Compute rolling standard deviation
    rolling_std_CS = pd.Series(T_CS).rolling(window=window_size, min_periods=1).std()  # just try with thermocouples (Optris actually) first
    #rolling_std_Op = pd.Series(T_Op).rolling(window=window_size, min_periods=1).std()

    # Find last point where temperature becomes stable
    stable_ind = np.where(rolling_std_CS < threshold)[0]
    if len(stable_ind) > stabil_len:
        # Check for consecutive points
        for i in range(len(stable_ind) - stabil_len):
            if np.all(np.diff(stable_ind[i:i + stabil_len]) == 1):
                trim_ind = stable_ind[i]
                break
        else:
            trim_ind = len(T_CS)
    else: 
        trim_ind = len(T_CS)

    # Trim Data
    df_merged_trim = df_merged.iloc[:trim_ind]  # doing it all at once!
    
    return df_merged_trim



r'''
#%% Required functions to test the function above
# To get the filepath
from get_filepaths import get_filepaths
path, files = get_filepaths('07/08/2024', 'PM')  # cold 25% pellets & water, has spike (unless hot one does)
# path gives a folder, and files are the files in that folder. Need to select specific file from files list
path_CS = path + '\\' + files[0]
path_Op = path + '\\' + files[2]

#path_CS = r"D:\MSc Results\August_2024\Wednesday07AugPM\CR3000_Table1.dat"
#path_Op = r"D:/MSc Results/August_2024/Wednesday07AugPM/Wed7AugPMOptris.dat"
path_CS = r"D:\MSc Results\August_2024\Tuesday20AugPM\CR3000_Table1.dat"
path_Op = r"D:\MSc Results\August_2024\Tuesday20AugPM\Tues20AugPMOptris.dat"

# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCS, temps_arrCS, stdevs_arrCS = read_CampbellSci(path_CS)
    
from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
df_sand_avgCS = sand_avgCS(dt_objsCS, temps_arrCS, stdevs_arrCS)
# print(df_sand_avgCS)
# The index here is actually just the numbers 0 to 5061, not the datetime objects! That is accessed by the 'datetimes' column
    
    
# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOp, a1, a2, a3, a4 = read_Optris(path_Op)
    
from read_Optris import resample_Optris
resampled_df_a1 = resample_Optris(dt_objsOp, a1)
resampled_df_a3 = resample_Optris(dt_objsOp, a3)
    
from read_Optris import average_Optris
avgOp_df = average_Optris(resampled_df_a1, resampled_df_a3)
# print(avgOp_df)


# Test this actual function
df_merged = create_merged_df(avgOp_df, df_sand_avgCS)
print(df_merged)
'''

#%%
#import matplotlib.pyplot as plt


r'''  # this is just to show results if needed
# Plot rolling stdev
plt.plot(rolling_std_CS, label='Rolling Std Dev')  # will need to make sure these separate variables for plotting are returned
plt.axhline(threshold, color='red', linestyle='--', label='Threshold')
plt.title('Rolling Standard Deviation of Temperature')
plt.xlabel('Index')
plt.ylabel('Std Dev')
plt.legend()
plt.grid()
plt.show()

# Plot results after trimming
plt.plot(timestamps, T_CS, label='Original T', alpha=0.2)  # will need to plot Optris too!
plt.plot(timestamps_trim, T_CS_trim, label='Trimmed T', lw=2)
plt.xlabel('Time')
plt.ylabel('Optris Temperature (deg C)')
plt.grid()
plt.legend()
plt.show()
'''

