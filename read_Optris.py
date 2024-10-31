# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:50:02 2024

A function to extract data from the Optris .dat files
(representing the thermocouple readings).

The Optris files (and filepaths) will be extracted from my 
MSc Results folder using the get_filepaths.py script function.

A resampling function then averages all the measurements per 5
second interval into one value, and returns a resampled dataframe.

Another function for calculating the averages of any two measurement area
resampled dataframe is included below as well (for sand and water experiments).

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
    with open(filepath, 'r', encoding='cp1252') as file:  # added this encoding parameter as was getting an error
        headers = [next(file).strip() for _ in range(7)]
    #print(headers)  # There are 4x different measurement areas
    
    # Extract date and time from the relevant lines
    date_line = headers[1]  # This is the line e.g. Date: 13/06/2024
    time_line = headers[2]  # e.g. Time: 10:51:17.112
    #print(date_line, time_line)  # and these are strings
    
    if '\t' in date_line and time_line:  # the columns are separated by either commas or tabs
        delim = '\t'
    elif ',' in date_line and time_line:  
        delim = ','
    else:
        print('unidentified separator between date and time in Optris files')
    # older Optris data files are likely to be tab delimited, and newer ones comma delimited
    
    # Split the lines to get the actual date and time values
    date_val = date_line.split(delim)[1]
    time_val = time_line.split(delim)[1]    
    
    print(f"Date: {date_val}")
    print(f"Time: {time_val}")
    
    # Combine date and time to a single string
    datetime_str = date_val + ' ' + time_val   # f"{date_value} {time_value}"  is chatGPT's method
    
    # Convert the combined string to a datetime object
    datetime_format = "%d/%m/%Y %H:%M:%S.%f"
    start_datetimeobj = datetime.strptime(datetime_str, datetime_format)
    
    # Read the Optris files, ignoring errors (from chatGPT)
    try: 
        df_Optris = pd.read_csv(filepath, delimiter=delim, encoding='utf-8', header=7)  # need to be weary of if the delimiter is ',' or '\t'
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")

    # Function to convert time string to timedelta
    def time_str_to_timedelta(time_str):
        if ',' in time_str:
            time_str = time_str.split(',')[0]  # only include the first column (actual time) if all columns are included
        #print(time_str)
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
    print(df_Optris.columns)   # has 11 columns
    
    new_column_names = ['Time', 'Area1', 'Area2', 'Area3', 'Area4', 'nan', 'Datetime']  # not sure what 'Unnamed: 5' column is for? so made it 'nan'

    df_Optris.columns = new_column_names      # assigning them to the DataFrame by correct length
    df_Optris = df_Optris.drop(columns=['Time'])  # drop the 'Time' column if only 'Datetime' is needed
    df_Optris = df_Optris.drop(columns=['nan'])   # remove the unnecessary 'Unnamed: 5' column too
    #print(df_Optris.columns)
    
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

    
'''
#%% Testing the read_Optris() function
the_filepath = r"D:\\MSc Results\\August_2024\\Thursday1AugAM\\Thurs1AugAMOptris.dat"  # was giving a SyntaxWarning because of slashes, said invalid escape sequence
datetimes, a1, a2, a3, a4 = read_Optris(the_filepath)

print(datetimes)
'''

#%% Resampling Function

# datetimeOp has 26 OR MORE measurements for each second. can't depend on an integer 26, need to actually just collect all the readings for that second and avg them!
def resample_Optris(datetimeOp, areaOp):
    #using chatgpt to help resample the data into 5-second intervals, after loading the 2 arrays into pd dataframe
    df_new = pd.DataFrame({     # creating a new dataframe
        'datetimes': datetimeOp,
        'Op_temp': areaOp})    # can only read in one mean Optris temperature array at once from the averaging Optris function, this could be half or small area
    
    
    df_new.set_index('datetimes', inplace=True)  # setting the datetimes column as the index
    # can extract datetimes using e.g. df_new.index
    
    def standard_error(x):
        return x.std() / np.sqrt(len(x))  # a function to calculate standard error
    
    resampled_df = df_new.resample('5s').agg({'Op_temp': ['mean', 'std', standard_error]})  
    # resampling whole dataframe to 5 sec intervals by taking the mean of temp, plus getting stdev and sterr
    # e.g. df.resample("3s").agg({'x':'sum','y':'mean','z':'last'}) can be used if using different functions for different columns
    #print(resampled_df.iloc[:, 1])  # this gives the 'std' column
    
    resampled_df.columns = ['mean_temp', 'stdev_resampled', 'sterr_resampled']  # renaming columns
    return resampled_df    

'''
#%% Testing the resample_Optris() function
resampled_df_a1 = resample_Optris(datetimes, a1)
print(resampled_df_a1)  # looks good!

resampled_df_a3 = resample_Optris(datetimes, a3)
'''

#%% Averaging and Uncertainties Function
    
def average_Optris(resampled_dfa1, resampled_dfa2):  # resampled_dfa1 and resampled_dfa2 represent 2 like areas: area1 & area3 for half the surface, or area2 & area4 for thermocouple surface
    std_specs = 2.4  # deg C, the accuracy for the Optris thermal PI450 camera
    stdev_arr = np.zeros(len(resampled_dfa1.index))
    sterr_arr = np.zeros(len(resampled_dfa1.index))
    
    datetimeOp = resampled_dfa1.index  # assuming that both resampled dataframes have the same datetime arrays
    area1 = resampled_dfa1.iloc[:,0].to_numpy()
    area2 = resampled_dfa2.iloc[:,0].to_numpy()
    std_resampled1 = resampled_dfa1.iloc[:,1].to_numpy()  # add each element of these squared together as part of standard deviation calculation
    std_resampled2 = resampled_dfa2.iloc[:,1].to_numpy()
    #print(np.shape(area1))  # changed from pandas series to np.ndarray with shape (4539,)
    
    if len(area1) == len(area2):
        mean_Op = np.zeros(len(area1))  # preallocating a mean temperature array
        mean_Op = (area1 + area2)/2   # taking the average
        
        # should just calculate the rest of the uncertainty here now within this function, and have it in the resampled_df
        for s in range(len(area1)):
            std_resamp = std_resampled1[s]**2 + std_resampled2[s]**2  # uncertainty as sum of the variances of standard deviations from resampling
            little_arr = np.array([area1[s], area2[s]])  # putting the two temperature values into an array to take the standard deviation of them below
            std_mean = np.std(little_arr)
            std_specs_sum = std_specs**2 + std_specs**2  # uncertainty as sum of the variances, because taking the mean of two areas

            std = np.sqrt(std_specs_sum + std_resamp + std_mean**2)  # so am including the specification accuracy in the standard deviation!
            stdev_arr[s] = std
            
            sterr = std / np.sqrt(2)
            sterr_arr[s] = sterr
        
        average_df = pd.DataFrame({     # creating a new dataframe
            'datetimes': datetimeOp,
            'Op_temp': mean_Op,
            'stdevs': stdev_arr,
            'sterrs': sterr_arr})
       
        return average_df

    else:
        print("The two area arrays don't have the same length")
        return   

'''
#%% Test the averaging function
avg_df = average_Optris(resampled_df_a1, resampled_df_a3)  #avg_Op_half, stdevs, sterrs
print(avg_df)
'''





