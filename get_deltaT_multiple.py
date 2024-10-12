 # -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:58:29 2024

Script for calculating multiple percentages of plastic's temperature difference
(deltaT) at once, and then plotting them with a reference y=0 line.

@author: kplo373
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.cm as cm


def get_deltaT_multiple(dict_x, dict_ypred, text_str):
    #print(dict_x.keys())
    x0 = dict_x['x0'].ravel()  # extracting and shrinking the ndarrays to arrays
    x5 = dict_x['x5'].ravel()
    x10 = dict_x['x10'].ravel()
    x25 = dict_x['x25'].ravel()
    x50 = dict_x['x50'].ravel()
    x100 = dict_x['x100'].ravel()
    
    y0 = dict_ypred['y0'].ravel()
    y5 = dict_ypred['y5'].ravel()
    y10 = dict_ypred['y10'].ravel()
    y25 = dict_ypred['y25'].ravel()
    y50 = dict_ypred['y50'].ravel()
    y100 = dict_ypred['y100'].ravel()
    

    lower_limit = min(x0[0], x5[0], x10[0], x25[0], x50[0], x100[0],
                      y0[0], y5[0], y10[0], y25[0], y50[0], y100[0])
    upper_limit = max( max(x0), max(x5), max(x10), max(x25), max(x50), max(x100),
                       max(y0), max(y5), max(y10), max(y25), max(y50), max(y100) )
    print(lower_limit, upper_limit)  # looks good: 11.213333333333333 32.632147450277685
    
    
    # If I can maybe plot the y=x line here (or get data from previous plot) then can use this for x-axis data
    #ref_line = plt.plot(x_comb, x_comb)
    x_ref0 = x0
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
    plt.figure(figsize=(6, 6))  # controlling size of font used by making it bigger or smaller (keep same x and y sizes so square!)
    
    # Combine all x and y arrays into a list (for plotting in a green spectrum)
    x_list = [x0, x5, x10, x25, x50, x100]
    y_list = [deltaT0, deltaT5, deltaT10, deltaT25, deltaT50, deltaT100]

    # Specify the percentage labels
    labels = ['0%', '5%', '10%', '25%', '50%', '100%']
    
    # Set the colormap to 'Blues' and get 6 shades of blue
    cmap = cm.get_cmap('Reds', 6)
    colors = cmap(np.linspace(0.4, 1, 6))  # Creates 6 shades ranging from lighter to darker green

    for i in range(6):
        #plt.plot(x_list[i], y_list[i], lw=1, color=colors[i], label=f'$\Delta T {labels[i]}$', alpha=0.6)
        label_str = labels[i]
        plt.plot(x_list[i], y_list[i], lw=1, color=colors[i], label=rf'$\Delta T$ {label_str}', alpha=0.6)  # plotting the data in a red spectrum

    plt.axhline(y=0, color='k', linestyle='--')
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
    dict_xref = {'x_ref0': x_ref0, 'x_ref5': x_ref5, 'x_ref10': x_ref10, 'x_ref25': x_ref25, 'x_ref50': x_ref50, 'x_ref100': x_ref100}
    dict_deltaT = {'delT0': deltaT0, 'delT5': deltaT5, 'delT10': deltaT10, 'delT25': deltaT25, 'delT50': deltaT50, 'delT100': deltaT100}
    
    return dict_xref, dict_deltaT

