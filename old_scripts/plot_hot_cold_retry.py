# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:10:51 2024

Retrying to get my nice professional green line plots back from accidentally replacing it with an older version of the file...

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


fileC1_hot = r"D:\MSc Results\July_2024\Friday19JulyAM\CR3000_Table1.dat"
df_C1_hot = pd.read_csv(fileC1_hot, delimiter=',', header=4)
print(df_C1_hot)  # have given it 4 headers, so the first row (0th) immediately begins with results
# this file represents hot Friday 18th July's test, with pure distilled water initially heated in oven at 40 deg C

fileC1_cold = r"D:\MSc Results\July_2024\Tues23JulyAM\CR3000_Table1.dat"
df_C1_cold = pd.read_csv(fileC1_cold, delimiter=',', header=4)
print(df_C1_cold)
# this file represents cold 24th July's test, with pure distilled water initially chilled

# Choose the filepaths of the Optris .dat files and insert here
path_Ophot = r"D:\MSc Results\July_2024\Friday19JulyAM\Fri19JulyOptris.dat"
path_Opcold = r"D:\MSc Results\July_2024\Tues23JulyAM\Tues23JulyOptris.dat"


#%% Extract data from the initially hot test's Campbell Table 1 file
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


#%% Extract data from the cold Campbell Table 1 file
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


#%% Extract date and time from hot and cold Optris, convert to datetime objects
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

#%% Read the Optris files into dataframes, ignoring errors (from chatGPT)
try: 
    df_Ophot = pd.read_csv(path_Ophot, delimiter='\t', encoding='utf-8', header=7)
    df_Opcold = pd.read_csv(path_Opcold, delimiter='\t', encoding='utf-8', header=7)
    print(df_Ophot)
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")


#%% Convert Optris times from timedeltas into dt objs, set up columns for df_Opcold and df_Ophot
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

# Now get the other columns!!
# Assign new names to the data columns
print(df_Ophot.columns)   # has 9 columns
print(df_Opcold.columns)  # has only 5 columns

new_column_names_9 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']  # not sure what 'Unnamed: 3' column is for? so made it 'nan'
new_column_names_5 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']

df_Ophot.columns = new_column_names_9      # assigning them to the DataFrame by correct length
df_Opcold.columns = new_column_names_5
df_Ophot = df_Ophot.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
df_Opcold = df_Opcold.drop(columns=['Time'])
df_Ophot = df_Ophot.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 3' column too
df_Opcold = df_Opcold.drop(columns=['nan'])
print(df_Ophot.columns)


#%% Extract the data from these columns, into separate pandas series, then take the averages
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

# Get two means for Optris data - mean for half of surface, and mean for thermocouple surface
mean_Op_halfhot = np.zeros(len(area1hot))
mean_Op_smallhot = np.zeros(len(area1hot))
mean_Op_halfcold = np.zeros(len(area1cold))
mean_Op_smallcold = np.zeros(len(area1cold))

mean_Op_halfhot = (area1hot + area3hot)/2   # taking the average, what is new stdev??
mean_Op_smallhot = (area2hot + area4hot)/2  # and this stdev??
mean_Op_halfcold = (area1cold + area3cold)/2
mean_Op_smallcold = (area2cold + area4cold)/2


#%% To get average of mean/average Optris measurements - RESAMPLING (this bit is in resample_Optris.py)
#new_datetimes has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!

#using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
df_newhot = pd.DataFrame({               # creating a new dataframe for wednesday 3rd
    'datetimes': datetimeOphot,
    'Op_temp_half': mean_Op_halfhot,
    'Op_temp_small': mean_Op_smallhot})
df_newcold = pd.DataFrame({               # creating another new dataframe for cold 3rd
    'datetimes': datetimeOpcold,
    'Op_temp_half': mean_Op_halfcold,
    'Op_temp_small': mean_Op_smallcold})


df_newhot.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
df_newcold.set_index('datetimes', inplace=True)
# can extract datetimes using e.g. df_newhot.index - this is just for Optris still

