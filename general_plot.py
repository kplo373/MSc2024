# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:29:24 2024

General extracting and plotting script for Optris thermal camera and 
Campbell Scientific logger (x6) thermocouples comparison.

You just need to update the filepath to where the Optris and Campbell
Sci Table 1 .dat files are, along with their file names, and it should
work! (these two filepaths are under the first #--------- line.)
       
Remember to use '%matplotlib inline' in the little terminal first, or 
else it will put all the plots into one combined plot...

@author: katep
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#-----------------------------------------------------------------------------------------------------------
fileC1 = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Wednesday17July\CR3000_Table1.dat"
df_Campbell1 = pd.read_csv(fileC1, delimiter=',', header=4)
print(df_Campbell1)  # have given it 4 headers, so the first row (0th) immediately begins with results

path_Op = r"C:\Users\katep\OneDrive\Desktop\MSc_2024\Plotting_Temp_Timeseries\Wednesday17July\Wed17JulyOptris.dat"
# to use below later...

#%% Extract data from Campbell Sci Table 1

the_index = df_Campbell1.index  # don't need this at all, but it's there

# Preallocating the datetime object, temperature, and standard deviation arrays
dt_objsC1 = np.zeros(len(df_Campbell1), dtype='datetime64[s]')

temp1_C1 = np.zeros(len(df_Campbell1))
temp2_C1 = np.zeros(len(df_Campbell1))
temp3_C1 = np.zeros(len(df_Campbell1))
temp4_C1 = np.zeros(len(df_Campbell1))
temp5_C1 = np.zeros(len(df_Campbell1))
temp6_C1 = np.zeros(len(df_Campbell1))

stdev1_C1 = np.zeros(len(df_Campbell1))
stdev2_C1 = np.zeros(len(df_Campbell1))
stdev3_C1 = np.zeros(len(df_Campbell1))
stdev4_C1 = np.zeros(len(df_Campbell1))
stdev5_C1 = np.zeros(len(df_Campbell1))
stdev6_C1 = np.zeros(len(df_Campbell1))

count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
for i in range(0, len(df_Campbell1)):
    row_seriesC1 = df_Campbell1.iloc[i]
    #print(row_seriesC1)
    timestr = str(row_seriesC1[0])  # e.g. 2024-06-13 10:59:55, type string
    #print(timestr)  # now need to convert it to a datetime object
    the_date = timestr[:10]  # extracting the date to print along x-axis
    dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
    dt_objsC1[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

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
    
    temp1_C1[count] = temp1
    temp2_C1[count] = temp2
    temp3_C1[count] = temp3
    temp4_C1[count] = temp4
    temp5_C1[count] = temp5
    temp6_C1[count] = temp6
    stdev1_C1[count] = stdev1
    stdev2_C1[count] = stdev2
    stdev3_C1[count] = stdev3
    stdev4_C1[count] = stdev4
    stdev5_C1[count] = stdev5
    stdev6_C1[count] = stdev6
    
    count += 1
    print(count)

print(count, len(temp1_C1))  # they are actually the same length! So technically don't need the below...
dt_objsC1 = dt_objsC1[:count]
temp1_C1 = temp1_C1[:count]  # only taking up to the count value, so cutting off preallocated zeroes
temp2_C1 = temp2_C1[:count]
temp3_C1 = temp3_C1[:count]
temp4_C1 = temp4_C1[:count]
temp5_C1 = temp5_C1[:count]
temp6_C1 = temp6_C1[:count]
stdev1_C1 = stdev1_C1[:count]
stdev2_C1 = stdev2_C1[:count]
stdev3_C1 = stdev3_C1[:count]
stdev4_C1 = stdev4_C1[:count]
stdev5_C1 = stdev5_C1[:count]
stdev6_C1 = stdev6_C1[:count]

#%% Plot Campbell Sci Table 1 Data
start_time = dt_objsC1[500]  # to cut out ambient temperatures recorded prior to the experiment
end_time = dt_objsC1[len(dt_objsC1)-1]  # or can use index [-1]

plt.plot(dt_objsC1, temp1_C1, 'o', label='H1')
plt.plot(dt_objsC1, temp2_C1, 'o', label='H2')
plt.plot(dt_objsC1, temp3_C1, 'o', label='H3')
plt.plot(dt_objsC1, temp4_C1, 'o', label='H4')
plt.plot(dt_objsC1, temp5_C1, 'o', label='H5')
plt.plot(dt_objsC1, temp6_C1, 'o', label='H6')
plt.title('Campbell Scientific Logger Table 1 Data')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_time, end_time)
#plt.ylim(23, 27)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()

#%% Plot Table 1 with lines rather than individual points
plt.plot(dt_objsC1, temp1_C1, label='H1')
plt.plot(dt_objsC1, temp2_C1, label='H2')
plt.plot(dt_objsC1, temp3_C1, label='H3')
plt.plot(dt_objsC1, temp4_C1, label='H4')
plt.plot(dt_objsC1, temp5_C1, label='H5')
plt.plot(dt_objsC1, temp6_C1, label='H6')
plt.title(f'Campbell Scientific Logger Table 1, {the_date}')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_time, end_time)
#plt.ylim(24, 28)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()

