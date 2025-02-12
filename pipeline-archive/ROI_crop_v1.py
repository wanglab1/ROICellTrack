# Crop ROI from the GeoMX ROI images
# pip install opencv-python

import cv2
import numpy as np
import os

#set input and output file directories here
input_path="your_ROI_path"
out_path="your_output_path"

#main function
def get_tiff_files(directory_path):
	return [file for file in os.listdir(directory_path) if file.endswith('.tiff')]

for tiff_file in get_tiff_files(directory_path):
	input_file = os.path.join(input_path, tiff_file)
	out_file	= os.path.join(out_path, tiff_file)
	#
	#
	# Load ROI TIFF (or png) image using OpenCV
	image = cv2.imread(input_file, cv2.IMREAD_COLOR)
	#
	#
	# Convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#
	# Apply a threshold to create a binary image (white lines on black background)
	_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
	#
	# Find contours in the binary image
	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# Find the largest contour by area (ROI)
	largest_contour = max(contours, key=cv2.contourArea)
	# Create a mask for the largest contour
	mask = np.zeros_like(gray)
	cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)
	#
	# Bitwise AND operation to extract the ROI
	roi = cv2.bitwise_and(image, image, mask=mask)
	#
	# Display the extracted ROI (Caution: Mac might not be able to close windows)
	#cv2.imshow('ROI', roi)
	#key = cv2.waitKey(0)
	#
	#
	# Save the ROI as a TIFF file named "ROI.tiff"
	cv2.imwrite(out_file, roi)
