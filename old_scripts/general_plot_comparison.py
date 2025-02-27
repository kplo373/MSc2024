# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:08:04 2024

Comparisons of Friday 12th July (50% nurdles with distilled water) and Wednesday 3rd
July (100% nurdles with distilled water) experiments.

@author: katep
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# If wanting to change the file naming convention, do ctrl+F+R to find and replace!

fileC1_50 = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Friday12July\CR3000_Table1.dat"
df_C1_50 = pd.read_csv(fileC1_50, delimiter=',', header=4)
print(df_C1_50)  # have given it 4 headers, so the first row (0th) immediately begins with results
# this file represents Friday 12th July's test, with 50% nurdles and distilled water initially chilled

fileC1_wed = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Wednesday3July\CR3000_Table1.dat"
df_C1_wed = pd.read_csv(fileC1_wed, delimiter=',', header=4)
print(df_C1_wed)
# this file represents Wed 3rd July's test, with 100% nurdles and distilled water initially chilled

#%% Extract data from Friday 12th July Campbell Table 1 file
# Preallocating the datetime object, temperature, and standard deviation arrays
dt_objsC150 = np.zeros(len(df_C1_50), dtype='datetime64[s]')

temp1_C150 = np.zeros(len(df_C1_50))
temp2_C150 = np.zeros(len(df_C1_50))
temp3_C150 = np.zeros(len(df_C1_50))
temp4_C150 = np.zeros(len(df_C1_50))
temp5_C150 = np.zeros(len(df_C1_50))
temp6_C150 = np.zeros(len(df_C1_50))

stdev1_C150 = np.zeros(len(df_C1_50))
stdev2_C150 = np.zeros(len(df_C1_50))
stdev3_C150 = np.zeros(len(df_C1_50))
stdev4_C150 = np.zeros(len(df_C1_50))
stdev5_C150 = np.zeros(len(df_C1_50))
stdev6_C150 = np.zeros(len(df_C1_50))

