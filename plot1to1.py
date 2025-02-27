# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:42:13 2024

Script for plotting 1:1 plots of raw temperature data from the 
thermocouples and thermal camera dataframe.

@author: kplo373
"""
import matplotlib.pyplot as plt
import sys

# str_expt parameter should be a string of the type of experiment done, e.g. '50% Pellet-Sand'
def plot1to1(df_in, str_expt):
    T_Op = df_in['temperature_Op']  # extracting the temperature arrays
    T_CS = df_in['temperature_CS']
    
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(T_CS.iloc[0], T_Op.iloc[0])
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max( max(T_CS), max(T_Op) )
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below
    print('Limits:', lower_lim, upper_lim)
    
    plt.figure(figsize=(6, 6))  # make it into a square shape, same axes limits!
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)

    # To plot the 1:1 reference line
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    plt.plot(T_CS, T_Op, 'b', label='Raw Data')  # listing this after errorbars and as dots allow it to show up over black errorbars    
    plt.title('Sensor Comparison For ' + str_expt)  # including what percentage of plastic etc.
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.grid()
    plt.legend()
    if 'hav' in str_expt:
        if 'and' in str_expt:
            final_folder = 'MP_sand'
        elif 'ater' in str_expt:
            final_folder = 'MP_water'
        file_str = r'\Raw_' + str_expt.replace("% Shavings", "_MP") + '.png'
    elif 'ellet' in str_expt:
        if 'and' in str_expt:
            final_folder = 'Nurdle_sand'
        elif 'ater' in str_expt:
            final_folder = 'Nurdle_water'
        file_str = r'\Raw_' + str_expt.replace("% Pellets", "_nurd") + '.png'
    elif 'hav' and 'ellet' not in str_expt:
        print('Invalid name given as str_expt parameter. Please use Shaved Plastic or Shavings for MP, and Pellets for Nurdles.')
        sys.exit()  # want to exit this script and not save the plot
    file_path = r"D:\MSc Results\SavedPlots\Raw_Separate" + '\\' + final_folder
    
    print(file_path + file_str)
    plt.savefig(file_path + file_str, bbox_inches='tight')  # removes the weird whitespace in the file once saved
    plt.show()    
    
    
    return

