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

# str_expt parameter should be a string of the type of experiment done, e.g. 'Pellet-Sand', or 'Shaved Plastic and Sand'
def plot1to1_multiple(dict_parameters, str_expt):
    print(dict_parameters.keys())
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
    
    '''
    p5_val10 = np.percentile(T_Opc10, 5)  # calculate the 5th percentile value for 10% MP-sand
    i5_10 = np.argmin(np.abs(T_Opc10 - p5_val10))
    p95_val10 = np.percentile(T_CSh10, 95)
    i95_10 = np.argmin(np.abs(T_CSh10 - p95_val10))
    '''  # and continue like this for 25%, 50%, and 100%...


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
    '''
    
    tempOpc5 = T_Opc5.iloc[i5_0:]  # getting the 5% MP-sand mixture data clipped to 5th and 95th percentiles
    tempCSc5 = T_CSc5.iloc[i5_0:]
    tempOph5 = T_Oph5.iloc[i95_0:]
    tempCSh5 = T_CSh5.iloc[i95_0:]
    # can add standard dev and standard error trimmings below later
    # and then also the other percentages: 10, 25, 50, 100% of MP-sand
    
    
    
    # Need to create limits for the plots below so that the plots are square-shaped
    import math
    def normal_round(n):  # create a function to round up if .5 or higher, or round down if less than .5
        if n - math.floor(n) < 0.5:
            return math.floor(n)
        return math.ceil(n)

    lower_limit = min(tempCSc0.iloc[0], tempOpc0.iloc[0], tempCSc5.iloc[0], tempOpc5.iloc[0])  # not really sure how to get limits, as I will have more arrays later...
    lower_lim = normal_round(lower_limit) - 1

    upper_limit = max(tempCSh0.iloc[0], tempOph0.iloc[0], tempCSh5.iloc[0], tempOph5.iloc[0])  # same here as above, will need to add in more arrays later...
    upper_lim = normal_round(upper_limit) + 1   # now set the x and y axes limits to lower_lim, upper_lim below
    print('Limits:', lower_lim, upper_lim)
    
    plt.figure(figsize=(6, 6))  # make it into a square shape, same axes limits!
    plt.xlim(lower_lim, upper_lim)  # for a square-shaped plot
    plt.ylim(lower_lim, upper_lim)

    # To plot the 1:1 reference line
    plt.plot([lower_lim, upper_lim], [lower_lim, upper_lim], color='black', linestyle='--', label='1:1 Reference Line (y=x)')
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, xerr=seCSc0, color='k')  # just include one errorbar maybe? Is there a better way to show them separately?
    #plt.errorbar(tempCSc0, tempOpc0, yerr=seOpc0, color='k')
    plt.plot(tempCSc0, tempOpc0, 'aqua', label='Cold Raw Data - 0%')  # listing this after errorbars and as dots allow it to show up over black errorbars
    #can add a plt.errorbar() here too for the hot data - assuming using standard error like Tom said
    # see list of colours here: https://matplotlib.org/stable/gallery/color/named_colors.html
    plt.plot(tempCSc5, tempOpc5, 'darkturquoise', label='Cold Raw Data - 5%') 
    
    plt.plot(tempCSh0, tempOph0, 'lightcoral', label='Hot Raw Data - 0%')
    plt.plot(tempCSh5, tempOph5, 'indianred', label='Hot Raw Data - 5%')
    
    
    plt.title('Sensor Comparison For ' + str_expt)  # including what percentage of plastic etc.
    plt.xlabel('Thermocouple Temperature (degrees Celsius)')
    plt.ylabel('Thermal Camera Temperature (degrees Celsius)')
    plt.grid()
    plt.legend()
    plt.show()

    
    # Create new merged dfs here that only have the clipped data. Then won't need to do the percentile limits in any other functions...
    #need to clip the stdev and sterr arrays too.. then create new merged df and return them.
    df_clipped_cold = pd.DataFrame({'tempCS0': tempCSc0, # 'stdCS0': sdCSc0, 'sterrCS0': seCSc0, 
                                    'tempOp0': tempOpc0, #'stdOp0': sdOpc0, 'sterrOp0': seOpc0})
                                    'tempCS5': tempCSc5, 'tempOp5': tempOpc5})
    df_clipped_hot = pd.DataFrame({'tempCS0': tempCSh0, #'stdCS0': sdCSh0, 'sterrCS0': seCSh0, 
                                    'tempOp0': tempOph0, #'stdOp0': sdOph0, 'sterrOp0': seOph0})
                                    'tempCS5': tempCSh5, 'tempOp5': tempOph5})
    
    
    
    return df_clipped_cold, df_clipped_hot