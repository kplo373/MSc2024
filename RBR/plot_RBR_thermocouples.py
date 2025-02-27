# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:30:42 2024

A plotting script for the RBR sensor, to compare its data to the thermocouples
for checking the thermocouples' accuracy.

@author: kplo373
"""
import sys
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")
from read_CampbellSci import read_CampbellSci

sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024\RBR")
#from read_RBR import read_RBR
from read_RBR_excel import read_RBR_excel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Get RBR data
filepathR = r"D:\MSc Results\RBR_Test\Part1redo\060728_20241112_1014.xlsx"  # Part 1
#filepathR = r"D:\MSc Results\RBR_Test\Part2redo\060728_20241112_1055.xlsx"  # Part 2
timestampsR, tempsR = read_RBR_excel(filepathR)


# Get Thermocouple data
filepathT = r"D:\MSc Results\RBR_Test\Part1redo\CR3000_Table1.dat"  # Part 1
#filepathT = r"D:\MSc Results\RBR_Test\Part2redo\CR3000_Table1.dat"  # Part 2
dt_objsT, temps_arrT, stdevsT = read_CampbellSci(filepathT)  # this should give 6x thermocouple arrays of temperature and standard deviation
print(temps_arrT)  # has shape (6, 794) - will have to split them up into each thermocouple if wanting to plot each of them

# Extracting the 6 thermocouple temperatures from the combined temps_arrT
tempT1 = temps_arrT[0]
tempT2 = temps_arrT[1]
tempT3 = temps_arrT[2]
tempT4 = temps_arrT[3]
tempT5 = temps_arrT[4]
tempT6 = temps_arrT[5]


# Using 5th Percentile Minimum Value for both arrays, using the RBR data - skip this for Part 2 onwards, as devices were already warmed up!!
# 1. Calculate the 5th percentile (minimum 5%) value
percentile_5_value = np.percentile(tempsR, 5)
# 2. Find the index of the closest value in tempsR to the 5th percentile value
index_5 = np.argmin(np.abs(tempsR - percentile_5_value))
# Print the result
print(f"5th percentile value: {percentile_5_value}")
print(f"Index of 5th percentile value in RBR temperatures: {index_5}")
tempsR = tempsR[index_5:]
timestampsR = timestampsR[index_5:]   # this ndarray is of datetime64s


df_R = pd.DataFrame({'temp_RBR': tempsR}, index = timestampsR)
df_CS = pd.DataFrame({'temp_T1': tempT1, 'temp_T2': tempT2, 'temp_T3': tempT3, 'temp_T4': tempT4, 'temp_T5': tempT5, 'temp_T6': tempT6}, index = dt_objsT)

#%% Use this bit if there is a time difference in RBR data file
# Step 1: Calculate the time difference
#correct_time = pd.Timestamp('2024-10-16T11:49:00')  # what I wrote in my book for Part 1, not sure exactly what second it was though...
#correct_time = pd.Timestamp('2024-10-16T13:10:00')  # started Part 2 at 1:10pm
#correct_time = pd.Timestamp('2024-10-16T15:00:00')  # started Part 2 retry at 3:00pm
#incorrect_time = pd.Timestamp(df_R.index[0])  # the first entry of df_R.index
#time_diff = correct_time - incorrect_time  # use this to correct the time

# Step 2: Shift the timestamps of the incorrect sensor
#df_R['corrected_time'] = df_R.index + time_diff

# Step 3: Merge the dataframes on the corrected timestamp
#df_merged = pd.merge(df_CS, df_R, left_on=df_CS.index, right_on='corrected_time', suffixes=('_CS', '_R'))

# Merge the resampled Optris data with the C1 data
df_merged = df_CS.join(df_R, how='inner', lsuffix='_CS', rsuffix='_R')  # this only includes values from both arrays (cutting out any values from only one sensor)


# Removing first 15 minutes (Part 1 only, otherwise minutes=0) of the whole dataframe
start_t0 = df_merged.index.min()
cutoff_t0 = start_t0 + pd.Timedelta(minutes=0)
df_trimmed = df_merged[df_merged.index >= cutoff_t0]


t1 = df_trimmed['temp_T1']
t2 = df_trimmed['temp_T2']
t3 = df_trimmed['temp_T3']
t4 = df_trimmed['temp_T4']
t5 = df_trimmed['temp_T5']
t6 = df_trimmed['temp_T6']
tR = df_trimmed['temp_RBR']
dt = np.array(df_trimmed.index)  # for the time in datetime objects
# Now all of these temperatures and datetimes are arrays of the same length!


#%%
dt_py = pd.to_datetime(dt[0]).to_pydatetime()  # to allow clear x-axis label

# Plotting all 6 thermocouples and the RBR as 7 separate lines
plt.plot(dt, tR, label='RBR')
plt.plot(dt, t1, label='Thermocouple 1')
plt.plot(dt, t2, label='Thermocouple 2')
plt.plot(dt, t3, label='Thermocouple 3')
plt.plot(dt, t4, label='Thermocouple 4')
plt.plot(dt, t5, label='Thermocouple 5')
plt.plot(dt, t6, label='Thermocouple 6')
plt.xlim(dt[0], dt[-1])
plt.title('RBR and Thermocouple Comparison - Pump on')
plt.ylabel('Temperature (degrees Celsius)')
plt.xlabel(dt_py.strftime('%d %B %Y'))  # having the actual date on the line below the x-axis time labels for context
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line
plt.legend()
plt.grid()
plt.show()


#%% Plotting average thermocouple temperatures against the RBR to compare over time
avgt = np.zeros(len(t1))
avgt = (t1 + t2 + t3 + t4 + t5 + t6) / 6
# am ignoring standard deviation here... can get the calculation from read_CampbellSci.py if needed

plt.plot(dt, tR, label='RBR')
plt.plot(dt, avgt, label='Average Thermocouples')
plt.title('RBR and Thermocouple Average Comparison - Pump on')
plt.ylabel('Temperature (degrees Celsius)')
plt.xlabel(dt_py.strftime('%d %B %Y'))  # having the actual date on the line below the x-axis time labels for context
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line
plt.xlim(dt[0], dt[-1])
plt.grid()
plt.legend()
plt.show()

#%% Plot the difference between the RBR and average thermocouple temperature
# Calculate the difference first
diff_arr = tR - avgt  # looks like RBR has higher temperature than thermocouples for both parts
print(diff_arr)

plt.plot(dt, diff_arr)
plt.axhline(y=0, color='k', linestyle='-')
plt.title('Average Temperature Differences - Pump on')
plt.ylabel(r'$\Delta T$ (degrees Celsius)')
plt.xlabel(dt_py.strftime('%d %B %Y'))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xlim(dt[0], dt[-1])
plt.ylim(-0.05, 0.45)
plt.grid()
plt.show()

# To show range of temperature differences
print(max(diff_arr))  # now can use this value, 0.442 deg C, as the thermocouples' uncertainty, after adding it to the RBR's uncertainty
print(min(diff_arr))
