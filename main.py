# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:53:49 2024

Main master script to run all the functions within the subroutines.

@author: kplo373
"""

#something def main as __main__??


# To get the filepath
from get_filepaths import get_filepaths
path, files = get_filepaths('13/08/2024', 'AM')
# path gives a folder, and files are the files in that folder. Need to select specific file from files list
path_Op = path + '\\' + files[0]
path_CS = path + '\\' + files[2]

# To collect the Campbell Scientific thermocouple data
from read_CampbellSci import read_CampbellSci
dt_objsCS, temps_arrCS, stdevs_arrCS = read_CampbellSci(path_CS)

from read_CampbellSci import sand_avgCS  # this function will depend on what type of test is being done...
df_sand_avgCS = sand_avgCS(dt_objsCS, temps_arrCS)

# To collect the Optris thermal camera data
from read_Optris import read_Optris
dt_objsOp, a1, a2, a3, a4 = read_Optris(path_Op)

from read_Optris import average_Optris
avg_Op_half, stdevsOp, sterrsOp = average_Optris(a1, a3)
print(avg_Op_half)

#%%
from resample_Optris import resample_Optris
resampled_df = resample_Optris(dt_objsOp, avg_Op_half, stdevsOp)



