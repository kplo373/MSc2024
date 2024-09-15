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
    # Assuming Tcold_Op is the temperature array and Tcold_time_Op is the corresponding time array
    dt_Op = pd.to_datetime(Optris_df.index)  # getting datetime index column as an array from Optris, then converting to pandas datetime
    mean_Op = Optris_df['mean_temp']
    datetime_Op = Optris_df.index
    T_Op = mean_Op.to_numpy()  # creating a numpy array for the Optris average temperatures
    df_optris = pd.DataFrame({'temperature': T_Op}, index = datetime_Op)  # creating a new dataframe for Optris
    
    # Resample to 5-second intervals, taking the mean for each interval - why am I doing this again actually?? Optris_df should already be in 5s intervals...
    #df_optris_resampled = df_optris.resample('5s').mean()
    
    # Extract the resampled temperature and time arrays
    #Tcold_Op_resampled = df_optris_resampled['temperature'].values
    #Tcold_time_Op_resampled = df_optris_resampled.index
    
    Tcold_C1 = ref_temps_C1cold
    
    # Verify the lengths now match
    print(f"Length of Tcold_Op_resampled: {len(Tcold_Op_resampled)}")
    print(f"Length of Tcold_C1: {len(Tcold_C1)}")  # they don't actually match, but are on the same scale now! df_merged line below only includes values from both arrays
    
    # Create a dataframe for C1 data
    df_C1 = pd.DataFrame({'temperature': Tcold_C1}, index = dt_objsC1cold)
    
    # Merge the resampled Optris data with the C1 data
    df_merged = df_C1.join(df_optris_resampled, how='inner', lsuffix='_C1', rsuffix='_Op')
    
    # Now you can access the aligned temperature arrays
    Tcold_C1_aligned = df_merged['temperature_C1'].values
    Tcold_Op_aligned = df_merged['temperature_Op'].values
    
    return   # WHAT AM I RETURNING HERE?? THE END DATAFRAME MAYBE...



#%% Test function
#what would I need to get from past functions?? this should follow on from resample_Optris.py

# To get the filepath
from get_filepaths import get_filepaths
#******************* then fix the stuff above, and use this instead of the_filepath below.

# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
the_filepath = r"D:\MSc Results\August_2024\Tuesday13AugAM\CR3000_Table1.dat"
dt_objs, temps_arr, stdevs_arr = read_CampbellSci(the_filepath)

from read_CampbellSci import sand_avgCS  # this function will depend on what type of test is being done...
df_sand_avgCS = sand_avgCS(dt_objs, temps_arr)

# To collect the Optris thermal camera data
from read_Optris import read_Optris
the_filepath = r"D:\MSc Results\August_2024\Thursday1AugAM\Thurs1AugAMOptris.dat"  # was giving a SyntaxWarning because of slashes, said invalid escape sequence
datetimes, a1, a2, a3, a4 = read_Optris(the_filepath)

from read_Optris import average_Optris
avg_Op_half, stdevs, sterrs = average_Optris(a1, a3)
print(avg_Op_half)

from resample_Optris import resample_Optris
resampled_df = resample_Optris(datetimes, avg_Op_half, stdevs)

# Now can use both the Campbell Scientific and Optris dataframes to test this new function


