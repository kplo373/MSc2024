# MSc2024
The Effect of Microplastic on the Radiative Properties of Sand and Water 

* extract_hyperspectral.py is for extracting the wavelengths from the HDR files, and the counts from the disc image files. These will be put into a dataframe with wavelengths as the index and counts as the first column.
* general_plot.py can plot one single test comparing the Optris thermal camera temperatures and the average of 6 thermocouple temperatures, including the correlation coefficient and polyfit line of best fit.
* general_plot_comparison.py does the same as general_plot.py, but can compare the 50% nurdle-water mixture with the 100% nurdle-water mixture (for one temperature range).
* get_filepaths.py is part of the new set of functions, and is a function that outputs the path and filenames of the thermal camera and thermocouple data files for that experimental date.
* plot_hot_cold_calibration.py extracts both hot and cold data and plots them on the same axes, for the pure water tests. An SVM fit is applied to the data, and this generates the .pkl files at the bottom of the list here.
* plot_hot_cold_retry.py is the file I accidentally deleted but have now recreated, to plot any other hot and cold datasets together for the same plastic proportion and calibrate it with the pure water .pkl files, giving the nice green plot.
* read_CampbellSci.py is also part of the new set of functions, and it extracts data from the Campbell Scientific thermocouple .dat files. Two little functions at the end calculate the averages of sand and water experiments.
* read_Optris.py is another new function, to extract data from the Optris thermal camera .dat files. It also includes one averaging function.

The last few files are .pkl or .npy and are used within the plot_hot_cold_retry.py script to calibrate the raw data (coming from the plot_hot_cold_calibration.py script where pure water was used).
