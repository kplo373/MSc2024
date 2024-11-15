# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:44:30 2024

Main script to test the pure sand calibration.

@author: adamk
"""
# Just in case it can't find the right data folder, use these two lines below
import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions called in the main function
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer
import pandas as pd


def main():
    # To get the filepath
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    pathCScold, pathOpcold = get_filepaths('23/07/2024', 'PM')  # for the cold pure sand test: Tues 23 July PM
    pathCShot, pathOphot = get_filepaths('25/07/2024', 'AM')  # for the hot pure sand test: Thurs 25 July AM


    # To collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci
    dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(pathCScold)
    dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(pathCShot)
  
    from read_CampbellSci import sand_avgCS
    df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
    df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
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
    df_merged_cold = create_merged_df(avgOp_dfcold, df_sand_avgCScold)
    df_merged_hot = create_merged_df(avgOp_dfhot, df_sand_avgCShot) 
    #print(df_mergedcold) 
    
    # Removing first 15 minutes of each cold data record
    df_ready_cold = df_merged_cold.copy()
    start_time = df_ready_cold.index.min()
    cutoff_time = start_time + pd.Timedelta(minutes=15)  # can extend if needed
    df_trimmed_cold = df_ready_cold[df_ready_cold.index >= cutoff_time]

    # Removing first 15 minutes of each hot data record
    df_ready_hot = df_merged_hot.copy()
    start_timeh = df_ready_hot.index.min()
    cutoff_timeh = start_timeh + pd.Timedelta(minutes=15)  # can extend if needed
    df_trimmed_hot = df_ready_hot[df_ready_hot.index >= cutoff_timeh]
    
    # Reverse the hot dataframe so it begins with coldest value
    df_trim_hot_rev = df_trimmed_hot.iloc[::-1].reset_index(drop=True)
    
    df_full = pd.concat([df_trimmed_cold, df_trim_hot_rev ])
    
    # To plot the 1-1 temperature plot
    from plot1to1 import plot1to1
    text_str = '0% Shavings-Sand'  # ***
    plot1to1(df_full, text_str)
    
    # then the apply_calibration() function to apply this pure sand fit to each sand mixture.
    from apply_calibration_puresand import apply_calibration
    y_nctrl_corrected, y_nctrl, x_nctrl = apply_calibration(df_full, text_str)  # use this for debug and purewater versions
    #df_out = apply_calibration(df_full, text_str)
    
    # then calculate deltaT from calibration SVM less the reference 1:1 line (which is the same as the x array for y)
    from get_deltaT import get_deltaT
    #deltaT = get_deltaT(x_comb, y_pred_plastic, text_str)  # (df_out, text_str)  And change within function!!
    #print(deltaT)  # including temperature difference plot
        
    return #y_nctrl_corrected, y_nctrl, x_nctrl



if __name__ == '__main__':
    main()



