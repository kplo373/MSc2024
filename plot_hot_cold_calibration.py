# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:30:13 2024

This script will be used to plot a hot and cold test together
on the same axes, to interpolate a line between any missing
temperatures (likely between 22-24 deg C).

@author: katep
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import joblib

# If wanting to change the file naming convention, do ctrl+F+R to find and replace!

fileC1_hot = r"C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\July_2024\Thurs18JulyAM\CR3000_Table1.dat"
df_C1_hot = pd.read_csv(fileC1_hot, delimiter=',', header=4)
print(df_C1_hot)  # have given it 4 headers, so the first row (0th) immediately begins with results
# this file represents hot Friday 18th July's test, with pure distilled water initially heated in oven at 40 deg C

fileC1_cold = r"C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\July_2024\Wednesday24JulyPM\CR3000_Table1.dat"
df_C1_cold = pd.read_csv(fileC1_cold, delimiter=',', header=4)
print(df_C1_cold)
# this file represents cold 24th July's test, with pure distilled water initially chilled

# Choose the filepaths of the Optris .dat files and insert here
path_Ophot = r"C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\July_2024\Thurs18JulyAM\Thurs18JulyOptris.dat"
path_Opcold = r"C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\July_2024\Wednesday24JulyPM\Wed25JulyPMOptris.dat"


#%% Extract data from Friday 12th July Campbell Table 1 file
# Preallocating the datetime object, temperature, and standard deviation arrays
dt_objsC1hot = np.zeros(len(df_C1_hot), dtype='datetime64[s]')

temp1_C1hot = np.zeros(len(df_C1_hot))
temp2_C1hot = np.zeros(len(df_C1_hot))
temp3_C1hot = np.zeros(len(df_C1_hot))
temp4_C1hot = np.zeros(len(df_C1_hot))
temp5_C1hot = np.zeros(len(df_C1_hot))
temp6_C1hot = np.zeros(len(df_C1_hot))

stdev1_C1hot = np.zeros(len(df_C1_hot))
stdev2_C1hot = np.zeros(len(df_C1_hot))
stdev3_C1hot = np.zeros(len(df_C1_hot))
stdev4_C1hot = np.zeros(len(df_C1_hot))
stdev5_C1hot = np.zeros(len(df_C1_hot))
stdev6_C1hot = np.zeros(len(df_C1_hot))

