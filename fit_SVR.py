# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:30:56 2024

A calibration function that applies a support vector machine
in regression (SVR) to the pure water hot and cold experiments,
to create pkl files storing this calibration data for the other
calibration function, apply_calibration.py.

@author: kplo373
"""
# need to get the final resampled dataframe from create_merged_df.py***
import numpy as np
# Fitting SVM curve (using ChatGPT)
from sklearn.preprocessing import StandardScaler  # used to scale the combined arrays below
from sklearn.svm import SVR  # used to train the SVM below
from sklearn.metrics import mean_squared_error

#want to also make sure that the 95th percentile thing is included... should I get it from the plot1to1.py script maybe? and return clipped arrays in that function?
def fit_SVR(df_merged_cold, df_merged_hot):
    tempCScold = df_merged_cold['temperature_CS']   #['tempCS']
    tempCShot = df_merged_hot['temperature_CS']
    tempOpcold = df_merged_cold['temperature_Op']
    tempOphot = df_merged_hot['temperature_Op']


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
    
    
    # Scale the combined dataset
    scaler_x = StandardScaler()  # has type: sklearn.preprocessing._data.StandardScaler
    scaler_y = StandardScaler()
    
    x_comb_scaled = scaler_x.fit_transform(x_comb)                         # shape (16702, 1)
    y_comb_scaled = scaler_y.fit_transform(y_comb.reshape(-1, 1)).ravel()  # shape (16702,)
    # ravel() converts a multi-dimensional array into 1D, flattening the array but not creating a new one
    
    
    # Train the SVR model
    svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)  
    # Radial Basis Function (rbf kernel), good for nonlinear relationships
    # RBF kernel eqn: K(xi, xj) = exp(-gamma*||xi-xj||^2)
    
    # gamma (Kernel Coefficient) is the spread of the kernel. If high gamma, each training pt has close (high?) influence,
    #(can lead to overfitting). Low gamma has more spread out influence and simpler decision boundary (maybe underfitting).
    # gamma=0.1 is moderate, balancing between capturing patterns and avoiding overfitting.
    
    # C is the regularization parameter: if a high C, model fits training data too well and may be overfitting
    #If a low C, model allows some errors on training data to generalise better.
    # C=100 is a relatively high C, so model fits training data more closely!
    
    # Epsilon is the margin of tolerance where no penalty given to errors. High epsilon is a wider tube, more errors allowed.
    #Low epsilon is a narrower tube, less errors allowed.
    # epsilon=0.1 is relatively small, so model is sensitive to errors.
    svr_rbf.fit(x_comb_scaled, y_comb_scaled)
    print(svr_rbf)  # SVR(C=100, gamma=0.1)
    
    
    # Predict using the RBF SVR model
    x_test = np.linspace(x_comb.min(), x_comb.max(), 100).reshape(-1,1)       # shape (100, 1)
    x_test_scaled = scaler_x.transform(x_test)  # use this x_array for both the straight and curved fit
    y_pred_rbf_scaled = svr_rbf.predict(x_test_scaled)
    y_pred_rbf = scaler_y.inverse_transform(y_pred_rbf_scaled.reshape(-1,1))  # shape (100, 1)
    
    
    # Train the linear SVR model
    linear_svr = SVR(kernel='linear', C=100, epsilon=0.1)
    linear_svr.fit(x_comb_scaled, y_comb_scaled)
    
    # Predict using the linear SVR model
    y_pred_linear_scaled = linear_svr.predict(x_test_scaled)
    y_pred_linear = scaler_y.inverse_transform(y_pred_linear_scaled.reshape(-1,1))  # shape (100, 1)
    
    return scaler_y, svr_rbf, linear_svr, y_pred_linear  # just guessing what to return... can update this at the end
    # takes a while to run this cell^^

#%% Test the actual function
scaler_y, svr_rbf, linear_svr, y_pred_linear = fit_SVR(df_merged_cold, df_merged_hot)  # this should ONLY BE FOR PURE WATER

#%%
# Calculate RMSE for both models (root mean square error)
y_true_scaled = scaler_y.transform(y_comb.reshape(-1, 1)).ravel()
y_pred_rbf_comb_scaled = svr_rbf.predict(x_comb_scaled)
y_pred_rbf_comb = scaler_y.inverse_transform(y_pred_rbf_comb_scaled.reshape(-1,1))
y_pred_linear_comb_scaled = linear_svr.predict(x_comb_scaled)
y_pred_linear_comb = scaler_y.inverse_transform(y_pred_linear_comb_scaled.reshape(-1,1))

rmse_rbf = np.sqrt(mean_squared_error(y_comb, y_pred_rbf_comb))
rmse_linear = np.sqrt(mean_squared_error(y_comb, y_pred_linear_comb))

print(f'Root Mean Square Error (RMSE) for RBF SVR: {rmse_rbf}')
print(f'Root Mean Square Error (RMSE) for Linear SVR: {rmse_linear}')


# getting a UnicodeDecodeError from the below script functions for this data... see website: https://saturncloud.io/blog/how-to-fix-the-pandas-unicodedecodeerror-utf8-codec-cant-decode-bytes-in-position-01-invalid-continuation-byte-error/
#%% to test
import sys
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")
# To get the filepath
from get_filepaths import get_filepaths
path_cold, files_cold = get_filepaths('24/07/2024', 'PM')  # for the cold pure water test: Wednesday 24th July PM
# path gives a folder, and files are the files in that folder. Need to select specific file from files list
path_CScold = path_cold + '\\' + files_cold[0]
path_Opcold = path_cold + '\\' + files_cold[2]

#%%
path_hot, files_hot = get_filepaths('18/07/2024', 'AM')  # for the hot pure water test: Thursday 18th July AM
path_CShot = path_hot + '\\' + files_hot[0]
path_Ophot = path_hot + '\\' + files_hot[2]


# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(path_CScold)
dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(path_CShot)

#from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
from read_CampbellSci import water_avgCS
#df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
df_water_avgCScold = water_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)
#df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
df_water_avgCShot = water_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
# print(df_sand_avgCScold)

    
# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOpcold, a1cold, a2cold, a3cold, a4cold = read_Optris(path_Opcold)  # giving error now, need to go to line 38 in read_Optris
dt_objsOphot, a1hot, a2hot, a3hot, a4hot = read_Optris(path_Ophot)
#%%
    
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
print(df_merged_cold)

#%%
from plot1to1 import plot1to1  # need to add text for title, relevant to what type of experiment was done
df_cold, df_hot = plot1to1(df_merged_cold, df_merged_hot, 'Pure Water')  # to give the clipped arrays... do we need these?

#%% Test the actual function
scaler_y, svr_rbf, linear_svr, y_pred_linear = fit_SVR(df_merged_cold, df_merged_hot)
