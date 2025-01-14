# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 09:36:21 2024

(older version)
Python script with a function that calculates the delta T value, which
represents the temperature difference from the reference 1:1 line of
the calibrated raw data. It uses the outputs from the apply_calibration.py
script and function.

DeltaT will be used to plot against the environmental temperature in 
the next plot...

@author: adamk
"""
import numpy as np
import matplotlib.pyplot as plt
import sys


def get_deltaT(df_in, text_str):
    print(df_in.columns)
    x = np.array(df_in['temperature_CS']).ravel()
    
    if 'ater' in text_str:
        y = np.array(df_in['y_corrected']).ravel()
    elif 'and' in text_str:
        y = np.array(df_in['y_corrected_sand']).ravel()
    

    lower_limit = min(x[0], y[0])
    upper_limit = max( max(x), max(y) )
    print(lower_limit, upper_limit)  # looks good: 15.716666666666667 29.458437940024325
    
 
    #ref_line = plt.plot(x_comb, x_comb)
    x_ref = x
    print(np.shape(x_ref))
    
    # Time to calculate deltaT
    deltaT = np.zeros(len(y))
    for yi in range(len(y)):
        delT = y[yi] - x_ref[yi]
        deltaT[yi] = delT    

    # Plotting deltaT against Environmental Temperature
    plt.plot(x, deltaT, 'r', label='DeltaT')
    plt.axhline(y=0, color='k', linestyle='--')
    plt.xlabel('Environmental Temperature (degrees Celsius)')
    plt.ylabel(r'$\Delta T$ (degrees Celsius)')
    plt.title(text_str +' Temperature Difference')
    plt.grid()
    if 'hav' in text_str:
        if 'and' in text_str:
            final_folder = 'MP_sand'
        elif 'ater' in text_str:
            final_folder = 'MP_water'
        file_str = r'\TempDiff_' + text_str.replace("% Shavings", "_MP") + '.png'  # not sure if I can have % signs in a filename, so taking it out to be safe...
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
    
    return deltaT
