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

def create_CampbellSci_Optris_dataframe(Optris_df, CampbellSci_df):
    print(Optris_df.columns)  # make sure to insert the standard deviation and standard error arrays per sensor into the end df_merged!
    print(CampbellSci_df.columns)
    
    # Setting up dataframes for Optris and Campbell Scientific cold temperature arrays
    mean_Op = Optris_df['Op_temp']
    datetime_Op = Optris_df['datetimes']
    T_Op = mean_Op.to_numpy()  # creating a numpy array for the Optris average temperatures
    df_optris = pd.DataFrame({'temperature_Op': T_Op}, index = datetime_Op)  # creating a new dataframe for Optris
    
    dt_objCS = CampbellSci_df['datetimes']
    T_CS = CampbellSci_df['mean_temperatures'].values  # adding .values converts it from pd.series to np.ndarray and prevents NaNs in final dataframe
    
    # Verify the lengths now match
    print(f"Length of T_Op: {len(T_Op)}")
    print(f"Length of T_CS: {len(T_CS)}")  # they don't actually match, but are on the same scale now! df_merged line below only includes values from both arrays
    
    # Create a dataframe for C1 data
    df_CS = pd.DataFrame({'temperature_CS': T_CS}, index = dt_objCS)
    
    # Merge the resampled Optris data with the C1 data
    df_merged = df_CS.join(df_optris, how='inner', lsuffix='_CS', rsuffix='_Op')
    
    return df_merged

df_merged = create_CampbellSci_Optris_dataframe(avgOp_df, df_sand_avgCS)
print(df_merged)

#%% Required functions to test the function above

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

#%% Test this actual function
df_merged = create_CampbellSci_Optris_dataframe(avgOp_df, df_sand_avgCS)
print(df_merged)
