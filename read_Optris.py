# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:50:02 2024

A function to extract data from the Optris .dat files
(representing the thermocouple readings).

The Optris files (and filepaths) will be extracted from my 
MSc Results folder using the get_filepaths.py script function.

One function for calculating the averages of any two measurement areas
is included below as well (for sand and water experiments).

@author: kplo373
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# filepath should be a full string path to one Optris.dat file, and it usually needs 'r' to convert it to a raw string
# e.g. r"C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\August_2024\Thursday1AugAM\Thurs1AugAMOptris.dat"
def read_Optris(filepath):
    # To extract the data from the headers of the Optris data, read the first 7 lines
    headers = []
    with open(filepath, 'r') as file:
        headers = [next(file).strip() for _ in range(7)]
    print(headers)  # There are 4x different measurement areas
    
    # Extract date and time from the relevant lines
    date_line = headers[1]  # This is the line e.g. Date: 13/06/2024
    time_line = headers[2]  # e.g. Time: 10:51:17.112
    
    # Split the lines to get the actual date and time values
    date_val = date_line.split(',')[1]  # the columns are separated by commas
    time_val = time_line.split(',')[1]
    
    print(f"Date: {date_val}")
    print(f"Time: {time_val}")
    
    # Combine date and time to a single string
    datetime_str = date_val + ' ' + time_val   # f"{date_value} {time_value}"  is chatGPT's method
    
    # Convert the combined string to a datetime object
    datetime_format = "%d/%m/%Y %H:%M:%S.%f"
    start_datetimeobj = datetime.strptime(datetime_str, datetime_format)
    
    # Read the Optris files, ignoring errors (from chatGPT)
    try: 
        df_Optris = pd.read_csv(filepath, delimiter=',', encoding='utf-8', header=7)
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        
    
    # Function to convert time string to timedelta
    def time_str_to_timedelta(time_str):
        # Time string format is 'HH:MM:SS.sss'
        hours, minutes, seconds = time_str.split(':')
        seconds, milliseconds = map(float, seconds.split('.'))
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=milliseconds)
    
    # Add the time deltas to the initial datetime
    df_Optris['Datetime'] = df_Optris.iloc[:-2,0].apply(lambda x: start_datetimeobj + time_str_to_timedelta(x))
    # added in the stop before the last 2 rows, as these do not contain actual data (e.g. '---', 'End of File')
    #print(df_Optris['Datetime'])

    # Now get the other columns!!
    # Assign new names to the data columns
    #print(df_Optris.columns)   # has 11 columns
    new_column_names = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']  # not sure what 'Unnamed: 5' column is for? so made it 'nan'

    df_Optris.columns = new_column_names      # assigning them to the DataFrame by correct length
    df_Optris = df_Optris.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
    df_Optris = df_Optris.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 5' column too
    print(df_Optris.columns)
    
    # Extract the data from these columns, into separate arrays
    area1 = df_Optris['Area1']  # temperature avg of whole/half [as excluding return pump] of water surface
    area2 = df_Optris['Area2']  # temperature avg of water surface above submerged thermocouples
    area3 = df_Optris['Area3']  # temperature avg of whole/half of surface of the water
    area4 = df_Optris['Area4']  # temperature avg of water surface above submerged thermocouples
    datetimeOp = df_Optris['Datetime']
    
    area1 = area1.iloc[:-2]  # removing the two NaN values at the end of each series
    area2 = area2.iloc[:-2]
    area3 = area3.iloc[:-2]
    area4 = area4.iloc[:-2]
    datetimeOp = datetimeOp[:-2]
    #print(datetimeOp)
    #print(area1)  # works! No NaNs or NaTs at the end anymore
    
    return datetimeOp, area1, area2, area3, area4

    
"""
#%% Testing the read_Optris() function
the_filepath = r"D:\\MSc Results\\August_2024\\Thursday1AugAM\\Thurs1AugAMOptris.dat"  # was giving a SyntaxWarning because of slashes, said invalid escape sequence
datetimes, a1, a2, a3, a4 = read_Optris(the_filepath)

print(datetimes)
"""

#%% Averaging Function
    
def average_Optris(area1, area2):  # area1 and area2 here are 2 like areas: area1 & area3 for half the surface, or area2 & area4 for thermocouple surface
    std_specs = 2.4  # deg C, the accuracy for the Optris thermal PI450 camera
    stdev_arr = np.zeros(len(area1))
    sterr_arr = np.zeros(len(area2))
    
    if len(area1) == len(area2):
        mean_Op = np.zeros(len(area1))  # preallocating a mean temperature array
        mean_Op = (area1 + area2)/2   # taking the average
        
        for s in range(len(area1)):
            std_specs_sum = std_specs**2 + std_specs**2  # uncertainty as sum of the variances, because taking the mean of two areas
            little_arr = np.array([area1[s], area2[s]])  # putting the two temperature values into an array to take the standard deviation of them below
            std_mean = np.std(little_arr)

            std = np.sqrt(std_specs_sum + std_mean**2)
            stdev_arr[s] = std
            sterr = std / np.sqrt(2)
            sterr_arr[s] = sterr
        
        return mean_Op, stdev_arr, sterr_arr
    else:
        print("The two area arrays don't have the same length")
        return

"""
#%% Test the averaging function
avg_Op_half, stdevs, sterrs = average_Optris(a1, a3)
print(avg_Op_half)
"""
