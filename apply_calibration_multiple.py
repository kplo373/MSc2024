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


def apply_calibration_multiple(dict_cold, dict_hot, str_expt):
    print(dict_cold.keys())
    #print(dict_hot.keys)
    
    # get temperature arrays per percentage of plastic from dfs above
    tempCSc0 = np.array(dict_cold['tempCS0'])
    tempOpc0 = np.array(dict_cold['tempOp0'])
    tempCSh0 = np.array(dict_hot['tempCS0'])
    tempOph0 = np.array(dict_hot['tempOp0'])
    
    tempCSc5 = np.array(dict_cold['tempCS5'])
    tempOpc5 = np.array(dict_cold['tempOp5'])
    tempCSh5 = np.array(dict_hot['tempCS5'])
    tempOph5 = np.array(dict_hot['tempOp5']) 
    
    tempCSc10 = np.array(dict_cold['tempCS10'])
    tempOpc10 = np.array(dict_cold['tempOp10'])
    tempCSh10 = np.array(dict_hot['tempCS10'])
    tempOph10 = np.array(dict_hot['tempOp10']) 
    
    tempCSc25 = np.array(dict_cold['tempCS25'])
    tempOpc25 = np.array(dict_cold['tempOp25'])
    tempCSh25 = np.array(dict_hot['tempCS25'])
    tempOph25 = np.array(dict_hot['tempOp25']) 
    
    tempCSc50 = np.array(dict_cold['tempCS50'])
    tempOpc50 = np.array(dict_cold['tempOp50'])
    tempCSh50 = np.array(dict_hot['tempCS50'])
    tempOph50 = np.array(dict_hot['tempOp50']) 
    
    tempCSc100 = np.array(dict_cold['tempCS100'])
    tempOpc100 = np.array(dict_cold['tempOp100'])
    tempCSh100 = np.array(dict_hot['tempCS100'])
    tempOph100 = np.array(dict_hot['tempOp100'])
    
    
    # Load the saved model and scalers
    svr_rbf_pure_water = joblib.load(r"D:\MSc Results\svr_rbf_pure_water.pkl")  # this is giving an error because there are nans in it?
    scaler_y_pure_water = joblib.load(r"D:\MSc Results\scaler_y_pure_water.pkl")
    
    # Prepare the plastic-water data
    x_c0 = tempCSc0.reshape(-1, 1)  # if an error, can do tempC1c0.to_numpy().reshape...
    x_c5 = tempCSc5.reshape(-1, 1)
    x_c10 = tempCSc10.reshape(-1, 1)
    x_c25 = tempCSc25.reshape(-1, 1)
    x_c50 = tempCSc50.reshape(-1, 1)
    x_c100 = tempCSc100.reshape(-1, 1)
    
    x_hot_descending0 = tempCSh0.reshape(-1, 1)  # this series begins with the hottest value... need to reverse it somehow
    x_hot_asc0 = x_hot_descending0[::-1]
    x_hot_descending5 = tempCSh5.reshape(-1, 1)  # 5%
    x_hot_asc5 = x_hot_descending5[::-1]
    x_hot_descending10 = tempCSh10.reshape(-1, 1)  # 10%
    x_hot_asc10 = x_hot_descending10[::-1]
    x_hot_descending25 = tempCSh25.reshape(-1, 1)  # 25%
    x_hot_asc25 = x_hot_descending25[::-1]
    x_hot_descending50 = tempCSh50.reshape(-1, 1)  # 50%
    x_hot_asc50 = x_hot_descending50[::-1]
    x_hot_descending100 = tempCSh100.reshape(-1, 1)  # 100%
    x_hot_asc100 = x_hot_descending100[::-1]
    

    y_c0 = tempOpc0.reshape(-1, 1)
    y_c5 = tempOpc5.reshape(-1, 1)
    y_c10 = tempOpc10.reshape(-1, 1)
    y_c25 = tempOpc25.reshape(-1, 1)
    y_c50 = tempOpc50.reshape(-1, 1)
    y_c100 = tempOpc100.reshape(-1, 1)

    
    y_hot_descending0 = tempOph0.reshape(-1, 1)  # same with this series - begins with hottest value
    y_hot_asc0 = y_hot_descending0[::-1]
    y_hot_descending5 = tempOph5.reshape(-1, 1)  # 5%
    y_hot_asc5 = y_hot_descending5[::-1]
    y_hot_descending10 = tempOph10.reshape(-1, 1)  # 10%
    y_hot_asc10 = y_hot_descending10[::-1]
    y_hot_descending25 = tempOph25.reshape(-1, 1)  # 25%
    y_hot_asc25 = y_hot_descending25[::-1]
    y_hot_descending50 = tempOph50.reshape(-1, 1)  # 50%
    y_hot_asc50 = y_hot_descending50[::-1]
    y_hot_descending100 = tempOph100.reshape(-1, 1)  # 100%
    y_hot_asc100 = y_hot_descending100[::-1]
    

    # Combining the hot and cold arrays per plastic proportion
    x_comb0 = np.vstack((x_c0, x_hot_asc0))  # 0%
    y_comb0 = np.concatenate((y_c0, y_hot_asc0))
    x_comb5 = np.vstack((x_c5, x_hot_asc5))  # 5%
    y_comb5 = np.concatenate((y_c5, y_hot_asc5))
    x_comb10 = np.vstack((x_c10, x_hot_asc10))  # 10%
    y_comb10 = np.concatenate((y_c10, y_hot_asc10))
    x_comb25 = np.vstack((x_c25, x_hot_asc25))  # 25%
    y_comb25 = np.concatenate((y_c25, y_hot_asc25))
    x_comb50 = np.vstack((x_c50, x_hot_asc50))  # 50%
    y_comb50 = np.concatenate((y_c50, y_hot_asc50))
    x_comb100 = np.vstack((x_c100, x_hot_asc100))  # 100%
    y_comb100 = np.concatenate((y_c100, y_hot_asc100))
    

    # Scale the y-axis data using the y-scaler from pure water
    y_comb_scaled0 = scaler_y_pure_water.transform(y_comb0)
    y_comb_scaled5 = scaler_y_pure_water.transform(y_comb5)
    y_comb_scaled10 = scaler_y_pure_water.transform(y_comb10)
    y_comb_scaled25 = scaler_y_pure_water.transform(y_comb25)
    y_comb_scaled50 = scaler_y_pure_water.transform(y_comb50)
    y_comb_scaled100 = scaler_y_pure_water.transform(y_comb100)

    
    # Predict using the SVM model trained on pure water data
    y_pred_plastic_scaled0 = svr_rbf_pure_water.predict(y_comb_scaled0)
    y_pred_plastic_scaled5 = svr_rbf_pure_water.predict(y_comb_scaled5)
    y_pred_plastic_scaled10 = svr_rbf_pure_water.predict(y_comb_scaled10)
    y_pred_plastic_scaled25 = svr_rbf_pure_water.predict(y_comb_scaled25)
    y_pred_plastic_scaled50 = svr_rbf_pure_water.predict(y_comb_scaled50)
    y_pred_plastic_scaled100 = svr_rbf_pure_water.predict(y_comb_scaled100)
    
    # Inverse transform the predicted values to get them back to the original scale
    y_pred_plastic0 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled0.reshape(-1, 1))  # use this ndarray while plotting! Has the calibration applied to it
    y_pred_plastic5 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled5.reshape(-1, 1))
    y_pred_plastic10 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled10.reshape(-1, 1))
    y_pred_plastic25 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled25.reshape(-1, 1))
    y_pred_plastic50 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled50.reshape(-1, 1))
    y_pred_plastic100 = scaler_y_pure_water.inverse_transform(y_pred_plastic_scaled100.reshape(-1, 1))

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

    # not sure what's going on here... are the limits meant to be determined by x_comb or x_c/x_h arrays??
    lower_limit = min(x_c0[0,0], y_pred_plastic0[0,0], x_c5[0,0], y_pred_plastic5[0,0], x_c10[0,0], y_pred_plastic10[0,0], x_c25[0,0], y_pred_plastic25[0,0],
                      x_c50[0,0], y_pred_plastic50[0,0], x_c100[0,0], y_pred_plastic100[0,0])
    lower_lim = normal_roundC(lower_limit) - 1

    print(x_comb0[-1,0], x_comb0[-1,-1], x_comb0[0,0], x_comb0[0,-1])
    # upper_limit = max( max(x_hot_asc), max(y_hot_asc) )
    upper_limit = max(x_comb0[-1,0], y_pred_plastic0[0,0], x_comb5[0,0], y_pred_plastic5[0,0], x_comb10[0,0], y_pred_plastic10[0,0], x_comb25[0,0], 
                      y_pred_plastic25[0,0], x_comb50[0,0], y_pred_plastic50[0,0], x_comb100[0,0], y_pred_plastic100[0,0])
    upper_lim = normal_roundH(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # Plot SVM Results, Add in Reference Line too
    plt.figure(figsize=(7, 7))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    
    # wanna do a similar thing here for plotting as I did with the plot1to1_multiple.py - need to get that code so it can be a spectrum of green? 
    #Just plot middle line too
    plt.plot(x_comb0, y_pred_plastic0, 'o', color='lightgreen', label='Calibrated Data 0% (Using Pure Water SVM)')
    plt.plot(x_comb0, y_pred_plastic0, color='green', lw=2, label='Calibrated Curve')
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