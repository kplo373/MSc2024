# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 08:40:58 2025

To briefly plot the distribution of calibration adjustments applied to the data
(to show that there are higher adjustments at the hotter end of Temp spectrum).

@author: kplo373
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


wfilepath = r"D:\MSc Results\calTable.csv"
wdf = pd.read_csv(wfilepath)
sfilepath = r"D:\MSc Results\calTableSand.csv"
sdf = pd.read_csv(sfilepath)


wdf.rename(columns={'Unnamed: 0': 'Temperatures', 'y_cal_adj': 'Adjustments'}, inplace=True)
sdf.rename(columns={'Unnamed: 0': 'Temperatures', 'y_cal_adj': 'Adjustments'}, inplace=True)
print(wdf)
wtemps = wdf.iloc[:, 0]  # to get the whole column, not just first row
wadjs = wdf.iloc[:, 1]
stemps = sdf.iloc[:, 0]
sadjs = sdf.iloc[:, 1]

#'.',
plt.plot(wtemps, wadjs, '.', label='Water')  # can add a 'markersize=' parameter before label to change dot size
plt.plot(stemps, sadjs, '.', color='orange', label='Sand')
plt.title('Thermal Camera Calibration Table Adjustments')
plt.xlabel('Temperature (degrees Celsius)')
plt.ylabel('Calibration Adjustment (degrees Celsius)')
plt.xlim(min(wtemps)-1, max(wtemps)+1)  # this may need to be updated
plt.grid()
plt.legend()
plt.show()



# can try plot the sand one as different data on here too - or is it too different to this water data??
#%%
plt.plot(stemps, sadjs, '.', color='orange', label='Sand')
plt.title('Thermal Camera Calibration Table Adjustments')
plt.xlabel('Temperature (degrees Celsius)')
plt.ylabel('Calibration Adjustment (degrees Celsius)')
plt.xlim(min(stemps)-1, max(stemps)+1)  # this may need to be updated
plt.grid()
plt.legend()
plt.show()