count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
for i in range(0, len(df_C1_50)):
    row_seriesC1 = df_C1_50.iloc[i]
    timestr = str(row_seriesC1[0])  # e.g. 2024-06-13 10:59:55, type string
    #print(timestr)  # now need to convert it to a datetime object
    the_date_50 = timestr[:10]  # extracting the date to print along x-axis
    dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
    dt_objsC150[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

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
    
    temp1_C150[count] = temp1
    temp2_C150[count] = temp2
    temp3_C150[count] = temp3
    temp4_C150[count] = temp4
    temp5_C150[count] = temp5
    temp6_C150[count] = temp6
    stdev1_C150[count] = stdev1
    stdev2_C150[count] = stdev2
    stdev3_C150[count] = stdev3
    stdev4_C150[count] = stdev4
    stdev5_C150[count] = stdev5
    stdev6_C150[count] = stdev6
    
    count += 1
    print(count)

print(count, len(temp1_C150)) 


#%% Extract data from Wed 3 July Campbell Table 1 file
# Preallocating the datetime object, temperature, and standard deviation arrays
dt_objsC1wed = np.zeros(len(df_C1_wed), dtype='datetime64[s]')

temp1_C1wed = np.zeros(len(df_C1_wed))
temp2_C1wed = np.zeros(len(df_C1_wed))
temp3_C1wed = np.zeros(len(df_C1_wed))
temp4_C1wed = np.zeros(len(df_C1_wed))
temp5_C1wed = np.zeros(len(df_C1_wed))
temp6_C1wed = np.zeros(len(df_C1_wed))

stdev1_C1wed = np.zeros(len(df_C1_wed))
stdev2_C1wed = np.zeros(len(df_C1_wed))
stdev3_C1wed = np.zeros(len(df_C1_wed))
stdev4_C1wed = np.zeros(len(df_C1_wed))
stdev5_C1wed = np.zeros(len(df_C1_wed))
stdev6_C1wed = np.zeros(len(df_C1_wed))

count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
for i in range(0, len(df_C1_wed)):
    row_seriesC1 = df_C1_wed.iloc[i]
    #print(row_seriesC1)
    timestr = str(row_seriesC1[0])  # e.g. 2024-06-13 10:59:55, type string
    #print(timestr)  # now need to convert it to a datetime object
    the_date_wed = timestr[:10]  # extracting the date to print along x-axis
    dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
    dt_objsC1wed[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

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
    
    temp1_C1wed[count] = temp1
    temp2_C1wed[count] = temp2
    temp3_C1wed[count] = temp3
    temp4_C1wed[count] = temp4
    temp5_C1wed[count] = temp5
    temp6_C1wed[count] = temp6
    stdev1_C1wed[count] = stdev1
    stdev2_C1wed[count] = stdev2
    stdev3_C1wed[count] = stdev3
    stdev4_C1wed[count] = stdev4
    stdev5_C1wed[count] = stdev5
    stdev6_C1wed[count] = stdev6
    
    count += 1
    print(count)

print(count, len(temp1_C1wed)) 


# not easy to plot their temperature data on top of each other, because the dt_objs are different
# so go straight to scatterplot lines below...
#%% Take the mean/average of all consistent thermocouples (think it's all of them??)
ref_temps_C150 = np.zeros(len(temp1_C150))
ref_temps_C150 = (temp1_C150 + temp2_C150 + temp3_C150 + temp4_C150 + temp5_C150 + temp6_C150)/6  # taking the average. what is new stdev??
print(ref_temps_C150)

ref_temps_C1wed = np.zeros(len(temp1_C1wed))
ref_temps_C1wed = (temp1_C1wed + temp2_C1wed + temp3_C1wed + temp4_C1wed + temp5_C1wed + temp6_C1wed)/6  # taking the average. what is new stdev??
print(ref_temps_C1wed)


#---------------------------------------------------------------------------------
#%% Check Optris too!
# To extract the data from the headers of the Optris data, read first 7 lines
path_Op50 = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Friday12July\Fri12JulyOptris.dat"
with open(path_Op50, 'r') as file:
    headers_50 = [next(file).strip() for _ in range(7)]
print(headers_50)  # Now, there are 4x different measurement areas


path_Opwed = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Wednesday3July\Wed3JulyOptris.dat"
with open(path_Opwed, 'r') as file:
    headers_wed = [next(file).strip() for _ in range(7)]
print(headers_wed)  # Now, there are 4x different measurement areas


#%%
# Extract date and time from the relevant lines
date_line_50 = headers_50[1]  # This is line Date: 13/06/2024
time_line_50 = headers_50[2]  # This is line Time: 10:51:17.112

date_line_wed = headers_wed[1]  # This is line Date: 13/06/2024
time_line_wed = headers_wed[2]  # This is line Time: 10:51:17.112

# Split the lines to get the actual date and time values
date_val_50 = date_line_50.split('\t')[1]
time_val_50 = time_line_50.split('\t')[1]

date_val_wed = date_line_wed.split('\t')[1]
time_val_wed = time_line_wed.split('\t')[1]

print(f"Date: {date_val_50}")
print(f"Time: {time_val_50}")
print(f"Date: {date_val_wed}")
print(f"Time: {time_val_wed}")  # nice, this is it! Now need to add on the individual seconds time for each measurement...
# time is a string, so need to turn into datetime obj to add seconds onto it

# Combine date and time to a single string
datetime_str50 = date_val_50 + ' ' + time_val_50   #f"{date_value} {time_value}"  is chatGPT's method
datetime_strwed = date_val_wed + ' ' + time_val_wed

# Convert the combined string to a datetime object
datetime_format = "%d/%m/%Y %H:%M:%S.%f"
start_datetimeobj50 = datetime.strptime(datetime_str50, datetime_format)
start_datetimeobjwed = datetime.strptime(datetime_strwed, datetime_format)
print(start_datetimeobj50)
print(start_datetimeobjwed)

df_Op50 = pd.read_csv(path_Op50, delimiter='\t', header=7) #, index_col=None)  # extracting the rest of the file as a dataframe
print(df_Op50)  # there is an extra column of NaN values at the end...

df_Opwed = pd.read_csv(path_Opwed, delimiter='\t', header=7) #, index_col=None)  # extracting the rest of the file as a dataframe
print(df_Opwed)  # there is an extra column of NaN values at the end...


# Function to convert time string to timedelta
def time_str_to_timedelta(time_str):
    # Time string format is 'HH:MM:SS.sss'
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = map(float, seconds.split('.'))
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=milliseconds)

# Add the time deltas to the initial datetime
df_Op50['Datetime'] = df_Op50.iloc[:-2, 0].apply(lambda x: start_datetimeobj50 + time_str_to_timedelta(x))
df_Opwed['Datetime'] = df_Opwed.iloc[:-2, 0].apply(lambda x: start_datetimeobjwed + time_str_to_timedelta(x))
#added in the stop before the last 2 rows, as these do not contain actual data (e.g. '---', 'End of File')

print(df_Op50['Datetime'])
print(df_Opwed['Datetime'])  # looks good, now the 0th column in the dataframe has been changed to the full datetime.
# still has the last two rows as 'NaT' but we don't really want these rows included at all...

#%% Assign new names to the data columns
print(df_Op50.columns)   # has 9 columns
print(df_Opwed.columns)  # has only 5 columns

new_column_names_9 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'Area5', 'Area6', 'Area7', 'Area8', 'nan', 'Datetime']  # not sure what 'Unnamed: 3' column is for? so made it 'nan'
new_column_names_5 = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']

