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

def get_deltaT(y_pred_plastic):
    # is this just y_pred_plastic - reference_line_ycomponent?
    # or is it the whole calibrated line equation (don't have this yet=best fit line?) - Reference line eqn (y=x)
    
    # how to get y component of reference line? y = x, can I make a linspace up to a value? at x=35, y=35.
    ref_y = np.linspace(0, 35, len(y_pred_plastic))  # needs to be same length as input array
    
    deltaT = y_pred_plastic - ref_y
    
    import matplotlib.pyplot as plt
    dummy_x = np.linspace(0, 35, len(y_pred_plastic))
    plt.plot(dummy_x, deltaT)
    plt.show()
    
    
    return deltaT

# takes a while to plot... very interesting haha
    
