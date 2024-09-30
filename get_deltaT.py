# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 09:36:21 2024

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


def get_deltaT(x_comb, y_pred_plastic, text_str):
    x = x_comb.ravel()  # to shrink the ndarrays to arrays
    y = y_pred_plastic.ravel()
    #print(type(x), type(y))  # should be np.array, are ndarrays
    # Get line of best fit to represent the applied calibration curve
    #z = np.polyfit(x, y, 4)  # which degree is best? 4 seems to fit data best
    #p = np.poly1d(z)  # creating a polyfit function
    #t = np.linspace(min(x), max(x), len(x))  
    
    
    # need to get ref_line as an equation
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.4:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(x[0], y[0])
    lower_lim = normal_round(lower_limit) - 1
    upper_limit = max( max(x), max(y) )
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # Reference line is y=x, will create a linspace for x
    x_ref = np.linspace(lower_limit, upper_limit, len(y))
    
    # Don't use the polyfit line of best fit to get my line equation! Go point by point
    deltaT = np.zeros(len(y))
    for yi in range(len(y)):
        delT = y[yi] - x_ref[yi]
        deltaT[yi] = delT
    
    
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'o', color = 'orange', label='Calibrated Data')
    #plt.plot(t, p(t), '-', color='black', label='Best Fit Curve')
    

    # Plot the 1:1 line across the entire plot from corner to corner
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)
    
    plt.title('Best Fit Line for Calibrated '+ text_str +' Data')
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.legend()
    plt.grid()
    plt.show()
    
    # Time to calculate deltaT
    #deltaT = p(x) - x
    #print(deltaT)
    plt.plot(x, deltaT, 'k', label='DeltaT')
    plt.xlabel('Environmental Temperature (degrees Celsius)')
    plt.ylabel(r'$\Delta T_y$ (degrees Celsius)')
    plt.title(text_str +' Temperature Difference (y)')
    #plt.ylim(0, max(deltaT))
    plt.grid()
    plt.show()
    
    return
