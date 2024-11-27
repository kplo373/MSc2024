 # -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:58:29 2024

Script for calculating multiple percentages of plastic's temperature difference
(deltaT) at once, and then plotting them with a reference y=0 line.

@author: kplo373
"""
import numpy as np
import matplotlib.pyplot as plt
#import sys
import matplotlib.cm as cm
from types import SimpleNamespace


def get_deltaT_multiple(dict_in, text_str):
    #print(dict_in.keys())
    params = SimpleNamespace(**dict_in)
    df0 = params.df0
    df5 = params.df5
    df10 = params.df10
    df25 = params.df25
    df50 = params.df50
    df100 = params.df100
    #print(df0.columns)
    
    x0 = df0['temperature_CS'].to_numpy()  # extracting the series
    x5 = df5['temperature_CS'].to_numpy()
    x10 = df10['temperature_CS'].to_numpy()
    x25 = df25['temperature_CS'].to_numpy()
    x50 = df50['temperature_CS'].to_numpy()
    x100 = df100['temperature_CS'].to_numpy()
    
    if 'ater' or 'and' in text_str:
        y0 = df0['y_corrected'].to_numpy()  # using the corrected/calibrated y values rather than raw Optris data
        y5 = df5['y_corrected'].to_numpy()
        y10 = df10['y_corrected'].to_numpy()
        y25 = df25['y_corrected'].to_numpy()
        y50 = df50['y_corrected'].to_numpy()
        y100 = df100['y_corrected'].to_numpy()


    lower_limit = min(x0[0], x5[0], x10[0], x25[0], x50[0], x100[0],
                      y0[0], y5[0], y10[0], y25[0], y50[0], y100[0])
    upper_limit = max(x0[-1], x5[-1], x10[-1], x25[-1], x50[-1], x100[-1],
                      y0[-1], y5[-1], y10[-1], y25[-1], y50[-1], y100[-1])
    print(lower_limit, upper_limit)  # looks good: 11.213333333333333 32.632147450277685
    
    
    # If I can maybe plot the y=x line here (or get data from previous plot) then can use this for x-axis data
    #ref_line = plt.plot(x_comb, x_comb)
    x_ref0 = x0  # not sure why I made these separate actually, could have just used x0 etc. below in deltaT calculations
    x_ref5 = x5
    x_ref10 = x10
    x_ref25 = x25
    x_ref50 = x50
    x_ref100 = x100
 
    
    # Time to calculate deltaT per percentage
    deltaT0 = np.zeros(len(y0))
    deltaT5 = np.zeros(len(y5))
    deltaT10 = np.zeros(len(y10))
    deltaT25 = np.zeros(len(y25))
    deltaT50 = np.zeros(len(y50))
    deltaT100 = np.zeros(len(y100))
    for ya in range(len(y0)):
        delT0 = y0[ya] - x_ref0[ya]
        deltaT0[ya] = delT0
    for yb in range(len(y5)):
        delT5 = y5[yb] - x_ref5[yb]
        deltaT5[yb] = delT5
    for yc in range(len(y10)):
        delT10 = y10[yc] - x_ref10[yc]
        deltaT10[yc] = delT10
    for yd in range(len(y25)):
        delT25 = y25[yd] - x_ref25[yd]
        deltaT25[yd] = delT25
    for ye in range(len(y50)):
        delT50 = y50[ye] - x_ref50[ye]
        deltaT50[ye] = delT50
    for yf in range(len(y100)):
        delT100 = y100[yf] - x_ref100[yf]
        deltaT100[yf] = delT100


    # Plotting deltaT against Environmental Temperature
    plt.figure(figsize=(6, 4))  # controlling size of font used by making it bigger or smaller. This plot doesn't need to be square!
    
    # Combine all x and y arrays into a list (for plotting in a green spectrum)
    x_list = [x0, x5, x10, x25, x50, x100]
    y_list = [deltaT0, deltaT5, deltaT10, deltaT25, deltaT50, deltaT100]

    # Specify the percentage labels
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    colors = ['r', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']  # just using the colours of the rainbow for now  
    
    # Set the colormap to 'Blues' and get 6 shades of blue
    #cmap = cm.get_cmap('Reds', 6)
    #colors = cmap(np.linspace(0.4, 1, 6))  # Creates 6 shades ranging from lighter to darker green

    for i in range(6):
        #plt.plot(x_list[i], y_list[i], lw=1, color=colors[i], label=f'$\Delta T {labels[i]}$', alpha=0.6)
        label_str = labels[i]
        plt.plot(x_list[i], y_list[i], lw=1, color=colors[i], label=rf'$\Delta T$ {label_str}', alpha=0.6)  # plotting the data in a red spectrum

    plt.axhline(y=0, color='k', linestyle='--')
    plt.axvline(x=21, color='k', linestyle='dotted')
    plt.xlabel('Environmental Temperature (degrees Celsius)')
    plt.ylabel(r'$\Delta T$ (degrees Celsius)')
    plt.title(text_str +' Temperature Difference')
    plt.grid()
    plt.legend()
    
    # To save the figure in the SavedPlots\TempDiff_Separate folder
    if 'hav' in text_str:
        if 'and' in text_str:
            final_folder = 'MP_sand'
        elif 'ater' in text_str:
            final_folder = 'MP_water'
        file_str = r'\TempDiff_' + text_str.replace("% Shavings", "_MP") + '.png'  # not sure if I can have % signs in a filename, so taking it out to be safe...
    elif 'ellet' in text_str:
        if 'and' in text_str:
            final_folder = 'Nurdle_sand'
        elif 'ater' in text_str:
            final_folder = 'Nurdle_water'
        file_str = r'\TempDiff_' + text_str.replace("% Pellets", "_nurd") + '.png'
    file_path = r"D:\MSc Results\SavedPlots\TempDiff_Separate" + '\\' + final_folder
    
    print(file_path + file_str)
    plt.savefig(file_path + file_str, bbox_inches='tight')  # removes whitespace in the file once saved
    plt.show()
    
    # Creating two dictionaries to transfer/return the data arrays used to make this deltaT plot
    dict_x = {'x0': x0, 'x5': x5, 'x10': x10, 'x25': x25, 'x50': x50, 'x100': x100}
    dict_deltaT = {'delT0': deltaT0, 'delT5': deltaT5, 'delT10': deltaT10, 'delT25': deltaT25, 'delT50': deltaT50, 'delT100': deltaT100}
    
    # Using ChatGPT to try the moving average to smooth these deltaT lines
    window_size = 50  # window for the moving average
    window = np.ones(window_size) / window_size  # moving average filter

    # Apply the filters using convolution
    y_smooth0 = np.convolve(deltaT0, window, mode='valid')
    y_smooth5 = np.convolve(deltaT5, window, mode='valid')
    y_smooth10 = np.convolve(deltaT10, window, mode='valid')
    y_smooth25 = np.convolve(deltaT25, window, mode='valid')
    y_smooth50 = np.convolve(deltaT50, window, mode='valid')
    y_smooth100 = np.convolve(deltaT100, window, mode='valid')

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

    x_list = [x0, x5, x10, x25, x50, x100]
    y_list = [deltaT0, deltaT5, deltaT10, deltaT25, deltaT50, deltaT100]
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    colors_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']  # just using the colours of the rainbow for now 

    for i in range(6):
        label_str = labels[i]  # using the same labels as the plot above (0, 5, 10% etc.)
        plt.plot(x_smooth_list[i], y_smooth_list[i], lw=2, color=colors_list[i], label=rf'$\Delta T$ {label_str}', alpha=1.0)
        plt.plot(x_list[i], y_list[i], lw=1, color=colors_list[i], alpha=0.5)  # for the noisy data

    plt.axhline(y=0, color='k', linestyle='--')
    plt.axvline(x=21, color='k', linestyle='dotted')
    plt.xlabel('Environmental Temperature (degrees Celsius)')
    plt.ylabel(r'$\Delta T$ (degrees Celsius)')
    plt.title(text_str +' Temperature Difference')
    plt.legend()
    plt.grid()
    plt.show()
    
    
    return dict_x, dict_deltaT

