# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 09:05:55 2024

Main script to run all the functions to plot all percentages for the nurdle 
(pellet)-sand experiments together.

Remember: microplastic = shavings/shaved plastic
and: nurdles = pellets
(for any formal titles).

@author: kplo373
"""

import sys
sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions called in the main function
#sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer

def main():
    # Get filepaths
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    pathCSc0, pathOpc0 = get_filepaths('23/07/2024', 'PM')  # first, collecting data filepaths from cold 0% pellet-sand mixture (pure sand)
    pathCSh0, pathOph0 = get_filepaths('25/07/2024', 'AM')  # and then the data filepaths from the hot 0% pellet-sand mixture

    pathCSc5, pathOpc5 = get_filepaths('14/08/2024', 'PM')  # cold 5% pellet-sand
    pathCSh5, pathOph5 = get_filepaths('16/08/2024', 'AM')  # hot 5% pellet-sand
    
    pathCSc10, pathOpc10 = get_filepaths('22/08/2024', 'PM')  # cold 10% pellet-sand
    pathCSh10, pathOph10 = get_filepaths('21/08/2024', 'AM')  # hot 10% pellet-sand
    
    pathCSc25, pathOpc25 = get_filepaths('12/08/2024', 'PM')  # cold 25% pellet-sand
    pathCSh25, pathOph25 = get_filepaths('13/08/2024', 'PM')  # hot 25% pellet-sand    
    
    pathCSc50, pathOpc50 = get_filepaths('12/08/2024', 'AM')  # cold 50% pellet-sand experiment
    pathCSh50, pathOph50 = get_filepaths('13/08/2024', 'AM')  # hot 50% pellet-sand experiment
    
    pathCSc100, pathOpc100 = get_filepaths('17/07/2024', 'AM')  # cold 100% pellet-sand experiment (pure pellets and 0 sand)
    pathCSh100, pathOph100 = get_filepaths('24/07/2024', 'AM')  # hot 100% pellet-sand (pure pellets)
    
    # Collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci, sand_avgCS  #, water_avgCS  # function used depends on type of experiment done!***
    dt_CSc0, temps_arrCSc0, stdevs_arrCSc0 = read_CampbellSci(pathCSc0)  # cold 0% pellet-sand mixture (pure sand) thermocouple data
    df_sand_avgCSc0 = sand_avgCS(dt_CSc0, temps_arrCSc0, stdevs_arrCSc0)  # and getting the averages in a dataframe for the cold 0% pellet-sand
    dt_CSh0, temps_arrCSh0, stdevs_arrCSh0 = read_CampbellSci(pathCSh0)  # hot 0% pellet-sand thermocouple data
    df_sand_avgCSh0 = sand_avgCS(dt_CSh0, temps_arrCSh0, stdevs_arrCSh0)  # and averaging hot 0% pellet-sand
    
    #df_water_avgCScold = water_avgCS(dt_objsCScold, temps_arrCScold, stdevs_arrCScold)  # use these lines if it involves a water experiment rather than sand
    #df_water_avgCShot = water_avgCS(dt_objsCShot, temps_arrCShot, stdevs_arrCShot)
    
    dt_CSc5, temps_arrCSc5, stdevs_arrCSc5 = read_CampbellSci(pathCSc5)  # continuing as above, with cold 5% pellet-sand thermocouple data...
    df_sand_avgCSc5 = sand_avgCS(dt_CSc5, temps_arrCSc5, stdevs_arrCSc5)
    dt_CSh5, temps_arrCSh5, stdevs_arrCSh5 = read_CampbellSci(pathCSh5)
    df_sand_avgCSh5 = sand_avgCS(dt_CSh5, temps_arrCSh5, stdevs_arrCSh5)
    
    dt_CSc10, temps_arrCSc10, stdevs_arrCSc10 = read_CampbellSci(pathCSc10)  # cold 10% pellet-sand thermocouple data...
    df_sand_avgCSc10 = sand_avgCS(dt_CSc10, temps_arrCSc10, stdevs_arrCSc10)
    dt_CSh10, temps_arrCSh10, stdevs_arrCSh10 = read_CampbellSci(pathCSh10)
    df_sand_avgCSh10 = sand_avgCS(dt_CSh10, temps_arrCSh10, stdevs_arrCSh10)
    
    dt_CSc25, temps_arrCSc25, stdevs_arrCSc25 = read_CampbellSci(pathCSc25)  # cold 25% pellet-sand thermocouple data...
    df_sand_avgCSc25 = sand_avgCS(dt_CSc25, temps_arrCSc25, stdevs_arrCSc25)
    dt_CSh25, temps_arrCSh25, stdevs_arrCSh25 = read_CampbellSci(pathCSh25)
    df_sand_avgCSh25 = sand_avgCS(dt_CSh25, temps_arrCSh25, stdevs_arrCSh25)
    
    dt_CSc50, temps_arrCSc50, stdevs_arrCSc50 = read_CampbellSci(pathCSc50)  # cold 50% pellet-sand thermocouple data...
    df_sand_avgCSc50 = sand_avgCS(dt_CSc50, temps_arrCSc50, stdevs_arrCSc50)
    dt_CSh50, temps_arrCSh50, stdevs_arrCSh50 = read_CampbellSci(pathCSh50)
    df_sand_avgCSh50 = sand_avgCS(dt_CSh50, temps_arrCSh50, stdevs_arrCSh50)
    
    dt_CSc100, temps_arrCSc100, stdevs_arrCSc100 = read_CampbellSci(pathCSc100)  # cold 100% pellet-sand (pure pellets) thermocouple data...
    df_sand_avgCSc100 = sand_avgCS(dt_CSc100, temps_arrCSc100, stdevs_arrCSc100)
    dt_CSh100, temps_arrCSh100, stdevs_arrCSh100 = read_CampbellSci(pathCSh100)
    df_sand_avgCSh100 = sand_avgCS(dt_CSh100, temps_arrCSh100, stdevs_arrCSh100)
    
    
    # Collect the Optris thermal camera data
    from read_Optris import read_Optris, resample_Optris, average_Optris
    dt_Opc0, a1c0, a2c0, a3c0, a4c0 = read_Optris(pathOpc0)  # cold 0% pellet-sand Optris data (pure sand)
    resampled_df_a1c0 = resample_Optris(dt_Opc0, a1c0)  # resampling areas 1 and 3 (below) to match thermocouple frequency of results
    resampled_df_a3c0 = resample_Optris(dt_Opc0, a3c0)
    avgOp_dfc0 = average_Optris(resampled_df_a1c0, resampled_df_a3c0)  # averaging between the resampled area 1 and area 3
    dt_Oph0, a1h0, a2h0, a3h0, a4h0 = read_Optris(pathOph0)  # hot 0% pellet-sand Optris data (pure sand)
    resampled_df_a1h0 = resample_Optris(dt_Oph0, a1h0)  # resampling
    resampled_df_a3h0 = resample_Optris(dt_Oph0, a3h0)
    avgOp_dfh0 = average_Optris(resampled_df_a1h0, resampled_df_a3h0)  # averaging
    
    dt_Opc5, a1c5, a2c5, a3c5, a4c5 = read_Optris(pathOpc5)  # cold 5% pellet-sand Optris data
    resampled_df_a1c5 = resample_Optris(dt_Opc5, a1c5)  # resampling
    resampled_df_a3c5 = resample_Optris(dt_Opc5, a3c5)
    avgOp_dfc5 = average_Optris(resampled_df_a1c5, resampled_df_a3c5)  # averaging 
    dt_Oph5, a1h5, a2h5, a3h5, a4h5 = read_Optris(pathOph5)  # hot 5% pellet-sand Optris data
    resampled_df_a1h5 = resample_Optris(dt_Oph5, a1h5)
    resampled_df_a3h5 = resample_Optris(dt_Oph5, a3h5)
    avgOp_dfh5 = average_Optris(resampled_df_a1h5, resampled_df_a3h5)
    
    dt_Opc10, a1c10, a2c10, a3c10, a4c10 = read_Optris(pathOpc10)  # cold 10% pellet-sand Optris data 
    resampled_df_a1c10 = resample_Optris(dt_Opc10, a1c10)  # resampling
    resampled_df_a3c10 = resample_Optris(dt_Opc10, a3c10)
    avgOp_dfc10 = average_Optris(resampled_df_a1c10, resampled_df_a3c10)  # averaging
    dt_Oph10, a1h10, a2h10, a3h10, a4h10 = read_Optris(pathOph10)  # hot 10% pellet-sand Optris data
    resampled_df_a1h10 = resample_Optris(dt_Oph10, a1h10)
    resampled_df_a3h10 = resample_Optris(dt_Oph10, a3h10)
    avgOp_dfh10 = average_Optris(resampled_df_a1h10, resampled_df_a3h10)
    
    dt_Opc25, a1c25, a2c25, a3c25, a4c25 = read_Optris(pathOpc25)  # cold 25% pellet-sand Optris data
    resampled_df_a1c25 = resample_Optris(dt_Opc25, a1c25)  # resampling
    resampled_df_a3c25 = resample_Optris(dt_Opc25, a3c25)
    avgOp_dfc25 = average_Optris(resampled_df_a1c25, resampled_df_a3c25)  # averaging 
    dt_Oph25, a1h25, a2h25, a3h25, a4h25 = read_Optris(pathOph25)  # hot 25% pellet-sand Optris data
    resampled_df_a1h25 = resample_Optris(dt_Oph25, a1h25)
    resampled_df_a3h25 = resample_Optris(dt_Oph25, a3h25)
    avgOp_dfh25 = average_Optris(resampled_df_a1h25, resampled_df_a3h25)
    
    dt_Opc50, a1c50, a2c50, a3c50, a4c50 = read_Optris(pathOpc50)  # cold 50% pellet-sand Optris data
    resampled_df_a1c50 = resample_Optris(dt_Opc50, a1c50)  # resampling
    resampled_df_a3c50 = resample_Optris(dt_Opc50, a3c50)
    avgOp_dfc50 = average_Optris(resampled_df_a1c50, resampled_df_a3c50)  # averaging 
    dt_Oph50, a1h50, a2h50, a3h50, a4h50 = read_Optris(pathOph50)  # hot 50% pellet-sand Optris data
    resampled_df_a1h50 = resample_Optris(dt_Oph50, a1h50)
    resampled_df_a3h50 = resample_Optris(dt_Oph50, a3h50)
    avgOp_dfh50 = average_Optris(resampled_df_a1h50, resampled_df_a3h50)
    
    dt_Opc100, a1c100, a2c100, a3c100, a4c100 = read_Optris(pathOpc100)  # cold 100% pellet-sand Optris data (pure pellets)
    resampled_df_a1c100 = resample_Optris(dt_Opc100, a1c100)  # resampling
    resampled_df_a3c100 = resample_Optris(dt_Opc100, a3c100)
    avgOp_dfc100 = average_Optris(resampled_df_a1c100, resampled_df_a3c100)  # averaging
    dt_Oph100, a1h100, a2h100, a3h100, a4h100 = read_Optris(pathOph100)  # hot 100% pellet-sand Optris data
    resampled_df_a1h100 = resample_Optris(dt_Oph100, a1h100)
    resampled_df_a3h100 = resample_Optris(dt_Oph100, a3h100)
    avgOp_dfh100 = average_Optris(resampled_df_a1h100, resampled_df_a3h100)
    
    
    # Merge these different sensors together into a cold and hot dataframe per percentage of plastic
    from create_merged_df import create_merged_df
    df_merged_c0 = create_merged_df(avgOp_dfc0, df_sand_avgCSc0)  #df_water_avgCSc0)
    df_merged_h0 = create_merged_df(avgOp_dfh0, df_sand_avgCSh0)  #df_water_avgCSh0) 
    
    df_merged_c5 = create_merged_df(avgOp_dfc5, df_sand_avgCSc5)
    df_merged_h5 = create_merged_df(avgOp_dfh5, df_sand_avgCSh5)
    
    df_merged_c10 = create_merged_df(avgOp_dfc10, df_sand_avgCSc10)
    df_merged_h10 = create_merged_df(avgOp_dfh10, df_sand_avgCSh10)
    
    df_merged_c25 = create_merged_df(avgOp_dfc25, df_sand_avgCSc25)
    df_merged_h25 = create_merged_df(avgOp_dfh25, df_sand_avgCSh25)
    
    df_merged_c50 = create_merged_df(avgOp_dfc50, df_sand_avgCSc50)
    df_merged_h50 = create_merged_df(avgOp_dfh50, df_sand_avgCSh50)
    
    df_merged_c100 = create_merged_df(avgOp_dfc100, df_sand_avgCSc100)
    df_merged_h100 = create_merged_df(avgOp_dfh100, df_sand_avgCSh100)
    # not easily possible to merge all these dfs together into one, as they have different datetimes along their indices per df...
    
    '''
    # To plot the 1-1 temperature plot
    from plot1to1_multiple import plot1to1_multiple
    text_str = 'Pellets and Sand'
    # Create a dictionary of df_merged dataframes made above, to put into function below
    df_merged_dict = dict(c0=df_merged_c0, h0=df_merged_h0, c5=df_merged_c5, h5=df_merged_h5, c10=df_merged_c10, h10=df_merged_h10, c25=df_merged_c25,
                          h25=df_merged_h25, c50=df_merged_c50, h50=df_merged_h50, c100=df_merged_c100, h100=df_merged_h100)
    # not sure how to do all the text strings for the legend of these lines yet... maybe can just do them in the plotting function itself?
    
    df_cold, df_hot = plot1to1_multiple(df_merged_dict, text_str)
    '''
    
    
    
    return df_merged_c0, df_merged_h0, df_merged_c5, df_merged_h5, df_merged_c10, df_merged_h10, df_merged_c25, df_merged_h25, df_merged_c50, df_merged_h50, df_merged_c100, df_merged_h100

if __name__ == '__main__':
    df_merged_c0, df_merged_h0, df_merged_c5, df_merged_h5, df_merged_c10, df_merged_h10, df_merged_c25, df_merged_h25, df_merged_c50, df_merged_h50, df_merged_c100, df_merged_h100 = main()    
    
    
#%%  
# To plot the 1-1 temperature plot
from plot1to1_multiple import plot1to1_multiple
text_str = 'Pellets and Sand'
# Create a dictionary of df_merged dataframes made above, to put into function below
df_merged_dict = dict(c0=df_merged_c0, h0=df_merged_h0, c5=df_merged_c5, h5=df_merged_h5, c10=df_merged_c10, h10=df_merged_h10, c25=df_merged_c25,
                      h25=df_merged_h25, c50=df_merged_c50, h50=df_merged_h50, c100=df_merged_c100, h100=df_merged_h100)
# not sure how to do all the text strings for the legend of these lines yet... maybe can just do them in the plotting function itself?

df_cold, df_hot = plot1to1_multiple(df_merged_dict, text_str)

#%%
print('Starting apply calibration script now')
# Next is apply calibration for all of these lines (after this and temp difference I should put these functions within the actual main function!)
from apply_calibration_multiple import apply_calibration_multiple
x_comb, y_pred_plastic = apply_calibration_multiple(df_cold, df_hot, text_str)