#%% Take the mean/average of all consistent thermocouples (think it's all of them??)
ref_temps_C1 = np.zeros(len(temp1_C1))
ref_temps_C1 = (temp1_C1 + temp2_C1 + temp3_C1 + temp4_C1 + temp5_C1 + temp6_C1)/6  # taking the average. what is new stdev??
print(ref_temps_C1)
# not including temp1_C1 as it is slightly higher T than the other thermocouples... like 0.025 deg C higher

#Plotting and comparing to individual thermocouples:
plt.plot(dt_objsC1, temp1_C1, label='H1')
plt.plot(dt_objsC1, temp2_C1, label='H2')
plt.plot(dt_objsC1, temp3_C1, label='H3')
plt.plot(dt_objsC1, temp4_C1, label='H4')
plt.plot(dt_objsC1, temp5_C1, label='H5')
plt.plot(dt_objsC1, temp6_C1, label='H6')
plt.plot(dt_objsC1, ref_temps_C1, label='Mean')  # putting it last so it plots on top

plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Temperature (degrees Celsius)')
plt.title(f'Campbell Scientific Logger Table 1, {the_date}')
plt.legend()
plt.grid()
# plt.ylim(24, 28)
plt.xlim(start_time, end_time)  # use same relevant times from Optris above
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.show()


#-------------------------------------------------------------------------------------------------
#%% Check Optris too!
# To extract the data from the headers of the Optris data, read first 7 lines
with open(path_Op, 'r') as file:
    headers = [next(file).strip() for _ in range(7)]

print(headers)  # Now, there are 4x different measurement areas
# now I just need to get the date and time as individual variables...
#%%
# Extract date and time from the relevant lines
date_line = headers[1]  # This is line Date: 13/06/2024
time_line = headers[2]  # This is line Time: 10:51:17.112

# Split the lines to get the actual date and time values
date_val = date_line.split('\t')[1]
time_val = time_line.split('\t')[1]

print(f"Date: {date_val}")
print(f"Time: {time_val}")  # nice, this is it! Now need to add on the individual seconds time for each measurement...
# time is a string, so need to turn into datetime obj? to add it to seconds later?

# Combine date and time to a single string
datetime_str = date_val + ' ' + time_val   #f"{date_value} {time_value}"  is chatGPT's method

# Convert the combined string to a datetime object
datetime_format = "%d/%m/%Y %H:%M:%S.%f"
start_datetimeobj = datetime.strptime(datetime_str, datetime_format)
print(start_datetimeobj)

df_Op = pd.read_csv(path_Op, delimiter='\t', header=7) #, index_col=None)  # extracting the rest of the file as a dataframe
print(df_Op)  # there is an extra column of NaN values at the end...

# Function to convert time string to timedelta
def time_str_to_timedelta(time_str):
    # Time string format is 'HH:MM:SS.sss'
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = map(float, seconds.split('.'))
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=milliseconds)

# Add the time deltas to the initial datetime
df_Op['Datetime'] = df_Op.iloc[:-2, 0].apply(lambda x: start_datetimeobj + time_str_to_timedelta(x))
#added in the stop before the last 2 rows, as these do not contain actual data (e.g. '---', 'End of File')

