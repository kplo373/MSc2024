# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:33:25 2024

Calibration script for applying the same calibration from the pure water
hot and cold experiments, to the rest of the experiments being plotted.
Pkl files are used to calibrate these plastic experiments.

@author: kplo373
"""

# Fitting the Pure Water Calibration SVM curve (using ChatGPT)
import joblib

# Load the saved model and scalers
svr_rbf_pure_water = joblib.load(r"C:\Users\kplo373\Documents\GitHub\MSc2024\old_scripts\svr_rbf_pure_water.pkl")
    #r"D:\MSc Results\svr_rbf_pure_water.pkl")
scaler_y_pure_water = joblib.load(r"C:\Users\kplo373\Documents\GitHub\MSc2024\old_scripts\scaler_y_pure_water.pkl")
    #r"D:\MSc Results\scaler_y_pure_water.pkl")

# Prepare the plastic-water data
x_cold = tempC1cold.reshape(-1, 1)  # if an error, can do tempC1cold.to_numpy().reshape...
x_hot_descending = tempC1hot.reshape(-1, 1)  # this series begins with the hottest value... need to reverse it somehow
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

