# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:30:42 2024

A plotting script for the RBR sensor, to compare its data to the thermocouples
for checking the thermocouples' accuracy.

@author: kplo373
"""
import sys
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024\RBR")

from read_RBR import read_RBR
from read_CampbellSci import read_CampbellSci
import numpy as np
import matplotlib.pyplot as plt

# Get RBR data
filepathR = r"D:\MSc Results\RBR_Test\060728_20241001_1004KateRBR.rsk"
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

# Plotting all 6 thermocouples and the RBR as 7 separate lines
plt.plot(timestampsR, tempsR, label='RBR')
plt.plot(dt_objsT, tempT1, label='Thermocouple 1')
plt.plot(dt_objsT, tempT2, label='Thermocouple 2')
plt.plot(dt_objsT, tempT3, label='Thermocouple 3')
plt.plot(dt_objsT, tempT4, label='Thermocouple 4')
plt.plot(dt_objsT, tempT5, label='Thermocouple 5')
plt.plot(dt_objsT, tempT6, label='Thermocouple 6')
plt.ylabel('Temperature (degrees Celsius)')
plt.title('Pure Water RBR vs. Thermocouples')
plt.legend()
plt.grid()
plt.show()

# need to cut out the starting bit where thermocouples were warming up (and some of the RBR warm up too!)
#see other notes in OneNote for this week's supervisor meeting... e.g. do x-axis label sort out...


#%% Plotting average thermocouple temperatures against the RBR to compare over time
avg_tempsT = np.zeros(len(temps_arrT[0,:]))
avg_tempsT = (temps_arrT[0] + temps_arrT[1] + temps_arrT[2] + temps_arrT[3] + temps_arrT[4] + temps_arrT[5]) / 6
# am ignoring standard deviation here... can get the calculation from read_CampbellSci.py if needed

plt.plot(timestampsR, tempsR, label='RBR')
plt.plot(dt_objsT, avg_tempsT, label='Average Thermocouples')
plt.title('Pure Water RBR vs. Thermocouple Average')
plt.ylabel('Temperature (degrees Celsius)')
# x-axis needs to have a better labelling system so it's more clear to read...
plt.grid()
plt.legend()
plt.show()