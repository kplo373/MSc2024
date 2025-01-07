# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 10:11:12 2024

A function to extract data from the Campbell Scientific .dat files
(representing the thermocouple readings).

The Campbell Scientific files (and filepaths) will be extracted 
from my MSc Results folder using the get_filepaths.py script function.

Two functions for calculating the averages of the consistent 
thermocouples are included below as well (for sand and water experiments).


@author: kplo373
"""
import pandas as pd
import numpy as np
from datetime import datetime


# filepath should be a full string path to one Campbell Sci Table 1 file
def read_CampbellSci(filepath):
    df = pd.read_csv(filepath, delimiter=',', header=4)  # make a dataframe
    
    # Preallocating the datetime object, temperature, and standard deviation arrays
    dt_objs = np.zeros(len(df), dtype='datetime64[s]')

    temp1 = np.zeros(len(df))
    temp2 = np.zeros(len(df))
    temp3 = np.zeros(len(df))
    temp4 = np.zeros(len(df))
    temp5 = np.zeros(len(df))
    temp6 = np.zeros(len(df))

    stdev1 = np.zeros(len(df))
    stdev2 = np.zeros(len(df))
    stdev3 = np.zeros(len(df))
    stdev4 = np.zeros(len(df))
    stdev5 = np.zeros(len(df))
    stdev6 = np.zeros(len(df))

    count = 0  # use this iterating variable to allocate the values found below to the correct index, rather than i (which starts at 4)
    for i in range(0, len(df)):
        row_series = df.iloc[i]
        #print(row_series)
        timestr = str(row_series.iloc[0])  # e.g. 2024-06-13 10:59:55, type string
        #print(timestr)  # now need to convert it to a datetime object
        the_date = timestr[:10]  # extracting the date to print along x-axis
        dt = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # to convert string to datetimeobj   
        dt_objs[count] = dt  # to insert this datetime object into the preallocated array, swapping it for a zero

        t1 = str(row_series.iloc[2])
        t2 = str(row_series.iloc[3])
        t3 = str(row_series.iloc[4])
        t4 = str(row_series.iloc[5])
        t5 = str(row_series.iloc[6])
        t6 = str(row_series.iloc[7])
        std1 = str(row_series.iloc[8])
        std2 = str(row_series.iloc[9])
        std3 = str(row_series.iloc[10])
        std4 = str(row_series.iloc[11])
        std5 = str(row_series.iloc[12])
        std6 = str(row_series.iloc[13])
        #print(temp1)  # now need to add all these variable elements to their array...
        
        temp1[count] = t1
        temp2[count] = t2
        temp3[count] = t3
        temp4[count] = t4
        temp5[count] = t5
        temp6[count] = t6
        stdev1[count] = std1
        stdev2[count] = std2
        stdev3[count] = std3
        stdev4[count] = std4
        stdev5[count] = std5
        stdev6[count] = std6
        
        count += 1
    
    dt_objs = dt_objs[:count]  # to remove any trailing zeroes if preallocating zeroes to an array with a slightly bigger length than needed
    temp1 = temp1[:count]
    temp2 = temp2[:count]
    temp3 = temp3[:count]
    temp4 = temp4[:count]
    temp5 = temp5[:count]
    temp6 = temp6[:count]
    stdev1 = stdev1[:count]
    stdev2 = stdev2[:count]
    stdev3 = stdev3[:count]
    stdev4 = stdev4[:count]
    stdev5 = stdev5[:count]
    stdev6 = stdev6[:count]
    
    #print(count, len(temp1)) 
    
    # Put the similar things to be returned into numpy arrays for efficiency
    temps_arr = np.array([temp1, temp2, temp3, temp4, temp5, temp6])
    stdevs_arr = np.array([stdev1, stdev2, stdev3, stdev4, stdev5, stdev6])
    
    return dt_objs, temps_arr, stdevs_arr


r'''
#%% Testing the read_CampbellSci() function
#the_filepath = r"D:\MSc Results\July_2024\Wednesday24JulyPM\CR3000_Table1.dat"
the_filepath = r"D:\MSc Results\August_2024\Tuesday13AugAM\CR3000_Table1.dat"
dt_objs, temps_arr, stdevs_arr = read_CampbellSci(the_filepath)
'''

#%% Averaging Function for Sand and Pure Experiments (used different thermocouples to Water Experiments)
def sand_avgCS(dt_objs, temps_arr, prev_std_arr):
    # Take the mean/average of all consistent thermocouples (only H1-3 for sand experiments, starting Wed 31 July PM and onwards)
    ref_dt = np.datetime64('2024-07-31T15:00:00')  # the 31 July PM experiment started at 15:09:30 PM and the AM test had the faulty computer so didn't work
    avg_temps = np.zeros(len(temps_arr[0,:]))  # preallocating the new average temperatures array to have same length as temp1
    stdev_arr = np.zeros(len(temps_arr[0,:]))
    sterr_arr = np.zeros(len(temps_arr[0,:]))
    therm_std = 1.75  # deg C, this is standard deviation uncertainty per thermocouple, from the manual specifications - used below to calculate mean stdev
    
    
    if dt_objs[0] < ref_dt:
        # Taking the average of all 6 thermocouple temps before Wed 31 July PM
        avg_temps = (temps_arr[0] + temps_arr[1] + temps_arr[2] + temps_arr[3] + temps_arr[4] + temps_arr[5]) / 6  
        print('Using all 6 thermocouples')
        
        # Get standard deviation of every time averaging in above step
        for s in range(len(temps_arr[0,:])):
            therm_std_sum = therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2
            std_sum = (prev_std_arr[0,s])**2 + (prev_std_arr[1,s])**2 + (prev_std_arr[2,s])**2 + (prev_std_arr[3,s])**2 + (prev_std_arr[4,s])**2 + (prev_std_arr[5,s])**2  # uncertainty in time (averaging every 5x1sec measurement into 5sec intervals)
            little_arr = np.array([temps_arr[0][s], temps_arr[1][s], temps_arr[2][s], temps_arr[3][s], temps_arr[4][s], temps_arr[5][s]])
            std_mean = np.std(little_arr)  # getting mean standard deviation from temperature measurements, using the array I made in the line above
            stdev = np.sqrt(therm_std_sum + std_sum + std_mean**2)  # combined standard deviation, including thermocouple uncertainties and averaging
            stdev_arr[s] = stdev
            sterr = stdev / np.sqrt(6)
            sterr_arr[s] = sterr
    
    elif dt_objs[0] >= ref_dt:
        print('Only using 3 thermocouples')
        avg_temps = (temps_arr[0] + temps_arr[1] + temps_arr[2]) / 3  # only using H1, H2, and H3 thermocouples
        
        for s in range(len(temps_arr[0,:])):
            therm_std_sum = therm_std**2 + therm_std**2 + therm_std**2
            std_sum = (prev_std_arr[0,s])**2 + (prev_std_arr[1,s])**2 + (prev_std_arr[2,s])**2  # uncertainty in time (averaging every 5x1sec measurement into 5sec intervals)
            little_arr = np.array([temps_arr[0][s], temps_arr[1][s], temps_arr[2][s]])
            std_mean = np.std(little_arr)  # getting mean standard deviation from temperature measurements, using the array I made in the line above
            stdev = np.sqrt(therm_std_sum + std_sum + std_mean**2)  # combined standard deviation, including thermocouple uncertainties and averaging
            stdev_arr[s] = stdev
            sterr = stdev / np.sqrt(3)
            sterr_arr[s] = sterr
    
    #print(avg_temps)
    df_sand_avgCS = pd.DataFrame({     # creating a new dataframe
        'datetimes': dt_objs,
        'mean_temperatures': avg_temps,
        'stdev': stdev_arr,
        'sterr': sterr_arr})
    
    return df_sand_avgCS

'''
# TEST the sand averaging function for Campbell Scientific data
df_sand_avgCS = sand_avgCS(dt_objs, temps_arr, stdevs_arr)
'''

#%% Averaging Function for Water Experiments - CHANGE THIS AFTER THE MONDAY MEETING (HAVE ALREADY UPDATED THE BOX ABOVE)
def water_avgCS(dt_objs, temps_arr, prev_std_arr):
    # Take the mean/average of all consistent thermocouples (only H4-6 for water experiments, starting Wed 31 July PM and onwards)
    ref_dt = np.datetime64('2024-07-31T15:00:00')  # the 31 July PM experiment started at 15:09:30 PM and the AM test had the faulty computer so didn't work
    avg_temps = np.zeros(len(temps_arr[0,:]))  # preallocating the new average temperatures array to have same length as temp1
    stdev_arr = np.zeros(len(temps_arr[0,:]))
    sterr_arr = np.zeros(len(temps_arr[0,:]))
    therm_std = 1.75  # deg C, this is standard deviation uncertainty per thermocouple, from the manual specifications - used below to calculate mean stdev
    
    
    if dt_objs[0] < ref_dt:
        # Taking the average of all 6 thermocouple temps before Wed 31 July PM
        avg_temps = (temps_arr[0] + temps_arr[1] + temps_arr[2] + temps_arr[3] + temps_arr[4] + temps_arr[5]) / 6  
        print('Using all 6 thermocouples')
        
        # Get standard deviation of every time averaging in above step
        for s in range(len(temps_arr[0,:])):
            therm_std_sum = therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2 + therm_std**2
            std_sum = (prev_std_arr[0,s])**2 + (prev_std_arr[1,s])**2 + (prev_std_arr[2,s])**2 + (prev_std_arr[3,s])**2 + (prev_std_arr[4,s])**2 + (prev_std_arr[5,s])**2  # uncertainty in time (averaging every 5x1sec measurement into 5sec intervals)
            little_arr = np.array([temps_arr[0][s], temps_arr[1][s], temps_arr[2][s], temps_arr[3][s], temps_arr[4][s], temps_arr[5][s]])
            std_mean = np.std(little_arr)  # getting mean standard deviation from temperature measurements, using the array I made in the line above
            stdev = np.sqrt(therm_std_sum + std_sum + std_mean**2)  # combined standard deviation, including thermocouple uncertainties and averaging
            stdev_arr[s] = stdev
            sterr = stdev / np.sqrt(6)
            sterr_arr[s] = sterr


    elif dt_objs[0] >= ref_dt:
        print('Only using 3 thermocouples')
        avg_temps = (temps_arr[3] + temps_arr[4] + temps_arr[5]) / 3  # only using H4, H5, and H6 thermocouples
        
        for s in range(len(temps_arr[0,:])):
            therm_std_sum = therm_std**2 + therm_std**2 + therm_std**2
            std_sum = (prev_std_arr[3,s])**2 + (prev_std_arr[4,s])**2 + (prev_std_arr[5,s])**2  # uncertainty in time (averaging every 5x1sec measurement into 5sec intervals)
            little_arr = np.array([temps_arr[3][s], temps_arr[4][s], temps_arr[5][s]])
            std_mean = np.std(little_arr)  # getting mean stdev from the temperature measurements
            stdev = np.sqrt(therm_std_sum + std_sum + std_mean**2)  # combined standard deviation, including thermocouple uncertainties and averaging
            stdev_arr[s] = stdev
            sterr = stdev / np.sqrt(3)
            sterr_arr[s] = sterr    
                
    #print(avg_temps)
    df_water_avgCS = pd.DataFrame({     # creating a new dataframe
        'datetimes': dt_objs,
        'mean_temperatures': avg_temps,
        'stdev': stdev_arr,
        'sterr': sterr_arr})
    
    return df_water_avgCS

'''
# Test the water averaging function for Campbell Scientific data
df_water_avgCS = water_avgCS(dt_objs, temps_arr, stdevs_arr)
print(df_water_avgCS['mean_temperatures'])
'''
