# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:53:49 2024

Main master script to run all the functions within the subroutines
(for one hot and cold experiment at a time).
As the main scripts were created for each mixture group separately 
afterwards, this is mainly to create the water calibration adjustments.

@author: kplo373
"""
# Just in case it can't find the right data folder, use these two lines below
import sys
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions called in the main function
import pandas as pd


def main():
    # To get the filepath
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    #pathCScold, pathOpcold = get_filepaths('24/07/2024', 'PM')  # for the cold pure water test: Wednesday 24th July PM
    pathCScold, pathOpcold = get_filepaths('06/11/2024', 'PM')  # for the cold pure water test: Wednesday 6th Nov PM
    pathCShot, pathOphot = get_filepaths('18/07/2024', 'AM')  # for the hot pure water test: Thursday 18th July AM  

    # To collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci
    dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(pathCScold)
    dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(pathCShot)
  
    #from read_CampbellSci import sand_avgCS  # this function depends on what type of test is being done!
    from read_CampbellSci import water_avgCS
    # df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
    df_water_avgCScold = water_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)
    # df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
    df_water_avgCShot = water_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
    # print(df_sand_avgCScold)
    
    # To collect the Optris thermal camera data
    from read_Optris import read_Optris
    dt_objsOpcold, a1cold, a2cold, a3cold, a4cold = read_Optris(pathOpcold)
    dt_objsOphot, a1hot, a2hot, a3hot, a4hot = read_Optris(pathOphot)
        
    from read_Optris import resample_Optris
    resampled_df_a1cold = resample_Optris(dt_objsOpcold, a1cold)
    resampled_df_a3cold = resample_Optris(dt_objsOpcold, a3cold)
    resampled_df_a1hot = resample_Optris(dt_objsOphot, a1hot)
    resampled_df_a3hot = resample_Optris(dt_objsOphot, a3hot)
       
    from read_Optris import average_Optris
    avgOp_dfcold = average_Optris(resampled_df_a1cold, resampled_df_a3cold)
    avgOp_dfhot = average_Optris(resampled_df_a1hot, resampled_df_a3hot)  
    # print(avgOp_dfcold)

    from create_merged_df import create_merged_df
    df_merged_cold = create_merged_df(avgOp_dfcold, df_water_avgCScold)  # df_sand_avgCScold)
    df_merged_hot = create_merged_df(avgOp_dfhot, df_water_avgCShot)  #df_sand_avgCShot) 
    #print(df_mergedcold) 
    
    # Removing first 15 minutes of each cold data record
    df_ready_cold = df_merged_cold.copy()
    start_time = df_ready_cold.index.min()
    cutoff_time = start_time + pd.Timedelta(minutes=30)
    df_trimmed_cold = df_ready_cold[df_ready_cold.index >= cutoff_time]

    # Removing first 15 minutes of each hot data record
    df_ready_hot = df_merged_hot.copy()
    start_timeh = df_ready_hot.index.min()
    cutoff_timeh = start_timeh + pd.Timedelta(minutes=20)
    df_trimmed_hot = df_ready_hot[df_ready_hot.index >= cutoff_timeh]
    
    # Reverse the hot dataframe so it begins with coldest value
    df_trim_hot_rev = df_trimmed_hot.iloc[::-1].reset_index(drop=True)
    
    df_full = pd.concat([df_trimmed_cold, df_trim_hot_rev ])
    
    # To plot the 1-1 temperature plot
    from plot1to1 import plot1to1
    text_str = '0% Shavings-Water'
    plot1to1(df_full, text_str)
   
    # then the apply_calibration() function to apply this pure water fit to each mixture.
    #from apply_calibration import apply_calibration
    from apply_calibration_purewater import apply_calibration  # use this function to update actual calibration
    df_out = apply_calibration(df_full, text_str)
    
    # then calculate deltaT from calibration SVM less the reference 1:1 line (which is the same as the x array for y)
    from get_deltaT import get_deltaT
    deltaT = get_deltaT(df_out, text_str)
    #print(deltaT)  # including temperature difference plot
        
    return



if __name__ == '__main__':
    main()


