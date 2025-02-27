# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 08:10:06 2024

A function to get the filenames and paths to be used as inputs
for the extracting Python scripts for Campbell Scientific and
the Optris data.
This function will have to be run separately for each experiment
(so once for hot, then again for cold experiment).

@author: kplo373
"""
import os
from datetime import datetime

folder_path = r"D:\MSc Results"  # can either get the files from the USB drive here

# The dates will be input and the Campbell Sci and Optris filepaths will be produced as output
# given_date should be in string format: 'DD/MM/YYYY' - this will include the month but not in word form
# given_time should give string of 'AM' or 'PM'
def get_filepaths(given_date, given_time):
    # determine which month here and then add that to the folder_path to go into that folder!
    given_datetime = datetime.strptime(given_date, '%d/%m/%Y')
    #print(given_datetime.month)
    
    if given_datetime.month == 7:  # navigating to the right folder depending on the month
        path = folder_path + r'\July_2024'  # creating a raw string using 'r', to prevent SyntaxWarnings of invalid escape sequences
        #the_month = 'July'
    elif given_datetime.month == 8:
        path = folder_path + r'\August_2024'
    elif given_datetime.month == 9:
        path = folder_path + r'\September_2024'
    elif given_datetime.month == 11:
        path = folder_path + r'\November_2024'
    
    # List all files in the directory
    all_files = os.listdir(path)  
    #print(all_files)
    
    # Filter files that contain both the given_date and given_time
    filtered_folders = [file for file in all_files if given_date[0:2] in file and given_time in file]  # the_month in file]
    # given_date is a string like '13/08/2024'. Only want the day, not the month or year string bit
    
    if not filtered_folders:
        raise ValueError("No folders found matching the given date and time.")  # it actually crashes earlier at all_files line anyway

    # Print the filtered files and initialize variables
    full_path = None
    sorted_files = None
    
    # Print the filtered files
    for folder in filtered_folders:
        full_path = path + "\\" + folder  # adding two slashes as they can cancel the "" after them, causing an error in the code
        files = os.listdir(full_path)
        sorted_files = sorted(files)  # put them into alphabetical order, so CampbellSci is always first
        #print(sorted_files)
    
    if full_path is None or sorted_files is None:
        raise ValueError("No valid folders or files found.")
    
    path_CS = full_path + '\\' + sorted_files[0]
    path_Op = full_path + '\\' + sorted_files[2]
    
    return path_CS, path_Op



r'''
#%% Check to see that the function works
pathCS, pathOp = get_filepaths('13/08/2024', 'AM')  # now I just need to make sure that Friday always has an 'AM' in it when I save it on the USB...
'''
