import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to crop ROI from GeoMx ROI image
def extract_roi(input_file, output_file):
    """
    Notes: Extracts the largest contour (Region of Interest) from the input TIFF image 
    and saves it as the output file.

    Args:
    input_file (str): Path to the input TIFF image.
    output_file (str): Path to save the processed ROI image.
    """

    # Load the input image
    image = cv2.imread(input_file, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error: Unable to read {input_file}")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a threshold to create a binary image (white lines on black background)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print(f"Warning: No contours found in {input_file}")
        return
    
    # Find the largest contour by area (ROI)
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask for the largest contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

    # Bitwise AND operation to extract ROI
    roi = cv2.bitwise_and(image, image, mask=mask)

    # Save the ROI as a TIFF file
    cv2.imwrite(output_file, roi)
    print(f"Processed ROI saved to: {output_file}")

def remove_white_pixels(image, white_threshold=200):
    # Find all nearly white pixels in the image
    nearly_white = (image[:, :, 0] > white_threshold) & \
                   (image[:, :, 1] > white_threshold) & \
                   (image[:, :, 2] > white_threshold)
    # Set those pixels to black
    image[nearly_white] = [0, 0, 0]
    #
    return image

# Function to crop and zoom into the ROI
def crop_and_zoom(input_file, output_file, zoom_factor=1.1):
    """
    Args:
    input_file (str): Path to the input TIFF image.
    output_file (str): Path to save the zoomed ROI image.
    zoom_factor (float): Factor by which to zoom into the ROI (default: 1.1).
    """

    # Load the input image
    image = cv2.imread(input_file, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error: Unable to read {input_file}")
        return
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"Warning: No contours found in {input_file}")
        return
    
    # Find the largest contour by area (ROI)
    largest_contour = max(contours, key=cv2.contourArea)
    # Create a mask for the largest contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

    # Extract ROI using a mask
    roi = cv2.bitwise_and(image, image, mask=mask)

    # Find the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    # Calculate the center of the bounding box
    center_x, center_y = x + w // 2, y + h // 2
    # Adjust the size of the bounding box based on the zoom factor
    new_w, new_h = int(w * zoom_factor), int(h * zoom_factor)
    # Calculate new top-left coordinates based on zoomed size
    new_x, new_y = center_x - new_w // 2, center_y - new_h // 2

    # Ensure new coordinates are within image bounds
    new_x, new_y = max(new_x, 0), max(new_y, 0)
    new_w, new_h = min(new_w, image.shape[1] - new_x), min(new_h, image.shape[0] - new_y)

    # Crop the zoomed ROI
    zoomed_roi = roi[new_y:new_y + new_h, new_x:new_x + new_w]

    # remove white boundary line
    zoomed_roi = remove_white_pixels(zoomed_roi)

    # Save the zoomed ROI as a TIFF file
    cv2.imwrite(output_file, zoomed_roi)
    print(f"Zoomed ROI saved to: {output_file}")

