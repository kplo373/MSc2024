# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:21:34 2024

Python script to plot just thermocouples for Parts 3 and 4, where
the RBR was not included in the bucket, to see exactly how the RBR
is affecting the thermocouple measurements (or if it isn't!).

Basically a copy of plot_RBR_thermocouples.py but excluding the RBR
read in and plotting. Excluding the trimming at 5th percentile too,
as these two tests were done subsequently after the first two and
so the sensors were all warmed up already.

@author: adamk
"""
import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # for uni MSc room computer
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer
from read_CampbellSci import read_CampbellSci

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Get Thermocouple data
#filepathT = r"D:\MSc Results\RBR_Test\Part3redo\CR3000_Table1.dat"  # for no pump, Part 3
filepathT = r"D:\MSc Results\RBR_Test\Part4redo\CR3000_Table1.dat"  # for with the pump, Part 4
dt_objsT, temps_arrT, stdevsT = read_CampbellSci(filepathT)  # this should give 6x thermocouple arrays of temperature and standard deviation
print(temps_arrT)  # has shape (6, 794) - will have to split them up into each thermocouple if wanting to plot each of them

# Extracting the 6 thermocouple temperatures from the combined temps_arrT
t1 = temps_arrT[0]
t2 = temps_arrT[1]
t3 = temps_arrT[2]
t4 = temps_arrT[3]
t5 = temps_arrT[4]
t6 = temps_arrT[5]

# Setting up a thermocouple dataframe with all these temperature readings and the datetimes as the index
df_CS = pd.DataFrame({'temp_T1': t1, 'temp_T2': t2, 'temp_T3': t3, 'temp_T4': t4, 'temp_T5': t5, 'temp_T6': t6}, index = dt_objsT)
# ^don't really need this dataframe anymore then if not merging? It's here anyway!

# skipping the time correction for RBR since the Campbell Sci logger had the right internal time already
# not cutting out any time initially either


#%%
dt_py = pd.to_datetime(dt_objsT[0]).to_pydatetime()  # to allow clear x-axis label

# Plotting all 6 thermocouples as separate lines
plt.plot(dt_objsT, t1, label='Thermocouple 1')
plt.plot(dt_objsT, t2, label='Thermocouple 2')
plt.plot(dt_objsT, t3, label='Thermocouple 3')
plt.plot(dt_objsT, t4, label='Thermocouple 4')
plt.plot(dt_objsT, t5, label='Thermocouple 5')
plt.plot(dt_objsT, t6, label='Thermocouple 6')
plt.xlim(dt_objsT[0], dt_objsT[-1])
plt.title('Pure Water Thermocouples - With Pump')
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

plt.plot(dt_objsT, avgt, label='Average Thermocouples')
plt.title('Pure Water Thermocouple Average - With Pump')
plt.ylabel('Temperature (degrees Celsius)')
plt.xlabel(dt_py.strftime('%d %B %Y'))  # having the actual date on the line below the x-axis time labels for context
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line
plt.xlim(dt_objsT[0], dt_objsT[-1])
plt.grid()
plt.legend()
plt.show()


