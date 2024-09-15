# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 08:28:09 2024

A function to resample the Optris thermal camera data into 5 second 
intervals, to match the Campbell Scientific data from the thermocouples.

@author: kplo373
"""
import pandas as pd
import numpy as np

# datetimeOp has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!
def resample_Optris(datetimeOp, mean_Op, stdev_arrOp):  # this mean_Op could be for half of the surface or for the smaller area just over the thermocouples
    #using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
    df_new = pd.DataFrame({     # creating a new dataframe
        'datetimes': datetimeOp,
        'Op_temp': mean_Op})    # can only read in one mean Optris temperature array at once from the averaging Optris function, this could be half or small area
    
    
    df_new.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
    # can extract datetimes using e.g. df_new.index
    
    def standard_error(x):
        return x.std() / np.sqrt(len(x))  # a function to calculate standard error
    
    resampled_df = df_new.resample('5s').agg({'Op_temp': ['mean', 'std', standard_error]})  
    # resampling whole dataframe to 5 sec intervals by taking the mean of temp, plus getting stdev and sterr
    # e.g. df.resample("3s").agg({'x':'sum','y':'mean','z':'last'}) can be used if using different functions for different columns
    print(resampled_df.iloc[:, 1])  # this gives the 'std' column
    stdev_resampled = resampled_df.iloc[:, 1]
    
    
    ##THE BELOW ISN'T WORKING, NEED TO FIGURE OUT BEST WAY TO COMBINE THE TWO DIFFERENT STANDARD DEVIATIONS OR ERRORS##
    
    # get this std column (or stderr??) and combine it with stdev_arrOp using eqn written down in notebook!
    #comb_sterr = np.sqrt((stdev_resampled**2 / len(stdev_resampled)) + (stdev_arrOp**2 / len(stdev_arrOp)))  # both terms are large arrays of stdevs with different lengths
    #print(comb_sterr)  # will need to put this into the resampled_df dataframe that is returned for this function!
    
    resampled_df.columns = ['mean_temp', 'stdev_temp', 'sterr_temp']  # renaming columns
    return resampled_df


#%% Testing the new function
#need to import the datetimes and mean Optris temp arrays from the read_Optris.py script function
from read_Optris import read_Optris
from read_Optris import average_Optris

the_filepath = r"D:\MSc Results\August_2024\Thursday1AugAM\Thurs1AugAMOptris.dat"
datetimes, a1, a2, a3, a4 = read_Optris(the_filepath)

avg_Op_half, stdevs, sterrs = average_Optris(a1, a3)   # what to do with these stdevs and sterrs? need to combine them with ones within the resampled_df
#print(avg_Op_half)


resampled_df = resample_Optris(datetimes, avg_Op_half, stdevs)
print(resampled_df.columns)  # these are only for Optris, not Campbell Sci thermocouples.


# need to combine the standard deviations/errors somehow, but both functions output separate ones! Could have std dev as an input for the resample_Optris fn??
