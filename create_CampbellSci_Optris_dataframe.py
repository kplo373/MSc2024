# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:53:48 2024

This is a function following on from resample_Optris.py that puts both the 
Campbell Scientific thermocouple data and the Optris thermal camera 
temperature data into one dataframe, with datetime as the index. Only the 
common time data should be included in the dataframe.

@author: kplo373
"""
import pandas as pd
#import numpy as np

# copy next bit from plot_hot_cold_retry.py into here and probably read in previous functions... see test for resample_Optris.py

#resample_Optris outputs resampled_df - an Optris dataframe, will probably need this
# where does the CampbellSci_df come from? We get them separately from read_CampbellSci.py and its averaging functions below...should I put these into a df?
def create_CampbellSci_Optris_dataframe(Optris_df, CampbellSci_df):

    # Setting up dataframes for Optris and Campbell Scientific cold temperature arrays
    dt_Op = pd.to_datetime(Optris_df.index)  # getting datetime index column as an array from Optris, then converting to pandas datetime
    mean_Op = Optris_df['Op_temp']
    datetime_Op = Optris_df['datetimes']
    T_Op = mean_Op.to_numpy()  # creating a numpy array for the Optris average temperatures
    #print(T_Op)  # also legit
    df_optris = pd.DataFrame({'temperature': T_Op}, index = datetime_Op)  # creating a new dataframe for Optris
    #print(df_optris['temperature'])  # has worked here!
    
    # Resample to 5-second intervals, taking the mean for each interval - why am I doing this again actually?? Optris_df should already be in 5s intervals...
    #df_optris_resampled = df_optris.resample('5s').mean()
    
    # Extract the resampled temperature and time arrays
    #Tcold_Op_resampled = df_optris_resampled['temperature'].values
    #Tcold_time_Op_resampled = df_optris_resampled.index
    
    dt_objCS = CampbellSci_df['datetimes']
    #print(dt_objCS)  # good
    T_CS = CampbellSci_df['mean_temperatures']
    #print(T_CS)  # this is legit
    
    # Verify the lengths now match
    print(f"Length of T_Op: {len(T_Op)}")
    print(f"Length of T_CS: {len(T_CS)}")  # they don't actually match, but are on the same scale now! df_merged line below only includes values from both arrays
    
    # Create a dataframe for C1 data
    df_CS = pd.DataFrame({'temperatures': T_CS}, index = dt_objCS)
    #print(df_CS.index)  # good
    print(len(dt_objCS), len(df_CS['temperatures']))  # both are length 5061
    print(df_CS['temperatures'])  # this is not legit... is all NaNs. Why? T_CS as an array is normal!
    
    # Merge the resampled Optris data with the C1 data
    df_merged = df_CS.join(df_optris, how='inner', lsuffix='_CS', rsuffix='_Op')
    
    # Now you can access the aligned temperature arrays
    #Tcold_C1_aligned = df_merged['temperature_C1'].values
   # Tcold_Op_aligned = df_merged['temperature_Op'].values
    
    return df_merged

df_merged = create_CampbellSci_Optris_dataframe(avgOp_df, df_sand_avgCS)
#print(df_merged)


#%% Test function
#what would I need to get from past functions?? this should follow on from resample_Optris.py

# To get the filepath
from get_filepaths import get_filepaths
path, files = get_filepaths('13/08/2024', 'AM')
# path gives a folder, and files are the files in that folder. Need to select specific file from files list
path_Op = path + '\\' + files[0]
path_CS = path + '\\' + files[2]

# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCS, temps_arrCS, stdevs_arrCS = read_CampbellSci(path_CS)
    
from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
df_sand_avgCS = sand_avgCS(dt_objsCS, temps_arrCS)
# print(df_sand_avgCS)
###the index here is actually just the numbers 0 to 5061, not the datetime objects! That is accessed by the 'datetimes' column
    
    
# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOp, a1, a2, a3, a4 = read_Optris(path_Op)
    
from read_Optris import resample_Optris
resampled_df_a1 = resample_Optris(dt_objsOp, a1)
resampled_df_a3 = resample_Optris(dt_objsOp, a3)
    
from read_Optris import average_Optris
avgOp_df = average_Optris(resampled_df_a1, resampled_df_a3)
# print(avgOp_df)

#%% test this function

df_merged = create_CampbellSci_Optris_dataframe(avgOp_df, df_sand_avgCS)
print(df_merged)
