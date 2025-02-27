# MSc2024
The Effect of Microplastic on the Radiative Properties of Sand and Water 

Kestrel folder:
* read_Kestrel.py loads in the Kestrel data and plots the humidity readings for the Coastal Laboratory.

RBR folder:
* plot_RBR_thermocouples.py is a plotting script that compares the RBR data to the thermocouples to see the thermocouples' accuracy.
* plot_thermocouples.py plots only the thermocouples for the two tests without the RBR present, to see the effect of the pump.
* read_RBR.py is a loading script for rsk format RBR data, returning time and temperature for plotting in a script above.
* read_RBR_excel.py is a loading script for excel format RBR data, that returns time and temperature to plot in another script.

hyperspectral folder:

* extract_hyperspectral.py is for extracting the wavelengths from the HDR files, and the counts from the disc image files. The intention was to put them into a dataframe with wavelengths as the index and counts as the first column, but this will need to be done in further research.

old_scripts folder:

* general_plot.py can plot one single test comparing the Optris thermal camera temperatures and the average of 6 thermocouple temperatures, including the correlation coefficient and polyfit line of best fit.
* general_plot_comparison.py does the same as general_plot.py, but can compare the 50% nurdle-water mixture with the 100% nurdle-water mixture (for one temperature range).
* plot_hot_cold_calibration.py extracts both hot and cold data and plots them on the same axes, for the pure water tests. An SVM fit is applied to the data, and this generates the .pkl files at the bottom of the list here.
* plot_hot_cold_retry.py is the file I accidentally deleted but have now recreated, to plot any other hot and cold datasets together for the same plastic proportion and calibrate it with the pure water .pkl files, giving the nice green plot.


These are the remaining files, saved separately in the general MSc2024 folder:
* apply_calibration.py has a function that fits the pure water calibration adjustments to the raw data in the dataframes output by the plot1to1.py script, and then plots the calibrated data for one mixture at a time.
* apply_calibration_multiple.py does the same as above, but applies the calibration to all the plastic percentages in a chosen mixture group at once and plots them together.
* apply_calibration_puresand.py sets up the calibration adjustments table for sand mixtures, after having the pure water adjustments applied.
* apply_calibration_purewater.py sets up the baseline water calibration adjustments table, using a linear regression model.
* calculate_quartz.py was used to calculate the percentage of quartz present in a photo of the sandy beach sediment used in the experiments.
* calculate_uncertainty.py calculates the uncertainty columns (mean, approximate mode, 90th and 10th percentiles) required from the standard errors calculated in the deltaT plots, which are then presented in my thesis results.
* calib_adj_plot.py was used to plot the calibration adjustments straight from the pure water and pure sand tables produced in the apply_calibration scripts, to show their general spread. These are presented in my thesis discussion.
* create_merged_df.py takes the outputs from the average Optris and average Campbell Scientific functions, and merges both into one dataframe, with the common datetime values along the dataframe index. Will be used once for cold data, then again for hot experiment data.
* get_deltaT.py calculates the delta T value, representing the temperature difference from the reference 1:1 line of the calibrated raw data from apply_calibration.py, and gives a quick plot of delta T against a linspace x-axis array.
* get_deltaT_errors.py is an updated version of get_deltaT.py, plotting the individual plastic percentages' deltaT separately with an error envelope to show the uncertainty.
* get_deltaT_multiple.py calculates and plots the deltaT values for all plastic percentages together within a mixture group, but without the error envelope as it was too difficult to interpret.
* get_filepaths.py is a function that outputs the path and filenames of the thermal camera and thermocouple data files for that experimental date.
* main.py is a script that imports all the functions from the other scripts and runs them together to produce plots for a chosen experimental mixture, and was mainly used to create the pure water calibration adjustments.
* main_MPsand.py is the master script to plot the raw, calibrated, and deltaT data for all the microplastic/shavings and sand mixtures.
* main_MPwater.py is the master script to plot the raw, calibrated, and deltaT data for all the microplastic/shavings and water mixtures.
* main_pelletsand.py is the main script for all the pellets and sand mixtures.
* main_pelletwater.py is the main script for all the pellets and water mixtures.
* main_sand.py is the main script to import all the functions from other scripts and run them together to create the pure sand calibration adjustments (after applying the pure water adjustments first).
* plot1to1.py involves a function that creates 1:1 plots of raw data, the thermocouple temperature (x) vs. the thermal camera temperature (y).
* plot1to1multiple.py is a function that creates 1:1 plots of raw temperature for all the plastic percentages within a mixture group.
* read_CampbellSci.py extracts data from the Campbell Scientific thermocouple .dat files. Two little functions at the end calculate the averages of sand and water experiments.
* read_Optris.py extracts data from the Optris thermal camera .dat files. It also includes one averaging function.

The last four files are excel files created by the calculate_uncertainty.py script, providing the statistics inserted in tables in my thesis results.

