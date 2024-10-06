# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:18:28 2024

Updated version of plot1to1.py, plotting multiple percentages of the same type
of situation (microplastic and sand) in one plot.

@author: kplo373
"""
import numpy as np
import pandas as pd
from types import SimpleNamespace
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # for creating colour spectrums and legends
from matplotlib.collections import LineCollection  # or this instead of one above...

# str_expt parameter should be a string of the type of experiment done, e.g. 'Pellet-Sand', or 'Shaved Plastic and Sand'
def plot1to1_multiple(dict_parameters, str_expt):
    #print(dict_parameters.keys())
    params = SimpleNamespace(**dict_parameters)
    dfc0 = params.c0
    dfh0 = params.h0
    dfc5 = params.c5
    dfh5 = params.h5
    dfc10 = params.c10
    dfh10 = params.h10
    dfc25 = params.c25
    dfh25 = params.h25
    dfc50 = params.c50
    dfh50 = params.h50
    dfc100 = params.c100
    dfh100 = params.h100
    print(dfc0.columns)
    
    T_Opc0 = dfc0['temperature_Op']  # extracting the temperature arrays from 0% (pure sand)
    T_CSc0 = dfc0['temperature_CS']
    T_Oph0 = dfh0['temperature_Op']
    T_CSh0 = dfh0['temperature_CS']
    '''
    stdOpc0 = dfc0['stdev_Op']  # extracting the standard deviation arrays from 0% (pure sand)
    stdCSc0 = dfc0['stdev_CS']
    stdOph0 = dfh0['stdev_Op']
    stdCSh0 = dfh0['stdev_CS']
    sterrOpc0 = dfc0['sterr_Op']  # extracting the standard error arrays from 0% MP-sand (pure sand)
    sterrCSc0 = dfc0['sterr_CS']
    sterrOph0 = dfh0['sterr_Op']
    sterrCSh0 = dfh0['sterr_CS']
    '''
    T_Opc5 = dfc5['temperature_Op']  # extracting the temperature arrays from 5% MP-sand
    T_CSc5 = dfc5['temperature_CS']
    T_Oph5 = dfh5['temperature_Op']
    T_CSh5 = dfh5['temperature_CS']
    # can get stdev and sterr for 5% after this too...
    # and then the 10, 25, 50, and 100% temperature and uncertainty values!
    T_Opc10 = dfc10['temperature_Op']  # extracting the temperature arrays from 10%
    T_CSc10 = dfc10['temperature_CS']
    T_Oph10 = dfh10['temperature_Op']
    T_CSh10 = dfh10['temperature_CS']
    
    T_Opc25 = dfc25['temperature_Op']  # extracting the temperature arrays from 25% MP-sand
    T_CSc25 = dfc25['temperature_CS']
    T_Oph25 = dfh25['temperature_Op']
    T_CSh25 = dfh25['temperature_CS']
    
    T_Opc50 = dfc50['temperature_Op']  # extracting the temperature arrays from 50% MP-sand
    T_CSc50 = dfc50['temperature_CS']
    T_Oph50 = dfh50['temperature_Op']
    T_CSh50 = dfh50['temperature_CS']
    
    T_Opc100 = dfc100['temperature_Op']  # extracting the temperature arrays from 100% MP-sand (pure microplastic shavings!)
    T_CSc100 = dfc100['temperature_CS']
    T_Oph100 = dfh100['temperature_Op']
    T_CSh100 = dfh100['temperature_CS']
    
    
    # Get the minimum temperature value for all the arrays and then use the 5th percentile value of that to be the starting index below??
    # OR do I calculate the 5th percentile minimum limit for all different percentages? Would I also pick the Optris sensor then?
    # can't just use the same 5th percentile for all proportions of plastic, as they have different shapes and flicks etc. - need to calculate separately!
    
    # Using 5th Percentile Minimum Value (from ChatGPT) for Cold Array of 0% MP-sand (pure sand)
    p5_val0 = np.percentile(T_Opc0, 5)  # calculate the 5th percentile value for 0%
    i5_0 = np.argmin(np.abs(T_Opc0 - p5_val0))  # find the index of the closest value in y_cold to the 5th percentile value
    # Likewise, using 95th Percentile Max Value for Hot Array of 0% MP-sand (pure sand)
    p95_val0 = np.percentile(T_CSh0, 95)
    i95_0 = np.argmin(np.abs(T_CSh0 - p95_val0))

    p5_val5 = np.percentile(T_Opc5, 5)  # getting 5th percentile value for 5% MP-sand
    i5_5 = np.argmin(np.abs(T_Opc5 - p5_val5))
    p95_val5 = np.percentile(T_CSh5, 95)
    i95_5 = np.argmin(np.abs(T_CSh5 - p95_val5))
    
    p5_val10 = np.percentile(T_Opc10, 5)  # calculate the 5th percentile value for 10% MP-sand
    i5_10 = np.argmin(np.abs(T_Opc10 - p5_val10))
    p95_val10 = np.percentile(T_CSh10, 95)
    i95_10 = np.argmin(np.abs(T_CSh10 - p95_val10))
    
    p5_val25 = np.percentile(T_Opc25, 5)  # getting 5th percentile value for 25% MP-sand
    i5_25 = np.argmin(np.abs(T_Opc25 - p5_val25))
    p95_val25 = np.percentile(T_CSh25, 95)
    i95_25 = np.argmin(np.abs(T_CSh25 - p95_val25))
    
    p5_val50 = np.percentile(T_Opc50, 5)  # getting 5th percentile value for 50% MP-sand
    i5_50 = np.argmin(np.abs(T_Opc50 - p5_val50))
    p95_val50 = np.percentile(T_CSh50, 95)
    i95_50 = np.argmin(np.abs(T_CSh50 - p95_val50))
    
    p5_val100 = np.percentile(T_Opc100, 5)  # calculate the 5th percentile value for 100% MP-sand (pure MP)
    i5_100 = np.argmin(np.abs(T_Opc100 - p5_val100))
    p95_val100 = np.percentile(T_CSh100, 95)
    i95_100 = np.argmin(np.abs(T_CSh100 - p95_val100))
    

    # Trimming off values in each array that are below the 5th percentile or above the 95th percentile
    tempOpc0 = T_Opc0.iloc[i5_0:]  # this needs to start and end at same indices as tempCSc0
    tempCSc0 = T_CSc0.iloc[i5_0:]
    tempOph0 = T_Oph0.iloc[i95_0:]
    tempCSh0 = T_CSh0.iloc[i95_0:] 
    '''
    sdOpc0 = stdOpc0.iloc[i5_0:]
    sdCSc0 = stdCSc0.iloc[i5_0:]
    sdOph0 = stdOph0.iloc[i95_0:]
    sdCSh0 = stdCSh0.iloc[i95_0:]
    seOpcold = sterrOpcold.iloc[i5_0:]
    seCScold = sterrCScold.iloc[i5_0:]
    seOphot = sterrOphot.iloc[i95_0:]
    seCShot = sterrCShot.iloc[i95_0:]
    '''  # can add standard dev and standard error trimmings below later
    
    tempOpc5 = T_Opc5.iloc[i5_5:]  # getting the 5% MP-sand mixture data clipped to 5th and 95th percentiles
    tempCSc5 = T_CSc5.iloc[i5_5:]
    tempOph5 = T_Oph5.iloc[i95_5:]
    tempCSh5 = T_CSh5.iloc[i95_5:]
    
    tempOpc10 = T_Opc10.iloc[i5_10:]  # trimming the 10% MP-sand mixture data
    tempCSc10 = T_CSc10.iloc[i5_10:]
    tempOph10 = T_Oph10.iloc[i95_10:]
    tempCSh10 = T_CSh10.iloc[i95_10:]
    
    tempOpc25 = T_Opc25.iloc[i5_25:]  # trimming the 25% MP-sand mixture data
    tempCSc25 = T_CSc25.iloc[i5_25:]
    tempOph25 = T_Oph25.iloc[i95_25:]
    tempCSh25 = T_CSh25.iloc[i95_25:]
    
    tempOpc50 = T_Opc50.iloc[i5_50:]  # trimming the 50% MP-sand mixture data
    tempCSc50 = T_CSc50.iloc[i5_50:]
    tempOph50 = T_Oph50.iloc[i95_50:]
    tempCSh50 = T_CSh50.iloc[i95_50:]
    
    tempOpc100 = T_Opc100.iloc[i5_100:]  # trimming the 100% MP-sand mixture data
    tempCSc100 = T_CSc100.iloc[i5_100:]
    tempOph100 = T_Oph100.iloc[i95_100:]
    tempCSh100 = T_CSh100.iloc[i95_100:]
    
    # Combine all x and y arrays into hot and cold lists (for plotting in red and blue spectrums)
    x_cold_arr = [tempCSc0, tempCSc5, tempCSc10, tempCSc25, tempCSc50, tempCSc100]
    y_cold_arr = [tempOpc0, tempOpc5, tempOpc10, tempOpc25, tempOpc50, tempOpc100]
    x_hot_arr = [tempCSh0, tempCSh5, tempCSh10, tempCSh25, tempCSh50, tempCSh100]
    y_hot_arr = [tempOph0, tempOph5, tempOph10, tempOph25, tempOph50, tempOph100]
    
    # Specify the percentage labels
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    
    # Set the colormap to 'Blues' and get 6 shades of blue
    cmap1 = cm.get_cmap('Blues', 6)
    colors1 = cmap1(np.linspace(0.4, 1, 6))  # Creates 6 shades ranging from lighter to darker blue - should range the other way for blue, but good for red...
    cmap2 = cm.get_cmap('Reds', 6)
    colors2 = cmap2(np.linspace(0.4, 1, 6))

    
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(tempCSc0.iloc[0], tempOpc0.iloc[0], tempCSc5.iloc[0], tempOpc5.iloc[0], tempCSc10.iloc[0], tempOpc10.iloc[0], tempCSc25.iloc[0],
                      tempOpc25.iloc[0], tempCSc50.iloc[0], tempOpc50.iloc[0], tempCSc100.iloc[0], tempOpc100.iloc[0])  # is this the right way to get the limits?
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max(tempCSh0.iloc[0], tempOph0.iloc[0], tempCSh5.iloc[0], tempOph5.iloc[0], tempCSh10.iloc[0], tempOph10.iloc[0], tempCSh25.iloc[0],
                      tempOph25.iloc[0], tempCSh50.iloc[0], tempOph50.iloc[0], tempCSh100.iloc[0], tempOph100.iloc[0])
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below
    print('Limits:', lower_lim, upper_lim)
    
    plt.figure(figsize=(6, 6))  # make it into a square shape, same axes limits!
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)

    # To plot the 1:1 reference line
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference')
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, xerr=seCSc0, color='k')  # just include one errorbar maybe? Is there a better way to show them separately?
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, color='k')
    # plt.plot(tempCSc0, tempOpc0, 'aqua', label='Cold Raw Data - 0%')  # listing this after errorbars and as dots allow it to show up over black errorbars
    #can add a plt.errorbar() here too for the hot data - assuming using standard error like Tom said
    # see list of colours here: https://matplotlib.org/stable/gallery/color/named_colors.html
    # plt.plot(tempCSc5, tempOpc5, 'powderblue', label='Cold Raw Data - 5%') 
    # plt.plot(tempCSc10, tempOpc10, 'skyblue', label='Cold Raw Data - 10%')
    # plt.plot(tempCSc25, tempOpc25, 'darkturquoise', label='Cold Raw Data - 25%') 
    # plt.plot(tempCSc50, tempOpc50, 'deepskyblue', label='Cold Raw Data - 50%') 
    # plt.plot(tempCSc100, tempOpc100, 'dodgerblue', label='Cold Raw Data - 100%')
    
    
    for i in range(6):
        plt.plot(x_cold_arr[i], y_cold_arr[i], color=colors1[i], label=f'Cold {labels[i]}')  # the labelling might be a bit tricky, want to do it in %s...
    
    for j in range(6):  # doing a second separate loop so that the legend lists all cold then hot experiments in the plot
        plt.plot(x_hot_arr[j], y_hot_arr[j], color=colors2[j], label=f'Hot {labels[j]}')
    
    # plt.plot(tempCSh0, tempOph0, 'lightsalmon', label='Hot Raw Data - 0%')
    # plt.plot(tempCSh5, tempOph5, 'coral', label='Hot Raw Data - 5%')
    #plt.plot(tempCSh10, tempOph10, 'orangered', label='Hot Raw Data - 10%')
    # plt.plot(tempCSh25, tempOph25, 'red', label='Hot Raw Data - 25%')
    # plt.plot(tempCSh50, tempOph50, 'chocolate', label='Hot Raw Data - 50%')
    # plt.plot(tempCSh100, tempOph100, 'sienna', label='Hot Raw Data - 100%')
    
    plt.title('Raw Data Comparison For ' + str_expt)  # including what percentage of plastic etc.
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.grid()
    plt.legend()
    plt.show()

    
    # Create new merged dfs here that only have the clipped data. Then won't need to do the percentile limits in any other functions...
    #need to clip the stdev and sterr arrays too.. then create new merged df and return them.
    df_clipped_cold = pd.DataFrame({'tempCS0': tempCSc0, # 'stdCS0': sdCSc0, 'sterrCS0': seCSc0, 
                                    'tempOp0': tempOpc0, #'stdOp0': sdOpc0, 'sterrOp0': seOpc0})
                                    'tempCS5': tempCSc5, 'tempOp5': tempOpc5, 'tempCS10': tempCSc10, 'tempOp10': tempOpc10, 'tempCS25': tempCSc25, 
                                    'tempOp25': tempOpc25,'tempCS50': tempCSc50, 'tempOp50': tempOpc50, 'tempCS100': tempCSc100, 'tempOp100': tempOpc100})
    df_clipped_hot = pd.DataFrame({'tempCS0': tempCSh0, #'stdCS0': sdCSh0, 'sterrCS0': seCSh0, 
                                    'tempOp0': tempOph0, #'stdOp0': sdOph0, 'sterrOp0': seOph0})
                                    'tempCS5': tempCSh5, 'tempOp5': tempOph5, 'tempCS10': tempCSh10, 'tempOp10': tempOph10, 'tempCS25': tempCSh25, 
                                    'tempOp25': tempOph25,'tempCS50': tempCSh50, 'tempOp50': tempOph50, 'tempCS100': tempCSh100, 'tempOp100': tempOph100})
    
    
    
    return df_clipped_cold, df_clipped_hot