print(df_Op['Datetime'])  # looks good, now the 0th column in the dataframe has been changed to the full datetime.
# still has the last two rows as 'NaT' but we don't really want these rows included at all...

#now get the other columns!!
#%% Assign new names to the data columns
print(df_Op.columns)  # has 5 columns...

new_column_names = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']  # not sure what 'Unnamed: 3' column is for? so made it 'nan'

df_Op.columns = new_column_names      # assigning them to the DataFrame
df_Op = df_Op.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
df_Op = df_Op.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 3' column too
print(df_Op.columns)


#%% Extract the data from these columns, into separate arrays
area1 = df_Op['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
area2 = df_Op['Area2']  # temperature avg of water surface above submerged thermocouples
area3 = df_Op['Area3']  # temperature avg of whole/half of surface of the water
area4 = df_Op['Area4']  # temperature avg of water surface above submerged thermocouples
datetimeOp = df_Op['Datetime']

print(area1)  # starts at 25.40 deg C, ends at 28.11 deg C (so maybe includes initial room temp)
# has 2 NaN values at the end... can I just plot it and it be okay? or do I need to cut these off?

#%% Plotting Optris data
start_t = datetimeOp[0]  # to cut off the initial spike from room temp, as the Optris was collecting data for like 8 mins before the expt started...
end_t = datetimeOp[len(datetimeOp)-1]
#[len(datetimeOp)-3]  # taking off 3 rows to remove the NaN values at the end to show the end of the file.

plt.plot(datetimeOp, area1, 'o', label='Half Surface 1')
plt.plot(datetimeOp, area2, 'o', label='Thermocouples Surface 2')
plt.plot(datetimeOp, area3, 'o', label='Half Surface 3')
plt.plot(datetimeOp, area4, 'o', label='Thermocouples Surface 4')

plt.title(f'Optris Thermal Camera, {the_date}')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Surface Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_t, end_t)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()

#%% Plotting Optris Data as connected lines
plt.plot(datetimeOp, area1, label='Half Surface 1')
plt.plot(datetimeOp, area2, label='Thermocouples Surface 2')
plt.plot(datetimeOp, area3, label='Half Surface 3')
plt.plot(datetimeOp, area4, label='Thermocouples Surface 4')

plt.title(f'Optris Thermal Camera, {the_date}')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Surface Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_t, end_t)
plt.ylim(11, 23)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()


#%% Get two means for Optris data - mean for half of surface, and mean for thermocouple surface
mean_Op_half = np.zeros(len(area1))
mean_Op_small = np.zeros(len(area1))

mean_Op_half = (area1 + area3)/2   # taking the average, what is new stdev??
mean_Op_small = (area2 + area4)/2  # and this stdev??


plt.plot(datetimeOp, area1, label='Half Surface 1')
plt.plot(datetimeOp, area2, label='Thermocouples Surface 2')
plt.plot(datetimeOp, area3, label='Half Surface 3')
plt.plot(datetimeOp, area4, label='Thermocouples Surface 4')

plt.plot(datetimeOp, mean_Op_half, label='Mean Half Surface')
plt.plot(datetimeOp, mean_Op_small, label='Mean Small Surface')

plt.title(f'Optris Thermal Camera, {the_date}')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Surface Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_t, end_t)
plt.ylim(11, 23)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()


#---------------------------
#%% Plot Comparison of Thermocouples to IR Camera
plt.plot(dt_objsC1, ref_temps_C1, label='Thermocouple Mean')

plt.plot(datetimeOp, mean_Op_half, label='Mean Half Surface')
plt.plot(datetimeOp, mean_Op_small, label='Mean Small Surface')

plt.title(f'Optris & Campbell Scientific Comparison, {the_date}')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_t, end_t)
plt.ylim(9, 22)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()


#%% To get average of mean/average Optris measurements - RESAMPLING
#new_datetimes has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!

#using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
df_new = pd.DataFrame({               # creating a new dataframe
    'datetimes': datetimeOp,
    'Op_temp_half': mean_Op_half,
    'Op_temp_small': mean_Op_small
})


df_new.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
#maybe the datetimes should just be column 0?? need to extract them.. can I use the .index? YES