count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
for i in range(0, len(df_C1_hot)):
    row_seriesC1 = df_C1_hot.iloc[i]
    #print(row_seriesC1)
    timestr = str(row_seriesC1[0])  # e.g. 2024-06-13 10:59:55, type string
    #print(timestr)  # now need to convert it to a datetime object
    the_date_hot = timestr[:10]  # extracting the date to print along x-axis
    dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
    dt_objsC1hot[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

    temp1 = str(row_seriesC1[2])
    temp2 = str(row_seriesC1[3])
    temp3 = str(row_seriesC1[4])
    temp4 = str(row_seriesC1[5])
    temp5 = str(row_seriesC1[6])
    temp6 = str(row_seriesC1[7])
    stdev1 = str(row_seriesC1[8])
    stdev2 = str(row_seriesC1[9])
    stdev3 = str(row_seriesC1[10])
    stdev4 = str(row_seriesC1[11])
    stdev5 = str(row_seriesC1[12])
    stdev6 = str(row_seriesC1[13])
    #print(temp1)  # now need to add all these variable elements to their array...
    
    temp1_C1hot[count] = temp1
    temp2_C1hot[count] = temp2
    temp3_C1hot[count] = temp3
    temp4_C1hot[count] = temp4
    temp5_C1hot[count] = temp5
    temp6_C1hot[count] = temp6
    stdev1_C1hot[count] = stdev1
    stdev2_C1hot[count] = stdev2
    stdev3_C1hot[count] = stdev3
    stdev4_C1hot[count] = stdev4
    stdev5_C1hot[count] = stdev5
    stdev6_C1hot[count] = stdev6
    
    count += 1
    print(count)

print(count, len(temp1_C1hot)) 


#%% Extract data from cold 3 July Campbell Table 1 file
# Preallocating the datetime object, temperature, and standard deviation arrays
dt_objsC1cold = np.zeros(len(df_C1_cold), dtype='datetime64[s]')

temp1_C1cold = np.zeros(len(df_C1_cold))
temp2_C1cold = np.zeros(len(df_C1_cold))
temp3_C1cold = np.zeros(len(df_C1_cold))
temp4_C1cold = np.zeros(len(df_C1_cold))
temp5_C1cold = np.zeros(len(df_C1_cold))
temp6_C1cold = np.zeros(len(df_C1_cold))

stdev1_C1cold = np.zeros(len(df_C1_cold))
stdev2_C1cold = np.zeros(len(df_C1_cold))
stdev3_C1cold = np.zeros(len(df_C1_cold))
stdev4_C1cold = np.zeros(len(df_C1_cold))
stdev5_C1cold = np.zeros(len(df_C1_cold))
stdev6_C1cold = np.zeros(len(df_C1_cold))

count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
for i in range(0, len(df_C1_cold)):
    row_seriesC1 = df_C1_cold.iloc[i]
    #print(row_seriesC1)
    timestr = str(row_seriesC1[0])  # e.g. 2024-06-13 10:59:55, type string
    #print(timestr)  # now need to convert it to a datetime object
    the_date_cold = timestr[:10]  # extracting the date to print along x-axis
    dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
    dt_objsC1cold[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

    temp1 = str(row_seriesC1[2])
    temp2 = str(row_seriesC1[3])
    temp3 = str(row_seriesC1[4])
    temp4 = str(row_seriesC1[5])
    temp5 = str(row_seriesC1[6])
    temp6 = str(row_seriesC1[7])
    stdev1 = str(row_seriesC1[8])
    stdev2 = str(row_seriesC1[9])
    stdev3 = str(row_seriesC1[10])
    stdev4 = str(row_seriesC1[11])
    stdev5 = str(row_seriesC1[12])
    stdev6 = str(row_seriesC1[13])
    #print(temp1)  # now need to add all these variable elements to their array...
    
    temp1_C1cold[count] = temp1
    temp2_C1cold[count] = temp2
    temp3_C1cold[count] = temp3
    temp4_C1cold[count] = temp4
    temp5_C1cold[count] = temp5
    temp6_C1cold[count] = temp6
    stdev1_C1cold[count] = stdev1
    stdev2_C1cold[count] = stdev2
    stdev3_C1cold[count] = stdev3
    stdev4_C1cold[count] = stdev4
    stdev5_C1cold[count] = stdev5
    stdev6_C1cold[count] = stdev6
    
    count += 1
    print(count)

print(count, len(temp1_C1cold)) 


# not going to be easy to plot their temperature data on top of each other because the dt_objs are different
# so go straight to scatterplot lines below...
#%% Take the mean/average of all consistent thermocouples (think it's all of them??)
ref_temps_C1hot = np.zeros(len(temp1_C1hot))
ref_temps_C1hot = (temp1_C1hot + temp2_C1hot + temp3_C1hot + temp4_C1hot + temp5_C1hot + temp6_C1hot)/6  # taking the average. what is new stdev??
print(ref_temps_C1hot)


ref_temps_C1cold = np.zeros(len(temp1_C1cold))
ref_temps_C1cold = (temp1_C1cold + temp2_C1cold + temp3_C1cold + temp4_C1cold + temp5_C1cold + temp6_C1cold)/6  # taking the average. what is new stdev??
print(ref_temps_C1cold)


#---------------------------------------------------------------------------------
#%% Check Optris too!
# To extract the data from the headers of the Optris data, read first 7 lines
headers = []
data = []
with open(path_Ophot, 'r') as file:
    headers_hot = [next(file).strip() for _ in range(7)]
    # for i, line in enumerate(file):
        # data.append(line.strip().split('\t'))  # this puts data into separate lines, rather than separating into columns
print(headers_hot)  # Now, there are 4x different measurement areas


with open(path_Opcold, 'r') as file:
    headers_cold = [next(file).strip() for _ in range(7)]
print(headers_cold)  # Now, there are 4x different measurement areas


#%%
# Extract date and time from the relevant lines
date_line_hot = headers_hot[1]  # This is line Date: 13/06/2024
time_line_hot = headers_hot[2]  # This is line Time: 10:51:17.112

date_line_cold = headers_cold[1]  # This is line Date: 13/06/2024
time_line_cold = headers_cold[2]  # This is line Time: 10:51:17.112

# Split the lines to get the actual date and time values
date_val_hot = date_line_hot.split('\t')[1]
time_val_hot = time_line_hot.split('\t')[1]

date_val_cold = date_line_cold.split('\t')[1]
time_val_cold = time_line_cold.split('\t')[1]

print(f"Date: {date_val_hot}")
print(f"Time: {time_val_hot}")
print(f"Date: {date_val_cold}")
print(f"Time: {time_val_cold}")  # nice, this is it! Now need to add on the individual seconds time for each measurement...
# time is a string, so need to turn into datetime obj? to add it to seconds later?

# Combine date and time to a single string
datetime_strhot = date_val_hot + ' ' + time_val_hot   #f"{date_value} {time_value}"  is chatGPT's method
datetime_strcold = date_val_cold + ' ' + time_val_cold

# Convert the combined string to a datetime object
datetime_format = "%d/%m/%Y %H:%M:%S.%f"
start_datetimeobjhot = datetime.strptime(datetime_strhot, datetime_format)
start_datetimeobjcold = datetime.strptime(datetime_strcold, datetime_format)
print(start_datetimeobjhot)
print(start_datetimeobjcold)
#%%

# Read the file, ignoring errors (chatGPT)
try: 
    df_Ophot = pd.read_csv(path_Ophot, delimiter='\t', encoding='utf-8', header=7)
    df_Opcold = pd.read_csv(path_Opcold, delimiter='\t', encoding='utf-8', header=7)
    print(df_Ophot)
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")



#%%

# Function to convert time string to timedelta
def time_str_to_timedelta(time_str):
    # Time string format is 'HH:MM:SS.sss'
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = map(float, seconds.split('.'))
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=milliseconds)

# Add the time deltas to the initial datetime
df_Ophot['Datetime'] = df_Ophot.iloc[:-2, 0].apply(lambda x: start_datetimeobjhot + time_str_to_timedelta(x))
df_Opcold['Datetime'] = df_Opcold.iloc[:-2, 0].apply(lambda x: start_datetimeobjcold + time_str_to_timedelta(x))
#added in the stop before the last 2 rows, as these do not contain actual data (e.g. '---', 'End of File')

print(df_Ophot['Datetime'])
print(df_Opcold['Datetime'])  # looks good, now the 0th column in the dataframe has been changed to the full datetime.
# still has the last two rows as 'NaT' but we don't really want these rows included at all...

#now get the other columns!!
#%% Assign new names to the data columns
print(df_Ophot.columns)   # has 9 columns
print(df_Opcold.columns)  # has only 5 columns
#%%
new_column_names_9 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']  # not sure what 'Unnamed: 3' column is for? so made it 'nan'
new_column_names_5 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']

df_Ophot.columns = new_column_names_9      # assigning them to the DataFrame by correct length
df_Opcold.columns = new_column_names_5
df_Ophot = df_Ophot.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
df_Opcold = df_Opcold.drop(columns=['Time'])
df_Ophot = df_Ophot.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 3' column too
df_Opcold = df_Opcold.drop(columns=['nan'])
print(df_Ophot.columns)


#%% Extract the data from these columns, into separate arrays
area1hot = df_Ophot['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
area2hot = df_Ophot['Area2']  # temperature avg of water surface above submerged thermocouples
area3hot = df_Ophot['Area3']  # temperature avg of whole/half of surface of the water
area4hot = df_Ophot['Area4']  # temperature avg of water surface above submerged thermocouples
datetimeOphot = df_Ophot['Datetime']

area1cold = df_Opcold['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
area2cold = df_Opcold['Area2']  # temperature avg of water surface above submerged thermocouples
area3cold = df_Opcold['Area3']  # temperature avg of whole/half of surface of the water
area4cold = df_Opcold['Area4']  # temperature avg of water surface above submerged thermocouples
datetimeOpcold = df_Opcold['Datetime']

print(area1hot)

#%% Get two means for Optris data - mean for half of surface, and mean for thermocouple surface
mean_Op_halfhot = np.zeros(len(area1hot))
mean_Op_smallhot = np.zeros(len(area1hot))
mean_Op_halfcold = np.zeros(len(area1cold))
mean_Op_smallcold = np.zeros(len(area1cold))

mean_Op_halfhot = (area1hot + area3hot)/2   # taking the average, what is new stdev??
mean_Op_smallhot = (area2hot + area4hot)/2  # and this stdev??
mean_Op_halfcold = (area1cold + area3cold)/2
mean_Op_smallcold = (area2cold + area4cold)/2


#%% To get average of mean/average Optris measurements - RESAMPLING
#new_datetimes has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!

#using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
df_newhot = pd.DataFrame({               # creating a new dataframe for hotnesday 3rd
    'datetimes': datetimeOphot,
    'Op_temp_half': mean_Op_halfhot,
    'Op_temp_small': mean_Op_smallhot})
df_newcold = pd.DataFrame({               # creating another new dataframe for cold 3rd
    'datetimes': datetimeOpcold,
    'Op_temp_half': mean_Op_halfcold,
    'Op_temp_small': mean_Op_smallcold})


df_newhot.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
df_newcold.set_index('datetimes', inplace=True)
#maybe the datetimes should just be column 0?? need to extract them.. can I use the .index? YES

# Define a function to calculate standard error
def standard_error(x):
    return x.std() / np.sqrt(len(x))

resampled_dfhot = df_newhot.resample('5S').agg({
    'Op_temp_half': ['mean', 'std', standard_error],
    'Op_temp_small': ['mean', 'std', standard_error]})  
# resampling whole dataframe to 5 sec intervals and averaging temp, plus getting stdev and sterr
resampled_dfcold = df_newcold.resample('5S').agg({
    'Op_temp_half': ['mean', 'std', standard_error],
    'Op_temp_small': ['mean', 'std', standard_error]})


resampled_dfhot.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns
resampled_dfcold.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns

print(resampled_dfhot.columns)

#%%
resampled_dthot = resampled_dfhot.index
Op_halfhot = resampled_dfhot['mean_temp_half']
Op_smallhot = resampled_dfhot['mean_temp_small']

resampled_dtcold = resampled_dfcold.index
Op_halfcold = resampled_dfcold['mean_temp_half']
Op_smallcold = resampled_dfcold['mean_temp_small']

#%%
#need to cut out some of the times where only one sensor collects data... can print dt_objsC1 and resampled_dt for Optris

# Create DataFrames for both sensors and both days
dfOphot = pd.DataFrame({'datetime': resampled_dthot,
                        'temperature1': Op_smallhot})
dfOpcold = pd.DataFrame({'datetime': resampled_dtcold,
                         'temperature1': Op_smallcold})

dfC1hot = pd.DataFrame({'datetime': dt_objsC1hot,
                        'temperature2': ref_temps_C1hot})
dfC1cold = pd.DataFrame({'datetime': dt_objsC1cold,
                         'temperature2': ref_temps_C1cold})


# Set the datetime column as the index
dfOphot.set_index('datetime', inplace=True)
dfC1hot.set_index('datetime', inplace=True)
dfOpcold.set_index('datetime', inplace=True)
dfC1cold.set_index('datetime', inplace=True)

# Already defined a function for standard_error above...
# Resample to 5-second intervals and calculate mean, std deviation, and std error for both temperature arrays
new_dfOphot = dfOphot.resample('5S').agg({'temperature1': ['mean', 'std', standard_error]})
new_dfC1hot = dfC1hot.resample('5S').agg({'temperature2': ['mean', 'std', standard_error]})

new_dfOpcold = dfOpcold.resample('5S').agg({'temperature1': ['mean', 'std', standard_error]})
new_dfC1cold = dfC1cold.resample('5S').agg({'temperature2': ['mean', 'std', standard_error]})


# Rename the columns for clarity
new_dfOphot.columns = ['mean_temp1', 'stddev_temp1', 'stderr_temp1']
new_dfC1hot.columns = ['mean_temp2', 'stddev_temp2', 'stderr_temp2']

new_dfOpcold.columns = ['mean_temp1', 'stddev_temp1', 'stderr_temp1']
new_dfC1cold.columns = ['mean_temp2', 'stddev_temp2', 'stderr_temp2']


# Merge the DataFrames on the datetime index
merged_dfhot = pd.merge(new_dfOphot, new_dfC1hot, on='datetime')
merged_dfcold = pd.merge(new_dfOpcold, new_dfC1cold, on='datetime')
print(merged_dfhot)


#%% Plot these merged dataframe temperatures against each other
tempOp_orighot = merged_dfhot['mean_temp1']
tempC1_orighot = merged_dfhot['mean_temp2']

tempOp_origcold = merged_dfcold['mean_temp1']
tempC1_origcold = merged_dfcold['mean_temp2']


# Automate the indices cut off initially for the warm-up period
minOpcold_i = np.argmin(tempOp_origcold)
print(minOpcold_i)  # works! This gives the index of the minimum value in the array
# (or it should give an array of indices if there are multiple occurrences of minimum value.)

maxC1hot_i = np.argmax(tempC1_orighot)
print(maxC1hot_i)  # works too! Gives max temp for thermocouples in the array's index.

# Can check the index gives min/max values by printing a few index values either side of it...


#%%
# Cutting out some initial ambient temperatures
tempOphot = tempOp_orighot[maxC1hot_i:]  # this needs to start and end at same indices as tempC1hot
tempC1hot = tempC1_orighot[maxC1hot_i:] 
tempOpcold = tempOp_origcold[minOpcold_i:]
tempC1cold = tempC1_origcold[minOpcold_i:]

plt.plot(tempC1cold, tempOpcold, label='Wed 24 July PM, cold')  # only plots from 22.6-24 deg C
plt.plot(tempC1hot, tempOphot, label='Thurs 18 July PM, hot')
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.title('Pure Water Comparison of Optris vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()


#need to fit a SVM line and curve of best fit to this plot!
#%% Fitting SVM curve (using ChatGPT)
from sklearn.preprocessing import StandardScaler  # used to scale the combined arrays below
from sklearn.svm import SVR  # used to train the SVM below
from sklearn.metrics import mean_squared_error

# Initially reshaping the hot and cold x arrays into 2D arrays for x, but keep y 1D
x_cold = tempC1cold.to_numpy().reshape(-1, 1)  # to make the x arrays 2D with a single column: (11518, 1)
x_hot = tempC1hot.to_numpy().reshape(-1, 1)
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

# takes a while to run this cell^^


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



#%% Plot SVM Results
plt.scatter(tempC1cold, tempOpcold, color='blue', label='Wed 24 July PM, Cold')
plt.scatter(tempC1hot, tempOphot, color='red', label='Thurs 18 July PM, Hot')
plt.plot(x_test, y_pred_rbf, color='white', lw=2, label='Curved SVR fit')
plt.plot(x_test, y_pred_linear, color='orange', lw=2, label='Linear SVR fit')

plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.title('Pure Water Comparison of Optris vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()


#%% For calibration in the other plot_hot_cold.py script

# After fitting the SVR model and scaling the data
svr_rbf.fit(x_comb_scaled, y_comb_scaled)
joblib.dump(svr_rbf, 'svr_rbf_pure_water.pkl')
joblib.dump(scaler_x, 'scaler_x_pure_water.pkl')
joblib.dump(scaler_y, 'scaler_y_pure_water.pkl')

# Save the predictions if needed
y_pred_pure_scaled = svr_rbf.predict(x_test_scaled)
y_pred_pure = scaler_y.inverse_transform(y_pred_pure_scaled.reshape(-1, 1))
np.save('y_pred_pure.npy', y_pred_pure)


'''
# Don't need this plot created below, but the code is here anyway
 #%% Create a linspace x-axis variable to plot Optris vs. Campbell data for both hot and cold tests

# Cut off the plateau ending off the cold experiment if needed (yes for pure water)
tempC1_cold = tempC1cold[:-5000]
tempOp_cold = tempOpcold[:-5000]


xlinsp_cold = np.linspace(0, len(tempC1_cold), len(tempC1_cold))
xlinsp_hot = np.linspace(0, len(tempC1hot), len(tempC1hot))

plt.plot(xlinsp_cold, tempC1_cold, label='Thermocouples, cold')
plt.plot(xlinsp_cold, tempOp_cold, label='Optris, cold')
plt.plot(xlinsp_hot, tempC1hot, label='Thermocouples, hot')
plt.plot(xlinsp_hot, tempOphot, label='Optris, hot')
plt.title('Pure Water Temperature Curves, Hot vs. Cold')
plt.xlabel('General Linspace For Time (units)')
plt.ylabel('Temperature (degrees Celsius)')
plt.legend()
plt.grid()
plt.show()

# probably need to cut off the plateau ending for the cold test...
'''
