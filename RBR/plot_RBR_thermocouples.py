# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:30:42 2024

A plotting script for the RBR sensor, to compare its data to the thermocouples
for checking the thermocouples' accuracy.

@author: kplo373
"""
import sys
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024\RBR")

from read_RBR import read_RBR
from read_CampbellSci import read_CampbellSci
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Get RBR data
#filepathR = r"D:\MSc Results\RBR_Test\060728_20241001_1004KateRBR.rsk"
filepathR = r"D:\MSc Results\RBR_Test\RBRtest2\060728_20241008_1145KateRBR2.rsk"
timestampsR, tempsR = read_RBR(filepathR)


# Get Thermocouple data
filepathT = r"D:\MSc Results\RBR_Test\CR3000_Table1.dat"
dt_objsT, temps_arrT, stdevsT = read_CampbellSci(filepathT)  # this should give 6x thermocouple arrays of temperature and standard deviation
print(temps_arrT)  # has shape (6, 794) - will have to split them up into each thermocouple if wanting to plot each of them

# Extracting the 6 thermocouple temperatures from the combined temps_arrT
tempT1 = temps_arrT[0]
tempT2 = temps_arrT[1]
tempT3 = temps_arrT[2]
tempT4 = temps_arrT[3]
tempT5 = temps_arrT[4]
tempT6 = temps_arrT[5]


# Using 5th Percentile Minimum Value (from ChatGPT) for both arrays, using the RBR data
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

# Merge the resampled Optris data with the C1 data
df_merged = df_CS.join(df_R, how='inner', lsuffix='_CS', rsuffix='_R')  # this only includes values from both arrays (cutting out any values from only one sensor)

t1 = df_merged['temp_T1']
t2 = df_merged['temp_T2']
t3 = df_merged['temp_T3']
t4 = df_merged['temp_T4']
t5 = df_merged['temp_T5']
t6 = df_merged['temp_T6']
tR = df_merged['temp_RBR']
dt = df_merged.index  # for the time in datetime objects
# Now all of these temperatures and datetimes are arrays of the same length!


# Plotting all 6 thermocouples and the RBR as 7 separate lines
plt.plot(dt, tR, label='RBR')
plt.plot(dt, t1, label='Thermocouple 1')
plt.plot(dt, t2, label='Thermocouple 2')
plt.plot(dt, t3, label='Thermocouple 3')
plt.plot(dt, t4, label='Thermocouple 4')
plt.plot(dt, t5, label='Thermocouple 5')
plt.plot(dt, t6, label='Thermocouple 6')
plt.xlim(dt[0], dt[-1])
plt.title('Pure Water RBR vs. Thermocouples')
plt.ylabel('Temperature (degrees Celsius)')
plt.xlabel(dt[0].strftime('%d %B %Y'))  # having the actual date on the line below the x-axis time labels for context
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
plt.title('Pure Water RBR vs. Thermocouple Average')
plt.ylabel('Temperature (degrees Celsius)')
plt.xlabel(dt[0].strftime('%d %B %Y'))  # having the actual date on the line below the x-axis time labels for context
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line
plt.xlim(dt[0], dt[-1])
plt.grid()
plt.legend()
plt.show()