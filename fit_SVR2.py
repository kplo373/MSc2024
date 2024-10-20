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
from sklearn.svm import SVR

# can put this into a function later maybe... it doesn't actually need to be one if I'm saving them as pkl files anyway!


# Get x and y combined arrays
import sys
#sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")
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


from plot1to1 import plot1to1  # need to add text for title, relevant to what type of experiment was done
df_cold, df_hot = plot1to1(df_merged_cold, df_merged_hot, 'Pure Water 0% Shavings')  # to give the clipped arrays... do we need these?
# the name string given in the above function needs to have 'Shavings' or 'Pellets' in it so isn't saving itself as a png but that's okay, is still plotting
# but I do need to get the df_cold and df_hot extracted from it so have added 0% Shavings in there now...


#%% Now, our fitting SVR script!!
tempCScold = df_merged_cold['temperature_CS']   #['tempCS']
tempCShot = df_merged_hot['temperature_CS']
tempOpcold = df_merged_cold['temperature_Op']
tempOphot = df_merged_hot['temperature_Op']

#tempCScold = df_cold['tempCS']  # try these ones when I have time to run it overnight...************
#tempCShot = df_hot['tempCS']
#tempOpcold = df_cold['tempOp']
#tempOphot = df_hot['tempOp']


# Initially reshaping the hot and cold x arrays into 2D arrays for x, but keep y 1D
x_cold = tempCScold.to_numpy().reshape(-1, 1)  # to make the x arrays 2D with a single column: (11518, 1)
x_hot = tempCShot.to_numpy().reshape(-1, 1)
y_cold = tempOpcold.to_numpy()  # y arrays are 1D: (11518,) and aren't pandas series (are np.ndarrays now).
y_hot = tempOphot.to_numpy()

print(f'x_cold shape: {x_cold.shape}, y_cold shape: {tempOpcold.shape}')
print(f'x_hot shape: {x_hot.shape}, y_hot shape: {tempOphot.shape}')

# Combine both the hot and cold x arrays, and the hot and cold y arrays
x_comb = np.vstack((x_cold, x_hot))  # shape is (16702, 1) so both the x and y arrays are put into the same column
y_comb = np.concatenate((y_cold, y_hot))  # shape is (16702,) so also same column as there only is one
print(f'x_combined shape: {x_comb.shape}, y_combined shape: {y_comb.shape}')

#%% Use this x_comb and y_comb in the predicting steps - takes a while to run this cell :)
from sklearn.preprocessing import StandardScaler
scaler_x = StandardScaler()

# Reshape and scale the x and y arrays to match the format expected by SVR (2D array)
x = x_comb.ravel()   # flattening the x array to be 1D (needed for fitting SVR)
y = y_comb  #.reshape(-1, 1)  # y needs to be 2D for features

x_scaled = scaler_x.fit_transform(x.reshape(-1, 1))

# Train SVR model on the scaled x data, without scaling y
svr_rbf = SVR(kernel='rbf', verbose=True)  # creating RBF kernel SVR model and fitting it below
svr_rbf.fit(y.reshape(-1, 1), x_scaled)

svr_linear = SVR(kernel='linear', verbose=True)  # and a linear kernel SVR model
svr_linear.fit(y.reshape(-1, 1), x)

# Predicting x values from y values
x_pred_rbf = scaler_x.inverse_transform(svr_rbf.predict(y.reshape(-1, 1)).reshape(-1, 1))
x_pred_linear = svr_linear.predict(y.reshape(-1, 1))



#%% Calculating RMSE for both models to see which is more accurate
rmse_rbf = np.sqrt(mean_squared_error(x, x_pred_rbf))
rmse_linear = np.sqrt(mean_squared_error(x, x_pred_linear))
print(f"RBF SVR RMSE: {rmse_rbf}")
print(f"Linear SVR RMSE: {rmse_linear}")

# Visualise the data to see if it will line up on the line? Or would that be in the apply calibration script...
import matplotlib.pyplot as plt
# Scatter plot of actual x vs. predicted x (RBF SVR)
plt.subplot(1, 2, 1)
plt.scatter(x, y, color='blue', label='Actual x', alpha=0.5)
plt.scatter(x_pred_rbf, y, color='red', label='Predicted x (RBF)', alpha=0.5)
plt.title('RBF SVR: Actual vs. Predicted x')
plt.xlabel('Thermocouple Temperature (degrees Celsius)')
plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
plt.legend()
plt.grid()

# Scatter plot of linear SVR actual x vs. predicted x
plt.subplot(1, 2, 2)
plt.scatter(x, y, color='blue', label='Actual x', alpha=0.5)
plt.scatter(x_pred_linear, y, color='green', label='Predicted x (Linear)', alpha=0.5)
plt.title('Linear SVR: Actual vs Predicted x')
plt.xlabel('Thermocouple Temperature (degrees Celsius)')
plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


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


# now can use these to apply the calibration in the apply_calibration.py script (just do the single one for pure water maybe!)



