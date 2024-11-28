# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:12:34 2024

Calibration script for applying the same calibration from the pure water (or sand)
hot and cold experiments, to the rest of the experiments being plotted -
but now multiple experiments (different percentages) at once.
Pkl files are used to calibrate these plastic experiments.


@author: kplo373
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.interpolate import interp1d
#import matplotlib.cm as cm
from types import SimpleNamespace


def apply_calibration_multiple(df_in_dict, str_expt):
    print(df_in_dict.keys())  # dict_keys(['df0', 'df5', 'df10', 'df25', 'df50', 'df100'])
    params = SimpleNamespace(**df_in_dict)
    df0 = params.df0
    df5 = params.df5
    df10 = params.df10
    df25 = params.df25
    df50 = params.df50
    df100 = params.df100
    
    print(df0.columns)  # Index(['temperature_CS', 'stdev_CS', 'sterr_CS', 'temperature_Op', 'stdev_Op','sterr_Op'])
    # get temperature arrays per percentage of plastic from dfs above, all are raw data
    x0 = np.array(df0['temperature_CS']).reshape(-1, 1)
    x5 = np.array(df5['temperature_CS']).reshape(-1, 1)
    x10 = np.array(df10['temperature_CS']).reshape(-1, 1) 
    x25 = np.array(df25['temperature_CS']).reshape(-1, 1)
    x50 = np.array(df50['temperature_CS']).reshape(-1, 1)
    x100 = np.array(df100['temperature_CS']).reshape(-1, 1)
    
    y0 = np.array(df0['temperature_Op']).reshape(-1, 1)
    y5 = np.array(df5['temperature_Op']).reshape(-1, 1)
    y10 = np.array(df10['temperature_Op']).reshape(-1, 1)
    y25 = np.array(df25['temperature_Op']).reshape(-1, 1)
    y50 = np.array(df50['temperature_Op']).reshape(-1, 1)
    y100 = np.array(df100['temperature_Op']).reshape(-1, 1)
    
    if 'ater' in str_expt:
        print('PICKED WATER CALIBRATION OPTION')
        # Load pure water calibration table from saved csv file
        filepath = r'D:\MSc Results\calTable.csv'  # this has the whole df_in for pure water
        calTable_df = pd.read_csv(filepath)
        print(calTable_df.columns)
        
        # Interpolate to match each y % values with calibration adjustments (as they will have different lengths)
        interp_func = interp1d(
           calTable_df.index,
           calTable_df['y_cal_adj'],
           kind='linear',  # to ensure linear interpolation
           bounds_error=False,
           fill_value="extrapolate")
        
        # Applying interpolation function to all y arrays
        y_cal_adj_interp0 = interp_func(y0.ravel())
        y_cal_adj_interp5 = interp_func(y5.ravel())
        y_cal_adj_interp10 = interp_func(y10.ravel())
        y_cal_adj_interp25 = interp_func(y25.ravel())
        y_cal_adj_interp50 = interp_func(y50.ravel())
        y_cal_adj_interp100 = interp_func(y100.ravel())
    
        # Apply the calibration adjustments (subtraction for correction)
        y_corr0 = y0.ravel() - y_cal_adj_interp0  # after this calibration, the y_sterr (and y_stdev) needs to include the y_cal_adj_interp sterr.
        y_corr5 = y5.ravel() - y_cal_adj_interp5
        y_corr10 = y10.ravel() - y_cal_adj_interp10
        y_corr25 = y25.ravel() - y_cal_adj_interp25
        y_corr50 = y50.ravel() - y_cal_adj_interp50
        y_corr100 = y100.ravel() - y_cal_adj_interp100
        
        # Store corrected values in each DataFrame
        df0['y_corrected'] = y_corr0
        df5['y_corrected'] = y_corr5
        df10['y_corrected'] = y_corr10
        df25['y_corrected'] = y_corr25
        df50['y_corrected'] = y_corr50
        df100['y_corrected'] = y_corr100
        
        # Calculate the y_sterr for all calibrated/corrected y percentages, and store in each df
        df0['y_corr_sterr'] = np.sqrt( (df0['sterr_Op'])**2 + ( np.sqrt(df0['sterr_Op']**2 + df0['sterr_CS']**2) )**2 )  # =sqrt(y_se^2 + (sqrt(y_se^2 + x_se^2))^2)
        df5['y_corr_sterr'] = np.sqrt( (df5['sterr_Op'])**2 + ( np.sqrt(df5['sterr_Op']**2 + df5['sterr_CS']**2) )**2 )
        df10['y_corr_sterr'] = np.sqrt( (df10['sterr_Op'])**2 + ( np.sqrt(df10['sterr_Op']**2 + df10['sterr_CS']**2) )**2 )
        df25['y_corr_sterr'] = np.sqrt( (df25['sterr_Op'])**2 + ( np.sqrt(df25['sterr_Op']**2 + df25['sterr_CS']**2) )**2 )
        df50['y_corr_sterr'] = np.sqrt( (df50['sterr_Op'])**2 + ( np.sqrt(df50['sterr_Op']**2 + df50['sterr_CS']**2) )**2 )
        df100['y_corr_sterr'] = np.sqrt( (df100['sterr_Op'])**2 + ( np.sqrt(df100['sterr_Op']**2 + df100['sterr_CS']**2) )**2 )
        
        # Calculate the mean standard errors for both x (thermocouples) and y_corrected (Optris) data
        xSE0 = np.mean(df0['sterr_CS'])
        xSE5 = np.mean(df5['sterr_CS'])
        xSE10 = np.mean(df10['sterr_CS'])
        xSE25 = np.mean(df25['sterr_CS'])
        xSE50 = np.mean(df50['sterr_CS'])
        xSE100 = np.mean(df100['sterr_CS'])
        print(xSE0, xSE5, xSE10, xSE25, xSE50, xSE100)
        
        
        ycSE0 = np.mean(df0['y_corr_sterr'])
        ycSE5 = np.mean(df5['y_corr_sterr'])
        ycSE10 = np.mean(df10['y_corr_sterr'])
        ycSE25 = np.mean(df25['y_corr_sterr'])
        ycSE50 = np.mean(df50['y_corr_sterr'])
        ycSE100 = np.mean(df100['y_corr_sterr'])
        print(ycSE0, ycSE5, ycSE10, ycSE25, ycSE50, ycSE100)
        

    # Load pure sand calibration table for sand experiments as a second step
    elif 'and' in str_expt:
        print('PICKED SAND CALIBRATION OPTION')
        filepathSand = r'D:\MSc Results\calTableSand.csv'
        calTable_dfSand = pd.read_csv(filepathSand)
        print(calTable_dfSand.columns)
         
        # Interpolate to match each y % values with calibration adjustments (as they will have different lengths)
        interp_func = interp1d(
           calTable_dfSand.index,
           calTable_dfSand['y_cal_adj'],
           kind='linear',  # to ensure linear interpolation
           bounds_error=False,
           fill_value="extrapolate")
         
        # Applying interpolation function to all y arrays
        y_cal_adj_interp0 = interp_func(y0.ravel())
        y_cal_adj_interp5 = interp_func(y5.ravel())
        y_cal_adj_interp10 = interp_func(y10.ravel())
        y_cal_adj_interp25 = interp_func(y25.ravel())
        y_cal_adj_interp50 = interp_func(y50.ravel())
        y_cal_adj_interp100 = interp_func(y100.ravel())
    
        # Apply the calibration adjustments (subtraction for correction)
        y_corr0 = y0.ravel() - y_cal_adj_interp0
        y_corr5 = y5.ravel() - y_cal_adj_interp5
        y_corr10 = y10.ravel() - y_cal_adj_interp10
        y_corr25 = y25.ravel() - y_cal_adj_interp25
        y_corr50 = y50.ravel() - y_cal_adj_interp50
        y_corr100 = y100.ravel() - y_cal_adj_interp100
        
        # Store corrected values in each DataFrame
        df0['y_corrected'] = y_corr0
        df5['y_corrected'] = y_corr5
        df10['y_corrected'] = y_corr10
        df25['y_corrected'] = y_corr25
        df50['y_corrected'] = y_corr50
        df100['y_corrected'] = y_corr100

        # Calculate the y_sterr for all calibrated/corrected y percentages, and store in each df
        df0['y_corr_sterr'] = np.sqrt( (df0['sterr_Op'])**2 + ( np.sqrt(df0['sterr_Op']**2 + df0['sterr_CS']**2) )**2 )  # =sqrt(y_se^2 + (sqrt(y_se^2 + x_se^2))^2)
        df5['y_corr_sterr'] = np.sqrt( (df5['sterr_Op'])**2 + ( np.sqrt(df5['sterr_Op']**2 + df5['sterr_CS']**2) )**2 )
        df10['y_corr_sterr'] = np.sqrt( (df10['sterr_Op'])**2 + ( np.sqrt(df10['sterr_Op']**2 + df10['sterr_CS']**2) )**2 )
        df25['y_corr_sterr'] = np.sqrt( (df25['sterr_Op'])**2 + ( np.sqrt(df25['sterr_Op']**2 + df25['sterr_CS']**2) )**2 )
        df50['y_corr_sterr'] = np.sqrt( (df50['sterr_Op'])**2 + ( np.sqrt(df50['sterr_Op']**2 + df50['sterr_CS']**2) )**2 )
        df100['y_corr_sterr'] = np.sqrt( (df100['sterr_Op'])**2 + ( np.sqrt(df100['sterr_Op']**2 + df100['sterr_CS']**2) )**2 )
        
        #print(df0['y_corr_sterr'])
        #print(df0.columns)
        
        # Calculate the mean standard errors for both x (thermocouples) and y_corrected (Optris) data
        xSE0 = np.mean(df0['sterr_CS'])
        xSE5 = np.mean(df5['sterr_CS'])
        xSE10 = np.mean(df10['sterr_CS'])
        xSE25 = np.mean(df25['sterr_CS'])
        xSE50 = np.mean(df50['sterr_CS'])
        xSE100 = np.mean(df100['sterr_CS'])
        print(xSE0, xSE5, xSE10, xSE25, xSE50, xSE100)
        
        
        ycSE0 = np.mean(df0['y_corr_sterr'])
        ycSE5 = np.mean(df5['y_corr_sterr'])
        ycSE10 = np.mean(df10['y_corr_sterr'])
        ycSE25 = np.mean(df25['y_corr_sterr'])
        ycSE50 = np.mean(df50['y_corr_sterr'])
        ycSE100 = np.mean(df100['y_corr_sterr'])
        print(ycSE0, ycSE5, ycSE10, ycSE25, ycSE50, ycSE100)

    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_roundH(n):  # create a hot function to round up if .3 or higher, or round down if less than .3. 
        if n - math.floor(n) < 0.3:
            return math.floor(n)
        return math.ceil(n)
    
    def normal_roundC(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    # Setting the limits for the plot
    lower_limit = min(y_corr0[0], x0[0], y_corr5[0], x5[0], y_corr10[0], x10[0], y_corr25[0], x25[0],
                      y_corr50[0], x50[0], y_corr100[0], x100[0])
    lower_lim = normal_roundC(lower_limit) - 1
    
    upper_limit = max(y_corr0[-1], x0[-1], y_corr5[-1], x5[-1], y_corr10[-1], x10[-1], 
                          y_corr25[-1], x25[-1], y_corr50[-1], x50[-1], y_corr100[-1], x100[-1])
    upper_lim = normal_roundH(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    y_list = [y_corr0, y_corr5, y_corr10, y_corr25, y_corr50, y_corr100]
        

    # Plot Calibrated Results, Add in Reference Line too
    plt.figure(figsize=(5, 5))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    
    # Combine all x and y arrays into a list (for plotting in a green spectrum)
    x_list = [x0, x5, x10, x25, x50, x100]
    # setting y_list above in the if/elif statements

    # Specify the percentage labels
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    colors = ['r', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']  # just using the colours of the rainbow for now    
    
    # Set the colormap to 'cool' and get 6 shades of blue, purple, pink
    #cmap = cm.get_cmap('jet', 6)
    #colors = cmap(np.linspace(0.4, 1, 6))  # Creates 6 shades ranging from lighter to darker green


    # Plot the 1:1 line across the entire plot from corner to corner
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference')
 
    for i in range(6):
        plt.plot(x_list[i], y_list[i], lw=1, color=colors[i], label=f'Calibrated {labels[i]}', alpha=0.6)  # plotting the data in a green spectrum
        
    #plt.text(23, 12, '(Using Pure Water)')  # adding in text to the plot in the bottom RH corner
    plt.axvline(x=21, color='k', linestyle='dotted')
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)
    
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.title('Calibrated Comparison For ' + str_expt)
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
    
    # Create a dictionary for x and for y to return and extract the data from in the next function (deltaT) 
    df_out_dict = {'df0': df0, 'df5': df5, 'df10': df10, 'df25': df25, 'df50': df50, 'df100': df100}

    
    return df_out_dict

# run this script through the main() function script