# Define a function to calculate standard error
def standard_error(x):
    return x.std() / np.sqrt(len(x))

resampled_dfhot = df_newhot.resample('5s').agg({'Op_temp_half': ['mean', 'std', standard_error],
                                                'Op_temp_small': ['mean', 'std', standard_error]})  
# resampling whole dataframe to 5 sec intervals by taking the mean of temp, plus getting stdev and sterr
resampled_dfcold = df_newcold.resample('5s').agg({'Op_temp_half': ['mean', 'std', standard_error],
                                                  'Op_temp_small': ['mean', 'std', standard_error]})
# e.g. df.resample("3s").agg({'x':'sum','y':'mean','z':'last'}) can be used if using different functions for different columns

resampled_dfhot.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns
resampled_dfcold.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns

print(resampled_dfhot.columns)  # these are only for Optris, not Campbell Sci thermocouples.


#%% Setting up dataframes for Optris and Campbell Scientific cold temperature arrays
# Assuming Tcold_Op is the temperature array and Tcold_time_Op is the corresponding time array
dtcold_Op = pd.to_datetime(resampled_dfcold.index)  # getting datetime index column as an array from Optris, then converting to pandas datetime
Tcold_Op = mean_Op_smallcold.to_numpy()
df_optris = pd.DataFrame({'temperature': Tcold_Op}, index = datetimeOpcold)  # didn't work with dtcold_Op

# Resample to 5-second intervals, taking the mean for each interval
df_optris_resampled = df_optris.resample('5s').mean()

# Extract the resampled temperature and time arrays
Tcold_Op_resampled = df_optris_resampled['temperature'].values
Tcold_time_Op_resampled = df_optris_resampled.index

Tcold_C1 = ref_temps_C1cold

# Verify the lengths now match
print(f"Length of Tcold_Op_resampled: {len(Tcold_Op_resampled)}")
print(f"Length of Tcold_C1: {len(Tcold_C1)}")  # they don't actually match, but are on the same scale now! df_merged line below only includes values from both arrays

# Create a dataframe for C1 data
df_C1 = pd.DataFrame({'temperature': Tcold_C1}, index = dt_objsC1cold)

# Merge the resampled Optris data with the C1 data
df_merged = df_C1.join(df_optris_resampled, how='inner', lsuffix='_C1', rsuffix='_Op')

# Now you can access the aligned temperature arrays
Tcold_C1_aligned = df_merged['temperature_C1'].values
Tcold_Op_aligned = df_merged['temperature_Op'].values


#%% Repeating the above for the hot arrays, putting into dataframes
dthot_Op = pd.to_datetime(resampled_dfhot.index)  # getting datetime index column as an array from Optris, then converting to pandas datetime
T_hot_Op = mean_Op_smallhot.to_numpy()
df_optrisH = pd.DataFrame({'temperature': T_hot_Op}, index = datetimeOphot)  # didn't work with dthot_Op

# Resample to 5-second intervals, taking the mean for each interval
df_optrisH_resampled = df_optrisH.resample('5s').mean()

# Extract the resampled temperature and time arrays
T_hot_Op_resampled = df_optrisH_resampled['temperature'].values
T_hot_time_Op_resampled = df_optris_resampled.index

T_hot_C1 = ref_temps_C1hot

# Verify the lengths now match
print(f"Length of T_hot_Op_resampled: {len(T_hot_Op_resampled)}")
print(f"Length of T_hot_C1: {len(T_hot_C1)}")

# Create a dataframe for C1 data
df_C1H = pd.DataFrame({'temperature': T_hot_C1}, index = dt_objsC1hot)

# Merge the resampled Optris data with the C1 data
df_mergedH = df_C1H.join(df_optrisH_resampled, how='inner', lsuffix='_C1', rsuffix='_Op')

