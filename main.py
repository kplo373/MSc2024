# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:53:49 2024

Main master script to run all the functions within the subroutines
(for one hot and cold experiment at a time).

@author: kplo373
"""
# Just in case it can't find the right data folder, use these two lines below
import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions called in the main function
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer
import pandas as pd
# can run this main() function within a for loop if possible, would need to automate the date and 'AM'
#chosen_date = '13/08/2024'  # this test was hot 50% nurdle sand (can check the excel sheet)
#chosen_period = 'AM'
# need to be careful if the sand_avgCS or the water_avgCS function is being used, and to change the title name in plot1to1.py**

def main():
    # To get the filepath
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    #pathCScold, pathOpcold = get_filepaths('24/07/2024', 'PM')  # for the cold pure water test: Wednesday 24th July PM
    pathCScold, pathOpcold = get_filepaths('06/11/2024', 'PM')  # for the cold pure water test: Wednesday 6th Nov PM
    pathCShot, pathOphot = get_filepaths('18/07/2024', 'AM')  # for the hot pure water test: Thursday 18th July AM  
    
    # Earlier tests (before the real experiments)
    #pathCScold, pathOpcold = get_filepaths('03/07/2024', 'AM')  # cold pure water
    #pathCShot, pathOphot = get_filepaths('01/07/2024', 'AM')  # hot pure water
    #pathCScold, pathOpcold = get_filepaths('02/09/2024', 'AM')  # cold 10% MP-water
    #pathCShot, pathOphot = get_filepaths('20/08/2024', 'AM')  # hot 10% MP-water
    # for the cold and hot % experiments^^

    # To collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci
    dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(pathCScold)
    dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(pathCShot)
  
    #from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...***
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
    df_merged_cold = create_merged_df(avgOp_dfcold, df_water_avgCScold)  # df_sand_avgCScold) ***
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
    text_str = '0% Shavings-Water'  # ***
    plot1to1(df_full, text_str)
   
    # next step is the fit_SVR() function, but this is only required once for pure water (have already run it and saved results.)
    
    # then the apply_calibration() function to apply this pure water fit to each mixture.
    #from apply_calibration import apply_calibration
    from apply_calibration_purewater import apply_calibration  # use this function to update actual calibration
    y_nctrl_corrected, y_nctrl, x_nctrl = apply_calibration(df_full, text_str)  # use this for debug and purewater versions
    #df_out = apply_calibration(df_full, text_str)
    
    # then calculate deltaT from calibration SVM less the reference 1:1 line (which is the same as the x array for y)
    from get_deltaT import get_deltaT
    #deltaT = get_deltaT(x_comb, y_pred_plastic, text_str)  # (df_out, text_str)  And change within function!!
    #print(deltaT)  # including temperature difference plot
        
    return #y_nctrl_corrected, y_nctrl, x_nctrl



if __name__ == '__main__':
    main()


