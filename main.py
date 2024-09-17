# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:53:49 2024

Main master script to run all the functions within the subroutines.

@author: kplo373
"""
# can run this main() function within a for loop if possible, would need to automate the date and 'AM'
chosen_date = '13/08/2024'  # this test was hot 50% nurdle sand (can check the excel sheet)
chosen_period = 'AM'
# need to be careful if the sand_avgCS or the water_avgCS function is being used**

def main():
    # To get the filepath
    from get_filepaths import get_filepaths
    path, files = get_filepaths(chosen_date, chosen_period)
    # path gives a folder, and files are the files in that folder. Need to select specific file from files list
    path_Op = path + '\\' + files[0]
    path_CS = path + '\\' + files[2]
    
    # To collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci
    dt_objsCS, temps_arrCS, stdevs_arrCS = read_CampbellSci(path_CS)
    
    from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
    df_sand_avgCS = sand_avgCS(dt_objsCS, temps_arrCS)
    print(df_sand_avgCS)
    
    
    # To collect the Optris thermal camera data
    from read_Optris import read_Optris
    dt_objsOp, a1, a2, a3, a4 = read_Optris(path_Op)
    
    from read_Optris import resample_Optris
    resampled_df_a1 = resample_Optris(dt_objsOp, a1)
    resampled_df_a3 = resample_Optris(dt_objsOp, a3)
    
    from read_Optris import average_Optris
    avgOp_df = average_Optris(resampled_df_a1, resampled_df_a3)
    print(avgOp_df)
    
    
    # To combine the thermocouple and Optris average dataframes together into a single df of times where both sensors record data
    from create_CampbellSci_Optris_dataframe import create_CampbellSci_Optris_dataframe
    df_merged = create_CampbellSci_Optris_dataframe(avgOp_df, df_sand_avgCS)
    print(df_merged)
    
    return



if __name__ == '__main__':
    main()


