# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:33:25 2024

Calibration script for applying the same calibration from the pure water
hot and cold experiments, to the rest of the experiments being plotted.
Pkl files are used to calibrate these plastic experiments.

@author: kplo373
"""

# Fitting the Pure Water Calibration SVM to this raw data (using ChatGPT)
#import joblib
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


def apply_calibration(df_in, str_expt):    
    # Load the saved model and scalers
    #svr_rbf = joblib.load(r"D:\MSc Results\svr_rbf_pure_water.pkl")  # for pure water
        #r"D:\MSc Results\svr_rbf_pure_water.pkl")
    # 2. Apply the correction to control sample, load SVR model first
    with open('svr_model.pkl', 'rb') as f:
        svr_model = pickle.load(f)  # for pure water
    
    # 3. Apply correction to non-control samples, load non-control sample data (x and y are independent)
    x_nctrl = np.array(df_in['temperature_CS']).reshape(-1, 1)
    y_nctrl = np.array(df_in['temperature_Op']).reshape(-1, 1)  # not sure if using this!!
    
    # Apply the correction using the model from the control sample
    y_nctrl_corrected = svr_model.predict(x_nctrl.reshape(-1, 1))  # correcting based on x values (thermocouples)
    df_in['y_corrected'] = y_nctrl_corrected  # store corrected y values as another column in the non-control sample
    
    # Save the corrected non-control sample as csv file
    df_in.to_csv(r'D:\MSc Results\corrected_non_control_sample.csv')

    print(y_nctrl)
    print(y_nctrl_corrected)
   

    r'''
    # Predict using the SVM model trained on pure water data
    #x_pred_plastic_scaled = svr_rbf.predict(x_comb_scaled)
    correction_y = svr_rbf.predict(y)  # need to reshape this correction_y from (16674, 16674) to (16674, 1)? Or (16674,)
    corr_y = correction_y.flatten()
    cor_y = corr_y.reshape(-1, 1)
    print(cor_y.shape)
    corrected_y = y + cor_y  
    '''
    # Inverse transform the predicted values to get them back to the original scale
    #x_pred_plastic = scaler_x.inverse_transform(x_pred_plastic_scaled.reshape(-1, 1))  # use this ndarray while plotting! Has the calibration applied to it

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

    lower_limit = min(x_nctrl[0], y_nctrl_corrected[0])
    lower_lim = normal_roundC(lower_limit) - 1

    upper_limit = max( max(x_nctrl), max(y_nctrl_corrected) )
    upper_lim = normal_roundH(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below

    # Plot SVM Results, Add in Reference Line too
    plt.figure(figsize=(7, 7))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    #plt.plot(x_pred, y_comb, 'o', color='lightgreen', label='Calibrated Data (Using Pure Water SVM)')
    plt.plot(x_nctrl, y_nctrl_corrected, color='green', lw=2, label='Calibrated Curve')
    plt.plot(x_nctrl, y_nctrl, 'r', label='Raw Data')
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
    
    return #x_pred, y_comb

# run this script through the main() function script