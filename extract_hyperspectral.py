# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 09:26:07 2024

Python script to try to put the processed hyperspectral data from the 
hard drive into a dataframe for plotting.


@author: kplo373
"""
import numpy as np
import spectral as sp  # need to install spectral via: conda install conda-forge::spectral  (in Anaconda Prompt)
#https://tobinghd.wordpress.com/2020/10/28/reading-a-hyperspectral-image-python/

# Read in the files first - the HDR files for getting wavelength as the index
hdr_path = r"E:\processed\Kate__SWIR_384_SN3234_11200us_2024-08-27T112156_raw_ref_bsq_float32.hdr"  # will need to make this automatically passing through all HDR files

hdr = sp.envi.open(hdr_path)
wvl = hdr.bands.centers
rows, cols, bands = hdr.nrows, hdr.ncols, hdr.nbands  # these are just integers of how many rows, columns, and bands are present
meta = hdr.metadata  # meta is a dictionary and shows the whole text within the .hdr file!
#print(meta['wavelength'])  # this length is only 288 though... not as long as the img data below! Is a list.
wavelength_list = meta['wavelength']  # comes as a list of strings
wavelengths = np.array(wavelength_list)

#%% And the img files for count (first column)
# https://stackoverflow.com/questions/32946436/read-img-medical-image-without-header-in-python

img_path = r"E:\processed\Kate__SWIR_384_SN3234_11200us_2024-08-27T112156_raw_ref_bsq_float32.img"  # this will need to automatically go through all .img files in folder
fid = open(img_path, 'rb')
data = np.fromfile(fid)  # has shape: (179714048,) and is a np.ndarray
#print(data)


#%% Then put these variables into the dataframe



