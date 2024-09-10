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

folder_path = r'C:\Users\kplo373\OneDrive - The University of Auckland\MSc Kate\PlottingMScResults\August_2024'

# The dates will be input and the Campbell Sci and Optris filepaths will be produced as output
# given_date should be in string format: 'DD/MM/YYYY' 
# given_time should give string of 'AM' or 'PM'
def get_filepaths(given_date, given_time):
    # List all files in the directory
    all_files = os.listdir(folder_path)
    
    # Filter files that contain both the given_date and given_time
    filtered_folders = [file for file in all_files if given_date in file and given_time in file]
    
    # Print the filtered files
    for folder in filtered_folders:
        #print(folder)
        full_path = folder_path + "\\" + folder  # adding two slashes as they can cancel the "" after them, causing an error in the code
        print(full_path)
        files = os.listdir(full_path)
        print(files)
    
    return full_path, files

'''
#%% Check to see that the function works
path, files = get_filepaths('13', 'AM')  # now I just need to make sure that Friday always has an 'AM' in it when I save it on the USB...
'''

