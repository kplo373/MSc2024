# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:33:25 2024

**Fitting the Pure Water Calibration to this raw data, and setting up the calibration table here.**
Have left in the SVR stuff just in case we want to go back to it...
but only using look up table for calibration in apply_calibration.py,
which we create in this script.

@author: kplo373
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.linear_model import LinearRegression


def apply_calibration(df_in, str_expt):    
    # Apply correction to non-control samples, load non-control sample data (x and y are independent)
    x_nctrl = np.array(df_in['temperature_CS']).reshape(-1, 1)
    y_nctrl = np.array(df_in['temperature_Op']).reshape(-1, 1)
    
    y_cal_vals =  y_nctrl - x_nctrl
    y_nctrl_corrected = y_nctrl - y_cal_vals
    df_in['y_corrected'] = y_nctrl_corrected  # store corrected y values as another column in the non-control sample
    
    # Create correction look up table
    cal_table_df = pd.DataFrame({'y_val': y_nctrl.ravel(), 'y_cal_adj': y_cal_vals.ravel()})
    cal_table_df.index = np.around(cal_table_df['y_val'], decimals=4)
    cal_table_df = cal_table_df.drop('y_val', axis=1)
    cal_table_df = cal_table_df.sort_index()
    
    
    # Reset the index and create a new column
    cal_table_df_reset = cal_table_df.reset_index()
    calTable_unique_df = cal_table_df_reset.drop_duplicates(subset='y_val')  # removing duplicates in the y_val column
    calTable_unique_df.loc[:, 'y_val'] = pd.to_numeric(calTable_unique_df['y_val'], errors='coerce')  # ensuring 'y_val' is numeric and checking for invalid values
    calTable_unique_df = calTable_unique_df.dropna(subset=['y_val'])  # removing any rows where 'y_val' is NaN after conversion
    calTable_unique_df = calTable_unique_df.set_index('y_val')  # set 'y_val' as the index
    
    
    # Step 1: Fit a linear model to the lower range of the calibration data
    lower_bound_data = calTable_unique_df.loc[calTable_unique_df.index <= calTable_unique_df.index.min() + 1]  # selecting points near the minimum
    X_lower = lower_bound_data.index.values.reshape(-1, 1)  # Reshape for regression
    y_lower = lower_bound_data['y_cal_adj'].values
    
    # Fit a linear model to extrapolate
    model = LinearRegression()
    model.fit(X_lower, y_lower)
    
    # Step 2: Extend calibration adjustments for temperatures below the minimum
    min_temp = calTable_unique_df.index.min()
    extended_temps = np.linspace(min_temp - 1, min_temp - 5, 10).reshape(-1, 1)  # Generate temperatures down to ~5 degrees below min
    extended_adjustments = model.predict(extended_temps)
    
    # Step 3: Create an extended DataFrame and append to original
    extended_df = pd.DataFrame(extended_adjustments, index=extended_temps.ravel(), columns=['y_cal_adj'])
    extended_calTable_df = pd.concat([extended_df, calTable_unique_df]).sort_index()
    
    
    # Save the extended calibration table for future use
    extended_calTable_df.to_csv(r'D:\MSc Results\calTable.csv')

    # Save the corrected non-control sample as csv file
    df_in.to_csv(r'D:\MSc Results\corrected_control_sample.csv')  # this only gives a y_corrected column though. Need adj column!

    #print(y_nctrl)
    print(y_nctrl_corrected)
   
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_roundH(n):  # create a hot function to round up if .27 or higher, or round down if less than .27. Calibration makes data flick up.
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

    # Plot SVM Results, Add in Reference Line too
    plt.figure(figsize=(7, 7))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    plt.plot(x_nctrl, y_nctrl_corrected, color='lime', lw=4, label='Pure Water Calibration')
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
        file_str = r'\Cal_' + str_expt.replace("% Shavings", "_MP") + '.png'
    elif 'ellet' in str_expt:
        if 'and' in str_expt:
            final_folder = 'Nurdle_sand'
        elif 'ater' in str_expt:
            final_folder = 'Nurdle_water'
        file_str = r'\Cal_' + str_expt.replace("% ", "_") + '.png'
    elif 'hav' and 'ellet' not in str_expt:
        print('Invalid name given as str_expt parameter. Please use Shaved Plastic or Shavings for MP, and Pellets for Nurdles.')
        sys.exit()  # want to exit this script and not save the plot
    file_path = r"D:\MSc Results\SavedPlots\Calibrated_Separate" + '\\' + final_folder
    
    print(file_path + file_str)
    plt.savefig(file_path + file_str, bbox_inches='tight')  # removes whitespace in the file once saved
    plt.show()
    
    return df_in

# run this script through the main() function script
