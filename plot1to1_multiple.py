# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:18:28 2024

Updated version of plot1to1.py, plotting multiple percentages of the same type
of situation (microplastic and sand) in one plot.

@author: kplo373
"""
import numpy as np
import pandas as pd
from types import SimpleNamespace
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # for creating colour spectrums and legends

# str_expt parameter should be a string of the type of experiment done, e.g. 'Pellet-Sand', or 'Shaved Plastic and Sand'
def plot1to1_multiple(dict_parameters, str_expt):
    #print(dict_parameters.keys())
    params = SimpleNamespace(**dict_parameters)
    df0 = params.df0
    df5 = params.df5
    df10 = params.df10
    df25 = params.df25
    df50 = params.df50
    df100 = params.df100


    T_Op0 = df0['temperature_Op']  # extracting the temperature arrays from 0% (pure sand/water)
    T_CS0 = df0['temperature_CS']
    '''
    stdOp0 = df0['stdev_Op']  # extracting the standard deviation arrays from 0% (pure sand)
    stdCS0 = df0['stdev_CS']
    sterrOp0 = df0['sterr_Op']  # extracting the standard error arrays from 0% MP-sand (pure sand)
    sterrCS0 = df0['sterr_CS']
    '''
    T_Op5 = df5['temperature_Op']  # extracting the temperature arrays from 5% MP-sand
    T_CS5 = df5['temperature_CS']

    # can get stdev and sterr for 5% after this too...
    # and then the 10, 25, 50, and 100% temperature and uncertainty values!
    T_Op10 = df10['temperature_Op']  # extracting the temperature arrays from 10%
    T_CS10 = df10['temperature_CS']
    
    T_Op25 = df25['temperature_Op']  # extracting the temperature arrays from 25% MP-sand
    T_CS25 = df25['temperature_CS']

    T_Op50 = df50['temperature_Op']  # extracting the temperature arrays from 50% MP-sand
    T_CS50 = df50['temperature_CS']

    T_Op100 = df100['temperature_Op']  # extracting the temperature arrays from 100% MP-sand (pure microplastic shavings!)
    T_CS100 = df100['temperature_CS']
    
    # These dataframes are already trimmed, so have removed the 5th and 95th percentile limits
    
    # Combine all x and y arrays into lists (for plotting in red and blue spectrums)
    x_arr = [T_CS0, T_CS5, T_CS10, T_CS25, T_CS50, T_CS100]
    y_arr = [T_Op0, T_Op5, T_Op10, T_Op25, T_Op50, T_Op100]

    # Specify the percentage labels
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    colors = ['r', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']  # just using the colours of the rainbow for now
    
    # Set the colormap to 'Blues' and get 6 shades of blue
    #cmap1 = cm.get_cmap('twilight', 6)
    #colors1 = cmap1(np.linspace(0.4, 1, 6))  # Creates 6 shades ranging from lighter to darker blue - should range the other way for blue, but good for red...
    #cmap2 = cm.get_cmap('Reds', 6)
    #colors2 = cmap2(np.linspace(0.4, 1, 6))

    
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(T_CS0.iloc[0], T_Op0.iloc[0], T_CS5.iloc[0], T_Op5.iloc[0], T_CS10.iloc[0], T_Op10.iloc[0], T_CS25.iloc[0],
                      T_Op25.iloc[0], T_CS50.iloc[0], T_Op50.iloc[0], T_CS100.iloc[0], T_Op100.iloc[0])  # is this the right way to get the limits?
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max(T_CS0.iloc[-1], T_Op0.iloc[-1], T_CS5.iloc[-1], T_Op5.iloc[-1], T_CS10.iloc[-1], T_Op10.iloc[-1], T_CS25.iloc[-1],
                      T_Op25.iloc[-1], T_CS50.iloc[-1], T_Op50.iloc[-1], T_CS100.iloc[-1], T_Op100.iloc[-1])
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below
    print('Limits:', lower_lim, upper_lim)
    
    plt.figure(figsize=(5, 5))  # make it into a square shape, same axes limits!
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)

    # To plot the 1:1 reference line
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference')
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, xerr=seCSc0, color='k')  # just include one errorbar maybe? Is there a better way to show them separately?
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, color='k')   
    plt.axvline(x=21, color='k', linestyle='dotted')  # for approximate ambient temperature
    
    for i in range(6):
        plt.plot(x_arr[i], y_arr[i], lw=1, color=colors[i], label=f'{labels[i]}', alpha=0.6)  #color=colors1[i]
    
    #for j in range(6):  # doing a second separate loop so that the legend lists all cold then hot experiments in the plot
        #plt.plot(x_hot_arr[j], y_hot_arr[j], lw=1, color=colors2[j], label=f'Hot {labels[j]}', alpha=0.6)  # alpha parameter sets transparency/opacity
    
    plt.title('Raw Comparison For ' + str_expt)  # including what percentage of plastic etc.
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.grid()
    plt.legend()
    plt.show()
    
    
    return

