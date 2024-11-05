# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:09:57 2024

Retry of applying pure water calibration to all other mixture raw data.
This function is run through main() after the plot1to1.py.

@author: adamk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.interpolate import interp1d


def apply_calibration(df_in, str_expt):    
    # Load non-control sample data from df_in (x and y are independent)
    x_nctrl = np.array(df_in['temperature_CS']).reshape(-1, 1)
    y_nctrl = np.array(df_in['temperature_Op']).reshape(-1, 1)
    
    # Load pure water calibration table from saved csv file
    filepath = r'D:\MSc Results\calTable.csv'  # this has the whole df_in for pure water
    calTable_df = pd.read_csv(filepath, index_col='y_val')  # just want to read a specific column?
    print(calTable_df.columns)
    
    # Interpolate to match y_nctrl values with calibration adjustments (as they will have different lengths)
    interp_func = interp1d(
       calTable_df.index,
       calTable_df['y_cal_adj'],
       kind='linear',  # to ensure linear interpolation
       bounds_error=False,
       fill_value="extrapolate")
    
    y_cal_adj_interpolated = interp_func(y_nctrl.ravel())
    
    # Apply the calibration adjustment (subtraction for correction)
    y_nctrl_corrected = y_nctrl.ravel() - y_cal_adj_interpolated

    # Store corrected values in the DataFrame
    df_in['y_corrected'] = y_nctrl_corrected

    #print(y_nctrl)  # to compare them if desired
    #print(y_nctrl_corrected)
    
    # Debugging print statements
    print("Calibration adjustments applied:")
    print(df_in[['temperature_Op', 'y_corrected']].head())  # View initial values for verification
    

    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_roundH(n):  # create a hot function to round up if .27 or higher, or round down if less than .27.
        if n - math.floor(n) < 0.27:
            return math.floor(n)
        return math.ceil(n)
    
    def normal_roundC(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(x_nctrl[0], y_nctrl_corrected[0])
    lower_lim = normal_roundC(lower_limit) - 1

    upper_limit = max( max(x_nctrl), max(y_nctrl_corrected) )
    upper_lim = normal_roundH(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # Plot Calibration Results, Add in Reference Line too
    plt.figure(figsize=(7, 7))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    plt.plot(x_nctrl, y_nctrl_corrected, color='green', lw=2, label='Calibrated Curve')
    plt.plot(x_nctrl, y_nctrl, 'r', label='Raw Data')
    # Plot the 1:1 line across the entire plot from corner to corner
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)
    
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.title('Calibrated Sensor Comparison For ' + str_expt)
    plt.legend()
    plt.grid()
    if 'hav' in str_expt:
        if 'and' in str_expt:
            final_folder = 'MP_sand'
        elif 'ater' in str_expt:
            final_folder = 'MP_water'
        file_str = r'\Cal_' + str_expt.replace("% Shavings", "_MP") + '.png'  # not sure if I can have % signs in a filename...
    elif 'ellet' in str_expt:
        if 'and' in str_expt:
            final_folder = 'Nurdle_sand'
        elif 'ater' in str_expt:
            final_folder = 'Nurdle_water'
        file_str = r'\Cal_' + str_expt.replace("% ", "_") + '.png'  # this didn't work but that's okay...
    elif 'hav' and 'ellet' not in str_expt:
        print('Invalid name given as str_expt parameter. Please use Shaved Plastic or Shavings for MP, and Pellets for Nurdles.')
        sys.exit()  # want to exit this script and not save the plot
    file_path = r"D:\MSc Results\SavedPlots\Calibrated_Separate" + '\\' + final_folder
    
    print(file_path + file_str)
    #plt.savefig(file_path + file_str, bbox_inches='tight')  # removes whitespace in the file once saved
    plt.show()
    
    return df_in