# Define a function to calculate standard error
def standard_error(x):
    return x.std() / np.sqrt(len(x))

resampled_df = df_new.resample('5S').agg({
    'Op_temp_half': ['mean', 'std', standard_error],
    'Op_temp_small': ['mean', 'std', standard_error]
})  # resampling whole dataframe to 5 sec intervals and averaging temp, plus getting stdev and sterr


resampled_df.columns = ['mean_temp_half', 'stdev_temp_half', 'sterr_temp_half', 
                        'mean_temp_small', 'stdev_temp_small', 'sterr_temp_small']  # renaming columns


#print(resampled_df)
print(resampled_df.columns)  # use this format to get the avg_temp, also printing datetime as index
# now those names I gave 2 lines above are the ones that get printed as the dataframe's headers
# and the index of resampled_df (the row names) are the datetimes - how to extract this?

#%% Plot the two resampled (mean) Optris temperature arrays
resampled_dt = resampled_df.index
Op_half = resampled_df['mean_temp_half']
Op_small = resampled_df['mean_temp_small']
plt.plot(resampled_dt, Op_half, label='Mean Half Surface')
plt.plot(resampled_dt, Op_small, label='Mean Small Surface')

plt.title('Optris Temperature Timeseries')
plt.xlabel(f'{the_date} Local Time')
plt.ylabel('Temperature (degrees Celsius)')
#plt.xticks(rotation=30)  # to rotate the x-axis labels and prevent overlapping
plt.xlim(start_t, end_t)
plt.ylim(12, 22)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line

plt.legend()
plt.grid()
plt.show()


#%%
#need to cut out some of the times where only one sensor collects data... can print dt_objsC1 and resampled_dt for Optris

# Create DataFrames for both sensors
dfOp = pd.DataFrame({
    'datetime': resampled_dt,
    'temperature1': Op_small
})

dfC1 = pd.DataFrame({
    'datetime': dt_objsC1,
    'temperature2': ref_temps_C1
})

# Set the datetime column as the index
dfOp.set_index('datetime', inplace=True)
dfC1.set_index('datetime', inplace=True)

# Already defined a function for standard_error above...
# Resample to 5-second intervals and calculate mean, std deviation, and std error for both temperature arrays
new_dfOp = dfOp.resample('5S').agg({
    'temperature1': ['mean', 'std', standard_error]
})
new_dfC1 = dfC1.resample('5S').agg({
    'temperature2': ['mean', 'std', standard_error]
})

# Rename the columns for clarity
new_dfOp.columns = ['mean_temp1', 'stddev_temp1', 'stderr_temp1']
new_dfC1.columns = ['mean_temp2', 'stddev_temp2', 'stderr_temp2']

# Merge the DataFrames on the datetime index
merged_df = pd.merge(new_dfOp, new_dfC1, on='datetime')
print(merged_df)

#%% Plot these merged dataframe temperatures against each other
tempOp_orig = merged_df['mean_temp1']
tempC1_orig = merged_df['mean_temp2']

tempOp = tempOp_orig[:len(tempOp_orig)-350]
tempC1 = tempC1_orig[:len(tempOp_orig)-350]
# was otherwise plotting strangely, so I cut out some initial ambient temperatures^^

plt.plot(tempC1, tempOp)
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.title(f'Comparison of Optris vs. Thermocouples, {the_date}')
plt.grid()
plt.show()

#%%
# Adding a linear line of best fit:
plt.plot(tempC1, tempOp, label='Original Data')
p = np.poly1d(np.polyfit(tempC1, tempOp, 1))
plt.plot(tempC1, p(tempC1), label="Best Fit Line")
plt.title(f'Comparison of Optris vs. Thermocouples, {the_date}')
plt.xlabel('Campbell Scientific Table 1 Temperature (degrees Celsius)')
plt.ylabel('Optris Temperature (degrees Celsius)')
plt.legend()
plt.grid()
plt.show() 

#%%
R = np.corrcoef(tempC1, tempOp)
print(R)  # correlation coefficient, indicates strength of the linear relationship between the x and y variables

print(p)  # gives equation of line of best fit that was created in cell above (y=mx+c)

