import tifffile as tiff
import numpy as np
from cellpose import models
from cellpose import plot
from cellpose import io
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import cv2
import pandas as pd
#import umap.umap_ as umap 


input_dir = "input_dir"
output_dir = "output_dir"


import os
import glob
tiff_files = glob.glob(os.path.join(input_dir, '*.tiff'))

for input_file in tiff_files:
    sid = os.path.basename(input_file)
    input_file=f"{input_dir}{sid}"
    #
    # Load image
    image = tiff.imread(input_file)
    #
    # Define the model. 'cyto' is for cytoplasm segmentation.
    # model = models.Cellpose(gpu=True, model_type='Cyto')
    # For TN1 and other models use models.CellposeModel()
    model = models.CellposeModel(gpu=False, model_type='TN3')
    #TN3, [2,3] is recommended over other methods:  [green, blue]
    #
    # Run the cellpose model, optimzie the parameter based on cellpose[gui]
    # diameter=17 for tumor-immune margin, 20-25 (23) for tumor core
    #Channels: 0=grayscale, 1=red, 2=green, 3=blue
    #flow_threshold 0.4(default)-0.6, senstive to white pixels
    #masks are main results, which are mask of segmented ROIs (cells)
    masks, flows, styles = model.eval(image, diameter=23, channels=[2,3], flow_threshold=0.4)
    #
    #count number of cells
    num_cells = len(np.unique(masks))-1
    print(f"Number of cells detected in this ROI: {num_cells}")
    #
    #############################################################BLOCK2
    #############################################################
    #
    #MAIN post-processing function 
    def extract_intensities_and_plot(image, masks):
        # 1. Extract the green, red, and blue channels from the image
        green_channel = image[:, :, 1]
        red_channel = image[:, :, 0]
        blue_channel = image[:, :, 2]
        
        # 2. Initialization
        green_intensities = []
        red_intensities = []
        blue_intensities = []
        Npis = []
        unique_cells = np.unique(masks)
        perimeters = []
        areas = []
        circularities = []
        coord_x= []
        coord_y= []
        
        # 3. Iterate through each cell and calculate average intensities
        for cell_id in unique_cells:
            if cell_id == 0:  # skip the background
                continue
            
            # Extract the region corresponding to the current cell
            green_cell_region = green_channel[masks == cell_id]
            red_cell_region = red_channel[masks == cell_id]
            blue_cell_region = blue_channel[masks == cell_id]
            #
            # Calculate average intensities for this cell region
            green_avg_intensity = np.mean(green_cell_region)
            red_avg_intensity = np.mean(red_cell_region)
            blue_avg_intensity = np.mean(blue_cell_region)
            #
            #cell size (number of pixels in the mask)
            Npi = np.sum(masks == cell_id)
            #
            #perimeter and circularity
            #Create a single cell mask and find countours
            cell_mask = (masks == cell_id).astype(np.uint8)
            contours, _ = cv2.findContours(cell_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            perimeter = cv2.arcLength(contours[0], True)
            area = cv2.contourArea(contours[0])
            circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
            #
             #y, x coordinates
            y, x = np.where(masks == cell_id)
            center_y, center_x = np.mean(y), np.mean(x)
            #
            green_intensities.append(green_avg_intensity)
            red_intensities.append(red_avg_intensity)
            blue_intensities.append(blue_avg_intensity)
            Npis.append(Npi)
            perimeters.append(perimeter)
            areas.append(area)
            circularities.append(circularity)
            coord_y.append(center_y)
            coord_x.append(center_x)
            #
        # 4. Plot density plot (optional)
        #
        return green_intensities, red_intensities, blue_intensities, Npis, perimeters, areas, circularities, coord_y, coord_x
    #
    # Call the function with your image and masks data
    green_intensities, red_intensities, blue_intensities, Npis, perimeters, areas, circularities, coord_y, coord_x = extract_intensities_and_plot(image, masks)
    #
    #output as DataFrame
    cell_stat = {
        'R_Int': red_intensities,
        'G_Int': green_intensities,
        'B_Int': blue_intensities,
        'Pixels': Npis,
        'Perimeter': perimeters,
        'Area': areas,
        'Circularity': circularities,
        'X_coordinate': coord_x,
        'Y_coordinate': coord_y
    }
    cell_stat = pd.DataFrame(cell_stat)
    #print(cell_stat)
    cell_stat.to_csv(f"{output_dir}{sid}.cell_stat.csv", index=False)
    #
    #############################################################BLOCK2.1
    #first visualization output blow
    plt.figure(figsize=(6, 3))
    plt.subplot(1, 2, 1)
    #
    sns.kdeplot(green_intensities, label='Green', fill=True, color='g')
    sns.kdeplot(red_intensities, label='Red', fill=True, color='r')
    sns.kdeplot(blue_intensities, label='Blue', fill=True, color='b')
    plt.xlabel('Intensity')
    plt.ylabel('Density')
    plt.legend()
    plt.title('Average Color Intensities')
    #
    # Plot scatterplot
    plt.subplot(1, 2, 2)
    plt.scatter(red_intensities, green_intensities, c='gray', marker='o', label='Segmented cells', s=1)
    plt.xlabel('Red')
    plt.ylabel('Green')
    plt.legend()
    plt.title('Red vs. Green Intensity')
    #
    plt.tight_layout()
    plt.savefig(f"{output_dir}{sid}.int.pdf",format="pdf")
    plt.show()


    #############################################################BLOCK2.2
    #############################################################

    #write own function to visuzlied with input of image and masks
    from matplotlib.colors import ListedColormap

    def mark_and_visualize_cells(image, masks):
        green_channel = image[:, :, 1]
        unique_cells = np.unique(masks)
        marked_mask = np.zeros_like(masks)
        
        cancer_cells_count = 0
        total_cells_count = 0

        for cell_id in unique_cells:
            if cell_id == 0:  # skip the background
                continue
            
            total_cells_count += 1  # Count each cell
            cell_region = green_channel[masks == cell_id]
            avg_intensity = np.mean(cell_region)
            
            # Mark the cell based on the intensity (use the benchmarked cutoff or clustering 15-40) <<<<<
            if avg_intensity > 20:
                marked_mask[masks == cell_id] = 2  # Mark cancer cells as 2
                cancer_cells_count += 1
            else:
                marked_mask[masks == cell_id] = 1  # Mark other cells as 1

        # Create a color map where 0 is black, blue for non-CC, pink for CC
        #custom_cmap = ListedColormap(['black', '#0057b7', '#ff69b4'])  # Blue and Pink

        # Determine the highest value in marked_mask to decide on the colormap
        max_value = np.max(marked_mask)
        if max_value == 1:  # Only non-cancer cells are present
            custom_cmap = ListedColormap(['black', '#0057b7'])  # Background, Non-CC
        else:  # Both non-cancer and cancer cells are present
            custom_cmap = ListedColormap(['black', '#0057b7', '#ff69b4'])  # Background, Non-CC, CC

        # Plot the original image and the marked mask
        fig, ax = plt.subplots(1, 2, figsize=(6, 4))

        # Original image
        ax[0].imshow(image)
        ax[0].axis('off')
        ax[0].set_title('Original Image')

        # Mask overlay on the original image
        ax[1].imshow(image)
        ax[1].imshow(marked_mask, cmap=custom_cmap, alpha=1)  # alpha for transparency
        ax[1].axis('off')
        ax[1].set_title('Segmented Cancer Cells')

        # Adding text (cell counts)
        text_str = (
            f"Total cells: {total_cells_count}\n"
            f"Cancer cells: {cancer_cells_count}\n"
            f"CC prop: {cancer_cells_count / total_cells_count:.2%}"
        )
        ax[1].text(0.02, 0.98, text_str, transform=ax[1].transAxes, fontsize=7,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.tight_layout()
        plt.savefig(f"{output_dir}{sid}.seg.pdf",format="pdf")
        plt.show()

    mark_and_visualize_cells(image, masks)
    ##>>>>>>>>>BATCH ABOVE
    print(f"Processed {sid}")
