# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 13:53:49 2024

Main master script to run all the functions within the subroutines.

@author: kplo373
"""
# Just in case it can't find the right data folder, use these two lines below
import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions in the second cell
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer

# can run this main() function within a for loop if possible, would need to automate the date and 'AM'
#chosen_date = '13/08/2024'  # this test was hot 50% nurdle sand (can check the excel sheet)
#chosen_period = 'AM'
# need to be careful if the sand_avgCS or the water_avgCS function is being used, and to change the title name in plot1to1.py**

def main():
    # To get the filepath  # 01/08/24 doesn't seem to exist... is there in actual files!
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    path_cold, files_cold = get_filepaths('06/08/2024', 'PM')  # for the cold 50% MP-sand experiment
    # path gives a folder, and files are the files in that folder. Need to select specific file from files list
    path_CScold = path_cold + '\\' + files_cold[0]
    path_Opcold = path_cold + '\\' + files_cold[2]

    path_hot, files_hot = get_filepaths('08/08/2024', 'AM')  # for the hot 50% MP-sand experiment
    path_CShot = path_hot + '\\' + files_hot[0]
    path_Ophot = path_hot + '\\' + files_hot[2]


    # To collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci
    dt_objsCScold, temps_arrCScold, stdevs_arrCScold = read_CampbellSci(path_CScold)
    dt_objsCShot, temps_arrCShot, stdevs_arrCShot = read_CampbellSci(path_CShot)
  
    #from read_CampbellSci import sand_avgCS  # **this function depends on what type of test is being done...
    from read_CampbellSci import water_avgCS
    #df_sand_avgCScold = sand_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  
    df_water_avgCScold = water_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)
    #df_sand_avgCShot = sand_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
    df_water_avgCShot = water_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
    # print(df_sand_avgCScold)
      
    # To collect the Optris thermal camera data
    from read_Optris import read_Optris
    dt_objsOpcold, a1cold, a2cold, a3cold, a4cold = read_Optris(path_Opcold)
    dt_objsOphot, a1hot, a2hot, a3hot, a4hot = read_Optris(path_Ophot)
        
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
    df_merged_cold = create_merged_df(avgOp_dfcold, df_water_avgCScold)  #df_sand_avgCScold)
    df_merged_hot = create_merged_df(avgOp_dfhot, df_water_avgCShot)  #df_sand_avgCShot) 
    #print(df_mergedcold) 
    
    #need to get all the hot/cold files imported above!
    # To plot the 1-1 temperature plot
    from plot1to1 import plot1to1
    text_str = '25% Microplastic-Water'
    df_cold, df_hot = plot1to1(df_merged_cold, df_merged_hot, text_str)
    print(df_cold.columns)
   
    # next step is the fit_SVR() function, but this is only required once for pure water (have already run it and saved results.)
    
    # then the apply_calibration() function to apply this pure water fit to each mixture.
    from apply_calibration import apply_calibration
    x_comb, y_pred_plastic = apply_calibration(df_cold, df_hot, text_str)
    
    # then calculate deltaT from calibration SVM less the reference 1:1 line - make this a function!!??
    from get_deltaT import get_deltaT
    deltaT = get_deltaT(y_pred_plastic)
    #print(deltaT)  # don't know if this is reasonable or not until I plot it!
    
    
    # Next: Temperature Difference Plot
    
    return



if __name__ == '__main__':
    main()


