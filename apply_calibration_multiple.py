# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:12:34 2024

Calibration script for applying the same calibration from the pure water
hot and cold experiments, to the rest of the experiments being plotted -
but now multiple experiments (different percentages) at once.
Pkl files are used to calibrate these plastic experiments.


@author: kplo373
"""


###adapt this code for multiple percentages!! get output from plot1to1_multiple.py


# Fitting the Pure Water Calibration SVM to this raw data (using ChatGPT)
import joblib
import numpy as np
import matplotlib.pyplot as plt
import sys


def apply_calibration_multiple(df_cold, df_hot, str_expt):
    #print(df_cold.columns)
    #print(df_hot.columns)
    
    # get temperature arrays per percentage of plastic from dfs above
    tempCSc0 = np.array(df_cold['tempCS0'])
    tempOpc0 = np.array(df_cold['tempOp0'])
    tempCSh0 = np.array(df_hot['tempCS0'])
    tempOph0 = np.array(df_hot['tempOp0'])
    
    tempCSc5 = np.array(df_cold['tempCS5'])
    tempOpc5 = np.array(df_cold['tempOp5'])
    tempCSh5 = np.array(df_hot['tempCS5'])
    tempOph5 = np.array(df_hot['tempOp5']) 
    
    tempCSc10 = np.array(df_cold['tempCS10'])
    tempOpc10 = np.array(df_cold['tempOp10'])
    tempCSh10 = np.array(df_hot['tempCS10'])
    tempOph10 = np.array(df_hot['tempOp10']) 
    
    tempCSc25 = np.array(df_cold['tempCS25'])
    tempOpc25 = np.array(df_cold['tempOp25'])
    tempCSh25 = np.array(df_hot['tempCS25'])
    tempOph25 = np.array(df_hot['tempOp25']) 
    
    tempCSc50 = np.array(df_cold['tempCS50'])
    tempOpc50 = np.array(df_cold['tempOp50'])
    tempCSh50 = np.array(df_hot['tempCS50'])
    tempOph50 = np.array(df_hot['tempOp50']) 
    
    tempCSc100 = np.array(df_cold['tempCS100'])
    tempOpc100 = np.array(df_cold['tempOp100'])
    tempCSh100 = np.array(df_hot['tempCS100'])
    tempOph100 = np.array(df_hot['tempOp100'])
    
    
    # Load the saved model and scalers
    svr_rbf_pure_water = joblib.load(r"D:\MSc Results\svr_rbf_pure_water.pkl")
        #r"D:\MSc Results\svr_rbf_pure_water.pkl")
    scaler_y_pure_water = joblib.load(r"D:\MSc Results\scaler_y_pure_water.pkl")
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
    def normal_roundH(n):  # create a hot function to round up if .27 or higher, or round down if less than .27. Calibration makes data flick up.
        if n - math.floor(n) < 0.27:
            return math.floor(n)
        return math.ceil(n)
    
    def normal_roundC(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(x_cold[0,0], y_cold[0,0])
    lower_lim = normal_roundC(lower_limit) - 1

    upper_limit = max( max(x_hot_asc), max(y_hot_asc) )
    upper_lim = normal_roundH(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # Plot SVM Results, Add in Reference Line too
    plt.figure(figsize=(7, 7))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    plt.plot(x_comb, y_pred_plastic, 'o', color='lightgreen', label='Calibrated Data (Using Pure Water SVM)')
    plt.plot(x_comb, y_pred_plastic, color='green', lw=2, label='Calibrated Curve')
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
    
    return x_comb, y_pred_plastic  # this will need to be a dataframe maybe... will have x_comb and y_pred_plastic for every percentage!

# run this script through the main() function script