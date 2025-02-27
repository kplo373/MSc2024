# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 09:09:45 2025

Script to calculate the uncertainty columns required from the standard errors
calculated for the deltaT plots, to put into my Word doc next to these plots.

These are: mean, approximate mode, 90th percentile, 10th percentile.


@author: kplo373
"""
import numpy as np

def calculate_uncertainty(SE_arr):  # use this function on one percentage's standard errors at once
    #print(SE_arr) 
    print(max(SE_arr), min(SE_arr))  # if not nan, there are no nans present!
    
    # Handle NaNs safely just in case
    SE_arr = SE_arr[~np.isnan(SE_arr)]
    
    if SE_arr.size == 0:  # if the array is empty after removing nans above
        unc_dict = {"Mean": np.nan, 
                    "Mode": np.nan, 
                    "90th Percentile": np.nan, 
                    "10th Percentile": np.nan}
        return unc_dict
    
    # Mean
    meanSE = np.mean(SE_arr)
    
    # Approximate Mode: Bin the non-nan data
    bin_width = 0.01  # adjust this if needed
    bins = np.arange(SE_arr.min(), SE_arr.max() + bin_width, bin_width)  # np.array
    hist, bin_edges = np.histogram(SE_arr, bins=bins)
    max_bin_index = np.argmax(hist)
    approx_modeSE = (bin_edges[max_bin_index] + bin_edges[max_bin_index + 1]) / 2  # bin midpoint
    
    # Percentiles
    p90SE = np.nanpercentile(SE_arr, 90)
    p10SE = np.nanpercentile(SE_arr, 10)
    
    uncertainty_dict = {"Mean": meanSE, 
                        "Mode": approx_modeSE, 
                        "90th Percentile": p90SE, 
                        "10th Percentile": p10SE}
    
    return uncertainty_dict