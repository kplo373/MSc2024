# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 20:48:49 2024

Quick Python script to import the shaded-in Quartz sand image and calculate
the percentage of Quartz present.
ChatGPT was used to help :)

@author: adamk
"""
import cv2  # may need to install opencv-python numpy to anaconda prompt if isn't there already, don't use pip though
import numpy as np

image_path = r"D:\shaded_quartz.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # loading in grayscale

# Thresholding the image, converting to a binary image
_, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)  # below 128 are considered shaded/black, above are considered white

# Calculating the shaded area
total_pixels = binary_image.size
shaded_pixels = np.sum(binary_image == 0)  # counting black pixels

shaded_percentage = (shaded_pixels / total_pixels) * 100
print(f"Percentage of shaded area: {shaded_percentage:.2f}%")


# Display binary image for verification
cv2.imshow('Binary Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

