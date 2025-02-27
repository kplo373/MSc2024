# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:31:50 2025

Updated version of get_deltaT.py, to plot the 6x individual plastic
percentages on their own, WITH an error envelope to show the uncertainty.

Python script with a function that calculates the delta T value, which
represents the temperature difference from the reference 1:1 line of
the calibrated raw data. It uses the outputs from the apply_calibration.py
script and function.

DeltaT is then used to plot against the environmental temperature.

@author: kplo373
"""

import numpy as np
import matplotlib.pyplot as plt

# y_limits parameter below is a list of two elements: the minimum y value, then the max y
def get_deltaT_errors(df_in, text_str, percentage, colour, y_limits):
    print(df_in.columns)
    x = np.array(df_in['temperature_CS']).ravel()
    y = np.array(df_in['y_corrected']).ravel()  # both sand and water calibrations are saved as y_corrected columns

    lower_limit = min(x[0], y[0])
    upper_limit = max( max(x), max(y) )
    print(lower_limit, upper_limit)  # looks good: 15.716666666666667 29.458437940024325
 
    x_ref = x
    #print(np.shape(x_ref))
    
    # Time to calculate deltaT
    deltaT = np.zeros(len(y))
    for yi in range(len(y)):
        delT = y[yi] - x_ref[yi]
        deltaT[yi] = delT
    
    
    # Using the standard error measurements for y_corrected and x to calculate standard error for deltaT
    delT_sterr = np.sqrt( (df_in['y_corr_sterr'])**2 + (df_in['sterr_CS'])**2 )  # = sqrt(y_corr_sterr^2 + x_sterr^2)
    # Compute the error envelope bounds per plastic %
    y_upper = deltaT + delT_sterr
    y_lower = deltaT - delT_sterr 
    
    print('y envelope range:', min(y_lower), max(y_upper))    

    # Plotting deltaT against Environmental Temperature
    plt.plot(x, deltaT, colour, label=r'$\Delta T$')
    plt.fill_between(x, y_lower, y_upper, color=colour, alpha=0.5, label='Error envelope')  # plotting error envelope
    plt.axhline(y=0, color='k', linestyle='--')
    plt.axvline(x=21, color='k', linestyle='dotted')
    plt.xlabel('Environmental Temperature (degrees Celsius)')
    plt.ylabel(r'$\Delta T$ (degrees Celsius)')
    plt.title(percentage + '% ' + text_str + ' Temperature Difference')
    plt.ylim(y_limits[0], y_limits[1])
    plt.legend
    plt.grid()
    if 'hav' in text_str:
        if 'and' in text_str:
            final_folder = 'MP_sand'
        elif 'ater' in text_str:
            final_folder = 'MP_water'
        file_str = r'\TempDiff_' + text_str.replace("% Shavings", "_MP") + '.png'
    elif 'ellet' in text_str:
        if 'and' in text_str:
            final_folder = 'Nurdle_sand'
        elif 'ater' in text_str:
            final_folder = 'Nurdle_water'
        file_str = r'\TempDiff_' + text_str.replace("% Pellets", "_nurd") + '.png'
    file_path = r"D:\MSc Results\SavedPlots\TempDiff_Separate" + '\\' + final_folder
    
    print(file_path + file_str)
    plt.savefig(file_path + file_str, bbox_inches='tight')  # removes whitespace in the file once saved
    plt.show()
    
    return delT_sterr
