# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:36:55 2024

A main script/function to plot all the different percentages of plastic
in one single plot, for the first of the four different scenarios (microplastic 
and sand, microplastic and water, nurdles and sand, nurdles and water).

Remember: microplastic = shavings/shaved plastic
and: nurdles = pellets
(for any formal titles).

@author: kplo373
"""

import sys
#sys.path.append(r"C:\Users\kplo373\Documents\GitHub\MSc2024")  # to allow it to find the different functions called in the main function
sys.path.append(r"C:\Users\adamk\Documents\GitHub\MSc2024")  # for home computer

import pandas as pd

def main():
    # Get filepaths
    from get_filepaths import get_filepaths
    # must put given_date below in format 'DD/MM/YYYY' (add 0 first if single digit D or M)
    pathCSc0, pathOpc0 = get_filepaths('23/07/2024', 'PM')  # first, collecting data filepaths from cold 0% MP-sand mixture (pure sand)
    pathCSh0, pathOph0 = get_filepaths('25/07/2024', 'AM')  # and then the data filepaths from the hot 0% MP-sand mixture

    pathCSc5, pathOpc5 = get_filepaths('16/08/2024', 'PM')  # cold 5% MP-sand
    pathCSh5, pathOph5 = get_filepaths('14/08/2024', 'AM')  # hot 5% MP-sand
    
    pathCSc10, pathOpc10 = get_filepaths('19/08/2024', 'AM')  # cold 10% MP-sand
    pathCSh10, pathOph10 = get_filepaths('15/08/2024', 'AM')  # hot 10% MP-sand
    
    pathCSc25, pathOpc25 = get_filepaths('01/08/2024', 'AM')  # cold 25% MP-sand
    pathCSh25, pathOph25 = get_filepaths('02/08/2024', 'AM')  # hot 25% MP-sand    
    
    pathCSc50, pathOpc50 = get_filepaths('01/08/2024', 'PM')  # cold 50% MP-sand experiment
    pathCSh50, pathOph50 = get_filepaths('31/07/2024', 'PM')  # hot 50% MP-sand experiment
    
    pathCSc100, pathOpc100 = get_filepaths('26/07/2024', 'AM')  # cold 100% MP-sand experiment (pure MP and 0 sand)
    pathCSh100, pathOph100 = get_filepaths('30/07/2024', 'AM')  # hot 100% MP-sand (pure MP)
    
    # Collect the Campbell Scientific thermocouple data
    from read_CampbellSci import read_CampbellSci, sand_avgCS  #, water_avgCS  # function used depends on type of experiment done!***
    dt_CSc0, temps_arrCSc0, stdevs_arrCSc0 = read_CampbellSci(pathCSc0)  # cold 0% MP-sand mixture (pure sand) thermocouple data
    df_sand_avgCSc0 = sand_avgCS(dt_CSc0, temps_arrCSc0, stdevs_arrCSc0)  # and getting the averages in a dataframe for the cold 0% MP-sand
    dt_CSh0, temps_arrCSh0, stdevs_arrCSh0 = read_CampbellSci(pathCSh0)  # hot 0% MP-sand thermocouple data
    df_sand_avgCSh0 = sand_avgCS(dt_CSh0, temps_arrCSh0, stdevs_arrCSh0)  # and averaging hot 0% MP-sand
    
    dt_CSc5, temps_arrCSc5, stdevs_arrCSc5 = read_CampbellSci(pathCSc5)  # continuing as above, with cold 5% MP-sand thermocouple data...
    df_sand_avgCSc5 = sand_avgCS(dt_CSc5, temps_arrCSc5, stdevs_arrCSc5)
    dt_CSh5, temps_arrCSh5, stdevs_arrCSh5 = read_CampbellSci(pathCSh5)
    df_sand_avgCSh5 = sand_avgCS(dt_CSh5, temps_arrCSh5, stdevs_arrCSh5)
    
    dt_CSc10, temps_arrCSc10, stdevs_arrCSc10 = read_CampbellSci(pathCSc10)  # cold 10% MP-sand thermocouple data...
    df_sand_avgCSc10 = sand_avgCS(dt_CSc10, temps_arrCSc10, stdevs_arrCSc10)
    dt_CSh10, temps_arrCSh10, stdevs_arrCSh10 = read_CampbellSci(pathCSh10)
    df_sand_avgCSh10 = sand_avgCS(dt_CSh10, temps_arrCSh10, stdevs_arrCSh10)
    
    dt_CSc25, temps_arrCSc25, stdevs_arrCSc25 = read_CampbellSci(pathCSc25)  # cold 25% MP-sand thermocouple data...
    df_sand_avgCSc25 = sand_avgCS(dt_CSc25, temps_arrCSc25, stdevs_arrCSc25)
    dt_CSh25, temps_arrCSh25, stdevs_arrCSh25 = read_CampbellSci(pathCSh25)
    df_sand_avgCSh25 = sand_avgCS(dt_CSh25, temps_arrCSh25, stdevs_arrCSh25)
    
    dt_CSc50, temps_arrCSc50, stdevs_arrCSc50 = read_CampbellSci(pathCSc50)  # cold 50% MP-sand thermocouple data...
    df_sand_avgCSc50 = sand_avgCS(dt_CSc50, temps_arrCSc50, stdevs_arrCSc50)
    dt_CSh50, temps_arrCSh50, stdevs_arrCSh50 = read_CampbellSci(pathCSh50)
    df_sand_avgCSh50 = sand_avgCS(dt_CSh50, temps_arrCSh50, stdevs_arrCSh50)
    
    dt_CSc100, temps_arrCSc100, stdevs_arrCSc100 = read_CampbellSci(pathCSc100)  # cold 100% MP-sand (pure MP) thermocouple data...
    df_sand_avgCSc100 = sand_avgCS(dt_CSc100, temps_arrCSc100, stdevs_arrCSc100)
    dt_CSh100, temps_arrCSh100, stdevs_arrCSh100 = read_CampbellSci(pathCSh100)
    df_sand_avgCSh100 = sand_avgCS(dt_CSh100, temps_arrCSh100, stdevs_arrCSh100)
    
    #print(df_sand_avgCSh100.columns)  #******************this has standard deviation and error.
    
    # Collect the Optris thermal camera data
    from read_Optris import read_Optris, resample_Optris, average_Optris
    dt_Opc0, a1c0, a2c0, a3c0, a4c0 = read_Optris(pathOpc0)  # cold 0% MP-sand Optris data (pure sand)
    resampled_df_a1c0 = resample_Optris(dt_Opc0, a1c0)  # resampling areas 1 and 3 (below) to match thermocouple frequency of results
    resampled_df_a3c0 = resample_Optris(dt_Opc0, a3c0)
    avgOp_dfc0 = average_Optris(resampled_df_a1c0, resampled_df_a3c0)  # averaging between the resampled area 1 and area 3
    dt_Oph0, a1h0, a2h0, a3h0, a4h0 = read_Optris(pathOph0)  # hot 0% MP-sand Optris data (pure sand)
    resampled_df_a1h0 = resample_Optris(dt_Oph0, a1h0)  # resampling
    resampled_df_a3h0 = resample_Optris(dt_Oph0, a3h0)
    avgOp_dfh0 = average_Optris(resampled_df_a1h0, resampled_df_a3h0)  # averaging
    
    dt_Opc5, a1c5, a2c5, a3c5, a4c5 = read_Optris(pathOpc5)  # cold 5% MP-sand Optris data
    resampled_df_a1c5 = resample_Optris(dt_Opc5, a1c5)  # resampling
    resampled_df_a3c5 = resample_Optris(dt_Opc5, a3c5)
    avgOp_dfc5 = average_Optris(resampled_df_a1c5, resampled_df_a3c5)  # averaging 
    dt_Oph5, a1h5, a2h5, a3h5, a4h5 = read_Optris(pathOph5)  # hot 5% MP-sand Optris data
    resampled_df_a1h5 = resample_Optris(dt_Oph5, a1h5)
    resampled_df_a3h5 = resample_Optris(dt_Oph5, a3h5)
    avgOp_dfh5 = average_Optris(resampled_df_a1h5, resampled_df_a3h5)
    
    dt_Opc10, a1c10, a2c10, a3c10, a4c10 = read_Optris(pathOpc10)  # cold 10% MP-sand Optris data 
    resampled_df_a1c10 = resample_Optris(dt_Opc10, a1c10)  # resampling
    resampled_df_a3c10 = resample_Optris(dt_Opc10, a3c10)
    avgOp_dfc10 = average_Optris(resampled_df_a1c10, resampled_df_a3c10)  # averaging
    dt_Oph10, a1h10, a2h10, a3h10, a4h10 = read_Optris(pathOph10)  # hot 10% MP-sand Optris data
    resampled_df_a1h10 = resample_Optris(dt_Oph10, a1h10)
    resampled_df_a3h10 = resample_Optris(dt_Oph10, a3h10)
    avgOp_dfh10 = average_Optris(resampled_df_a1h10, resampled_df_a3h10)
    
    dt_Opc25, a1c25, a2c25, a3c25, a4c25 = read_Optris(pathOpc25)  # cold 25% MP-sand Optris data
    resampled_df_a1c25 = resample_Optris(dt_Opc25, a1c25)  # resampling
    resampled_df_a3c25 = resample_Optris(dt_Opc25, a3c25)
    avgOp_dfc25 = average_Optris(resampled_df_a1c25, resampled_df_a3c25)  # averaging 
    dt_Oph25, a1h25, a2h25, a3h25, a4h25 = read_Optris(pathOph25)  # hot 25% MP-sand Optris data
    resampled_df_a1h25 = resample_Optris(dt_Oph25, a1h25)
    resampled_df_a3h25 = resample_Optris(dt_Oph25, a3h25)
    avgOp_dfh25 = average_Optris(resampled_df_a1h25, resampled_df_a3h25)
    
    dt_Opc50, a1c50, a2c50, a3c50, a4c50 = read_Optris(pathOpc50)  # cold 50% MP-sand Optris data
    resampled_df_a1c50 = resample_Optris(dt_Opc50, a1c50)  # resampling
    resampled_df_a3c50 = resample_Optris(dt_Opc50, a3c50)
    avgOp_dfc50 = average_Optris(resampled_df_a1c50, resampled_df_a3c50)  # averaging 
    dt_Oph50, a1h50, a2h50, a3h50, a4h50 = read_Optris(pathOph50)  # hot 50% MP-sand Optris data
    resampled_df_a1h50 = resample_Optris(dt_Oph50, a1h50)
    resampled_df_a3h50 = resample_Optris(dt_Oph50, a3h50)
    avgOp_dfh50 = average_Optris(resampled_df_a1h50, resampled_df_a3h50)
    
    dt_Opc100, a1c100, a2c100, a3c100, a4c100 = read_Optris(pathOpc100)  # cold 100% MP-sand Optris data (pure MP)
    resampled_df_a1c100 = resample_Optris(dt_Opc100, a1c100)  # resampling
    resampled_df_a3c100 = resample_Optris(dt_Opc100, a3c100)
    avgOp_dfc100 = average_Optris(resampled_df_a1c100, resampled_df_a3c100)  # averaging
    dt_Oph100, a1h100, a2h100, a3h100, a4h100 = read_Optris(pathOph100)  # hot 100% MP-sand Optris data
    resampled_df_a1h100 = resample_Optris(dt_Oph100, a1h100)
    resampled_df_a3h100 = resample_Optris(dt_Oph100, a3h100)
    avgOp_dfh100 = average_Optris(resampled_df_a1h100, resampled_df_a3h100)
    
    #print(avgOp_dfh100.columns)  #***** This has stdev/sterr too!
    
    # Merge these different sensors together into a cold and hot dataframe per percentage of plastic
    from create_merged_df import create_merged_df
    df_merged_c0 = create_merged_df(avgOp_dfc0, df_sand_avgCSc0)
    df_merged_h0 = create_merged_df(avgOp_dfh0, df_sand_avgCSh0)
    
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
    
    #print(df_merged_c100.columns)  # does this have stdev/sterr?? YES, has both for both sensors
    
    # Removing first 15 minutes of each data record/merged dataframe
    df_ready_c0 = df_merged_c0.copy()  # cold 0% MP-sand (pure sand)
    start_t0 = df_ready_c0.index.min()
    cutoff_t0 = start_t0 + pd.Timedelta(minutes=20)
    df_trimmed_c0 = df_ready_c0[df_ready_c0.index >= cutoff_t0]
    df_ready_h0 = df_merged_h0.copy()  # hot 0% MP-sand (pure sand)
    start_th0 = df_ready_h0.index.min()
    cutoff_th0 = start_th0 + pd.Timedelta(minutes=20)
    df_trimmed_h0 = df_ready_h0[df_ready_h0.index >= cutoff_th0]
    
    df_ready_c5 = df_merged_c5.copy()  # cold 5% MP-sand
    start_t5 = df_ready_c5.index.min()
    cutoff_t5 = start_t5 + pd.Timedelta(minutes=20)
    df_trimmed_c5 = df_ready_c5[df_ready_c5.index >= cutoff_t5]
    df_ready_h5 = df_merged_h5.copy()  # hot 5% MP-sand
    start_th5 = df_ready_h5.index.min()
    cutoff_th5 = start_th5 + pd.Timedelta(minutes=20)
    df_trimmed_h5 = df_ready_h5[df_ready_h5.index >= cutoff_th5]
    
    df_ready_c10 = df_merged_c10.copy()  # cold 10% MP-sand
    start_t10 = df_ready_c10.index.min()
    cutoff_t10 = start_t10 + pd.Timedelta(minutes=20)
    df_trimmed_c10 = df_ready_c10[df_ready_c10.index >= cutoff_t10]
    df_ready_h10 = df_merged_h10.copy()  # hot 10% MP-sand
    start_th10 = df_ready_h10.index.min()
    cutoff_th10 = start_th10 + pd.Timedelta(minutes=20)
    df_trimmed_h10 = df_ready_h10[df_ready_h10.index >= cutoff_th10]
    
    df_ready_c25 = df_merged_c25.copy()  # cold 25% MP-sand
    start_t25 = df_ready_c25.index.min()
    cutoff_t25 = start_t25 + pd.Timedelta(minutes=20)
    df_trimmed_c25 = df_ready_c25[df_ready_c25.index >= cutoff_t25]
    df_ready_h25 = df_merged_h25.copy()  # hot 25% MP-sand
    start_th25 = df_ready_h25.index.min()
    cutoff_th25 = start_th25 + pd.Timedelta(minutes=20)
    df_trimmed_h25 = df_ready_h25[df_ready_h25.index >= cutoff_th25]
    
    df_ready_c50 = df_merged_c50.copy()  # cold 50% MP-sand
    start_t50 = df_ready_c50.index.min()
    cutoff_t50 = start_t50 + pd.Timedelta(minutes=20)
    df_trimmed_c50 = df_ready_c50[df_ready_c50.index >= cutoff_t50]
    df_ready_h50 = df_merged_h50.copy()  # hot 50% MP-sand
    start_th50 = df_ready_h50.index.min()
    cutoff_th50 = start_th50 + pd.Timedelta(minutes=40)
    df_trimmed_h50 = df_ready_h50[df_ready_h50.index >= cutoff_th50]
    
    df_ready_c100 = df_merged_c100.copy()  # cold 100% MP-sand (pure MP)
    start_t100 = df_ready_c100.index.min()
    cutoff_t100 = start_t100 + pd.Timedelta(minutes=20)
    df_trimmed_c100 = df_ready_c100[df_ready_c100.index >= cutoff_t100]
    df_ready_h100 = df_merged_h100.copy()  # hot 100% MP-sand (pure MP)
    start_th100 = df_ready_h100.index.min()
    cutoff_th100 = start_th100 + pd.Timedelta(minutes=20)
    df_trimmed_h100 = df_ready_h100[df_ready_h100.index >= cutoff_th100]
    
    # Reverse the hot dataframes so they each begin with coldest value
    df_trim_hot_rev0 = df_trimmed_h0.iloc[::-1].reset_index(drop=True)
    df_trim_hot_rev5 = df_trimmed_h5.iloc[::-1].reset_index(drop=True)
    df_trim_hot_rev10 = df_trimmed_h10.iloc[::-1].reset_index(drop=True)
    df_trim_hot_rev25 = df_trimmed_h25.iloc[::-1].reset_index(drop=True)
    df_trim_hot_rev50 = df_trimmed_h50.iloc[::-1].reset_index(drop=True)
    df_trim_hot_rev100 = df_trimmed_h100.iloc[::-1].reset_index(drop=True)
    
    # Concatenating the hot and cold dataframes together in the right order
    df_full0 = pd.concat([df_trimmed_c0, df_trim_hot_rev0])
    df_full5 = pd.concat([df_trimmed_c5, df_trim_hot_rev5])
    df_full10 = pd.concat([df_trimmed_c10, df_trim_hot_rev10])
    df_full25 = pd.concat([df_trimmed_c25, df_trim_hot_rev25])
    df_full50 = pd.concat([df_trimmed_c50, df_trim_hot_rev50])
    df_full100 = pd.concat([df_trimmed_c100, df_trim_hot_rev100])
    print(df_full100.columns)  # think this has standard deviation too yay! 
    
    # To plot the 1-1 temperature plot
    from plot1to1_multiple import plot1to1_multiple
    text_str = 'Shaved Plastic and Sand'
    # Create a dictionary of df_merged dataframes made above, to put into function below
    df_full_dict = dict(df0=df_full0, df5=df_full5, df10=df_full10, df25=df_full25,
                          df50=df_full50, df100=df_full100)
    plot1to1_multiple(df_full_dict, text_str)
    
    # Next is apply calibration for all of these lines/percentages
    from apply_calibration_multiple import apply_calibration_multiple
    df_calib_dict = apply_calibration_multiple(df_full_dict, text_str)
    
    # Then calculate deltaT from calibration less the reference 1:1 line
    from get_deltaT_multiple import get_deltaT_multiple
    dict_x, dict_deltaT = get_deltaT_multiple(df_calib_dict, text_str)
    #print(dict_deltaT.keys())  # including temperature difference plot
    
    r'''
    # Now need to also plot the 6 %s separately for their deltaT plots, with error envelopes each
    from get_deltaT_errors import get_deltaT_errors  # feed through the percentages one by one in this function
    y_lims = [-5.5, 2]
    df_list = [df_full0, df_full5, df_full10, df_full25, df_full50, df_full100]
    percentages = ['0', '5', '10', '25', '50', '100']
    colours = ['red', 'orange', 'darkgoldenrod', 'green', 'blue', 'purple']  #'gold' is too light on white
    
    stats_results = []  # empty list to put uncertainties dictionaries below into

    from calculate_uncertainty import calculate_uncertainty
    for j in range(len(df_list)):
        delT_sterr = get_deltaT_errors(df_list[j], text_str, percentages[j], colours[j], y_lims)  # should plot 6 plots, per plastic percentage, as individual deltaTs
        unc_dict = calculate_uncertainty(delT_sterr)
        unc_dict["Plastic Percentage"] = percentages[j]
        stats_results.append(unc_dict)
        
    df_results = pd.DataFrame(stats_results)  # converting list to df
    
    # Exporting to Excel        
    excel_filename = 'uncertainty_shavings_sand.xlsx'
    df_results.to_excel(excel_filename, index=False)
    print(f"Results saved to {excel_filename}")
    '''
    
    return dict_x, dict_deltaT

if __name__ == '__main__':
    dict_x, dict_deltaT = main()    
    

# Don't run the box below or else it will output it as text
#%% Checking smoothing with deltaT plot comparison - works here!! Just need to get it working within the get_deltaT_multiple.py function...
r'''
from types import SimpleNamespace
params_x = SimpleNamespace(**dict_x)
x0 = params_x.x0
x5 = params_x.x5
x10 = params_x.x10
x25 = params_x.x25
x50 = params_x.x50
x100 = params_x.x100

params_delT = SimpleNamespace(**dict_deltaT)
delT0 = params_delT.delT0 
delT5 = params_delT.delT5 
delT10 = params_delT.delT10 
delT25 = params_delT.delT25
delT50 = params_delT.delT50
delT100 = params_delT.delT100 
   
   
import numpy as np
import matplotlib.pyplot as plt
# Using ChatGPT to try the moving average to smooth these deltaT lines
window_size = 50  # window for the moving average
window = np.ones(window_size) / window_size  # moving average filter

# Apply the filters using convolution
y_smooth0 = np.convolve(delT0, window, mode='valid')
y_smooth5 = np.convolve(delT5, window, mode='valid')
y_smooth10 = np.convolve(delT10, window, mode='valid')
y_smooth25 = np.convolve(delT25, window, mode='valid')
y_smooth50 = np.convolve(delT50, window, mode='valid')
y_smooth100 = np.convolve(delT100, window, mode='valid')

# Adjust x to match the length of y_smooth - or else the data extrapolates at both ends and this data isn't there
offset = (window_size - 1) // 2  # offset for odd or even window size
x_smooth0 = x0[offset : -offset] if window_size % 2 == 1 else x0[offset + 1 : -offset]


# Adjust x to match the length of y_smooth - or else the data extrapolates at both ends and this data isn't there
offset = (window_size - 1) // 2  # offset for odd or even window size
x_smooth0 = x0[offset : -offset] if window_size % 2 == 1 else x0[offset + 1 : -offset]
x_smooth5 = x5[offset : -offset] if window_size % 2 == 1 else x5[offset + 1 : -offset]
x_smooth10 = x10[offset : -offset] if window_size % 2 == 1 else x10[offset + 1 : -offset]
x_smooth25 = x25[offset : -offset] if window_size % 2 == 1 else x25[offset + 1 : -offset]
x_smooth50 = x50[offset : -offset] if window_size % 2 == 1 else x50[offset + 1 : -offset]
x_smooth100 = x100[offset : -offset] if window_size % 2 == 1 else x100[offset + 1 : -offset]

x_smooth_list = [x_smooth0, x_smooth5, x_smooth10, x_smooth25, x_smooth50, x_smooth100]  # need to plot these all now
y_smooth_list = [y_smooth0, y_smooth5, y_smooth10, y_smooth25, y_smooth50, y_smooth100]
print(np.shape(x_smooth_list[0]), np.shape(y_smooth_list[0]))  #(17215,) (17215,) shape here which is good! why is it different in deltaT??

x_list = [x0, x5, x10, x25, x50, x100]
y_list = [delT0, delT5, delT10, delT25, delT50, delT100]
labels = ['0%', '5%', '10%', '25%', '50%', '100%']
colors_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']  # just using the colours of the rainbow for now 

for i in range(6):
    print(colors_list[i])
    label_str = labels[i]  # using the same labels as the plot above (0, 5, 10% etc.)
    plt.plot(x_smooth_list[i], y_smooth_list[i], lw=1, color=colors_list[i], label=rf'$\Delta T$ {label_str}', alpha=1.0)
    plt.plot(x_list[i], y_list[i], lw=2, color=colors_list[i], alpha=0.5)  # for the noisy data

text_str = 'Shaved Plastic and Sand'

plt.axhline(y=0, color='k', linestyle='--')
plt.axvline(x=21, color='k', linestyle='dotted')
plt.xlabel('Environmental Temperature (degrees Celsius)')
plt.ylabel(r'$\Delta T$ (degrees Celsius)')
plt.title(text_str +' Temperature Difference')
plt.legend()
plt.show()
'''  
    
    
    
    
    





