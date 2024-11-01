# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:08:31 2024

Second attempt at fitting SVR to the x and y combined data from the pure
water test. Will merge this temporary file into fit_SVR.py once I figure out
how to do it properly! Trying with ChatGPT...


@author: kplo373
"""
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
#from sklearn.svm import SVR   # have put this below already
import pandas as pd

# can put this into a function later maybe... it doesn't actually need to be one if I'm saving them as pkl files anyway!


# Get x and y combined arrays
import sys
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")
# To get the filepath
from get_filepaths import get_filepaths
pathCScold, pathOpcold = get_filepaths('24/07/2024', 'PM')  # for the cold pure water test: Wednesday 24th July PM
pathCShot, pathOphot = get_filepaths('18/07/2024', 'AM')  # for the hot pure water test: Thursday 18th July AM

# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(pathCScold)
dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(pathCShot)

#from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
from read_CampbellSci import water_avgCS
#df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
df_water_avgCScold = water_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)
#df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
df_water_avgCShot = water_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
# print(df_sand_avgCScold)

 
# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOpcold, a1cold, a2cold, a3cold, a4cold = read_Optris(pathOpcold)  # giving error now, need to go to line 38 in read_Optris
dt_objsOphot, a1hot, a2hot, a3hot, a4hot = read_Optris(pathOphot)

from read_Optris import resample_Optris
resampled_df_a1cold = resample_Optris(dt_objsOpcold, a1cold)
resampled_df_a3cold = resample_Optris(dt_objsOpcold, a3cold)
resampled_df_a1hot = resample_Optris(dt_objsOphot, a1hot)
resampled_df_a3hot = resample_Optris(dt_objsOphot, a3hot)
    
from read_Optris import average_Optris
avgOp_dfcold = average_Optris(resampled_df_a1cold, resampled_df_a3cold)
avgOp_dfhot = average_Optris(resampled_df_a1hot, resampled_df_a3hot)
# print(avgOp_dfcold)

from create_merged_df import create_merged_df
df_merged_cold = create_merged_df(avgOp_dfcold, df_water_avgCScold)  #df_sand_avgCScold)
df_merged_hot = create_merged_df(avgOp_dfhot, df_water_avgCShot)     #df_sand_avgCShot)
#print(df_merged_cold)

#%% Removing first 15 minutes of each data record
df_ready_cold = df_merged_cold.copy()
start_time = df_ready_cold.index.min()
cutoff_time = start_time + pd.Timedelta(minutes=15)
df_trimmed_cold = df_ready_cold[df_ready_cold.index >= cutoff_time]

# Removing first 15 minutes of each data record
df_ready_hot = df_merged_hot.copy()
start_timeh = df_ready_hot.index.min()
cutoff_timeh = start_timeh + pd.Timedelta(minutes=20)
df_trimmed_hot = df_ready_hot[df_ready_hot.index >= cutoff_timeh]

# Plotting quickly to visualise
df_trimmed_cold.plot("temperature_CS", "temperature_Op")
df_trimmed_hot.plot("temperature_CS", "temperature_Op")  # can't tell order but it is plotting hot to cold

# Want to reverse the arrays within df_trimmed_hot to allow room temperatures to directly follow room temperatures at end of cold trimmed df
df_reversed_hot = df_trimmed_hot.iloc[::-1].reset_index(drop=True)
# this reversed df looks good in the variable explorer! Both temperature arrays have been reversed, use this below!


#%% Now, our fitting SVR script!!
# Merging the cold and hot dataframes into one full df
df_full = pd.concat([df_trimmed_cold, df_reversed_hot])
df_full.plot("temperature_CS", "temperature_Op")  # again, plotting to visualise

from plot1to1 import plot1to1  # need to add text for title, relevant to what type of experiment was done
plot1to1(df_full, 'Pure Water 0% Shavings')


r'''
#%% Use this x_comb and y_comb in the predicting steps - takes a while to run this cell :)
from sklearn.preprocessing import StandardScaler
scaler_x = StandardScaler()

x = df_full['temperature_CS'].to_numpy()
y = df_full['temperature_Op'].to_numpy()

# Reshape and scale the x and y arrays to match the format expected by SVR (2D array)
#x = x_comb.ravel()   # flattening the x array to be 1D (needed for fitting SVR)
#y = y_comb  #.reshape(-1, 1)  # y needs to be 2D for features

#x_scaled = scaler_x.fit_transform(x.reshape(-1, 1))

# Train SVR model on the scaled x data, without scaling y
svr_rbf = SVR(kernel='rbf', verbose=True)  # creating RBF kernel SVR model and fitting it below
svr_rbf.fit(y.reshape(-1, 1), x)

svr_linear = SVR(kernel='linear', verbose=True)  # and a linear kernel SVR model
svr_linear.fit(y.reshape(-1, 1), x)

# Predicting x values from y values
x_pred_rbf = svr_rbf.predict(y.reshape(-1, 1)).reshape(-1, 1)
x_pred_linear = svr_linear.predict(y.reshape(-1, 1))
'''
#%% Redo Fitting SVR From Tom's Code
# 1. Train SVR on the control sample, split into x and y
x_control = df_full['temperature_CS'].to_numpy(dtype='float64')
y_control = df_full['temperature_Op'].to_numpy(dtype='float64')

#%%
# Train Support Vector Regressor (SVR) to model relationship between x and y (are independent of each other)
from sklearn.svm import SVR
svr = SVR()

# Fit SVR on control data - CAN POTENTIALLY GET RID OF THIS ACTUALLY...*** only use look up table??
svr.fit(x_control.reshape(-1, 1), y_control)  # so am not using RBF or linear SVR...

# Save the model using pickle
import pickle
with open(r'D:\MSc Results\svr_model.pkl', 'wb') as f:
    pickle.dump(svr, f)
    
    
# 2. Apply the correction to control sample, load SVR model first
with open(r'D:\MSc Results\svr_model.pkl', 'rb') as f:
    svr_model = pickle.load(f)

# Predict corrected y values for control sample using x values
y_ctrl_corrected = svr_model.predict(x_control.reshape(-1, 1))

# Save the corrected control sample
df_full['y_corrected_SVR'] = y_ctrl_corrected   # not sure if I need this column?? Have it anyway
#df_full.to_csv(r'D:\MSc Results\corrected_ctrl_sample.csv')  # I have this below too
# then can apply the correction to non-control samples in my apply calibration script

y_cal_vals =  y_control - x_control  # getting temperature difference between two sensors
y_control_corrected = y_control - y_cal_vals
df_full['y_corrected'] = y_control_corrected  # store corrected y values as another column in the full dataframe, array not series
df_full['y_cal_adjustments'] = y_cal_vals

# Create correction look up table - need to apply this table adjustment column to raw mixture data in apply_calibration afterwards
cal_table_df = pd.DataFrame({'y_val': y_control, 'y_cal_adj': y_cal_vals})
cal_table_df.index = np.around(cal_table_df['y_val'], decimals=4)
cal_table_df = cal_table_df.drop('y_val', axis=1)
cal_table_df = cal_table_df.sort_index()


# Reset the index and create a new column
cal_table_df_reset = cal_table_df.reset_index()
calTable_unique_df = cal_table_df_reset.drop_duplicates(subset='y_val')  # removing duplicates in the y_val column
calTable_unique_df.loc[:, 'y_val'] = pd.to_numeric(calTable_unique_df['y_val'], errors='coerce')  # ensuring 'y_val' is numeric and checking for invalid values
calTable_unique_df = calTable_unique_df.dropna(subset=['y_val'])  # removing any rows where 'y_val' is NaN after conversion
calTable_unique_df = calTable_unique_df.set_index('y_val')  # set 'y_val' as the index
# Save this calibration table!


# Get the nearest y value in the cal_table_df.index to the y variables in the different mixtures' data
sel_cal_vals = np.zeros(len(y_control))  # Preallocate for the nearest_y_vals collected in the for loop
for i in range(len(y_control)):
    y = float(y_control[i])  # add [0] after [i] if extracting the first element from the array, if y_ntrl is 2D
    nearest_index = calTable_unique_df.index.get_indexer([y], method='nearest')[0]  # get nearest index
    
    # Check if the nearest_index is valid
    if nearest_index >= 0:  # Valid index
        nearest_y_val = calTable_unique_df.index[nearest_index]
        sel_cal_vals[i] = nearest_y_val  # Store the nearest y value
    else:
        print(f"Warning: Nearest index for y={y} is not valid.")


     

# Save the corrected control sample as csv file
df_full.to_csv(r'D:\MSc Results\corrected_control_sample.csv')
# then extract this csv file look up table data in apply_calibration.py! (working in apply_calib_debug.py first)

#print(y_control)
#print(y_control_corrected)






# haven't calculated RMSE for this yet...

r'''
#%% Calculating RMSE for both models to see which is more accurate
rmse_rbf = np.sqrt(mean_squared_error(x, x_pred_rbf))
rmse_linear = np.sqrt(mean_squared_error(x, x_pred_linear))
print(f"RBF SVR RMSE: {rmse_rbf}")
print(f"Linear SVR RMSE: {rmse_linear}")
'''

# Visualise the data to see if it will line up on the line? Or would that be in the apply calibration script...
import matplotlib.pyplot as plt
# Scatter plot of actual y vs. predicted y, using look up table
plt.subplot(1, 2, 1)
plt.scatter(x_control, y_control, color='blue', label='Actual y', alpha=0.5)
plt.scatter(x_control, y_control_corrected, color='red', label='Calibrated y', alpha=0.5)
plt.title('Actual vs. Calibrated y')
plt.xlabel('Thermocouple Temperature (degrees Celsius)')
plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
plt.legend()
plt.grid()

# Scatter plot of (RBF?) SVR actual y vs. predicted y
plt.subplot(1, 2, 2)
plt.scatter(x_control, y_control, color='blue', label='Actual y', alpha=0.5)
plt.scatter(x_control, y_ctrl_corrected, color='green', label='Predicted y (SVR)', alpha=0.5)
plt.title('SVR: Actual vs Predicted y')
plt.xlabel('Thermocouple Temperature (degrees Celsius)')
plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


# maybe delete the section below??
r'''
#%% Also need to save this fit/prediction to a pkl file so that I can apply it to the rest of the data

# from prev script... try chatgpt too! Chatgpt gives an option to use joblib (better for larger datasets) or pkl.
import joblib
# For calibrating the rest of the experiment mixtures, after fitting the SVR model and scaling the data
joblib.dump(svr_rbf, r"D:\MSc Results\svr_rbf_pure_water.pkl")
joblib.dump(scaler_x, r"D:\MSc Results\scaler_y_pure_water.pkl")


# Save the predictions if needed
#x_pred_pure_scaled = svr_rbf.predict(y_test_scaled)
#y_pred_pure = scaler_y.inverse_transform(y_pred_pure_scaled.reshape(-1, 1))
#np.save('y_pred_pure.npy', y_pred_pure)
np.save(r"D:\MSc Results\x_pred_rbf.npy", x_pred_rbf)

# do I save the linear ones too? RBF gives best results so just saved them so far...
'''

# now can use these to apply the calibration in the apply_calibration.py script (just do the single one for pure water maybe!)


