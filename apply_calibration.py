# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:33:25 2024

Calibration script for applying the same calibration from the pure water
hot and cold experiments, to the rest of the experiments being plotted.
Pkl files are used to calibrate these plastic experiments.

@author: kplo373
"""

# Fitting the Pure Water Calibration SVM to this raw data (using ChatGPT)
import joblib
import numpy as np
import matplotlib.pyplot as plt


def apply_calibration(df_cold, df_hot):
    
    # get tempCScold, tempCShot, tempOpcold, tempOphot from dfs above
    tempCScold = np.array(df_cold['tempCS'])
    tempCShot = np.array(df_cold['tempCS'])
    tempOpcold = np.array(df_cold['tempOp'])
    tempOphot = np.array(df_hot['tempOp'])
    
    # Load the saved model and scalers
    svr_rbf_pure_water = joblib.load(r"C:\Users\kplo373\Documents\GitHub\MSc2024\old_scripts\svr_rbf_pure_water.pkl")
        #r"D:\MSc Results\svr_rbf_pure_water.pkl")
    scaler_y_pure_water = joblib.load(r"C:\Users\kplo373\Documents\GitHub\MSc2024\old_scripts\scaler_y_pure_water.pkl")
        #r"D:\MSc Results\scaler_y_pure_water.pkl")
    
    # Prepare the plastic-water data
    x_cold = tempCScold.reshape(-1, 1)  # if an error, can do tempC1cold.to_numpy().reshape...
    x_hot_descending = tempCShot.reshape(-1, 1)  # this series begins with the hottest value... need to reverse it somehow
    x_hot_asc = x_hot_descending[::-1]
    
    y_cold = tempOpcold.reshape(-1, 1)
    y_hot_descending = tempOphot.reshape(-1, 1)  # same with this series - begins with hottest value
    y_hot_asc = y_hot_descending[::-1]
    
    x_comb = np.vstack((x_cold, x_hot_asc))
    y_comb = np.concatenate((y_cold, y_hot_asc))
    
    # Scale the y-axis data using the y-scaler from pure water
    y_comb_scaled = scaler_y_pure_water.transform(y_comb)
    
    # Predict using the SVM model trained on pure water data
    y_pred_plastic_scaled = svr_rbf_pure_water.predict(y_comb_scaled)
    # Inverse transform the predicted values to get them back to the original scale
    y_pred_plastic = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled.reshape(-1, 1))  # use this ndarray while plotting! Has the calibration applied to it


    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(x_cold[0,0], y_cold[0,0])
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max(x_hot_asc[-1,0], y_hot_asc[-1,0])
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # To plot the 1:1 reference line - can also plot this in SVM results plot below...
    xlim = plt.gca().get_xlim()  # get the current limits of the plot
    ylim = plt.gca().get_ylim()
    line_min = min(xlim[0], ylim[0])  # determine the start and end points of the 1:1 line
    line_max = max(xlim[1], ylim[1])


    # Plot SVM Results, Add in Reference Line too
    plt.figure(figsize=(8, 8))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    plt.plot(x_comb, y_pred_plastic, 'o', color='lightgreen', label='Calibrated 50% Pellet Water Data (Using Pure Water SVM)')
    plt.plot(x_comb, y_pred_plastic, color='green', lw=2, label='Calibrated 50% Pellet Water Curve')
    # Plot the 1:1 line across the entire plot from corner to corner
    plt.plot([line_min, line_max], [line_min, line_max], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)
    
    plt.xlabel('Campbell Scientific Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Optris Thermal Camera Temperature (degrees Celsius)')
    plt.title('Calibrated 50% Pellet-Water Temperature Comparison')
    plt.legend()
    plt.grid()
    plt.show()
    
    return x_comb, y_pred_plastic

# run this script through the main() function script