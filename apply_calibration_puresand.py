# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:27:25 2024

To calibrate according to the pure sand test (this calibration will only
be applied to the sand + pellets and sand + microplastic mixtures).
Setting up calibration table for sand in this function.

@author: adamk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression


def apply_calibration_sand(df_in, str_expt):   # df_in is the df from after water calibration has been applied   
    # 3. Apply correction to the y_corrected column now!
    x_nctrl = np.array(df_in['temperature_CS']).reshape(-1, 1)
    y_nctrl = np.array(df_in['y_corrected']).reshape(-1, 1)  # this was corrected using baseline correction in pure water calibration previously
    
    y_cal_vals =  y_nctrl - x_nctrl
    y_nctrl_corrected = y_nctrl - y_cal_vals
    df_in['y_corrected_sand'] = y_nctrl_corrected  # store sand corrected y values as another column in the non-control sample
    
    # Create correction look up table
    cal_table_df = pd.DataFrame({'y_val': y_nctrl.ravel(), 'y_cal_adj': y_cal_vals.ravel()})
    cal_table_df.index = np.around(cal_table_df['y_val'], decimals=4)
    cal_table_df = cal_table_df.drop('y_val', axis=1)
    cal_table_df = cal_table_df.sort_index()  # maybe this gets rid of the column header for the index? that's okay though
    
    
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
    
    # Fit a linear model to extrapolate -- might not be linear for sand!! Try for now though...
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
    extended_calTable_df.to_csv(r'D:\MSc Results\calTableSand.csv')
    
    
    
    r'''
    # Get the nearest y value in the cal_table_df.index to the y variables in the different mixtures' data
    sel_cal_vals = np.zeros(len(y_nctrl))  # Preallocate for the nearest_y_vals collected in the for loop
    for i in range(len(y_nctrl)):
        y = float(y_nctrl[i][0])  # extract the first element from the array, as y_ntrl is 2D
        nearest_index = calTable_unique_df.index.get_indexer([y], method='nearest')[0]  # get nearest index
        
        # Check if the nearest_index is valid
        if nearest_index >= 0 and nearest_index < len(calTable_unique_df):
            nearest_y_val = calTable_unique_df.iloc[nearest_index, 0]  # collecting values from the calibrated column of the lookup table, not the index
            sel_cal_vals[i] = nearest_y_val  # Store the nearest y value
        else:
            print(f"Warning: Nearest index for y={y} is not valid.")
    
    # what am I doing with this sel_cal_vals array after all?? Is an array of selected calibration values.
    #print(sel_cal_vals)  # do I need to plot them? Or are these the adjustments to apply?
    # put them into the df_in??
    # my sel_cal_vals are currently the same as y_nctrl. Need to be same as y_nctrl_corrected! Wrong column
    # tried first column, now they are just the actual differences, ranging 0.66 to 6.4...
    # the index is y_val = y_nctrl, first column (0) is y_cal_adj, ranging from 5.94 up and down to 1.39
    # can't use the index, so have to apply the first column to the y_nctrl somehow, like done above, minus??
    cal_y = y_nctrl[:, 0] - sel_cal_vals  # use these for the actual mixture data
    print(cal_y)  # this cal_y is a noisy version of y_nctrl_corrected!
    '''

         
    
    # Save the corrected non-control sample as csv file
    #df_in.to_csv(r'D:\MSc Results\corrected_control_sample.csv')  # this only gives a y_corrected column though. Need adj column!

    #print(y_nctrl)
    print(y_nctrl_corrected)
   


    # Inverse transform the predicted values to get them back to the original scale
    #x_pred_plastic = scaler_x.inverse_transform(x_pred_plastic_scaled.reshape(-1, 1))  # use this ndarray while plotting! Has the calibration applied to it

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
    #plt.plot(x_pred, y_comb, 'o', color='lightgreen', label='Calibrated Data (Using Pure Water SVM)')
    plt.plot(x_nctrl, y_nctrl_corrected, color='violet', lw=4, label='Pure Sand Calibration')
    plt.plot(x_nctrl, y_nctrl, 'green', label='Pure Water Calibration')
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
    plt.savefig(file_path + file_str, bbox_inches='tight')  # removes whitespace in the file once saved
    plt.show()
    
    return df_in

# run this script through the main() function script