# Now you can access the aligned temperature arrays
T_hot_C1_aligned = df_mergedH['temperature_C1'].values
T_hot_Op_aligned = df_mergedH['temperature_Op'].values



#%% Plot these merged dataframe temperatures against each other
tempOp_orighot = T_hot_Op_aligned
tempC1_orighot = T_hot_C1_aligned

tempOp_origcold = Tcold_Op_aligned
tempC1_origcold = Tcold_C1_aligned



#%% Using 5th Percentile Minimum Value (from ChatGPT) for Cold and Hot Arrays
# 1. Calculate the 5th percentile value
percentile_5_value = np.percentile(tempOp_origcold, 5)
# 2. Find the index of the closest value in y_cold to the 95th percentile value
index_5 = np.argmin(np.abs(tempOp_origcold - percentile_5_value))
# Print the result
print(f"5th percentile value: {percentile_5_value}")
print(f"Index of 5th percentile value in y_cold: {index_5}")
print(f"Corresponding x_cold value: {tempC1_origcold[index_5]}")  # or else add .iloc[index_95] if tempC1_origcold is a pandas series
print()

# Likewise, using 95th Percentile Max Value for Hot Array
percentile_95_value = np.percentile(tempC1_orighot, 95)
index_95 = np.argmin(np.abs(tempC1_orighot - percentile_95_value))
print(f"95th percentile value: {percentile_95_value}")
print(f"Index of 95th percentile value in x_hot: {index_95}")
print(f"Corresponding y_hot value: {tempOp_orighot[index_95]}")


#%% Cutting out some initial ambient temperatures
tempOphot = tempOp_orighot[index_95:]  # this needs to start and end at same indices as tempC1hot
tempC1hot = tempC1_orighot[index_95:] 
tempOpcold = tempOp_origcold[index_5:]
tempC1cold = tempC1_origcold[index_5:]

plt.plot(tempC1cold, tempOpcold, label='Wed 24 July PM, cold')  # only plots from 22.6-24 deg C
plt.plot(tempC1hot, tempOphot, label='Thurs 18 July PM, hot')
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.title('Pure Water Comparison of Optris vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()



#%% Fitting the Pure Water Calibration SVM curve (using ChatGPT)
import joblib

# Load the saved model and scalers
svr_rbf_pure_water = joblib.load(r"D:\MSc Results\svr_rbf_pure_water.pkl")
scaler_y_pure_water = joblib.load(r"D:\MSc Results\scaler_y_pure_water.pkl")

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


#%% Need to create limits for the plots below so that the plots are square-shaped
import math
def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

lower_limit = min(x_cold[0,0], y_cold[0,0])
lower_lim = normal_round(lower_limit) - 1

upper_limit = max(x_hot_asc[-1,0], y_hot_asc[-1,0])
upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below


#%% Plot the results
plt.figure(figsize=(7, 7))  # make it into a square shape, same axes limits!
plt.scatter(x_cold, y_cold, color='blue', label='Cold data (50% Pellet Water)')
plt.scatter(x_hot_asc, y_hot_asc, color='red', label='Hot data (50% Pellet Water)')

# To plot the 1:1 reference line - can also plot this in SVM results plot below...
xlim = plt.gca().get_xlim()  # get the current limits of the plot
ylim = plt.gca().get_ylim()
line_min = min(xlim[0], ylim[0])  # determine the start and end points of the 1:1 line
line_max = max(xlim[1], ylim[1])
# Plot the 1:1 line across the entire plot from corner to corner
plt.plot([line_min, line_max], [line_min, line_max], color='black', linestyle='--', label='1:1 Reference Line (y=x)')

plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
plt.ylim(lower_lim, upper_lim)


plt.xlabel('Campbell Scientific Thermocouple Temperature (degrees Celsius)')
plt.ylabel('Optris Thermal Camera Temperature (degrees Celsius)')
plt.title('50% Pellet-Water Raw Comparison of Optris vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()


#%% Plot SVM Results, Add in Reference Line too
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


#%% havent got this cell working yet
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







