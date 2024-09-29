# MSc2024
The Effect of Microplastic on the Radiative Properties of Sand and Water 


hyperspectral folder:

* extract_hyperspectral.py is for extracting the wavelengths from the HDR files, and the counts from the disc image files. These will be put into a dataframe with wavelengths as the index and counts as the first column.


old_scripts folder:

* general_plot.py can plot one single test comparing the Optris thermal camera temperatures and the average of 6 thermocouple temperatures, including the correlation coefficient and polyfit line of best fit.
* general_plot_comparison.py does the same as general_plot.py, but can compare the 50% nurdle-water mixture with the 100% nurdle-water mixture (for one temperature range).
* plot_hot_cold_calibration.py extracts both hot and cold data and plots them on the same axes, for the pure water tests. An SVM fit is applied to the data, and this generates the .pkl files at the bottom of the list here.
* plot_hot_cold_retry.py is the file I accidentally deleted but have now recreated, to plot any other hot and cold datasets together for the same plastic proportion and calibrate it with the pure water .pkl files, giving the nice green plot.

The last few files are .pkl or .npy and are used within the plot_hot_cold_retry.py script to calibrate the raw data (coming from the plot_hot_cold_calibration.py script where pure water was used).



* apply_calibration.py has a function that fits the pure water calibration SVM to the raw data in the dataframes output by the plot1to1.py script, and then plots the calibrated data in a nice green plot.
* create_merged_df.py takes the outputs from the average Optris and average Campbell Scientific functions, and merges both into one dataframe, with the common datetime values along the dataframe index. Will be used once for cold data, then again for hot experiment data.
* fit_SVR.py will only be run once on the pure water experiments, applying a support vector machine in regression (SVR) to the raw data and then storing the calibration data in pkl files for use in apply_calibration.py.
* get_deltaT.py calculates the delta T value, representing the temperature difference from the reference 1:1 line of the calibrated raw data from apply_calibration.py, and gives a quick plot of delta T against a linspace x-axis array.
* get_filepaths.py is a function that outputs the path and filenames of the thermal camera and thermocouple data files for that experimental date.
* main.py is a script that imports all the functions from the other scripts and runs them together to produce plots for a chosen experimental mixture.
* plot1to1.py involves a function that creates 1:1 plots of raw data, the thermocouple temperature (x) vs. the thermal camera temperature (y).
* read_CampbellSci.py extracts data from the Campbell Scientific thermocouple .dat files. Two little functions at the end calculate the averages of sand and water experiments.
* read_Optris.py extracts data from the Optris thermal camera .dat files. It also includes one averaging function.

The last few files are .pkl or .npy and are used within the apply_calibration.py script to calibrate the raw data (coming from the fit_SVR.py script where pure water was used).