df_Op50.columns = new_column_names_9      # assigning them to the DataFrame by correct length
df_Opwed.columns = new_column_names_5
df_Op50 = df_Op50.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
df_Opwed = df_Opwed.drop(columns=['Time'])
df_Op50 = df_Op50.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 3' column too
df_Opwed = df_Opwed.drop(columns=['nan'])
print(df_Op50.columns)


#%% Extract the data from these columns, into separate arrays
area150 = df_Op50['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
area250 = df_Op50['Area2']  # temperature avg of water surface above submerged thermocouples
area350 = df_Op50['Area3']  # temperature avg of whole/half of surface of the water
area450 = df_Op50['Area4']  # temperature avg of water surface above submerged thermocouples
datetimeOp50 = df_Op50['Datetime']

area1wed = df_Opwed['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
area2wed = df_Opwed['Area2']  # temperature avg of water surface above submerged thermocouples
area3wed = df_Opwed['Area3']  # temperature avg of whole/half of surface of the water
area4wed = df_Opwed['Area4']  # temperature avg of water surface above submerged thermocouples
datetimeOpwed = df_Opwed['Datetime']

print(area150)

#%% Get two means for Optris data - mean for half of surface, and mean for thermocouple surface
mean_Op_half50 = np.zeros(len(area150))
mean_Op_small50 = np.zeros(len(area150))
mean_Op_halfwed = np.zeros(len(area1wed))
mean_Op_smallwed = np.zeros(len(area1wed))

mean_Op_half50 = (area150 + area350)/2   # taking the average
mean_Op_small50 = (area250 + area450)/2
mean_Op_halfwed = (area1wed + area3wed)/2
mean_Op_smallwed = (area2wed + area4wed)/2


#%% To get average of mean/average Optris measurements - RESAMPLING
#new_datetimes has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!

#using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
df_new50 = pd.DataFrame({               # creating a new dataframe for 50nesday 3rd
    'datetimes': datetimeOp50,
    'Op_temp_half': mean_Op_half50,
    'Op_temp_small': mean_Op_small50
})
df_newwed = pd.DataFrame({               # creating another new dataframe for Wed 3rd
    'datetimes': datetimeOpwed,
    'Op_temp_half': mean_Op_halfwed,
    'Op_temp_small': mean_Op_smallwed
})


df_new50.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
df_newwed.set_index('datetimes', inplace=True)
#maybe the datetimes should just be column 0?? need to extract them.. can I use the .index? YES

# Define a function to calculate standard error
def standard_error(x):
    return x.std() / np.sqrt(len(x))

resampled_df50 = df_new50.resample('5S').agg({
    'Op_temp_half': ['mean', 'std', standard_error],
    'Op_temp_small': ['mean', 'std', standard_error]
})  # resampling whole dataframe to 5 sec intervals and averaging temp, plus getting stdev and sterr
resampled_dfwed = df_newwed.resample('5S').agg({
    'Op_temp_half': ['mean', 'std', standard_error],
    'Op_temp_small': ['mean', 'std', standard_error]
})


resampled_df50.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns
resampled_dfwed.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns

print(resampled_df50.columns)


#%%
resampled_dt50 = resampled_df50.index
Op_half50 = resampled_df50['mean_temp_half']
Op_small50 = resampled_df50['mean_temp_small']

resampled_dtwed = resampled_dfwed.index
Op_halfwed = resampled_dfwed['mean_temp_half']
Op_smallwed = resampled_dfwed['mean_temp_small']

#%% Need to cut out some of the times where only one sensor collects data... can print dt_objsC1 and resampled_dt for Optris

# Create DataFrames for both sensors and both days
dfOp50 = pd.DataFrame({
    'datetime': resampled_dt50,
    'temperature1': Op_small50
})
dfOpwed = pd.DataFrame({
    'datetime': resampled_dtwed,
    'temperature1': Op_smallwed
})

dfC150 = pd.DataFrame({
    'datetime': dt_objsC150,
    'temperature2': ref_temps_C150
})
dfC1wed = pd.DataFrame({
    'datetime': dt_objsC1wed,
    'temperature2': ref_temps_C1wed
})


# Set the datetime column as the index
dfOp50.set_index('datetime', inplace=True)
dfC150.set_index('datetime', inplace=True)
dfOpwed.set_index('datetime', inplace=True)
dfC1wed.set_index('datetime', inplace=True)

# Already defined a function for standard_error above...
# Resample to 5-second intervals and calculate mean, std deviation, and std error for both temperature arrays
new_dfOp50 = dfOp50.resample('5S').agg({
    'temperature1': ['mean', 'std', standard_error]
})
new_dfC150 = dfC150.resample('5S').agg({
    'temperature2': ['mean', 'std', standard_error]
})

new_dfOpwed = dfOpwed.resample('5S').agg({
    'temperature1': ['mean', 'std', standard_error]
})
new_dfC1wed = dfC1wed.resample('5S').agg({
    'temperature2': ['mean', 'std', standard_error]
})


# Rename the columns for clarity
new_dfOp50.columns = ['mean_temp1', 'stddev_temp1', 'stderr_temp1']
new_dfC150.columns = ['mean_temp2', 'stddev_temp2', 'stderr_temp2']

new_dfOpwed.columns = ['mean_temp1', 'stddev_temp1', 'stderr_temp1']
new_dfC1wed.columns = ['mean_temp2', 'stddev_temp2', 'stderr_temp2']


# Merge the DataFrames on the datetime index
merged_df50 = pd.merge(new_dfOp50, new_dfC150, on='datetime')
merged_dfwed = pd.merge(new_dfOpwed, new_dfC1wed, on='datetime')
print(merged_df50)


#%% Plot these merged dataframe temperatures against each other
tempOp_orig50 = merged_df50['mean_temp1']
tempC1_orig50 = merged_df50['mean_temp2']

tempOp_origwed = merged_dfwed['mean_temp1']
tempC1_origwed = merged_dfwed['mean_temp2']


tempOp50 = tempOp_orig50[135:]
tempC150 = tempC1_orig50[135:]
tempOpwed = tempOp_origwed[135:]
tempC1wed = tempC1_origwed[135:]
# was otherwise plotting strangely, so I cut out some initial ambient temperatures^^

plt.plot(tempC1wed, tempOpwed, label='Wed 3 July, 0%')
plt.plot(tempC150, tempOp50, label='Fri 12 July, 50%')
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.title('Comparison of Optris vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()


#%% Adding a linear line of best fit:
plt.plot(tempC1wed, tempOpwed, label='Original Data Wed 3 July, 0%')
plt.plot(tempC150, tempOp50, label='Original Data Fri 12 July, 50%')

p_50 = np.poly1d(np.polyfit(tempC150, tempOp50, 1))
p_wed = np.poly1d(np.polyfit(tempC1wed, tempOpwed, 1))
plt.plot(tempC1wed, p_wed(tempC1wed), label="Best Fit Line Wed 3 July")
plt.plot(tempC150, p_50(tempC150), label="Best Fit Line Fri 12 July")

plt.title('Comparison of Optris vs. Thermocouples')
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.legend()
plt.grid()
plt.show()



