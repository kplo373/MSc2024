# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:53:21 2025

Script to read in the Kestrel data and then plot 
the humidity readings for the Coastal Lab.

@author: kplo373
"""
import pandas as pd
from datetime import datetime
import numpy as np

filepath = r"D:\MSc Results\WEATHER_-_2156970_22_11_2024___1_20_00_PM.csv"

data_reversed = pd.read_csv(filepath, header=4)
#print(data)
# Reverse the entire DataFrame to give oldest dates first
data = data_reversed.iloc[::-1]

time = data.index  # pandas.Index with time strings
time_arr = time.to_numpy()  # ndarray of strings, need to change into datetimes!

date_obj = np.empty(len(time_arr), dtype=object)  # preallocating empty array for datetime objects
for i in range(len(time_arr)):
    date_obj[i] = datetime.strptime(time_arr[i], "%Y-%m-%d %I:%M:%S %p")

humidity = data.iloc[:, 2]  # measured in %
#print(humidity)

#%% Time to plot this data against time!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.plot(date_obj, humidity)
plt.title('Relative Humidity Over a Week in the Laboratory')
plt.ylabel('Relative Humidity (%)')
plt.xlabel(date_obj[0].strftime('%Y'))  # having the actual date on the line below the x-axis time labels for context
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))  #'%d-%b\n%Y' = %b for month, %Y for year, \n for new line. '%H:%M' for hour and min
plt.xlim(date_obj[0], date_obj[-1])
plt.grid()
plt.show()
