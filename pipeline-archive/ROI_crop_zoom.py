# Crop ROI from the GeoMX ROI images and zoom into (or out) the middle part

import cv2
import numpy as np
import os

# Set input and output file directories here
input_path = "your_ROI_path"
output_path = "your_output_path"


# Function to get .tiff files from a directory
def get_tiff_files(directory_path):
    return [file for file in os.listdir(directory_path) if file.endswith('.tiff')]

# Function to crop and zoom into the ROI
def crop_and_zoom(image, zoom_factor=1.1):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour by area (ROI)
    largest_contour = max(contours, key=cv2.contourArea)
    # Create a mask for the largest contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)
    #white_threshold = 210
    #Modify the mask: set mask pixels to 0 where the original image is white or nearly white
    #white_areas = np.where((image[:, :, 0] > white_threshold) & 
    #                       (image[:, :, 1] > white_threshold) & 
    #                       (image[:, :, 2] > white_threshold))
    #mask[white_areas] = 0
    # Bitwise AND operation to extract the ROI
    roi = cv2.bitwise_and(image, image, mask=mask)
    # Find the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Calculate the center of the bounding box
    center_x, center_y = x + w // 2, y + h // 2
    # Adjust the size of the bounding box based on the zoom factor
    new_w, new_h = int(w * zoom_factor), int(h * zoom_factor)
    # Calculate new x and y coordinates based on the zoomed size
    new_x, new_y = center_x - new_w // 2, center_y - new_h // 2
    # Ensure new coordinates are within image bounds
    new_x, new_y = max(new_x, 0), max(new_y, 0)
    new_w, new_h = min(new_w, image.shape[1] - new_x), min(new_h, image.shape[0] - new_y)
    # Crop the zoomed ROI from the ROI
    zoomed_roi = roi[new_y:new_y+new_h, new_x:new_x+new_w]
    return zoomed_roi

def remove_white_pixels(image, white_threshold=200):
    # Find all nearly white pixels in the image
    nearly_white = (image[:, :, 0] > white_threshold) & \
                   (image[:, :, 1] > white_threshold) & \
                   (image[:, :, 2] > white_threshold)
    # Set those pixels to black
    image[nearly_white] = [0, 0, 0]
    #
    return image

# Main loop to process each file
for tiff_file in get_tiff_files(input_path):
    input_file = os.path.join(input_path, tiff_file)
    #out_file = os.path.join(out_path, "zoomed_" + tiff_file)
    out_file = os.path.join(output_path,tiff_file)
    
    # Load the image using OpenCV
    image = cv2.imread(input_file, cv2.IMREAD_COLOR)
    
    # Crop and zoom into the ROI
    zoomed_roi = crop_and_zoom(image)
    zoomed_roi = remove_white_pixels(zoomed_roi)
    #
    # Save the zoomed ROI as a TIFF file
    cv2.imwrite(out_file, zoomed_roi)
